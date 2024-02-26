"""Users api endpoint"""
from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api
from project import db  # pylint: disable=import-error ; there is no error
from project.models.users import Users as UserModel  # pylint: disable=import-error ; there is no error

users_bp = Blueprint("users", __name__)
users_api = Api(users_bp)


class Users(Resource):
    """Api endpoint for the /users route"""

    def get(self):
        """
        This function will respond to get requests made to /users.
        It should return all users from the database.
        """
        users = UserModel.query.all()

        return jsonify(users)

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
        try:
            user = db.session.get(UserModel, uid)
            if user is not None:
                # bad request, error code could be 409 but is rarely used
                return {"Message": f"User {uid} already exists"}, 400
            # Code to create a new user in the database using the uid, is_teacher, and is_admin
            new_user = UserModel(uid=uid, is_teacher=is_teacher, is_admin=is_admin)
            db.session.add(new_user)
            db.session.commit()

        except Exception as e:  # pylint: disable=broad-exception-caught ;
            # every exception should result in a rollback
            db.session.rollback()
            return {"Message": f"An error occurred while creating the user: {str(e)}"}, 500

        return {"Message": "User created successfully!"}, 201


class User(Resource):
    """Api endpoint for the /users/{user_id} route"""

    def get(self, user_id):
        """
        This function will respond to GET requests made to /users/<user_id>.
        It should return the user with the given user_id from the database.
        """
        user = db.session.get(UserModel, user_id)
        if user is None:
            return {"Message": "User not found!"}, 404

        return jsonify(user)

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
            user = db.session.get(UserModel, user_id)
            if user is None:
                return {"Message": "User not found!"}, 404

            if is_teacher is not None:
                user.is_teacher = is_teacher
            if is_admin is not None:
                user.is_admin = is_admin

            # Save the changes to the database
            db.session.commit()
        except Exception as e:  # pylint: disable=broad-exception-caught ;
            # every exception should result in a rollback
            db.session.rollback()
            return {"Message": f"An error occurred while patching the user: {str(e)}"}, 500
        return {"Message": "User updated successfully!"}

    def delete(self, user_id):
        """
        This function will respond to DELETE requests made to /users/<user_id>.
        It should delete the user with the given user_id from the database.
        """
        try:
            user = db.session.get(UserModel, user_id)
            if user is None:
                return {"Message": "User not found!"}, 404

            db.session.delete(user)
            db.session.commit()
        except Exception as e:  # pylint: disable=broad-exception-caught ;
            # every exception should result in a rollback
            db.session.rollback()
            return {"Message": f"An error occurred while deleting the user: {str(e)}"}, 500
        return {"Message": "User deleted successfully!"}


users_api.add_resource(Users, "/users")
users_api.add_resource(User, "/users/<string:user_id>")
