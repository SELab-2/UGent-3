""" This file will change the JWT return messages to custom messages
    and make it so the access tokens implicitly refresh
"""
from datetime import timedelta, timezone, datetime

from flask_jwt_extended import get_jwt, get_jwt_identity,\
      create_access_token, set_access_cookies
from .utils.models.user_utils import get_user
from .models.user import Role

def auth_init(jwt, app):
    """
    This function will overwrite the default return messages from
    the flask-jwt-extended package with custom messages
    and make it so the access tokens implicitly refresh
    """
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            {"message":"Your access token cookie has expired, please log in again"},
            401)

    @jwt.invalid_token_loader
    def invalid_token_callback(jwt_header):
        return (
            {"message":("The server cannot recognize this access token cookie, "
                        "please log in again if you think this is an error")},
            401)

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            {"message":("This access token cookie has been revoked, "
             "possibly from logging out. Log in again to receive a new access token")},
            401)

    @jwt.unauthorized_loader
    def unauthorized_callback(jwt_header):
        return {"message":"You need an access token to get this data, please log in"}, 401

    @app.after_request
    def refresh_expiring_jwts(response):
        try:
            exp_timestamp = get_jwt()["exp"]
            now = datetime.now(timezone.utc)
            target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
            if target_timestamp > exp_timestamp:
                uid = get_jwt_identity()
                user = get_user(uid)
                access_token = create_access_token(
                    identity=uid,
                    additional_claims=
                        {"is_admin":user.role==Role.ADMIN,
                        "is_teacher":user.role==Role.TEACHER}
                    )
                set_access_cookies(response, access_token)
            return response
        except (RuntimeError, KeyError):
            # Case where there is not a valid JWT. Just return the original response
            return response
