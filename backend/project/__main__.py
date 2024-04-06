"""Main entry point for the application."""

from dotenv import load_dotenv
from project import create_app_with_db
from project.db_in import url

load_dotenv()
DEBUG=getenv("DEBUG")

if __name__ == "__main__":
    app = create_app_with_db(url)

    if DEBUG and DEBUG.lower() == "true":
        app.run(debug=True, host='0.0.0.0')
    else:
        from waitress import serve
        serve(app, host='0.0.0.0', port=5000)
