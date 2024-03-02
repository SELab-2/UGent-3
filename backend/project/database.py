"""Database file"""

from os import getenv
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from sqlalchemy import URL

db = SQLAlchemy()

def get_database_uri() -> str:
    """Get the database URI made from environment variables

    Returns:
        str: Database URI
    """
    load_dotenv()
    uri = URL.create(
        drivername="postgresql",
        username=getenv("POSTGRES_USER"),
        password=getenv("POSTGRES_PASSWORD"),
        host=getenv("POSTGRES_HOST"),
        database=getenv("POSTGRES_NAME")
    )
    return uri
