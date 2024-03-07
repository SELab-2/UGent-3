"""Users api endpoint"""
from os import getenv

from dotenv import load_dotenv
from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy.exc import SQLAlchemyError

from project import db
from project.models.users import User as userModel

users_bp = Blueprint("users", __name__)
users_api = Api(users_bp)

load_dotenv()
API_URL = getenv("API_HOST")

class Users(Resource):
    """Api endpoint for the /users route"""

    def get(self):
        """
        This function will respond to get requests made to /users.
        It should return all users from the database.
        """
        users = userModel.query.all()

        result = jsonify({"message": "Queried all users", "data": users, "url":f"{API_URL}/users/"})
        return result

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
                "message": "Invalid request data!",
                "Correct Format": {
                    "uid": "User ID (string)",
                    "is_teacher": "Teacher status (boolean)",
                    "is_admin": "Admin status (boolean)"
                }
            }, 400
        try:
            user = db.session.get(userModel, uid)
            if user is not None:
                # bad request, error code could be 409 but is rarely used
                return {"message": f"User {uid} already exists"}, 400
            # Code to create a new user in the database using the uid, is_teacher, and is_admin
            new_user = userModel(uid=uid, is_teacher=is_teacher, is_admin=is_admin)
            db.session.add(new_user)
            db.session.commit()

        except SQLAlchemyError:
            # every exception should result in a rollback
            db.session.rollback()
            return {"message": "An error occurred while creating the user"}, 500
        user_js = {
            'uid': user.uid,
            'is_teacher': user.is_teacher,
            'is_admin': user.is_admin
        }
        return {"message": "User created successfully!", "data": user_js, "url": f"{API_URL}/users/{user.uid}"}, 201


class User(Resource):
    """Api endpoint for the /users/{user_id} route"""

    def get(self, user_id):
        """
        This function will respond to GET requests made to /users/<user_id>.
        It should return the user with the given user_id from the database.
        """
        user = db.session.get(userModel, user_id)
        if user is None:
            return {"message": "User not found!"}, 404

        user_js = {
            'uid': user.uid,
            'is_teacher': user.is_teacher,
            'is_admin': user.is_admin
        }
        return {"message": "User queried","data":user_js, "url": f"{API_URL}/users/{user.uid}"}, 200

    def patch(self, user_id):
        """
        Update the user's information.

        Returns:
            dict: A dictionary containing the message indicating the success
             or failure of the update.
        """
        is_teacher = request.json.get('is_teacher')
        is_admin = request.json.get('is_admin')
        try:
            user = db.session.get(userModel, user_id)
            if user is None:
                return {"message": "User not found!"}, 404

            if is_teacher is not None:
                user.is_teacher = is_teacher
            if is_admin is not None:
                user.is_admin = is_admin

            # Save the changes to the database
            db.session.commit()
        except SQLAlchemyError:
            # every exception should result in a rollback
            db.session.rollback()
            return {"message": "An error occurred while patching the user"}, 500
        user_js = {
            'uid': user.uid,
            'is_teacher': user.is_teacher,
            'is_admin': user.is_admin
        }
        return {"message": "User updated successfully!", "data": user_js, "url": f"{API_URL}/users/{user.uid}"}

    def delete(self, user_id):
        """
        This function will respond to DELETE requests made to /users/<user_id>.
        It should delete the user with the given user_id from the database.
        """
        try:
            user = db.session.get(userModel, user_id)
            if user is None:
                return {"message": "User not found!"}, 404

            db.session.delete(user)
            db.session.commit()
        except SQLAlchemyError:
            # every exception should result in a rollback
            db.session.rollback()
            return {"message": "An error occurred while deleting the user"}, 500
        return {"message": "User deleted successfully!"}


users_api.add_resource(Users, "/users")
users_api.add_resource(User, "/users/<string:user_id>")
