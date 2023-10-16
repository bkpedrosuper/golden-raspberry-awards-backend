from flask import request
from flask_restx import Resource, fields, reqparse
from sqlalchemy import and_
from app.models.movie import MovieModel
from app.schemas.movie import MovieSchema

from app.extensions.api import api

movie_ns = api.namespace(name='movies', description="Movie related operations")

ITEM_NOT_FOUND = "Movie not found."

movie_schema = MovieSchema()
movie_list_schema = MovieSchema(many=True)

# Define parsers
movie_parser = reqparse.RequestParser()
movie_parser.add_argument('page', type=int, default=1, help='Page number')
movie_parser.add_argument('limit', type=int, default=10, help='Movies per page')
movie_parser.add_argument('winner', type=str, default=None, help='Filter by winner')
movie_parser.add_argument('year', type=int, default=None, help='Filter by year')

# Model required by flask_restplus for expect
item = movie_ns.model('Movie', {
    'title': fields.String('Movie title'),
    'winner': fields.Integer(0),
    'year': fields.Integer(1990),
})

@movie_ns.route('/<id>')
class Movie(Resource):

    def get(self, id):
        movie_data = MovieModel.find_by_id(id)
        if movie_data:
            return movie_schema.dump(movie_data)
        return {'message': ITEM_NOT_FOUND}, 404

    def delete(self, id):
        movie_data = MovieModel.find_by_id(id)
        if movie_data:
            movie_data.delete_from_db()
            return '', 204
        return {'message': ITEM_NOT_FOUND}, 404

    @movie_ns.expect(item)
    def put(self, id):
        movie_data = MovieModel.find_by_id(id)
        movie_json = request.get_json()

        if movie_data:
            movie_data.title = movie_json['title']
            movie_data.year = movie_json['year']
            movie_data.winner = movie_json['winner']
        else:
            movie_data = movie_schema.load(movie_json)

        movie_data.save_to_db()
        return movie_schema.dump(movie_data), 200

@movie_ns.route('/')
class MovieList(Resource):

    @movie_ns.expect(movie_parser)
    @movie_ns.doc('Get all the Items')
    def get(self):
        args = movie_parser.parse_args()
        page = args['page']
        limit = args['limit']
        winner_param = args['winner']
        year_param = args['year']

        query = MovieModel.query
        count = MovieModel.query.count()

        filters = []

        if winner_param is not None and winner_param.lower() == 'true':
            filters.append(MovieModel.winner == 1)
        elif winner_param is not None and winner_param.lower() == 'false':
            filters.append(MovieModel.winner == 0)
        
        if year_param is not None:
            filters.append(MovieModel.year == int(year_param))

        if filters:
            query = query.filter(and_(*filters))
        
        movies_paginated = query.offset((page - 1) * limit).limit(limit).all()
        count_query = query.count()

        return {
            'count': count,
            'count_query': count_query,
            'limit': limit,
            'page': page,
            'data': movie_list_schema.dump(movies_paginated)
        }, 200

    @movie_ns.expect(item)
    @movie_ns.doc('Create an Item')
    def post(self):
        movie_json = request.get_json()
        movie_data = movie_schema.load(movie_json)

        movie_data.save_to_db()

        return movie_schema.dump(movie_data), 201
