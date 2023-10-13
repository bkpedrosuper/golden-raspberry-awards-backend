from flask import Flask
from app.extensions.api import api, server_blueprint
import os

from app.resources.movie import movie_ns
from app.resources.producer import producer_ns
from app.resources.producer_movie import producer_movie_ns
from app.resources.problem import problem_ns

class Server():
    def __init__(self, database_uri = f'sqlite:///{os.getcwd()}/app/db_files/database.db'):
        self.app = Flask(__name__)
        self.api = api
        self.app.register_blueprint(server_blueprint)

        # Register namespaces
        self.api.add_namespace(movie_ns)
        self.api.add_namespace(producer_ns)
        self.api.add_namespace(producer_movie_ns)
        self.api.add_namespace(problem_ns)

        self.app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['PROPAGATE_EXCEPTIONS'] = True

        super().__init__()

    def run(self, ):
        self.app.run(
            port=3300,
            debug=True,
            host='0.0.0.0'
        )

server = Server()
