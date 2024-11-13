import pytest
from models.cine import Cine
from bson import ObjectId, json_util

def test_insertar_cine(mocker):
    data_cine = {
        "cif": "A12345678",
        "nombre_cine": "Cine Central",
        "id_administrador": ObjectId("672fe5a7658b89859dc24839"),
        "peliculas": []
    }
    mock_db = mocker.patch('models.cine.mongo.db')
    mock_cines = mock_db.cines
    mock_cines.insert_one.return_value.inserted_id = ObjectId("672fe5a7658b89859dc24838")

    cine = Cine(data_cine)
    response = cine.insertar_cine()
    assert response["message"] == "Cine creado con éxito"
    assert response["id"] == "672fe5a7658b89859dc24838"

def test_eliminar_cine_existente(mocker):
    mock_db = mocker.patch('models.cine.mongo.db')
    mock_cines = mock_db.cines
    mock_cines.find_one.return_value = {"_id": ObjectId("672fe5a7658b89859dc24838")}
    mock_cines.delete_one.return_value.deleted_count = 1

    response = Cine.eliminar_cine("672fe5a7658b89859dc24838")
    assert response["message"] == "Cine 672fe5a7658b89859dc24838 eliminado con éxito"

def test_eliminar_cine_no_encontrado(mocker):
    mock_db = mocker.patch('models.cine.mongo.db')
    mock_cines = mock_db.cines
    mock_cines.find_one.return_value = None

    with pytest.raises(ValueError, match="Cine no encontrado"):
        Cine.eliminar_cine("672fe5a7658b89859dc24838")

def test_consultar_cines(mocker):
    mock_db = mocker.patch('models.cine.mongo.db')
    mock_cines = mock_db.cines
    mock_cines.find.return_value = [{"_id": ObjectId("672fe5a7658b89859dc24838"), "nombre_cine": "Cine Moderno"}]

    response = Cine.consultar_cines()
    assert '"nombre_cine": "Cine Moderno"' in response

def test_consultar_cine_encontrado(mocker):
    mock_db = mocker.patch('models.cine.mongo.db')
    mock_cines = mock_db.cines
    mock_cines.find_one.return_value = {
        "_id": ObjectId("672fe5a7658b89859dc24838"),
        "nombre_cine": "Cine Moderno"
    }

    response = Cine.consultar_cine("672fe5a7658b89859dc24838")
    assert '"nombre_cine": "Cine Moderno"' in response

def test_consultar_cine_no_encontrado(mocker):
    mock_db = mocker.patch('models.cine.mongo.db')
    mock_cines = mock_db.cines
    mock_cines.find_one.return_value = None

    with pytest.raises(ValueError, match="Cine no encontrado"):
        Cine.consultar_cine("672fe5a7658b89859dc24838")
