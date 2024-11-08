from flask import Blueprint, request, Response, jsonify
from models.cine import Cine
from marshmallow import ValidationError

blueprint = Blueprint("Cine", "cines", url_prefix="/cines")

@blueprint.route("", methods=["POST"])
def crear_cine():
    data = request.json
    resultado, status_code = Cine.insertar_cine(data)
    return jsonify(resultado), status_code

@blueprint.route("/<id>", methods=["DELETE"])
def eliminar_cine(id):
    try:
        respuesta = Cine.eliminar_cine(id)
        return respuesta, 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"Error inesperado: {e}"}), 500

@blueprint.route("", methods=["GET"])
def consultar_cines():
    try:
        respuesta = Cine.consultar_cines()
        return Response(respuesta, mimetype="application/json"), 200
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"Error inesperado al consultar cines: {e}"}), 500

@blueprint.route("/<id>", methods=["GET"])
def consultar_cine(id):
    try:
        respuesta = Cine.consultar_cine(id)
        return Response(respuesta, mimetype="application/json"), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"Error inesperado al consultar cine: {e}"}), 500
