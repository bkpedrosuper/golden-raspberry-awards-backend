from extensions.ma import ma
from models.producer_movie import ProducerMovieModel


class ProducerMovieSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProducerMovieModel
        load_instance = True
