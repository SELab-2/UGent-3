""" Flask API base file
This file is the base of the Flask API. It contains the basic structure of the API.    
"""

from flask import Flask
from flask_cors import CORS
from .db_in import db
from .endpoints.index.index import index_bp
from .endpoints.users import users_bp
from .endpoints.courses.courses_config import courses_bp
from .endpoints.projects.project_endpoint import project_bp
from .endpoints.submissions import submissions_bp
from .endpoints.courses.join_codes.join_codes_config import join_codes_bp
from .endpoints.docs.docs_endpoint import swagger_ui_blueprint

def create_app():
    """
    Create a Flask application instance.
    Returns:
        Flask -- A Flask application instance
    """

    app = Flask(__name__)
    app.register_blueprint(index_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(courses_bp)
    app.register_blueprint(project_bp)
    app.register_blueprint(submissions_bp)
    app.register_blueprint(join_codes_bp)
    app.register_blueprint(swagger_ui_blueprint)

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
    CORS(app)
    return app
