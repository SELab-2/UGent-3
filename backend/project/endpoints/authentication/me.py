"""User info api endpoint"""
from os import getenv

from dotenv import load_dotenv
from flask import Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource, Api

from project.models.user import User
from project.utils.query_agent import query_by_id_from_model

load_dotenv()
API_URL = getenv("API_HOST")

me_bp = Blueprint("me", __name__)
me_api = Api(me_bp)

class Me(Resource):
    """Api endpoint for the /user_info route"""

    @jwt_required()
    def get(self):
        """
        Will return all user data associated with the access token in the request
        """
        uid = get_jwt_identity

        return query_by_id_from_model(User,
                                      "uid",
                                      uid,
                                      "Could not find you in the database, please log in again")

me_api.add_resource(Me, "/me")
