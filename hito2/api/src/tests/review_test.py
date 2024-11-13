import pytest
from models.review import Review
from bson import ObjectId, json_util

id_review = ObjectId("672fdf7af627c95d2c39b6a7")
id_usuario = ObjectId("6734cec1687778e880f2d499")
id_pelicula = ObjectId("672fde2685100afefc644244")

data_review = {
    "calificacion": 4.9,
    "mensaje": "Excelente película",
    "id_usuario": str(id_usuario),
    "id_pelicula": str(id_pelicula),
    "fecha_creacion": "2024-12-10T18:30:00"
}

def test_insertar_review(mocker):
    mock_db = mocker.patch('models.review.mongo.db')
    mock_reviews = mock_db.reviews
    mock_peliculas = mock_db.peliculas

    mock_reviews.insert_one.return_value.inserted_id = id_review
    mock_peliculas.find_one.return_value = {"_id": id_pelicula}
    mock_peliculas.update_one.return_value.modified_count = 1

    review = Review(data_review)
    response, status_code = review.insertar_review()
    assert response["message"] == "Review creada con éxito"
    assert response["id_review"] == str(id_review)

def test_insertar_review_pelicula_no_encontrada(mocker):
    mock_db = mocker.patch('models.review.mongo.db')
    mock_peliculas = mock_db.peliculas
    mock_peliculas.find_one.return_value = None

    review = Review(data_review)
    response, status_code = review.insertar_review()
    assert response["error"] == "Película no encontrada"

def test_eliminar_review_existente(mocker):
    mock_db = mocker.patch('models.review.mongo.db')
    mock_reviews = mock_db.reviews

    mock_reviews.find_one.return_value = {"_id": id_review}
    mock_reviews.delete_one.return_value.deleted_count = 1

    response, status_code = Review.eliminar_review(str(id_review))
    assert response["message"] == "Review eliminada con éxito"

def test_eliminar_review_no_encontrada(mocker):
    mock_db = mocker.patch('models.review.mongo.db')
    mock_reviews = mock_db.reviews
    mock_reviews.find_one.return_value = None

    response, status_code = Review.eliminar_review(str(id_review))
    assert response["error"] == "Review no encontrada"

def test_consultar_reviews(mocker):
    mock_db = mocker.patch('models.review.mongo.db')
    mock_reviews = mock_db.reviews
    mock_reviews.find.return_value = [{"_id": id_review, "mensaje": "Excelente pelicula"}]

    response, status_code = Review.consultar_reviews()
    assert '"mensaje": "Excelente pelicula"' in response

def test_consultar_review_encontrada(mocker):
    mock_db = mocker.patch('models.review.mongo.db')
    mock_reviews = mock_db.reviews
    mock_usuarios = mock_db.usuarios_genericos
    mock_peliculas = mock_db.peliculas

    mock_reviews.find_one.return_value = {"_id": id_review, "id_usuario": id_usuario, "id_pelicula": id_pelicula}
    mock_usuarios.find_one.return_value = {"nombre_usuario": "Carlos"}
    mock_peliculas.find_one.return_value = {"nombre_pelicula": "Inception"}

    response, status_code = Review.consultar_review(str(id_review))
    assert '"nombre_usuario": "Carlos"' in response
    assert '"nombre_pelicula": "Inception"' in response

def test_consultar_review_no_encontrada(mocker):
    mock_db = mocker.patch('models.review.mongo.db')
    mock_reviews = mock_db.reviews
    mock_reviews.find_one.return_value = None

    response, status_code = Review.consultar_review(str(id_review))
    assert response["error"] == "Review no encontrada"
