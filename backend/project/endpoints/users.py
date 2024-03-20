"""Users api endpoint"""
from os import getenv

from dotenv import load_dotenv
from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy.exc import SQLAlchemyError

from project import db
from project.models.user import User as userModel
from project.utils.authentication import login_required, authorize_user, not_allowed

users_bp = Blueprint("users", __name__)
users_api = Api(users_bp)

load_dotenv()
API_URL = getenv("API_HOST")


class Users(Resource):
    """Api endpoint for the /users route"""

    @login_required
    def get(self):
        """
        This function will respond to get requests made to /users.
        It should return all users from the database.
        """
        try:
            query = userModel.query
            role = request.args.get("role")

            if role is not None:
                query = query.filter(userModel.role == role.lower())

            users = query.all()

            result = jsonify({"message": "Queried all users", "data": users,
                              "url":f"{API_URL}/users", "status_code": 200})
            return result
        except SQLAlchemyError:
            return {"message": "An error occurred while fetching the users",
                    "url": f"{API_URL}/users"}, 500

    @not_allowed
    def post(self):
        # TODO make it so this just creates a user for yourself
        """
        This function will respond to post requests made to /users.
        It should create a new user and return a success message.
        """
        uid = request.json.get('uid')
        role = request.args.get("role")

        if role is None or uid is None:
            return {
                "message": "Invalid request data!",
                "correct_format": {
                    "uid": "User ID (string)",
                    "role": "User role (string)"
                },"url": f"{API_URL}/users"
            }, 400
        try:
            user = db.session.get(userModel, uid)
            if user is not None:
                # bad request, error code could be 409 but is rarely used
                return {"message": f"User {uid} already exists"}, 400
            # Code to create a new user in the database using the uid and role
            new_user = userModel(uid=uid, role=role)
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

    @login_required
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

    @not_allowed
    def patch(self, user_id):
        """
        Update the user's information.

        Returns:
            dict: A dictionary containing the message indicating the success
             or failure of the update.
        """
        role = request.args.get("role")
        try:
            user = db.session.get(userModel, user_id)
            if user is None:
                return {"message": "User not found!","url": f"{API_URL}/users"}, 404

            if role is not None:
                user.role = role

            # Save the changes to the database
            db.session.commit()
            return jsonify({"message": "User updated successfully!",
                    "data": user, "url": f"{API_URL}/users/{user.uid}", "status_code": 200})
        except SQLAlchemyError:
            # every exception should result in a rollback
            db.session.rollback()
            return {"message": "An error occurred while patching the user",
                    "url": f"{API_URL}/users"}, 500


    @authorize_user
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
