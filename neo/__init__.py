from flask import Flask
from neo.db import initialize_db
from dotenv import load_dotenv
import os

app = Flask(__name__)

dotenv_path = 'neo/.env'
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

initialize_db(app)
