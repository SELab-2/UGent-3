from flask import Blueprint, send_from_directory
from flask_restful import Resource, Api
import os

index_bp = Blueprint("index", __name__)
index_endpoint = Api(index_bp)

class Index(Resource):
    def get(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        return send_from_directory(dir_path, "OpenAPI_Object.json")
    
index_bp.add_url_rule("/", view_func=Index.as_view("index"))