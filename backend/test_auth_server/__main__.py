"""Main entry point for the application."""

from dotenv import load_dotenv
from flask import Flask

"""Index api point"""
from flask import Blueprint, request
from flask_restful import Resource, Api

index_bp = Blueprint("index", __name__)
index_endpoint = Api(index_bp)

token_dict = {
    "teacher1":{
        "id":"brinkmann",
        "jobCategory":"teacher"
    },
    "teacher2":{
        "id":"laermans",
        "jobCategory":"teacher"
    },
    "student1":{
        "id":"student01",
        "jobCategory":None
    },
    "student2":{
        "id":"student02",
        "jobCategory":None
    },
    "course_admin1":{
        "id":"Rien",
        "jobCategory":None
    },
    "del_user":{
        "id":"del",
        "jobCategory":None
    }
}

class Index(Resource):
    """Api endpoint for the / route"""

    def get(self):
        auth = request.headers.get("Authorization")
        if not auth:
            return {"message":"Please give authorization"}, 401
        bearer, token = auth.split(" ")
        if bearer != "Bearer":
            return {"message":"Not this kind of authorization"}, 401
        if token in token_dict.keys():
            return token_dict[token], 200
        return {"message":"Wrong address"}, 401
        

index_bp.add_url_rule("/", view_func=Index.as_view("index"))

if __name__ == "__main__":
    load_dotenv()

    app = Flask(__name__)
    app.register_blueprint(index_bp)

    app.run(debug=True, host='0.0.0.0')

