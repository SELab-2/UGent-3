""" Flask API base file
This file is the base of the Flask API. It contains the basic structure of the API.    
"""

from flask import Flask, jsonify

def create_app():
    """
    Create a Flask application instance.
    Returns:
        Flask -- A Flask application instance
    """
    app = Flask(__name__)

    @app.route("/")
    def hello():
        return jsonify({"Message": "Hello World!"})

    return app
