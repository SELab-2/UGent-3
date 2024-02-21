"""Main entry point for the application."""
from sys import path
from os import getenv
from project import init_db
from dotenv import load_dotenv

path.append(".")

if __name__ == "__main__":
    load_dotenv(dotenv_path='environment.env')
    app = init_db(getenv("DB_HOST"))
    app.run(debug=True)
