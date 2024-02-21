"""Main entry point for the application."""
from sys import path
from os import getenv
from dotenv import load_dotenv
from project import init_db

path.append(".")

if __name__ == "__main__":
    load_dotenv(dotenv_path='environment.env')
    app = init_db(getenv("DB_HOST"))
    app.run(debug=True)
