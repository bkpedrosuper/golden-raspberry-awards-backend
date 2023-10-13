from flask import jsonify
from extensions.ma import ma
from db_files.db_utils import populate_db
from extensions.db import db
from marshmallow import ValidationError

from server.instance import server


from resources.movie import movie_ns
from resources.producer import producer_ns
from resources.producer_movie import producer_movie_ns
from resources.problem import problem_ns


api = server.api
app = server.app


@app.before_first_request
def create_tables():
    db.create_all()


@api.errorhandler(ValidationError)
def handle_validation_error(error):
    return jsonify(error.messages), 400

# ADD NAMESPACES
api.add_namespace(movie_ns)
api.add_namespace(producer_ns)
api.add_namespace(producer_movie_ns)
api.add_namespace(problem_ns)



if __name__ == '__main__':
    db.init_app(app)
    # populate_db(db, app)
    ma.init_app(app)
    server.run()
