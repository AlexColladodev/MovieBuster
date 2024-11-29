import pytest
from bson import ObjectId
from pymongo.errors import PyMongoError
from models.administrador_cine import AdministradorCine
from app import app
from unittest.mock import patch

data_administrador = {
    "nombre": "Carlos",
    "nombre_usuario": "carlos1234",
    "password": "adminpass",
    "email": "carlos@gmail.com",
    "telefono": "123456789",
    "dni": "12345678X"
}

@pytest.fixture
def mock_mongo(mocker):
    return mocker.patch("models.administrador_cine.mongo.db")


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_insertar_administrador_cine(mocker):
    mock_db = mocker.patch('models.administrador_cine.mongo.db')
    mock_administradores = mock_db.administradores_cines
    mock_administradores.insert_one.return_value.inserted_id = ObjectId("672fe33274197c464143ee64")
    
    mocker.patch('models.administrador_cine.AdministradorCine.correo_es_valido', return_value=True)
    
    administrador = AdministradorCine(data_administrador)
    response = administrador.insertar_administrador_cine()
    
    assert response["message"] == "Administrador creado con éxito"
    assert response["id"] == "672fe33274197c464143ee64"

def test_eliminar_administrador_cine(mocker):
    mock_db = mocker.patch('models.administrador_cine.mongo.db')
    mock_administradores = mock_db.administradores_cines
    mock_administradores.find_one.return_value = {"_id": ObjectId("672fe33274197c464143ee64")}
    mock_administradores.delete_one.return_value.deleted_count = 1
    
    response = AdministradorCine.eliminar_administrador_cine(ObjectId("672fe33274197c464143ee64"))
    assert response["message"] == "administrador eliminado con éxito"

def test_eliminar_administrador_cine_no_encontrado(mocker):
    mock_db = mocker.patch('models.administrador_cine.mongo.db')
    mock_administradores = mock_db.administradores_cines
    mock_administradores.find_one.return_value = None
    
    with pytest.raises(ValueError, match="administrador no encontrado"):
        AdministradorCine.eliminar_administrador_cine(ObjectId("672fe33274197c464143ee64"))

from bson import ObjectId
from bson import json_util

def test_consultar_administrador_encontrado(mocker):
    mock_db = mocker.patch('models.administrador_cine.mongo.db')
    mock_administradores = mock_db.administradores_cines

    administrador_data = {
        "_id": ObjectId("672fe33274197c464143ee64"),
        "nombre": "Carlos",
        "nombre_usuario": "carlos123",
        "email": "carlos@example.com",
        "telefono": "123456789",
        "dni": "12345678X"
    }

    mock_administradores.find_one.return_value = administrador_data

    response = AdministradorCine.consultar_administrador("672fe33274197c464143ee64")

    assert response == json_util.dumps(administrador_data)

def test_consultar_administrador_no_encontrado(mocker):
    mock_db = mocker.patch('models.administrador_cine.mongo.db')
    mock_administradores = mock_db.administradores_cines

    mock_administradores.find_one.return_value = None

    with pytest.raises(ValueError):
        AdministradorCine.consultar_administrador("id_incorrecto")


def test_actualizar_administrador_sin_cambios(mocker):
    mock_db = mocker.patch('models.administrador_cine.mongo.db')
    mock_administradores = mock_db.administradores_cines
    mock_administradores.update_one.return_value.modified_count = 0
    mock_administradores.find_one.return_value = {"_id": ObjectId("672fe33274197c464143ee64")}
    
    response = AdministradorCine.actualizar_administrador(ObjectId("672fe33274197c464143ee64"), {})
    assert response["message"] == "No se realizaron cambios o administrador no encontrado"

def test_correo_es_valido():
    assert AdministradorCine.correo_es_valido("carlos@gmail.com") == True
    assert AdministradorCine.correo_es_valido("carlos@gmail") == False

def test_consultar_administradores_cines(mocker):
    mock_db = mocker.patch('models.administrador_cine.mongo.db')
    mock_administradores = mock_db.administradores_cines
    mock_administradores.find.return_value = [{"_id": ObjectId("672fe33274197c464143ee64"), "nombre": "Carlos"}]
    
    response = AdministradorCine.consultar_administradores_cines()
    
    assert '"nombre": "Carlos"' in response 
    assert '"_id": {"$oid": "672fe33274197c464143ee64"}' in response


def test_crear_administrador_cine_incorrectamente(client, mock_mongo):
    payload = {
        "nombre": "",
        "nombre_usuario": "admin123",
        "password": "securepassword",
        "email": "admincine.com",
        "dni": "123",
        "telefono": "abc"
    }
    response = client.post("/administrador_cine", json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

def test_eliminar_administrador_cine_correctamente(client, mock_mongo):
    mock_mongo.administradores_cines.find_one.return_value = {"_id": ObjectId("672fe33274197c464143ee69")}
    mock_mongo.administradores_cines.delete_one.return_value.deleted_count = 1
    response = client.delete("/administrador_cine/672fe33274197c464143ee69")
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "administrador eliminado con éxito"

def test_eliminar_administrador_cine_incorrectamente(client, mock_mongo):
    mock_mongo.administradores_cines.find_one.return_value = None
    response = client.delete("/administrador_cine/672fe33274197c464143ee69")
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "administrador no encontrado"

def test_obtener_administrador_cine_correctamente(client, mock_mongo):
    mock_mongo.administradores_cines.find_one.return_value = {
        "_id": ObjectId("672fe33274197c464143ee69"),
        "nombre": "Cine Admin",
        "nombre_usuario": "admin123",
        "email": "admin@cine.com",
        "dni": "12345678A",
        "telefono": "1234567890"
    }
    response = client.get("/administrador_cine/672fe33274197c464143ee69")
    assert response.status_code == 200
    data = response.get_json()
    assert data["nombre"] == "Cine Admin"
    assert data["nombre_usuario"] == "admin123"
    assert data["email"] == "admin@cine.com"