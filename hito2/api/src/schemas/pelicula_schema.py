from marshmallow import Schema, fields, validate, ValidationError
from bson import ObjectId
from db import mongo

class ObjectIdField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return str(value)

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return ObjectId(value)
        except Exception:
            raise ValidationError("El ID proporcionado no es válido.")

def validar_existencia_id_cine(value):
    try:
        oid = ObjectId(value)
    except Exception:
        raise ValidationError("ID de Cine debe ser un ObjectId válido.")
    if mongo.db.cines.find_one({"_id": oid}) is None:
        raise ValidationError("ID de Cine no válido")

class PeliculaSchema(Schema):
    nombre_pelicula = fields.Str(
        required=True,
        validate=validate.Length(min=1, error="Nombre de película requerido")
    )
    descripcion_pelicula = fields.Str(
        required=True,
        validate=validate.Length(min=1, error="Descripción de película requerida")
    )
    id_cine = fields.Str(
        required=True,
        validate=validar_existencia_id_cine
    )
    fecha_hora = fields.List(
        fields.DateTime(),
        required=True,
        error_messages={"required": "Fecha y hora son requeridos"}
    )
