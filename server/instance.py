from flask import Flask
from extensions.api import api, server_blueprint
import os

class Server():
    def __init__(self):
        self.app = Flask(__name__)
        self.api = api
        self.app.register_blueprint(server_blueprint)

        self.app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.getcwd()}/db_files/database.db'
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
