""" Flask API base file
This file is the base of the Flask API. It contains the basic structure of the API.    
"""

from os import getenv
from dotenv import load_dotenv
from sqlalchemy import URL
from flask import Flask
from .database import db
from .endpoints.index.index import index_bp
from .endpoints.submissions import submissions_bp

def create_app():
    """
    Create a Flask application instance.
    Returns:
        Flask -- A Flask application instance
    """

    app = Flask(__name__)
    app.register_blueprint(index_bp)
    app.register_blueprint(submissions_bp)

    return app

def create_app_with_db(db_uri: str = None):
    """
    Initialize the database with the given uri 
    and connect it to the app made with create_app.
    Parameters:
    db_uri (str): The URI of the database to initialize.
    Returns:
        Flask -- A Flask application instance
    """

    #$ flask --app project:create_app_with_db run
    if db_uri is None:
        load_dotenv()
        db_uri = URL.create(
            drivername=getenv("DB_DRIVER"),
            username=getenv("DB_USER"),
            password=getenv("DB_PASSWORD"),
            host=getenv("DB_HOST"),
            port=int(getenv("DB_PORT")),
            database=getenv("DB_NAME")
        )

    app = create_app()
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    db.init_app(app)
    return app
