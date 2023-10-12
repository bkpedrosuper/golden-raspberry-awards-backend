from flask import Flask, Blueprint, jsonify
from flask_restx import Api
from ma import ma
from db_files.db_utils import populate_db
from db import db
from marshmallow import ValidationError

from server.instance import server

from resources.book import Book, BookList
from resources.movie import Movie, MovieList
from resources.producer import Producer, ProducerList
from resources.producer_movie import ProducerMovie, ProducerMovieList
from resources.problem import Problem, problem_ns


api = server.api
app = server.app


@app.before_first_request
def create_tables():
    db.create_all()


@api.errorhandler(ValidationError)
def handle_validation_error(error):
    return jsonify(error.messages), 400

# ADD RESOURCES
api.add_resource(Book, '/books/<int:id>')
api.add_resource(BookList, '/books')

api.add_resource(Movie, '/movies/<int:id>')
api.add_resource(MovieList, '/movies')

api.add_resource(Producer, '/producers/<int:id>')
api.add_resource(ProducerList, '/producers')

api.add_resource(ProducerMovie, '/producer_movies/<int:id>')
api.add_resource(ProducerMovieList, '/producer_movies')

api.add_resource(Problem, '/problem')

api.add_namespace(problem_ns)


if __name__ == '__main__':
    db.init_app(app)
    populate_db(db, app)
    ma.init_app(app)
    server.run()
