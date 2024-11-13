import re
from flask import jsonify
from db import mongo
from werkzeug.security import generate_password_hash
from bson import json_util
from bson.objectid import ObjectId
from pymongo.errors import PyMongoError
from datetime import datetime

class AdministradorCine:
    def __init__(self, data: dict) -> None:
        self.nombre = data.get("nombre")
        self.nombre_usuario = data.get("nombre_usuario")
        self.password = data.get("password")
        self.email = data.get("email")
        self.telefono = data.get("telefono")
        self.dni = data.get("dni")

    def insertar_administrador_cine(self):
        try:
            if not self.correo_es_valido(self.email):
                raise ValueError("Administrador no encontrado")
            data_insertar = self.__dict__
            data_insertar["password"] = generate_password_hash(data_insertar["password"])
            id = str(mongo.db.administradores_cines.insert_one(data_insertar).inserted_id)
            return {"message": "Administrador creado con éxito", "id": id}
        except PyMongoError as e:
            raise RuntimeError(f"Error en la base de datos al crear un administrador: {e}")

    @staticmethod
    def eliminar_administrador_cine(id):
        try:
            administrador_a_eliminar = mongo.db.administradores_cines.find_one({"_id": ObjectId(id)})
            if not administrador_a_eliminar:
                raise ValueError("administrador no encontrado")
            resultado = mongo.db.administradores_cines.delete_one({"_id": ObjectId(id)})
            if resultado.deleted_count == 0:
                raise RuntimeError("No se pudo eliminar al administrador")
            return {"message": "administrador eliminado con éxito"}
        except PyMongoError as e:
            raise RuntimeError(f"Error en la base de datos al eliminar a un administrador: {e}")
    
    @staticmethod
    def consultar_administradores_cines():
        try:
            administradores_cines = mongo.db.administradores_cines.find()
            return json_util.dumps(administradores_cines)
        except PyMongoError as e:
            raise RuntimeError(f"Error de base de datos al consultar administradores_cines genericos de establecimientos: {e}")
    
    @staticmethod
    def consultar_administrador(id):
        try:
            
            if not ObjectId.is_valid(id):
                raise ValueError("El ID proporcionado no es un ObjectId válido")
            
            
            administrador = mongo.db.administradores_cines.find_one({"_id": ObjectId(id)})
            if not administrador:
                raise ValueError("administrador no encontrado")
            
            
            return json_util.dumps(administrador)
        
        except PyMongoError as e:
            raise RuntimeError(f"Error en la base de datos al consultar al administrador: {e}")

    @staticmethod
    def actualizar_administrador(id, data):
        try:
            if not ObjectId.is_valid(id):
                raise ValueError("El ID proporcionado no es un ObjectId válido")
            
            data.pop("password", None)

            resultado = mongo.db.administradores_cines.update_one({"_id": ObjectId(id)}, {"$set": data})

            if resultado.modified_count == 0:
                return {"message": "No se realizaron cambios o administrador no encontrado"}

            return {"message": "administrador actualizado con éxito"}
        
        except PyMongoError as e:
            raise RuntimeError(f"Error en la base de datos al actualizar al administrador: {e}")

    @staticmethod
    def correo_es_valido(email):
        patron = r'\w+@\w+\.\w+'
        return re.match(patron, email) is not None
