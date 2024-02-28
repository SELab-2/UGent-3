"""Main entry point for the application."""
from os import getenv
from sqlalchemy import URL
from project import create_app_with_db
from dotenv import load_dotenv


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
