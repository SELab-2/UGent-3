"""Main entry point for the application."""
from sys import path
from os import getenv
from dotenv import load_dotenv
from sqlalchemy import URL
from project import create_app_with_db

path.append(".")

if __name__ == "__main__":
    load_dotenv()

    url = URL.create(
        drivername=getenv("DB_DRIVER"),
        username=getenv("DB_USER"),
        password=getenv("DB_PASSWORD"),
        host=getenv("DB_HOST"),
        port=int(getenv("DB_PORT")),
        database=getenv("DB_NAME")
    )

    app = create_app_with_db(url)
    app.run(debug=True)
