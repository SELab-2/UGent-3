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
        drivername=getenv("DB_DRIVER"),
        username=getenv("DB_USER"),
        password=getenv("DB_PASSWORD"),
        host=getenv("DB_HOST"),
        port=int(getenv("DB_PORT")),
        database=getenv("DB_NAME")
    )
    return uri
