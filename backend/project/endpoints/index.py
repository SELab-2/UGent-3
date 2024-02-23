"""Index api point"""
from flask import Blueprint
from flask_restful import Resource

index_bp = Blueprint("index", __name__)


class Index(Resource):
    """Api endpoint for the / route"""

    def get(self):
        """Example of an api endpoint function that will respond to get requests made to /
        return a json data structure with key Message and value Hello World!"""
        return {"Message": "Hello World!"}


index_bp.add_url_rule("/", view_func=Index.as_view("index"))
