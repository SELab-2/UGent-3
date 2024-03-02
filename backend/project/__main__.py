"""Main entry point for the application."""
from sys import path
from os import getenv
from dotenv import load_dotenv
from sqlalchemy import URL
from project import create_app_with_db
from project.db_in import url
path.append(".")

if __name__ == "__main__":
    
    app = create_app_with_db(url)
    app.run(debug=True)
