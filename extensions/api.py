from flask import Blueprint
from flask_restx import Api

from flask_restx import Resource

server_blueprint = Blueprint('api', __name__,)
api = Api(server_blueprint, title='Golden Raspberry Awards API')