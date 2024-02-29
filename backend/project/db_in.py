"""fix for circular import statements"""

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
