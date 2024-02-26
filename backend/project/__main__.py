"""Main entry point for the application."""
# TODO: remove is for dev purposes
from sys import path
path.append(".")
from os import getenv # pylint: disable=wrong-import-position
from sqlalchemy import URL # pylint: disable=wrong-import-position
from project import create_app_with_db # pylint: disable=wrong-import-position
from dotenv import load_dotenv # pylint: disable=wrong-import-position



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
