"""Index api point"""
import os
from flask import Blueprint, request
from flask_restful import Resource, Api

from test_auth_server.db_in import db
from test_auth_server.user_data import User_data

from sqlalchemy.exc import SQLAlchemyError

index_bp = Blueprint("index", __name__)
index_endpoint = Api(index_bp)

class Index(Resource):
    """Api endpoint for the / route"""

    def get(self):
        auth = request.headers.get("Authorization")
        if not auth:
            return {"message":"Please give authorization"}, 401
        bearer, token = auth.split(" ")
        if bearer != "Bearer":
            return {"message":"Not this kind of authorization"}, 401
        try:
            user_data = db.session.get(User_data, token)
        except SQLAlchemyError:
            # every exception should result in a rollback
            db.session.rollback()
            return {"message":"An unexpected database error occured while fetching the user"}, 500
        if user_data:
            return (200, {"id":user_data.id,
                    "jobCategory":user_data.jobCategory})
        return {"message":"Wrong address man"}, 401


index_bp.add_url_rule("/", view_func=Index.as_view("index"))