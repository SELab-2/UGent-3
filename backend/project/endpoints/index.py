"""
This is the index endpoint file. It contains the index endpoint of the API as specified by OpenAPI.
"""

from flask import Blueprint
from flask_restful import Resource

index_bp = Blueprint("index", __name__)

class Index(Resource):
    """
    Subclass of restfull Resource, used to define the index endpoint of the API.
    """

    def get(self):
        """
        Implementation of the GET method for the index endpoint. Returns the OpenAPI object.
        """

        return {"Message": "Hello World!"}

index_bp.add_url_rule("/", view_func=Index.as_view("index"))
