"""Main entry point for the application."""
from sys import path

path.append(".")

if __name__ == "__main__":
    from project import create_app
    app = create_app()
    app.run(debug=True)
