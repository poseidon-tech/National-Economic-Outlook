from flask import Flask
from neo.db import initialize_db
from dotenv import load_dotenv
import os


def create_app():
    app = Flask(__name__)

    dotenv_path = 'neo/.env'
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

    initialize_db(app)
    register_blueprints(app)
    return app


def register_blueprints(app: Flask):
    from neo.query import query1

    app.register_blueprint(query1.bp)


