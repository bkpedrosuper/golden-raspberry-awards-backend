from extensions.ma import ma
from models.movie import MovieModel


class MovieSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MovieModel
        load_instance = True
