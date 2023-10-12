from flask import request, jsonify
from flask_restx import Resource, fields

from models.producer_movie import ProducerMovieModel
from schemas.producer_movie import ProducerMovieSchema

from api import api

producer_movie_ns = api.namespace(name='ProducerMovies', description='ProducerMovie related operations', path='/producer_movies')

ITEM_NOT_FOUND = "ProducerMovie not found."


producer_movie_schema = ProducerMovieSchema()
producer_movie_list_schema = ProducerMovieSchema(many=True)

# Model required by flask_restplus for expect
item = producer_movie_ns.model('ProducerMovie', {
    'movie_id': fields.String('Movie ID'),
    'producer_id': fields.String('Producer ID'),
})


class ProducerMovie(Resource):

    def get(self, id):
        producer_movie_data = ProducerMovieModel.find_by_id(id)
        if producer_movie_data:
            return producer_movie_schema.dump(producer_movie_data)
        return {'message': ITEM_NOT_FOUND}, 404

    def delete(self, id):
        producer_movie_data = ProducerMovieModel.find_by_id(id)
        if producer_movie_data:
            producer_movie_data.delete_from_db()
            return '', 204
        return {'message': ITEM_NOT_FOUND}, 404

class ProducerMovieList(Resource):
    @producer_movie_ns.doc('Get all the Items')
    def get(self):
        return producer_movie_list_schema.dump(ProducerMovieModel.find_all()), 200

    @producer_movie_ns.expect(item)
    @producer_movie_ns.doc('Create an Item')
    def post(self):
        producer_movie_json = request.get_json()
        producer_movie_data: ProducerMovieModel = producer_movie_schema.load(producer_movie_json)

        producer_movie_data.save_to_db()

        return producer_movie_schema.dump(producer_movie_data), 201
