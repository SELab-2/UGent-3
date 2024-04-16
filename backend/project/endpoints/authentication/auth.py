"""Auth api endpoint"""
from os import getenv

from dotenv import load_dotenv
import requests
from flask import Blueprint, request, redirect, abort, make_response
from flask_jwt_extended import create_access_token, set_access_cookies
from flask_restful import Resource, Api
from sqlalchemy.exc import SQLAlchemyError

from project import db

from project.models.user import User, Role

auth_bp = Blueprint("auth", __name__)
auth_api = Api(auth_bp)

load_dotenv()
API_URL = getenv("API_HOST")
AUTH_METHOD = getenv("AUTH_METHOD")
AUTHENTICATION_URL = getenv("AUTHENTICATION_URL")
CLIENT_ID = getenv("CLIENT_ID")
CLIENT_SECRET = getenv("CLIENT_SECRET")
CODE_VERIFIER = getenv("CODE_VERIFIER")
TENANT_ID = getenv("TENANT_ID")

def microsoft_authentication():
    code = request.args.get("code")
    if code is None:
        return {"message":"This endpoint is only used for authentication."}, 400
    # got code from microsoft
    data = {"client_id":CLIENT_ID,
            "scope":".default",
            "code":code,
            "redirect_uri":f"{API_URL}/auth",
            "grant_type":"authorization_code",
            "code_verifier":CODE_VERIFIER,
            "client_secret":CLIENT_SECRET}
    try: 
        res = requests.post(f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token", 
                            data=data, 
                            timeout=5)
        token = res.json()["access_token"]
        profile_res = requests.get("https://graph.microsoft.com/v1.0/me", 
                                    headers={"Authorization":f"Bearer {token}"},
                                    timeout=5)
        auth_user_id = profile_res.json()["id"]
    except:
        return {"message":"An error occured while trying to access the Microsoft servers"}, 500
    try:
        user = db.session.get(User, auth_user_id)
    except SQLAlchemyError:
        db.session.rollback()
        abort(make_response(({"message":
                            "An unexpected database error occured while fetching the user"},
                            500)))

    if not user:
        role = Role.STUDENT
        if profile_res.json()["jobTitle"] is not None:
            role = Role.TEACHER

        # add user if not yet in database
        try:
            new_user = User(uid=auth_user_id, role=role)
            db.session.add(new_user)
            db.session.commit()
            user = new_user
        except SQLAlchemyError:
            db.session.rollback()
            abort(make_response(({"message":
                                    """An unexpected database error occured 
                                while creating the user during authentication"""}, 500)))
    resp = redirect("http://localhost:5173", code=303) # hier nog .env variable voor homepage
    additional_claims = {"is_teacher":user.role == Role.TEACHER,
                         "is_admin":user.role == Role.ADMIN}
    set_access_cookies(resp, create_access_token(identity=profile_res.json()["id"], additional_claims=additional_claims))
    return resp


def test_authentication():
    code = request.args.get("code")
    if code is not None:
        profile_res = requests.get(AUTHENTICATION_URL, headers={"Authorization":f"{code}"})
        print(profile_res.json())
        resp = redirect("http://localhost:5173", code=303) # hier nog .env variable voor homepage
        set_access_cookies(resp, create_access_token(identity=profile_res.json()["id"]))
        return resp
    return {"message":"Not yet"}, 500

class Auth(Resource):
    def get(self):
        if AUTH_METHOD == "Microsoft":
            return microsoft_authentication()
        else:
            return test_authentication()

auth_api.add_resource(Auth, "/auth")