"""PROYECTO DE APRENDIZAJE
"""
import os
from flask import Flask

def create_app():
    """Creamos la APP


    si quieres evitar estar escribiendo esto puedes usar:
    (al final del archivo activate de tu entorno de desarrolo (VENV))
    export FLASK_DATABASE_HOST='127.0.0.1'
    export FLASK_DATABASE_USER='user'
    export FLASK_DATABASE_PASSWORD='password'
    export FLASK_DATABASE='tudatabase'
    export FLASK_APP='aplicacion:create_app'
    """
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY = "mikey",
        DATABASE_HOST = os.environ.get('FLASK_DATABASE_HOST'),
        DATABASE_PASSWORD = os.environ.get('FLASK_DATABASE_PASSWORD'),
        DATABASE_USER = os.environ.get('FLASK_DATABASE_USER'),
        DATABASE = os.environ.get('FLASK_DATABASE'),
    )

    @app.route('/')#podemos tener las rutas que necesitemos
    def hola():
        """Devuelve un hola mundo como simulando lo que seria un index"""
        return 'Hola Mundo!!! esta es una pagina secreta que solo se podra acceder si tenemos la ruta /saludo'
    return app