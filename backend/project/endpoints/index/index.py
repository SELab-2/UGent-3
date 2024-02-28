"""Index api point"""
import os
from flask import Blueprint, send_from_directory
from flask_restful import Resource, Api

index_bp = Blueprint("index", __name__)
index_endpoint = Api(index_bp)

class Index(Resource):
    """Api endpoint for the / route"""

    def get(self):
        """
        Example of an api endpoint function that will respond to get requests made to
        return a json data structure with key Message and value Hello World!
        """
        dir_path = os.path.dirname(os.path.realpath(__file__))
        return send_from_directory(dir_path, "OpenAPI_Object.json")


index_bp.add_url_rule("/", view_func=Index.as_view("index"))
