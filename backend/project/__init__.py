""" Flask API base file
This file is the base of the Flask API. It contains the basic structure of the API.    
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    """
    Create a Flask application instance.
    Returns:
        Flask -- A Flask application instance
    """
    from .endpoints.index import index_bp
    from .endpoints.courses import courses_bp

    app = Flask(__name__)
    app.register_blueprint(index_bp)
    app.register_blueprint(courses_bp)

    return app

def create_app_with_db(db_uri:str):
    """
    Initialize the database with the given uri 
    and connect it to the app made with create_app.
    Parameters:
    db_uri (str): The URI of the database to initialize.
    Returns:
        Flask -- A Flask application instance
    """
    from project.models.users import Users
    from project.models.courses import Courses
    from project.models.course_relations import CourseStudents

    app = create_app()
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    db.init_app(app)

    with app.app_context():
        db.create_all()
        for table in reversed(db.metadata.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()

        # Add initial data
        db.session.add(Users(uid="student"))
        db.session.add(Users(uid="teacher", is_teacher=True))
        db.session.commit()
        db.session.add(Courses(name="course", teacher="teacher"))
        db.session.commit()
        course_id = db.session.query(Courses).filter_by(name="course").first().course_id
        db.session.add(CourseStudents(course_id=course_id, uid="student"))
        db.session.commit()

    return app
