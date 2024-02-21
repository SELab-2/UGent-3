""" Flask API base file
This file is the base of the Flask API. It contains the basic structure of the API.    
"""

from os import getenv
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .endpoints.index import index_bp

db = SQLAlchemy()
load_dotenv()

def create_app():
    """
    Create a Flask application instance.
    Returns:
        Flask -- A Flask application instance
    """
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DB_HOST')
    app.register_blueprint(index_bp)
    db.init_app(app)

    return app
