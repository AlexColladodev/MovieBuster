from flask import jsonify
from db import mongo
from bson import ObjectId
from datetime import datetime
from schemas.pelicula_schema import PeliculaSchema
from marshmallow import ValidationError
from bson import json_util
from pymongo.errors import PyMongoError

class Pelicula:
    def __init__(self, data: dict) -> None:
        self.nombre_pelicula = data.get("nombre_pelicula")
        self.descripcion = data.get("descripcion_pelicula")
        self.id_cine = data.get("id_cine")
        self.fecha_hora = data.get("fecha_hora")

    @staticmethod
    def insertar_pelicula(data):
        schema = PeliculaSchema()
        try:
            datos_validados = schema.load(data)
            id = str(mongo.db.peliculas.insert_one(datos_validados).inserted_id)
            return {"message": "Película creada con éxito", "id": id}, 200
        except ValidationError as e:
            return {"error": e.messages}, 400
        except Exception as e:
            return {"error": f"Error en la base de datos al crear película: {str(e)}"}, 500

    @staticmethod
    def eliminar_pelicula(id):
        try:
            pelicula = mongo.db.peliculas.find_one({"_id": ObjectId(id)})
            if not pelicula:
                raise ValueError("Película no encontrada")
            resultado = mongo.db.peliculas.delete_one({"_id": ObjectId(id)})
            if resultado.deleted_count == 0:
                raise RuntimeError("No se pudo eliminar la película")
            return {"message": "Película eliminada con éxito"}, 200
        except Exception as e:
            return {"error": str(e)}, 500

    @staticmethod
    def consultar_peliculas():
        try:
            peliculas = mongo.db.peliculas.find()
            return json_util.dumps(peliculas)
        except Exception as e:
            return {"error": str(e)}, 500

    @staticmethod
    def consultar_pelicula(id):
        try:
            
            if not ObjectId.is_valid(id):
                raise ValueError("El ID proporcionado no es un ObjectId válido")
            
            
            usuario = mongo.db.peliculas.find_one({"_id": ObjectId(id)})
            if not usuario:
                raise ValueError("Pelicula no encontrada")
         
            return json_util.dumps(usuario)
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except PyMongoError as e:
            raise RuntimeError(f"Error en la base de datos al consultar la película: {e}")

    @staticmethod
    def actualizar_pelicula(id, data):
        schema = PeliculaSchema()
        try:
            datos_validados = schema.load(data)
            resultado = mongo.db.peliculas.update_one({"_id": ObjectId(id)}, {"$set": datos_validados})
            if resultado.modified_count == 0:
                return {"message": "No se realizaron cambios o película no encontrada"}, 404
            return {"message": "Película actualizada con éxito"}, 200
        except ValidationError as e:
            return {"error": e.messages}, 400
        except Exception as e:
            return {"error": str(e)}, 500
