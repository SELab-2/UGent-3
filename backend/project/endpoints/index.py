"""Index api point"""
from flask import Blueprint
from flask_restful import Resource

index_bp = Blueprint("index", __name__)


class Index(Resource):
    """Temporary"""

    def get(self):
        """Hello world"""
        return {"Message": "Hello World!"}


index_bp.add_url_rule("/", view_func=Index.as_view("index"))
