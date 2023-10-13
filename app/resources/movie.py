from flask import request
from flask_restx import Resource, fields

from app.models.movie import MovieModel
from app.schemas.movie import MovieSchema

from app.extensions.api import api

movie_ns = api.namespace(name='movies', description="Movie related operations")

ITEM_NOT_FOUND = "Movie not found."

movie_schema = MovieSchema()
movie_list_schema = MovieSchema(many=True)

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
    @movie_ns.doc('Get all the Items')
    def get(self):
        return movie_list_schema.dump(MovieModel.find_all()), 200

    @movie_ns.expect(item)
    @movie_ns.doc('Create an Item')
    def post(self):
        movie_json = request.get_json()
        movie_data = movie_schema.load(movie_json)

        movie_data.save_to_db()

        return movie_schema.dump(movie_data), 201
