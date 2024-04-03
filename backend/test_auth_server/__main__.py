"""Main entry point for the application."""

from dotenv import load_dotenv
from flask import Flask, Blueprint, request
from flask_restful import Resource, Api


index_bp = Blueprint("index", __name__)
index_endpoint = Api(index_bp)

# Take the key the same as the id, uid can then be used in backend
token_dict = {
    "teacher1":{
        "id":"Gunnar",
        "jobTitle":"teacher"
    },
    "teacher2":{
        "id":"Bart",
        "jobTitle":"teacher"
    },
    "student1":{
        "id":"w_student",
        "jobTitle":None
    },
    "student01":{
        "id":"student01",
        "jobTitle":None
    },
    "course_admin1":{
        "id":"Rien",
        "jobTitle":None
    },
    "del_user":{
        "id":"del",
        "jobTitle":None
    },
    "ad3_teacher":{
        "id":"brinkmann",
        "jobTitle0":"teacher"
    },
    "student02":{
        "id":"student02",
        "jobTitle":None
    },
    "admin1":{
        "id":"admin_person",
        "jobTitle":"admin"
    },
    # Lowest authorized user to test login requirement
    "login": {
        "id": "login",
        "jobTitle": None
    },
    # Student authorization access, associated with valid_...
    "student": {
        "id": "student",
        "jobTitle": None
    },
    # Student authorization access, other
    "student_other": {
        "id": "student_other",
        "jobTitle": None
    },
    # Teacher authorization access, associated with valid_...
    "teacher": {
        "id": "teacher",
        "jobTitle": "teacher"
    },
    # Teacher authorization access, other
    "teacher_other": {
        "id": "teacher_other",
        "jobTitle": "teacher"
    },
    # Admin authorization access, associated with valid_...
    "admin": {
        "id": "admin",
        "jobTitle": "admin"
    },
    # Admin authorization access, other
    "admin_other": {
        "id": "admin_other",
        "jobTitle": "admin"
    }
}

class Index(Resource):
    """Api endpoint for the / route"""

    def get(self):
        "Returns the data associated with the authorization bearer token"
        auth = request.headers.get("Authorization")
        if not auth:
            return {"error":"Please give authorization"}, 401
        if token_dict.get(auth, None):
            return token_dict[auth], 200
        return {"error":"Wrong address"}, 401


index_bp.add_url_rule("/", view_func=Index.as_view("index"))

load_dotenv()

app = Flask(__name__)
app.register_blueprint(index_bp)

app.run(debug=True, host='0.0.0.0', port=5001)
