import pytest
from models.pelicula import Pelicula
from bson import ObjectId, json_util

id_cine = ObjectId("672fe5a7658b89859dc24838")
id_pelicula = ObjectId("672fde2685100afefc644244")

data_pelicula = {
    "nombre_pelicula": "Inception",
    "descripcion_pelicula": "A mind-bending thriller",
    "id_cine": str(id_cine),
    "fecha_hora": "2024-12-10T18:30:00",
    "genero": ["Sci-Fi", "Thriller"],
    "reviews": []
}

def test_insertar_pelicula(mocker):
    mock_db = mocker.patch('models.pelicula.mongo.db')
    mock_cines = mock_db.cines
    mock_peliculas = mock_db.peliculas

    mock_cines.find_one.return_value = {"_id": id_cine}
    mock_peliculas.insert_one.return_value.inserted_id = id_pelicula

    pelicula = Pelicula(data_pelicula)
    response = pelicula.insertar_pelicula()
    assert response["message"] == "Película creada con éxito"
    assert response["id"] == str(id_pelicula)

def test_insertar_pelicula_cine_no_encontrado(mocker):
    mock_db = mocker.patch('models.pelicula.mongo.db')
    mock_cines = mock_db.cines
    mock_cines.find_one.return_value = None

    pelicula = Pelicula(data_pelicula)
    with pytest.raises(ValueError, match="Cine no encontrado"):
        pelicula.insertar_pelicula()

def test_eliminar_pelicula_existente(mocker):
    mock_db = mocker.patch('models.pelicula.mongo.db')
    mock_peliculas = mock_db.peliculas

    mock_peliculas.find_one.return_value = {"_id": id_pelicula}
    mock_peliculas.delete_one.return_value.deleted_count = 1

    response = Pelicula.eliminar_pelicula(str(id_pelicula))
    assert response["message"] == "Película eliminada con éxito"

def test_eliminar_pelicula_no_encontrada(mocker):
    mock_db = mocker.patch('models.pelicula.mongo.db')
    mock_peliculas = mock_db.peliculas
    mock_peliculas.find_one.return_value = None

    with pytest.raises(ValueError, match="Película no encontrada"):
        Pelicula.eliminar_pelicula(str(id_pelicula))

def test_consultar_peliculas(mocker):
    mock_db = mocker.patch('models.pelicula.mongo.db')
    mock_peliculas = mock_db.peliculas
    mock_peliculas.find.return_value = [{"_id": id_pelicula, "nombre_pelicula": "Inception"}]

    response = Pelicula.consultar_peliculas()
    assert '"nombre_pelicula": "Inception"' in response

def test_consultar_pelicula_encontrada(mocker):
    mock_db = mocker.patch('models.pelicula.mongo.db')
    mock_peliculas = mock_db.peliculas
    mock_peliculas.find_one.return_value = {
        "_id": id_pelicula,
        "nombre_pelicula": "Inception"
    }

    response = Pelicula.consultar_pelicula(str(id_pelicula))
    assert '"nombre_pelicula": "Inception"' in response

def test_consultar_pelicula_no_encontrada(mocker):
    mock_db = mocker.patch('models.pelicula.mongo.db')
    mock_peliculas = mock_db.peliculas
    mock_peliculas.find_one.return_value = None

    with pytest.raises(ValueError, match="Película no encontrada"):
        Pelicula.consultar_pelicula(str(id_pelicula))

def test_actualizar_pelicula(mocker):
    mock_db = mocker.patch('models.pelicula.mongo.db')
    mock_peliculas = mock_db.peliculas
    mock_peliculas.update_one.return_value.modified_count = 1

    response = Pelicula.actualizar_pelicula(str(id_pelicula), {"nombre_pelicula": "Inception 2"})
    assert response["message"] == "Película actualizada con éxito"

def test_actualizar_pelicula_no_encontrada(mocker):
    mock_db = mocker.patch('models.pelicula.mongo.db')
    mock_peliculas = mock_db.peliculas
    mock_peliculas.update_one.return_value.modified_count = 0

    response, status_code = Pelicula.actualizar_pelicula(str(id_pelicula), {"nombre_pelicula": "Inception 2"})
    assert response["message"] == "No se realizaron cambios o película no encontrada"
