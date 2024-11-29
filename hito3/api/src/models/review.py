from typing import Dict
from db import mongo
from bson import json_util, ObjectId
from pymongo.errors import PyMongoError

class Review:
    def __init__(self, data: Dict) -> None:
        self.calificacion = data.get("calificacion")
        self.mensaje = data.get("mensaje")
        self.id_usuario = data.get("id_usuario")
        self.id_pelicula = data.get("id_pelicula")
        self.fecha_creacion = data.get("fecha_creacion")

    def insertar_review(self):
        try:
            id_review = str(mongo.db.reviews.insert_one(self.__dict__).inserted_id)
            id_pelicula = self.id_pelicula
            pelicula = mongo.db.peliculas.find_one({"_id": ObjectId(id_pelicula)})
            if not pelicula:
                return {"error": "Película no encontrada"}, 404

            mongo.db.peliculas.update_one(
                {"_id": ObjectId(id_pelicula)},
                {"$addToSet": {"reviews": id_review}}
            )

            return {"message": "Review creada con éxito", "id_review": id_review}, 200

        except PyMongoError as e:
            return {"error": f"Error en la base de datos al crear review: {str(e)}"}, 500
        except Exception as e:
            return {"error": f"Error inesperado: {str(e)}"}, 500

    @staticmethod
    def eliminar_review(id):
        try:
            review_eliminar = mongo.db.reviews.find_one({"_id": ObjectId(id)})
            if not review_eliminar:
                return {"error": "Review no encontrada"}, 404

            resultado = mongo.db.reviews.delete_one({"_id": ObjectId(id)})
            if resultado.deleted_count == 0:
                return {"error": "No se pudo eliminar la review"}, 500

            return {"message": "Review eliminada con éxito"}, 200

        except PyMongoError as e:
            return {"error": f"Error de base de datos al eliminar review: {str(e)}"}, 500
        except Exception as e:
            return {"error": f"Error inesperado: {str(e)}"}, 500

    @staticmethod
    def consultar_reviews():
        try:
            reviews = mongo.db.reviews.find()
            return json_util.dumps(reviews), 200
        except PyMongoError as e:
            return {"error": f"Error de base de datos al consultar reviews: {str(e)}"}, 500
        except Exception as e:
            return {"error": f"Error inesperado: {str(e)}"}, 500

    @staticmethod
    def consultar_review(id):
        try:
            review = mongo.db.reviews.find_one({"_id": ObjectId(id)})
            if not review:
                return {"error": "Review no encontrada"}, 404

            usuario = mongo.db.usuarios_genericos.find_one({"_id": ObjectId(review["id_usuario"])})
            if not usuario:
                return {"error": "Usuario no encontrado"}, 404

            pelicula = mongo.db.peliculas.find_one({"_id": ObjectId(review["id_pelicula"])})
            if not pelicula:
                return {"error": "Película no encontrada"}, 404

            resultado = {
                "review": review,
                "nombre_usuario": usuario.get("nombre_usuario", ""),
                "nombre_pelicula": pelicula.get("nombre_pelicula", "")
            }
            return json_util.dumps(resultado), 200

        except PyMongoError as e:
            return {"error": f"Error de base de datos al consultar review: {str(e)}"}, 500
        except Exception as e:
            return {"error": f"Error inesperado: {str(e)}"}, 500
