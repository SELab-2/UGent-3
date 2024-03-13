"""Users api endpoint"""
from os import getenv

from dotenv import load_dotenv
from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy.exc import SQLAlchemyError

from project.db_in import db
from project.models.user import User as userModel

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
        try:
            query = userModel.query
            is_teacher = request.args.get('is_teacher')
            is_admin = request.args.get('is_admin')

            if is_teacher is not None:
                query = query.filter(userModel.is_teacher == (is_teacher.lower() == 'true'))

            if is_admin is not None:
                query = query.filter(userModel.is_admin == (is_admin.lower() == 'true'))

            users = query.all()

            result = jsonify({"message": "Queried all users", "data": users,
                              "url":f"{API_URL}/users", "status_code": 200})
            return result
        except SQLAlchemyError:
            return {"message": "An error occurred while fetching the users",
                    "url": f"{API_URL}/users"}, 500

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
                "correct_format": {
                    "uid": "User ID (string)",
                    "is_teacher": "Teacher status (boolean)",
                    "is_admin": "Admin status (boolean)"
                },"url": f"{API_URL}/users"
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
            return jsonify({"message": "User created successfully!",
                    "data": user, "url": f"{API_URL}/users/{user.uid}", "status_code": 201})

        except SQLAlchemyError:
            # every exception should result in a rollback
            db.session.rollback()
            return {"message": "An error occurred while creating the user",
                    "url": f"{API_URL}/users"}, 500



class User(Resource):
    """Api endpoint for the /users/{user_id} route"""

    def get(self, user_id):
        """
        This function will respond to GET requests made to /users/<user_id>.
        It should return the user with the given user_id from the database.
        """
        try:
            user = db.session.get(userModel, user_id)
            if user is None:
                return {"message": "User not found!","url": f"{API_URL}/users"}, 404

            return jsonify({"message": "User queried","data":user,
                    "url": f"{API_URL}/users/{user.uid}", "status_code": 200})
        except SQLAlchemyError:
            return {"message": "An error occurred while fetching the user",
                    "url": f"{API_URL}/users"}, 500

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
                return {"message": "User not found!","url": f"{API_URL}/users"}, 404

            if is_teacher is not None:
                user.is_teacher = is_teacher
            if is_admin is not None:
                user.is_admin = is_admin

            # Save the changes to the database
            db.session.commit()
            return jsonify({"message": "User updated successfully!",
                    "data": user, "url": f"{API_URL}/users/{user.uid}", "status_code": 200})
        except SQLAlchemyError:
            # every exception should result in a rollback
            db.session.rollback()
            return {"message": "An error occurred while patching the user",
                    "url": f"{API_URL}/users"}, 500


    def delete(self, user_id):
        """
        This function will respond to DELETE requests made to /users/<user_id>.
        It should delete the user with the given user_id from the database.
        """
        try:
            user = db.session.get(userModel, user_id)
            if user is None:
                return {"message": "User not found!", "url": f"{API_URL}/users"}, 404

            db.session.delete(user)
            db.session.commit()
            return {"message": "User deleted successfully!", "url": f"{API_URL}/users"}, 200
        except SQLAlchemyError:
            # every exception should result in a rollback
            db.session.rollback()
            return {"message": "An error occurred while deleting the user",
                    "url": f"{API_URL}/users"}, 500


users_api.add_resource(Users, "/users")
users_api.add_resource(User, "/users/<string:user_id>")
