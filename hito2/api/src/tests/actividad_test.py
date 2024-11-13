import pytest
from datetime import date, datetime
from models.actividad import Actividad
from bson import ObjectId, json_util

data_actividad = {
    "nombre_actividad": "Serie en Casa de Matías",
    "descripcion_actividad": "Nos vamos a ver Hazbin Hotel entera",
    "ubicacion": "Casa de Matías",
    "fecha_actividad": "2024-12-10",
    "hora_actividad": "18:30:00",
    "id_usuario_creador": ObjectId("672fe21e3a6026f528db5f7b"),
    "participantes": []
}

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
