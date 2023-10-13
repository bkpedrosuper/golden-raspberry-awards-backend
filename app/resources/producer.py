from flask import request
from flask_restx import Resource, fields

from app.models.producer import ProducerModel
from app.schemas.producer import ProducerSchema

from app.extensions.api import api

producer_ns = api.namespace(name='producers', description='Producer related operations')

ITEM_NOT_FOUND = "Producer not found."


producer_schema = ProducerSchema()
producer_list_schema = ProducerSchema(many=True)

# Model required by flask_restplus for expect
item = producer_ns.model('Producer', {
    'name': fields.String('Producer name'),
})

@producer_ns.route('/<id>')
class Producer(Resource):

    def get(self, id):
        producer_data = ProducerModel.find_by_id(id)
        if producer_data:
            return producer_schema.dump(producer_data)
        return {'message': ITEM_NOT_FOUND}, 404

    def delete(self, id):
        producer_data = ProducerModel.find_by_id(id)
        if producer_data:
            producer_data.delete_from_db()
            return '', 204
        return {'message': ITEM_NOT_FOUND}, 404

    @producer_ns.expect(item)
    def put(self, id):
        producer_data = ProducerModel.find_by_id(id)
        producer_json = request.get_json()

        if producer_data:
            producer_data.pages = producer_json['pages']
            producer_data.title = producer_json['title']
        else:
            producer_data = producer_schema.load(producer_json)

        producer_data.save_to_db()
        return producer_schema.dump(producer_data), 200

@producer_ns.route('/')
class ProducerList(Resource):
    @producer_ns.doc('Get all the Items')
    def get(self):
        return producer_list_schema.dump(ProducerModel.find_all()), 200

    @producer_ns.expect(item)
    @producer_ns.doc('Create an Item')
    def post(self):
        producer_json = request.get_json()
        producer_data = producer_schema.load(producer_json)

        producer_data.save_to_db()

        return producer_schema.dump(producer_data), 201
