from flask import Blueprint, request, jsonify, Response
from models.usuario_generico import UsuarioGenerico
from schemas.usuario_generico_schema import UsuarioGenericoSchema
from marshmallow import ValidationError

blueprint = Blueprint("UsuarioGenerico", "usuario_generico", url_prefix="/usuario_generico")

@blueprint.route("", methods=["POST"])
def crear_usuario_generico():
    data = request.json

    data['preferencias'] = data['preferencias'].split(',')
    schema = UsuarioGenericoSchema()
    
    try:
        datos_validados = schema.load(data)
        nuevo_usuario = UsuarioGenerico(datos_validados)
        respuesta = nuevo_usuario.insertar_usuario_generico()
        return respuesta, 200
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500
    except ValidationError as e:
        errors = e.messages
        first_error_key = next(iter(errors))
        error_message = errors[first_error_key][0]
        return jsonify({"error": error_message}), 400
    except Exception as e:
        return jsonify({"error": f"{e}"}), 500

@blueprint.route("/<id>", methods=["DELETE"])
def eliminar_usuario(id):
    try:
        respuesta = UsuarioGenerico.eliminar_usuario_generico(id)
        return respuesta, 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"Error inesperado: {e}"}), 500

@blueprint.route("", methods=["GET"])
def consultar_usuarios():
    try:
        respuesta = UsuarioGenerico.consultar_usuarios()
        return Response(respuesta, mimetype="application/json"), 200
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"Error inesperado: {e}"}), 500

@blueprint.route("/<id>", methods=["GET"])
def consultar_usuario(id):
    try:
        respuesta = UsuarioGenerico.consultar_usuario(id)
        return Response(respuesta, mimetype="application/json"), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"Error inesperado: {e}"}), 500

@blueprint.route("/<id>", methods=["PUT"])
def actualizar_usuario(id):
    data = request.json
    try:
        respuesta = UsuarioGenerico.actualizar_usuario(id, data)
        return respuesta, 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"Error inesperado: {e}"}), 500

@blueprint.route("/invita_actividad", methods=["POST"])
def invita_actividad():
    data = request.json
    id_actividad = data.get("id_actividad")
    id = data.get("id_usuario")

    print(data)
    try:
        respuesta = UsuarioGenerico.invita_actividad(id, id_actividad)
        return respuesta, 200
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"Error inesperado: {e}"}), 500