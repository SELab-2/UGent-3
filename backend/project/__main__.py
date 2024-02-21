"""Main entry point for the application."""
from sys import path
from project import create_app

path.append(".")

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
