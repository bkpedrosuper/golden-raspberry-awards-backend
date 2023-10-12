from flask import Blueprint
from flask_restx import Api

server_blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(server_blueprint, doc='/doc', title='Golden Raspberry Awards API')