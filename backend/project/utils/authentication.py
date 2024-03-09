"""
This module contains the functions to authenticate API calls.
"""
from os import getenv

from dotenv import load_dotenv

import requests

from project import db

from project.models.users import User
from sqlalchemy.exc import SQLAlchemyError

load_dotenv()
API_URL = getenv("API_HOST")
AUTHENTICATION_URL = "https://graph.microsoft.com/v1.0/me"


# TODO add type hinting
def add_user_if_not_in_database(user_info):
    
    try:
        user = db.session.get(User, uid)
    except SQLAlchemyError:
        # every exception should result in a rollback
        db.session.rollback()
        return {"message": "An error occurred while fetching the user",
                    "url": f"{API_URL}/users"}, 500

    if user:
        return {"message": "User queried","data":user,
                    "url": f"{API_URL}/users/{user.uid}"}, 200
    
    # toevoegen
    try:
        new_user = User(uid=uid, is_teacher=is_teacher, is_admin=is_admin)
        db.session.add(new_user)
        db.session.commit()
    except SQLAlchemyError:
            # every exception should result in a rollback
            db.session.rollback()
            return {"message": "An error occurred while creating the user",
                    "url": f"{API_URL}/users"}, 500
    return {"message": "User created successfully!",
                "data": user, "url": f"{API_URL}/users/{user.uid}"}, 201


def get_user_info(authorization: str):
    auth_header = {"Authorization": authorization}
    user_info = requests.get(AUTHENTICATION_URL, headers=auth_header).json()
    
    return 0