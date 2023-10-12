from ma import ma
from models.producer import ProducerModel


class ProducerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProducerModel
        load_instance = True
