from app.extensions.ma import ma
from app.models.producer import ProducerModel


class ProducerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProducerModel
        load_instance = True
