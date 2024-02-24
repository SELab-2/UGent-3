"""Main entry point for the application."""
from sys import path
from os import getenv
from dotenv import load_dotenv
from sqlalchemy import URL
from project import create_app_with_db

path.append(".")

if __name__ == "__main__":
    load_dotenv()
    DATABSE_NAME = getenv('POSTGRES_DB')
    DATABASE_USER = getenv('POSTGRES_USER')
    DATABASE_PASSWORD = getenv('POSTGRES_PASSWORD')
    DATABASE_HOST = getenv('POSTGRES_HOST')

    url = URL.create(
        drivername="postgresql",
        username=DATABASE_USER,
        host=DATABASE_HOST,
        database=DATABSE_NAME,
        password=DATABASE_PASSWORD
    )
    app = create_app_with_db(url)
    app.run(debug=True)
