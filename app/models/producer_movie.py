from app.extensions.db import db
from typing import List

class ProducerMovieModel(db.Model):
    __tablename__ = 'producer_movies'
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'))
    producer_id = db.Column(db.Integer, db.ForeignKey('producers.id'))

    def __init__(self, producer_id: int, movie_id: int) -> None:
        self.movie_id = movie_id
        self.producer_id = producer_id

    def find_by_movie_id(cls, movie_id) -> "ProducerMovieModel":
        return cls.query.filter_by(movie_id=movie_id).first()

    @classmethod
    def find_by_producer_id(cls, producer_id) -> "ProducerMovieModel":
        return cls.query.filter_by(producer_id=producer_id).first()

    @classmethod
    def find_all(self) -> List["ProducerMovieModel"]:
        return self.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
