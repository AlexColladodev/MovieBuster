from flask import jsonify
from db import mongo
from bson import json_util, ObjectId
from pymongo.errors import PyMongoError

class Cine:
    def __init__(self, data: dict) -> None:
        self.cif = data.get("cif")
        self.nombre_cine = data.get("nombre_cine")
        self.id_administrador = data.get("id_administrador")
        self.peliculas = data.get("peliculas", [])

    def insertar_cine(self):
        try:
            data_insertar = self.__dict__
            id = str(mongo.db.cines.insert_one(data_insertar).inserted_id)
            return {"message": "Cine creado con éxito", "id": id}
        except PyMongoError as e:
            raise RuntimeError("Error en la base de datos al crear cine") from e

    def eliminar_cine(id):
        try:
            establecimiento_eliminar = mongo.db.cines.find_one({"_id": ObjectId(id)})
            if not establecimiento_eliminar:
                raise ValueError("Cine no encontrado")
            id_administrador = establecimiento_eliminar.get("id_administrador")
            resultado = mongo.db.cines.delete_one({"_id": ObjectId(id)})
            if resultado.deleted_count == 0:
                raise RuntimeError("No se pudo eliminar el cine")
            return {"message": "Cine " + id + " eliminado con éxito"}
        except PyMongoError as e:
            raise RuntimeError(f"Error de base de datos al eliminar cine: {e}")

    def consultar_cines():
        try:
            cines = mongo.db.cines.find()
            return json_util.dumps(cines)
        except PyMongoError as e:
            raise RuntimeError(f"Error de base de datos al consultar los cines: {e}")

    def consultar_cine(id):
        try:
            cine = mongo.db.cines.find_one({"_id": ObjectId(id)})
            if not cine:
                raise ValueError("Cine no encontrado")
            respuesta = json_util.dumps(cine)
            return respuesta
        except PyMongoError as e:
            raise RuntimeError(f"Error de base de datos al consultar el cine: {e}")
