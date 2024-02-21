""" Flask API base file
This file is the base of the Flask API. It contains the basic structure of the API.    
"""

from flask import Flask
from .endpoints.index import index_bp


def create_app():
    """
    Create a Flask application instance.
    Returns:
        Flask -- A Flask application instance
    """
    app = Flask(__name__)

    app.register_blueprint(index_bp)

    #TODO: connect to db
    return app
