import pytest
from models.pelicula import Pelicula
from bson import ObjectId, json_util
from app import app

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

@pytest.fixture
def mock_mongo(mocker):
    return mocker.patch("models.pelicula.mongo.db")


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

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


def test_crear_pelicula_correctamente(client, mock_mongo):
    def mock_find_one(query):
        if "_id" in query:
            return {"_id": ObjectId(query["_id"])} 
        return None

    mock_mongo.cines.find_one.side_effect = mock_find_one
    mock_mongo.peliculas.insert_one.return_value.inserted_id = ObjectId("1234567890abcdef12345678")

    payload = {
        "nombre_pelicula": "El Conjuro",
        "descripcion_pelicula": "Película de miedo",
        "id_cine": "1234567890abcdef12345678",
        "fecha_hora": ["2024-12-01T20:00:00", "2024-12-02T22:00:00"],
        "genero": ["Drama", "Suspenso"]
    }

    response = client.post("/peliculas", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Película creada con éxito"


def test_crear_pelicula_incorrectamente(client, mock_mongo):
    mock_mongo.cines.find_one.return_value = None  

    payload = {
        "nombre_pelicula": "El Conjuro",
        "descripcion_pelicula": "Película de miedo",
        "id_cine": "1234567890abcdef12345678", 
        "fecha_hora": ["2024-12-01T20:00:00", "2024-12-02T22:00:00"],
        "genero": ["Drama", "Suspenso"]
    }

    response = client.post("/peliculas", json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "ID de Cine no válido"


def test_eliminar_pelicula_correctamente(client, mock_mongo):
    mock_mongo.peliculas.find_one.return_value = {"_id": ObjectId("1234567890abcdef12345678")}
    mock_mongo.peliculas.delete_one.return_value.deleted_count = 1

    response = client.delete("/peliculas/1234567890abcdef12345678")
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Película eliminada con éxito"


def test_eliminar_pelicula_incorrectamente(client, mock_mongo):
    mock_mongo.peliculas.find_one.return_value = None 

    response = client.delete("/peliculas/1234567890abcdef12345678")
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Película no encontrada"


def test_obtener_pelicula_correctamente(client, mock_mongo):
    mock_mongo.peliculas.find_one.return_value = {
        "_id": ObjectId("1234567890abcdef12345678"),
        "nombre_pelicula": "El Conjuro",
        "descripcion_pelicula": "Película de miedo",
        "id_cine": "1234567890abcdef12345678",
        "fecha_hora": ["2024-12-01T20:00:00", "2024-12-02T22:00:00"],
        "genero": ["Drama", "Suspenso"],
        "reviews": []
    }

    response = client.get("/peliculas/1234567890abcdef12345678")
    assert response.status_code == 200
    data = response.get_json()
    assert data["nombre_pelicula"] == "El Conjuro"


def test_obtener_pelicula_incorrectamente(client, mock_mongo):
    mock_mongo.peliculas.find_one.return_value = None  

    response = client.get("/peliculas/1234567890abcdef12345678")
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Película no encontrada"


def test_actualizar_pelicula_correctamente(client, mock_mongo):
    mock_mongo.peliculas.find_one.return_value = {"_id": ObjectId("1234567890abcdef12345678")}
    mock_mongo.peliculas.update_one.return_value.modified_count = 1

    payload = {
        "nombre_pelicula": "El Conjuro",
        "descripcion_pelicula": "Película de miedo",
        "id_cine": "1234567890abcdef12345678",
        "fecha_hora": ["2024-12-03T18:00:00"],
        "genero": ["Acción", "Aventura"]
    }

    response = client.put("/peliculas/1234567890abcdef12345678", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Película actualizada con éxito"