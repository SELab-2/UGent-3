"""Users api endpoint"""
from flask import Blueprint, request
from flask_restful import Resource, Api
from project import db
from project.models.users import Users as UserModel

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
        users_list = [{"uid": user.uid, "is_teacher": user.is_teacher, "is_admin": user.is_admin} for user in users]
        return users_list

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

        new_user = UserModel(uid=uid, is_teacher=is_teacher, is_admin=is_admin)
        db.session.add(new_user)
        db.session.commit()
        return {"Message": "User created successfully!"}

    def update(self):
            """
            Update the user's information.

            Returns:
                dict: A dictionary containing the message indicating the success or failure of the update.
            """
            uid = request.json.get('uid')
            is_teacher = request.json.get('is_teacher')
            is_admin = request.json.get('is_admin')
            if uid is None:
                return {"Message": "User ID is required!"}, 400

            user = UserModel.query.get(uid)
            if user is None:
                return {"Message": "User not found!"}, 404

            if is_teacher is not None:
                user.is_teacher = is_teacher
            if is_admin is not None:
                user.is_admin = is_admin

            # Save the changes to the database
            db.session.commit()
            return {"Message": "User updated successfully!"}


users_api.add_resource(Users, "/users")
