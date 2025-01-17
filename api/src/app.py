from flask import Flask, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from werkzeug.security import check_password_hash
from flask_restx import Api
from flask_cors import CORS
from db import init_mongo
from services import usuario_generico_service, administrador_cine_service, cine_service, pelicula_service, actividad_service, review_service
from flask_swagger_ui import get_swaggerui_blueprint
import logging
from logging.handlers import RotatingFileHandler
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "Ap?&/u]rk0b5=:+E"

jwt = JWTManager(app)
CORS(app)

# Set up MongoDB connection
mongo_uri = os.getenv(
    "MONGO_URI",
    "mongodb+srv://AlexColladodev:Alex-25-MovieBuster@moviebuster.lezf0.mongodb.net/?retryWrites=true&w=majority&appName=MovieBuster"
)
client = MongoClient(mongo_uri, server_api=ServerApi('1'))
db = client["MovieBuster"]  # Use the correct database name

init_mongo(app)

api = Api(app)

access_log_handler = RotatingFileHandler("api_access.log", maxBytes=1000000, backupCount=3)
access_log_handler.setLevel(logging.INFO)
access_log_formatter = logging.Formatter('%(message)s')
access_log_handler.setFormatter(access_log_formatter)

console_handler = logging.StreamHandler()  
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(access_log_formatter)

werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.setLevel(logging.INFO)
werkzeug_logger.addHandler(access_log_handler)
werkzeug_logger.addHandler(console_handler)

app.register_blueprint(usuario_generico_service.blueprint)
app.register_blueprint(administrador_cine_service.blueprint)
app.register_blueprint(cine_service.blueprint)
app.register_blueprint(pelicula_service.blueprint)
app.register_blueprint(actividad_service.blueprint)
app.register_blueprint(review_service.blueprint)

SWAGGER_URL = '/swagger'
API_URL = '/static/openapi.yaml'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "MovieBuster API"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/nombre', methods=['GET'])
def obtener_nombre_usuario():
    return jsonify({"nombre_usuario": "nombre"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
