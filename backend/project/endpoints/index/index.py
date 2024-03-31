"""Index api point"""
import os
from flask import Blueprint, send_file
from flask_restful import Resource, Api

index_bp = Blueprint("index", __name__)
index_endpoint = Api(index_bp)

API_URL = os.getenv("DOCS_JSON_PATH")

class Index(Resource):
    """Api endpoint for the / route"""

    def get(self):
        """
        Example of an api endpoint function that will respond to get requests made to
        return a json data structure with key Message and value Hello World!
        """
        return send_file(API_URL)


index_bp.add_url_rule("/", view_func=Index.as_view("index"))
