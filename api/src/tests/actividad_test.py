import pytest
from datetime import date, datetime
from models.actividad import Actividad
from bson import ObjectId, json_util
from app import app

data_actividad = {
    "nombre_actividad": "Serie en Casa de Matías",
    "descripcion_actividad": "Nos vamos a ver Hazbin Hotel entera",
    "ubicacion": "Casa de Matías",
    "fecha_actividad": "2024-12-10",
    "hora_actividad": "18:30:00",
    "id_usuario_creador": ObjectId("672fe21e3a6026f528db5f7b"),
    "participantes": []
}

@pytest.fixture
def mock_mongo(mocker):
    return mocker.patch("models.actividad.mongo.db")


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_insertar_actividad(mocker):
    mock_db = mocker.patch('models.actividad.mongo.db')
    mock_actividades = mock_db.actividades
    mock_actividades.insert_one.return_value.inserted_id = ObjectId("672fe21e3a6026f528db5f7a")

    actividad = Actividad(data_actividad)
    response = actividad.insertar_actividad()
    assert response["message"] == "Actividad creada con éxito"
    assert response["id"] == "672fe21e3a6026f528db5f7a"

def test_eliminar_actividad_existente(mocker):
    mock_db = mocker.patch('models.actividad.mongo.db')
    mock_actividades = mock_db.actividades
    mock_actividades.find_one.return_value = {"_id": ObjectId("672fe21e3a6026f528db5f7a")}
    mock_actividades.delete_one.return_value.deleted_count = 1

    response = Actividad.eliminar_actividad("672fe21e3a6026f528db5f7a")
    assert response["message"] == "Actividad eliminada con éxito"

def test_eliminar_actividad_no_encontrada(mocker):
    mock_db = mocker.patch('models.actividad.mongo.db')
    mock_actividades = mock_db.actividades
    mock_actividades.find_one.return_value = None

    with pytest.raises(ValueError, match="Actividad no encontrada"):
        Actividad.eliminar_actividad("672fe21e3a6026f528db5f7a")

def test_consultar_actividades(mocker):
    mock_db = mocker.patch('models.actividad.mongo.db')
    mock_actividades = mock_db.actividades
    mock_actividades.find.return_value = [
        {"_id": ObjectId("672fe21e3a6026f528db5f7a"), "nombre_actividad": "HazbinHotel"}
    ]

    response = Actividad.consultar_actividades()
    assert '"nombre_actividad": "HazbinHotel"' in response

def test_consultar_actividad_encontrada(mocker):
    mock_db = mocker.patch('models.actividad.mongo.db')
    mock_actividades = mock_db.actividades
    mock_actividades.find_one.return_value = {
        "_id": ObjectId("672fe21e3a6026f528db5f7a"),
        "nombre_actividad": "HazbinHotel"
    }

    response = Actividad.consultar_actividad("672fe21e3a6026f528db5f7a")
    assert '"nombre_actividad": "HazbinHotel"' in response

def test_consultar_actividad_no_encontrada(mocker):
    mock_db = mocker.patch('models.actividad.mongo.db')
    mock_actividades = mock_db.actividades
    mock_actividades.find_one.return_value = None

    with pytest.raises(ValueError, match="Actividad no encontrada"):
        Actividad.consultar_actividad("672fe21e3a6026f528db5f7a")

def test_actualizar_actividad(mocker):
    mock_db = mocker.patch('models.actividad.mongo.db')
    mock_actividades = mock_db.actividades
    mock_actividades.update_one.return_value.matched_count = 1

    response = Actividad.actualizar_actividad("672fe21e3a6026f528db5f7a", {"nombre_actividad": "HazbinHotel S2"})
    assert response["message"] == "Actividad actualizada con éxito"

def test_actualizar_actividad_no_encontrada(mocker):
    mock_db = mocker.patch('models.actividad.mongo.db')
    mock_actividades = mock_db.actividades
    mock_actividades.update_one.return_value.matched_count = 0

    with pytest.raises(RuntimeError, match="No se puedo actualizar la actividad"):
        Actividad.actualizar_actividad("672fe21e3a6026f528db5f7a", {"nombre_actividad": "HazbinHotel S2"})

def test_crear_actividad_incorrectamente(client, mock_mongo):
    mock_mongo.usuarios_genericos.find_one.return_value = None  

    payload = {
        "nombre_actividad": "Ver película en casa",
        "descripcion_actividad": "Ver 'Inception' en casa de Juan.",
        "ubicacion": "Casa de Juan",
        "fecha_actividad": "2024-12-01",
        "hora_actividad": "20:00",
        "id_usuario_creador": "123",  
        "participantes": []
    }

    response = client.post("/actividades", json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Id de Usuario debe ser un ObjectId válido."


def test_eliminar_actividad_correctamente(client, mock_mongo):
    mock_mongo.actividades.find_one.return_value = {"_id": ObjectId("1234567890abcdef12345678")}
    mock_mongo.actividades.delete_one.return_value.deleted_count = 1

    response = client.delete("/actividades/1234567890abcdef12345678")
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Actividad eliminada con éxito"


def test_eliminar_actividad_incorrectamente(client, mock_mongo):
    mock_mongo.actividades.find_one.return_value = None 

    response = client.delete("/actividades/1234567890abcdef12345678")
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Actividad no encontrada"


def test_consultar_actividades_correctamente(client, mock_mongo):
    mock_mongo.actividades.find.return_value = [
        {
            "_id": ObjectId("1234567890abcdef12345678"),
            "nombre_actividad": "Ver película en casa",
            "descripcion_actividad": "Ver 'Inception' en casa de Juan.",
            "ubicacion": "Casa de Juan",
            "fecha_actividad": "2024-12-01",
            "hora_actividad": "20:00",
            "id_usuario_creador": "1234567890abcdef12345678",
            "participantes": []
        }
    ]

    response = client.get("/actividades")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["nombre_actividad"] == "Ver película en casa"


def test_consultar_actividad_correctamente(client, mock_mongo):
    mock_mongo.actividades.find_one.return_value = {
        "_id": ObjectId("1234567890abcdef12345678"),
        "nombre_actividad": "Ver película en casa",
        "descripcion_actividad": "Ver 'Inception' en casa de Juan.",
        "ubicacion": "Casa de Juan",
        "fecha_actividad": "2024-12-01",
        "hora_actividad": "20:00",
        "id_usuario_creador": "1234567890abcdef12345678",
        "participantes": []
    }

    response = client.get("/actividades/1234567890abcdef12345678")
    assert response.status_code == 200
    data = response.get_json()
    assert data["nombre_actividad"] == "Ver película en casa"
