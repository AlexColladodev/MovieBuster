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

def validar_nombre_cine_unico(value):
    if mongo.db.cines.find_one({"nombre_cine": value}):
        raise ValidationError("El nombre de cine ya está en uso.")

def validar_cif_unico(value):
    cif_sin_espacios = value.strip()
    if len(cif_sin_espacios) < 9:
        raise ValidationError("El CIF debe tener al menos 9 caracteres, sin contar espacios en blanco.")
    if mongo.db.cines.find_one({"cif": cif_sin_espacios}):
        raise ValidationError("El CIF ya está en uso.")

def validar_existencia_id(value):
    try:
        oid = ObjectId(value)
    except Exception:
        raise ValidationError("Id de Administrador de cine debe ser un ObjectId válido.")
    if mongo.db.administradores_cines.find_one({"_id": oid}) is None:
        raise ValidationError("Id de Administrador de establecimiento no válido")

class CinesSchema(Schema):
    cif = fields.Str(
        required=True,
        validate=[validar_cif_unico],
        error_messages={"required": "CIF sin rellenar"}
    )
    nombre_cine = fields.Str(
        required=True,
        validate=[validate.Length(min=1, error="Nombre de cine sin rellenar"), validar_nombre_cine_unico]
    )
    id_administrador = fields.Str(
        required=True,
        validate=[validar_existencia_id],
        error_messages={"required": "No existe este administrador"}
    )
    peliculas = fields.List(fields.Str(), required=False, missing=[])