from flask import Blueprint, request, jsonify, Response
from models.pelicula import Pelicula
from marshmallow import ValidationError

blueprint = Blueprint("Pelicula", "peliculas", url_prefix="/peliculas")

@blueprint.route("", methods=["POST"])
def crear_pelicula():
    data = request.json
    try:
        resultado, status_code = Pelicula.insertar_pelicula(data)
        return jsonify(resultado), status_code
    except Exception as e:
        return jsonify({"error": f"Error inesperado al crear película: {str(e)}"}), 500

@blueprint.route("/<id>", methods=["DELETE"])
def eliminar_pelicula(id):
    try:
        resultado, status_code = Pelicula.eliminar_pelicula(id)
        return jsonify(resultado), status_code
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": f"Error inesperado al eliminar película: {str(e)}"}), 500

@blueprint.route("", methods=["GET"])
def consultar_peliculas():
    try:
        respuesta = Pelicula.consultar_peliculas()
        return Response(respuesta, mimetype="application/json"), 200
    except Exception as e:
        return jsonify({"error": f"Error inesperado al consultar películas: {str(e)}"}), 500

@blueprint.route("/<id>", methods=["GET"])
def consultar_pelicula(id):
    try:
        respuesta = Pelicula.consultar_pelicula(id)
        return Response(respuesta, mimetype="application/json"), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"Error inesperado: {e}"}), 500

@blueprint.route("/<id>", methods=["PUT"])
def actualizar_pelicula(id):
    data = request.json
    try:
        resultado, status_code = Pelicula.actualizar_pelicula(id, data)
        return jsonify(resultado), status_code
    except ValidationError as e:
        return jsonify({"error": e.messages}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": f"Error inesperado al actualizar película: {str(e)}"}), 500
