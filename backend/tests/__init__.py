"""
This module is used to create a SQLAlchemy URL object for a PostgreSQL database.

It uses environment variables to get the necessary database configuration details:
- 'POSTGRES_DB': The name of the database.
- 'POSTGRES_USER': The username to connect to the database.
- 'POSTGRES_PASSWORD': The password to connect to the database.
- 'POSTGRES_HOST': The host where the database is located.

"""
import os
from sqlalchemy.engine.url import URL
from dotenv import load_dotenv
load_dotenv()

DATABSE_NAME = os.getenv('POSTGRES_DB')
DATABASE_USER = os.getenv('POSTGRES_USER')
DATABASE_PASSWORD = os.getenv('POSTGRES_PASSWORD')
DATABASE_HOST = os.getenv('POSTGRES_HOST')
db_url = URL.create(
    drivername="postgresql",
    username=DATABASE_USER,
    host=DATABASE_HOST,
    database=DATABSE_NAME,
    password=DATABASE_PASSWORD
)
