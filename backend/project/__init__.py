""" Flask API base file
This file is the base of the Flask API. It contains the basic structure of the API.    
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .endpoints.index import index_bp

db = SQLAlchemy()

def create_app():
    """
    Create a Flask application instance.
    Returns:
        Flask -- A Flask application instance
    """

    app = Flask(__name__)
    app.register_blueprint(index_bp)

    return app

def init_db(db_uri):
    """Initialize the database with the given uri"""
    app = create_app()
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    db.init_app(app)
    return app
