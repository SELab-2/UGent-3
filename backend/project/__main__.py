"""Main entry point for the application."""
# TODO: remove is for dev purposes
from sys import path
from os import getenv
from dotenv import load_dotenv
from project import create_app_with_db


from sqlalchemy import URL

path.append(".")

path.append(".")

if __name__ == "__main__":
    load_dotenv()

    url = URL.create(
        drivername="postgresql",
        username=getenv("POSTGRES_USER"),
        password=getenv("POSTGRES_PASSWORD"),
        host=getenv("POSTGRES_HOST"),
        database=getenv("POSTGRES_DB")
    )
    app = create_app_with_db(url)
    app.run(debug=True)
