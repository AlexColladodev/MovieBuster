from flask import Blueprint, request, jsonify, Response
from models.pelicula import Pelicula
from schemas.pelicula_schema import PeliculaSchema
from marshmallow import ValidationError

blueprint = Blueprint("Pelicula", "peliculas", url_prefix="/peliculas")

@blueprint.route("", methods=["POST"])
def crear_pelicula():
    data = request.json
    schema = PeliculaSchema()

    try:
        datos_validados = schema.load(data)
        pelicula = Pelicula(datos_validados)
        resultado = pelicula.insertar_pelicula()
        return jsonify(resultado), 200
    except ValidationError as e:
        errors = e.messages
        first_error_key = next(iter(errors))
        error_message = errors[first_error_key][0]
        return jsonify({"error": error_message}), 400
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"Error inesperado al crear película: {str(e)}"}), 500

@blueprint.route("/<id>", methods=["DELETE"])
def eliminar_pelicula(id):
    try:
        resultado = Pelicula.eliminar_pelicula(id)
        return jsonify(resultado), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"Error inesperado al eliminar película: {str(e)}"}), 500

@blueprint.route("", methods=["GET"])
def consultar_peliculas():
    try:
        respuesta = Pelicula.consultar_peliculas()
        return Response(respuesta, mimetype="application/json"), 200
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500
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
        return jsonify({"error": f"Error inesperado al consultar película: {str(e)}"}), 500

@blueprint.route("/<id>", methods=["PUT"])
def actualizar_pelicula(id):
    data = request.json
    schema = PeliculaSchema()
    
    try:
        datos_validados = schema.load(data)
        resultado = Pelicula.actualizar_pelicula(id, datos_validados)
        return jsonify(resultado), 200
    except ValidationError as e:
        errors = e.messages
        first_error_key = next(iter(errors))
        error_message = errors[first_error_key][0]
        return jsonify({"error": error_message}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"Error inesperado al actualizar película: {str(e)}"}), 500
