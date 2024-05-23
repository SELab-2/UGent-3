"""Api endpoint to handle logout requests"""
from os import getenv

from dotenv import load_dotenv
from flask import Blueprint, redirect
from flask_jwt_extended import unset_jwt_cookies, jwt_required
from flask_restful import Resource, Api

logout_bp = Blueprint("logout", __name__)
logout_api = Api(logout_bp)

load_dotenv()
HOMEPAGE_URL = getenv("HOMEPAGE_URL")

class Logout(Resource):
    """Api endpoint for the /auth route"""

    @jwt_required()
    def get(self):
        """
        Will handle the request according to the method defined in the .env variables.
        Currently only Microsoft and our test authentication are supported
        """
        resp = redirect(HOMEPAGE_URL, 303)
        unset_jwt_cookies(resp)
        return resp

logout_api.add_resource(Logout, "/logout")
