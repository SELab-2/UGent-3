"""Main entry point for the application."""

from sys import path
from flask_cors import CORS
from project import create_app_with_db
from project.db_in import url

path.append(".")

if __name__ == "__main__":
    app = create_app_with_db(url)
    CORS(app)  # Enable CORS for all origins
    app.run(debug=True)
