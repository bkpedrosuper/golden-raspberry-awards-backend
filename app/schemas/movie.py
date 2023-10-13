from app.extensions.ma import ma
from app.models.movie import MovieModel


class MovieSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MovieModel
        load_instance = True
