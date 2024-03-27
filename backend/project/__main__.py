"""Main entry point for the application."""

from os import getenv
from dotenv import load_dotenv
from flask_cors import CORS
from project import create_app_with_db
from project.db_in import url

load_dotenv()
DEBUG=getenv("DEBUG")

if __name__ == "__main__":
    app = create_app_with_db(url)
    CORS(app)
    if DEBUG and DEBUG.lower() == "true":
        app.run(debug=True, host='0.0.0.0')
    else:
        from waitress import serve
        serve(app, host='0.0.0.0', port=5000)
