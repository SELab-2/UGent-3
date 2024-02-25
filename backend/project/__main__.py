"""Main entry point for the application."""

from sys import path
from project import create_app_with_db
from project.database import get_database_uri

path.append(".")

if __name__ == "__main__":
    app = create_app_with_db(get_database_uri())
    app.run(debug=True)
