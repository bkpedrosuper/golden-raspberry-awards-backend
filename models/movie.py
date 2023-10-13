from extensions.db import db
from typing import List

class MovieModel(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    year = db.Column(db.Integer)
    winner = db.Column(db.Integer)

    def __init__(self, year,title,winner) -> None:

        self.year: int = year
        self.title: str = title
        self.winner: int = int(winner)

    @classmethod
    def find_by_id(cls, _id) -> "MovieModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_title(cls, title) -> "MovieModel":
        return cls.query.filter_by(title=title).first()

    @classmethod
    def find_all(cls) -> List["MovieModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
