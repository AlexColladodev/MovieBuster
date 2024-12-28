import pytest
from models.cine import Cine
from bson import ObjectId, json_util
from app import app

@pytest.fixture
def mock_mongo(mocker):
    return mocker.patch("models.administrador_cine.mongo.db")


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

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


def test_crear_cine_correctamente(client, mock_mongo):
    def mock_find_one(query):
        if "nombre_cine" in query or "cif" in query:
            return None
        if "_id" in query:
            return {"_id": ObjectId(query["_id"])}
        return None

    mock_mongo.cines.find_one.side_effect = mock_find_one
    mock_mongo.cines.insert_one.return_value.inserted_id = ObjectId("1234567890abcdef12345678")

    payload = {
        "cif": "A12345678",
        "nombre_cine": "Cine Ejemplo",
        "id_administrador": "1234567890abcdef12345678",
        "peliculas": []
    }

    response = client.post("/cines", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Cine creado con éxito"


def test_crear_cine_incorrectamente(client, mock_mongo):
    mock_mongo.cines.find_one.side_effect = lambda query: None

    payload = {
        "cif": "A123", 
        "nombre_cine": "Cine No Válido",
        "id_administrador": "1234567890abcdef12345678",
        "peliculas": []
    }

    response = client.post("/cines", json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "El CIF debe tener al menos 9 caracteres, sin contar espacios en blanco."


def test_eliminar_cine_correctamente(client, mock_mongo):
    mock_mongo.cines.find_one.return_value = {"_id": ObjectId("1234567890abcdef12345678")}
    mock_mongo.cines.delete_one.return_value.deleted_count = 1

    response = client.delete("/cines/1234567890abcdef12345678")
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Cine 1234567890abcdef12345678 eliminado con éxito"


def test_eliminar_cine_incorrectamente(client, mock_mongo):
    mock_mongo.cines.find_one.return_value = None

    response = client.delete("/cines/1234567890abcdef12345678")
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Cine no encontrado"


def test_consultar_cine_correctamente(client, mock_mongo):
    mock_mongo.cines.find_one.return_value = {
        "_id": ObjectId("1234567890abcdef12345678"),
        "cif": "A12345678",
        "nombre_cine": "Cine Ejemplo",
        "id_administrador": "1234567890abcdef12345678",
        "peliculas": []
    }

    response = client.get("/cines/1234567890abcdef12345678")
    assert response.status_code == 200
    data = response.get_json()
    assert data["nombre_cine"] == "Cine Ejemplo"


def test_consultar_cine_incorrectamente(client, mock_mongo):
    mock_mongo.cines.find_one.return_value = None

    response = client.get("/cines/1234567890abcdef12345678")
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Cine no encontrado"