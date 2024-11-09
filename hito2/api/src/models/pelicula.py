from flask import jsonify
from db import mongo
from bson import ObjectId
from datetime import datetime
from pymongo.errors import PyMongoError
from bson import json_util

class Pelicula:
    def __init__(self, data: dict) -> None:
        self.nombre_pelicula = data.get("nombre_pelicula")
        self.descripcion = data.get("descripcion_pelicula")
        self.id_cine = data.get("id_cine")
        self.fecha_hora = data.get("fecha_hora")
        self.genero = data.get("genero", [])
        self.reviews = data.get("reviews", [])

    def insertar_pelicula(self):
        try:
            data_insertar = self.__dict__

            cine = mongo.db.cines.find_one({"_id": ObjectId(self.id_cine)})
            if not cine:
                raise ValueError("Cine no encontrado")

            id_pelicula = str(mongo.db.peliculas.insert_one(data_insertar).inserted_id)
            mongo.db.cines.update_one(
                {"_id": ObjectId(self.id_cine)},
                {"$addToSet": {"peliculas": id_pelicula}}
            )

            return {"message": "Película creada con éxito", "id": id_pelicula}
        except PyMongoError as e:
            raise RuntimeError("Error en la base de datos al crear película") from e

    @staticmethod
    def eliminar_pelicula(id):
        try:
            pelicula = mongo.db.peliculas.find_one({"_id": ObjectId(id)})
            if not pelicula:
                raise ValueError("Película no encontrada")
            resultado = mongo.db.peliculas.delete_one({"_id": ObjectId(id)})
            if resultado.deleted_count == 0:
                raise RuntimeError("No se pudo eliminar la película")
            return {"message": "Película eliminada con éxito"}
        except PyMongoError as e:
            raise RuntimeError(f"Error de base de datos al eliminar película: {e}")

    @staticmethod
    def consultar_peliculas():
        try:
            peliculas = mongo.db.peliculas.find()
            return json_util.dumps(peliculas)
        except PyMongoError as e:
            raise RuntimeError(f"Error de base de datos al consultar las películas: {e}")

    @staticmethod
    def consultar_pelicula(id):
        try:
            if not ObjectId.is_valid(id):
                raise ValueError("El ID proporcionado no es un ObjectId válido")

            pelicula = mongo.db.peliculas.find_one({"_id": ObjectId(id)})
            if not pelicula:
                raise ValueError("Película no encontrada")
            return json_util.dumps(pelicula)
        except PyMongoError as e:
            raise RuntimeError(f"Error de base de datos al consultar la película: {e}")

    @staticmethod
    def actualizar_pelicula(id, data):
        try:
            resultado = mongo.db.peliculas.update_one({"_id": ObjectId(id)}, {"$set": data})
            if resultado.modified_count == 0:
                return {"message": "No se realizaron cambios o película no encontrada"}, 404
            return {"message": "Película actualizada con éxito"}
        except PyMongoError as e:
            raise RuntimeError(f"Error de base de datos al actualizar película: {e}")
