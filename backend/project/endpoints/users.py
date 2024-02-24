# users.py
from flask import Blueprint, request
from flask_restful import Resource, Api

users_bp = Blueprint("users", __name__)
users_api = Api(users_bp)

class Users(Resource):
    """Api endpoint for the /users route"""


    def post(self):
        """
        This function will respond to post requests made to /users.
        It should create a new user and return a success message.
        """
        uid = request.json.get('uid')
        is_teacher = request.json.get('is_teacher')
        is_admin = request.json.get('is_admin')

        if is_teacher is None or is_admin is None or uid is None:
            return {
                "Message": "Invalid request data!",
                "Correct Format": {
                    "uid": "User ID (string)",
                    "is_teacher": "Teacher status (boolean)",
                    "is_admin": "Admin status (boolean)"
                    }
                }, 400
        
        # Code to create a new user in the database using the uid, is_teacher, and is_admin values

        return {"Message": "User created successfully!"}

users_api.add_resource(Users, "/users")