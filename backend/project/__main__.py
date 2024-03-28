"""Main entry point for the application."""

from sys import path

from dotenv import load_dotenv
from flask_cors import CORS
from project import create_app_with_db
from project.db_in import url

path.append(".")

if __name__ == "__main__":
    load_dotenv()
    app = create_app_with_db(url)
    CORS(app)
    app.run(debug=True)
