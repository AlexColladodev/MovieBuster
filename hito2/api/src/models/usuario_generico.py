import re
from flask import jsonify
from db import mongo
from werkzeug.security import generate_password_hash
from bson import json_util
from bson.objectid import ObjectId
from pymongo.errors import PyMongoError
from datetime import datetime

class UsuarioGenerico:
    def __init__(self, data: dict) -> None:
        self.nombre = data.get("nombre")
        self.nombre_usuario = data.get("nombre_usuario")
        self.password = data.get("password")
        self.email = data.get("email")
        self.telefono = data.get("telefono")
        self.seguidos = data.get("seguidos", [])
        self.preferencias = data.get("preferencias", [])
        self.actividades_creadas = data.get("actividades_creadas", [])
        self.reviews = data.get("reviews", [])
        self.fecha_nac = data.get("fecha_nac")

    def insertar_usuario_generico(self):
        try:
            if not self.correo_es_valido(self.email):
                raise ValueError("Usuario no encontrado")
            if self.fecha_nac:
                if isinstance(self.fecha_nac, str):
                    self.fecha_nac = datetime.fromisoformat(self.fecha_nac)
            data_insertar = self.__dict__
            data_insertar["password"] = generate_password_hash(data_insertar["password"])
            id = str(mongo.db.usuarios_genericos.insert_one(data_insertar).inserted_id)
            return {"message": "Usuario creado con éxito", "id": id}
        except PyMongoError as e:
            raise RuntimeError(f"Error en la base de datos al crear un usuario: {e}")

    @staticmethod
    def eliminar_usuario_generico(id):
        try:
            usuario_a_eliminar = mongo.db.usuarios_genericos.find_one({"_id": ObjectId(id)})
            if not usuario_a_eliminar:
                raise ValueError("Usuario no encontrado")
            resultado = mongo.db.usuarios_genericos.delete_one({"_id": ObjectId(id)})
            if resultado.deleted_count == 0:
                raise RuntimeError("No se pudo eliminar al usuario")
            return {"message": "Usuario eliminado con éxito"}
        except PyMongoError as e:
            raise RuntimeError(f"Error en la base de datos al eliminar a un usuario: {e}")
    
    @staticmethod
    def consultar_usuarios():
        try:
            usuarios_genericos = mongo.db.usuarios_genericos.find()
            return json_util.dumps(usuarios_genericos)
        except PyMongoError as e:
            raise RuntimeError(f"Error de base de datos al consultar usuarios genericos de establecimientos: {e}")
    
    @staticmethod
    def consultar_usuario(id):
        try:
            
            if not ObjectId.is_valid(id):
                raise ValueError("El ID proporcionado no es un ObjectId válido")
            
            
            usuario = mongo.db.usuarios_genericos.find_one({"_id": ObjectId(id)})
            if not usuario:
                raise ValueError("Usuario no encontrado")
            
            
            return json_util.dumps(usuario)

        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except PyMongoError as e:
            raise RuntimeError(f"Error en la base de datos al consultar al usuario: {e}")
        
    @staticmethod
    def actualizar_usuario(id, data):
        try:
            if not ObjectId.is_valid(id):
                raise ValueError("El ID proporcionado no es un ObjectId válido")
            
            data.pop("password", None)

            if 'fecha_nac' in data and isinstance(data['fecha_nac'], str):
                data['fecha_nac'] = datetime.fromisoformat(data['fecha_nac'])

            if 'preferencias' in data and isinstance(data['preferencias'], str):
                data['preferencias'] = data['preferencias'].split(',')

            resultado = mongo.db.usuarios_genericos.update_one({"_id": ObjectId(id)}, {"$set": data})

            if resultado.modified_count == 0:
                return {"message": "No se realizaron cambios o usuario no encontrado"}

            return {"message": "Usuario actualizado con éxito"}
        
        except PyMongoError as e:
            raise RuntimeError(f"Error en la base de datos al actualizar al usuario: {e}")

    @classmethod
    def correo_es_valido(cls, email):
        patron = r'\w+@\w+\.\w+'
        return re.match(patron, email) is not None

    @classmethod
    def existe_nombre_usuario(cls, nombre):
        try:
            usuario = mongo.db.usuarios_genericos.find_one({"nombre_usuario": nombre})
            if usuario:
                id_usuario = str(usuario.get("_id"))
                return id_usuario
            else:
                return None
        except Exception as e:
            raise RuntimeError(f"Error en la base de datos al consultar nombre de usuario: {e}")
