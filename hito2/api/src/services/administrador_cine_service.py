from flask import Blueprint, request, Response, jsonify
from models.administrador_cine import AdministradorCine
from schemas.administrador_cine_schema import AdministradorCineSchema
from marshmallow import ValidationError

blueprint = Blueprint("AdministradorCine", "administrador_cine", url_prefix="/administrador_cine")

@blueprint.route("", methods=["POST"])
def crear_administrador_cine():
    data = request.json
    schema = AdministradorCineSchema()

    try:
        datos_validados = schema.load(data)
        administrador_cine = AdministradorCine(datos_validados)
        resultado = administrador_cine.insertar_administrador_cine()
        return jsonify(resultado), 200
    except ValidationError as e:
        errors = e.messages
        first_error_key = next(iter(errors))
        error_message = errors[first_error_key][0]
        return jsonify({"error": error_message}), 400
    except Exception as e:
        return jsonify({"error": f"{e}"}), 500

@blueprint.route("/<id>", methods=["DELETE"])
def eliminar_administrador_cine(id):
    try:
        respuesta = AdministradorCine.eliminar_administrador_cine(id)
        return jsonify(respuesta), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"{e}"}), 500

@blueprint.route("", methods=["GET"])
def consultar_administradores_cine():
    try:
        respuesta = AdministradorCine.consultar_administradores_cines()
        return Response(respuesta, mimetype="application/json"), 200
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"Error inesperado al consultar administradores de cine: {e}"}), 500

@blueprint.route("/<id>", methods=["GET"])
def consultar_administrador_cine(id):
    try:
        respuesta = AdministradorCine.consultar_administrador(id)
        return Response(respuesta, mimetype="application/json"), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"Error inesperado al consultar administrador de cine: {e}"}), 500

