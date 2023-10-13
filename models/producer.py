from extensions.db import db
from typing import List

class ProducerModel(db.Model):
    __tablename__ = 'producers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __init__(self, name: str) -> None:
        self.name = name.strip()

    @classmethod
    def find_by_id(cls, _id) -> "ProducerModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_title(cls, title) -> "ProducerModel":
        return cls.query.filter_by(title=title).first()

    @classmethod
    def find_all(cls) -> List["ProducerModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
