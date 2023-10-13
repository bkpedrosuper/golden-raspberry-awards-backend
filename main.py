from flask import jsonify
from app.extensions.ma import ma
from app.db_files.db_utils import populate_db
from app.extensions.db import db
from marshmallow import ValidationError

from app.server.instance import server

api = server.api
app = server.app


@app.before_first_request
def create_tables():
    db.create_all()


@api.errorhandler(ValidationError)
def handle_validation_error(error):
    return jsonify(error.messages), 400


if __name__ == '__main__':
    db.init_app(app)
    populate_db(db, app, True)
    ma.init_app(app)
    server.run()
