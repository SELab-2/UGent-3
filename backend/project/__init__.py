""" Flask API base file
This file is the base of the Flask API. It contains the basic structure of the API.    
"""
from os import getenv
from datetime import timedelta

from dotenv import load_dotenv

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from .db_in import db
from .endpoints.index.index import index_bp
from .endpoints.users import users_bp
from .endpoints.courses.courses_config import courses_bp
from .endpoints.projects.project_endpoint import project_bp
from .endpoints.submissions import submissions_bp
from .endpoints.courses.join_codes.join_codes_config import join_codes_bp
from .endpoints.docs.docs_endpoint import swagger_ui_blueprint
from .endpoints.authentication.auth import auth_bp

load_dotenv()
JWT_SECRET_KEY = getenv("JWT_SECRET_KEY")

def create_app():
    """
    Create a Flask application instance.
    Returns:
        Flask -- A Flask application instance
    """

    app = Flask(__name__)
    app.config["JWT_COOKIE_SECURE"] = True
    app.config["JWT_COOKIE_CSRF_PROTECT"] = True
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=3)
    app.config["JWT_ACCESS_COOKIE_NAME"] = "peristeronas_access_token"
    app.config["JWT_SESSION_COOKIE"] = False
    app.register_blueprint(index_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(courses_bp)
    app.register_blueprint(project_bp)
    app.register_blueprint(submissions_bp)
    app.register_blueprint(join_codes_bp)
    app.register_blueprint(swagger_ui_blueprint)
    app.register_blueprint(auth_bp)

    jwt = JWTManager(app)
    auth_init(jwt)
    return app

def create_app_with_db(db_uri: str):
    """
    Initialize the database with the given uri
    and connect it to the app made with create_app.
    Parameters:
    db_uri (str): The URI of the database to initialize.
    Returns:
        Flask -- A Flask application instance
    """

    app = create_app()
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app.config["UPLOAD_FOLDER"] = "/"
    db.init_app(app)
    CORS(app, supports_credentials=True)
    return app

def auth_init(jwt):
    """
    This function will overwrite the default return messages from
    the flask-jwt-extended package with custom messages
    """
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            {"message":"Your access token cookie has expired, please log in again"},
            401)

    @jwt.invalid_token_loader
    def invalid_token_callback(jwt_header, jwt_payload):
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
