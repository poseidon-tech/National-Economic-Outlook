from flask import Flask
from flask_cors import CORS
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

    cors = CORS()
    cors.init_app(app, origins=['http://localhost:3000', 'http://127.0.0.1:3000'])
    return app


def register_blueprints(app: Flask):
    from neo.query import count_query
    from neo.query import query1

    app.register_blueprint(query1.bp)
    app.register_blueprint(count_query.bp)


