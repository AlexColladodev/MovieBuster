from marshmallow import Schema, fields, validate, ValidationError
from bson import ObjectId
from marshmallow.exceptions import ValidationError as MarshmallowValidationError
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
            raise MarshmallowValidationError("El ID proporcionado no es válido.")


def validar_existencia_id(value):
    try:
        oid = ObjectId(value)
    except Exception:
        raise ValidationError("ID Usuario debe ser un ObjectId válido.")

    if mongo.db.usuarios_genericos.find_one({"_id": oid}) is None:
        raise ValidationError("ID Usuario no válido")


def validar_existencia_id_pelicula(value):
    try:
        oid = ObjectId(value)
    except Exception:
        raise ValidationError("ID Pelicula debe ser un ObjectId válido.")

    if mongo.db.peliculas.find_one({"_id": oid}) is None:
        raise ValidationError("Pelicula no válido")


class ReviewSchema(Schema):
    calificacion = fields.Float(
        required=True,
        validate=validate.Range(min=0, max=5),
        error_messages={"required": "Calificación sin rellenar"}
    )
    mensaje = fields.Str(
        required=True,
        validate=[validate.Length(min=1, max=201)],
        error_messages={"required": "Mensaje sin rellenar", "max": "Mensaje demasiado largo"}
    )
    id_usuario = ObjectIdField(
        required=True,
        validate=[validar_existencia_id],
        error_messages={"required": "ID Usuario sin rellenar"}
    )
    id_pelicula = ObjectIdField(
        required=True,
        validate=[validar_existencia_id_pelicula],
        error_messages={"required": "ID Pelicula sin rellenar"}
    )
    fecha_creacion = fields.Str(
        required=True,
        validate=[validate.Length(min=1)],
        error_messages={"required": "Fecha de creación sin rellenar"}
    )
