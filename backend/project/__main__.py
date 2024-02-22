"""Main entry point for the application."""
from sys import path
from os import getenv
from dotenv import load_dotenv
from project import create_app_with_db

path.append(".")

if __name__ == "__main__":
    load_dotenv()
    app = create_app_with_db(getenv("DB_HOST"))
    app.run(debug=True)
