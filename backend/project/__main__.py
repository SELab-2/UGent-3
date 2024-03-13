"""Main entry point for the application."""

from dotenv import load_dotenv
from project import create_app_with_db
from project.db_in import url

if __name__ == "__main__":
    load_dotenv()
    app = create_app_with_db(url)
    app.run(debug=True, host='0.0.0.0')
