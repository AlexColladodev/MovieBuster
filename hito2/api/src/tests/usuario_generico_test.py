import pytest
from models.usuario_generico import UsuarioGenerico
from bson import ObjectId
from pymongo.errors import PyMongoError

data_usuario = {
    "nombre": "Alex",
    "nombre_usuario": "alex123",
    "password": "password123",
    "email": "alex@gmail.com",
    "telefono": "1234567890",
    "seguidos": [],
    "preferencias": ["cine", "teatro"],
    "actividades_creadas": [],
    "reviews": [],
    "fecha_nac": "2000-09-25"
}

data_usuario_fecha_invalida = {
    "nombre": "Alex",
    "nombre_usuario": "alex123",
    "password": "password123",
    "email": "alex@gmail.com",
    "telefono": "1234567890",
    "seguidos": [],
    "preferencias": ["cine", "teatro"],
    "actividades_creadas": [],
    "reviews": [],
    "fecha_nac": "25-09-2000"
}

def test_insertar_usuario_generico(mocker):
    mock_db = mocker.patch('models.usuario_generico.mongo.db')
    mock_usuarios_genericos = mock_db.usuarios_genericos
    mock_usuarios_genericos.insert_one.return_value.inserted_id = ObjectId("672fa7d59bb2e4ad65f9a1b2")
    
    usuario = UsuarioGenerico(data_usuario)
    response = usuario.insertar_usuario_generico()
    
    assert response["message"] == "Usuario creado con éxito"
    assert response["id"] == "672fa7d59bb2e4ad65f9a1b2"

def test_insertar_usuario_generico_fecha_invalida(mocker):
    mock_db = mocker.patch('models.usuario_generico.mongo.db')
    mock_usuarios_genericos = mock_db.usuarios_genericos
    mock_usuarios_genericos.insert_one.return_value.inserted_id = "672fa7d59bb2e4ad65f9a1b2"

    mocker.patch('models.usuario_generico.UsuarioGenerico.correo_es_valido', return_value=True)
    
    usuario = UsuarioGenerico(data_usuario_fecha_invalida)

    with pytest.raises(ValueError):
        usuario.insertar_usuario_generico()


def test_eliminar_usuario_generico(mocker):
    mock_db = mocker.patch('models.usuario_generico.mongo.db')
    mock_usuarios_genericos = mock_db.usuarios_genericos
    mock_usuarios_genericos.find_one.return_value = True
    mock_usuarios_genericos.delete_one.return_value.deleted_count = 1
    
    response = UsuarioGenerico.eliminar_usuario_generico(ObjectId("672fa7d59bb2e4ad65f9a1b2"))
    
    assert response["message"] == "Usuario eliminado con éxito"

def test_eliminar_usuario_no_encontrado(mocker):
    mock_db = mocker.patch('models.usuario_generico.mongo.db')
    mock_usuarios_genericos = mock_db.usuarios_genericos
    mock_usuarios_genericos.find_one.return_value = None

    with pytest.raises(ValueError, match="Usuario no encontrado"):
        UsuarioGenerico.eliminar_usuario_generico(ObjectId("672fa7d59bb2e4ad65f9a1b2"))

def test_actualizar_usuario_sin_cambios(mocker):
    mock_db = mocker.patch('models.usuario_generico.mongo.db')
    mock_usuarios_genericos = mock_db.usuarios_genericos
    mock_usuarios_genericos.update_one.return_value.modified_count = 0
    mock_usuarios_genericos.find_one.return_value = True
    
    response = UsuarioGenerico.actualizar_usuario(ObjectId("672fa7d59bb2e4ad65f9a1b2"), {})
    
    assert response["message"] == "No se realizaron cambios"

def test_actualizar_usuario_con_cambios(mocker):
    mock_db = mocker.patch('models.usuario_generico.mongo.db')
    mock_usuarios_genericos = mock_db.usuarios_genericos
    mock_usuarios_genericos.update_one.return_value.modified_count = 1
    mock_usuarios_genericos.find_one.return_value = True

    data_usuario_modificada = {
        "nombre": "Alexander",
        "nombre_usuario": "alex123",
        "password": "password123",
        "email": "alex@gmail.com",
        "telefono": "1234567890",
        "seguidos": [],
        "preferencias": ["cine", "teatro"],
        "actividades_creadas": [],
        "reviews": [],
        "fecha_nac": "2000-09-25"
    }
    
    response = UsuarioGenerico.actualizar_usuario(ObjectId("672fa7d59bb2e4ad65f9a1b2"), data_usuario_modificada)
    
    assert response["message"] == "Usuario actualizado con éxito"

def test_correo_es_valido():
    assert UsuarioGenerico.correo_es_valido("alex@gmail.com") == True
    assert UsuarioGenerico.correo_es_valido("alex@gmail") == False

def test_invitacion_actividad(mocker):
    mock_db = mocker.patch('models.usuario_generico.mongo.db')
    mock_actividades = mock_db.actividades
    mock_actividades.update_one.return_value.modified_count = 1
    
    response = UsuarioGenerico.invita_actividad(ObjectId("672fa7d59bb2e4ad65f9a1b2"), ObjectId("672fa7d59bb2e4ad65f9a1b3"))
    
    assert response["message"] == "Actividad añadida con éxito al usuario"

def test_invitacion_actividad_id_inexistente(mocker):
    mock_db = mocker.patch('models.usuario_generico.mongo.db')
    mock_actividades = mock_db.actividades
    mock_usuarios = mock_db.usuarios_genericos
    
    mock_actividades.find_one.return_value = None
    mock_usuarios.find_one.return_value = {"_id": ObjectId("672fa7d59bb2e4ad65f9a1b2")}

    with pytest.raises(ValueError, match="La actividad especificada no existe"):
        UsuarioGenerico.invita_actividad(ObjectId("672fa7d59bb2e4ad65f9a1b2"), ObjectId("672fa7d59bb2e4ad65f9a1b3"))

