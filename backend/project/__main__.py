"""Main entry point for the application."""
from sys import path
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey


path.append(".")

if __name__ == "__main__":
    from project import create_app
    app = create_app()
    app.run(debug=True)

db = SQLAlchemy(app)

class Teachers(db.Model):
    """Teachers model"""
    __tablename__ = 'Teachers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False,unique=False)
    #TODO: add login column

class Students(db.Model):
    """Student model"""
    __tablename__ = 'Students'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100), nullable=False,unique=False)
    #TODO: add login column

class Courses(db.Model):
    """Course model""" 
    __tablename__ = 'Courses'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100), nullable=False,unique=False)
    #Maybe also add a column for course code from ufora

class Teacher_Course(db.Model):
    """Teacher to course relation model"""
    __tablename__ = 'Teacher_Course'
    teacher = db.Column(db.Integer,ForeignKey('Teachers.id'))
    course = db.Column(db.Integer,ForeignKey('Courses.id'))

class Student_Course(db.Model):
    """Student to course relation model"""
    __tablename__ = 'Student_Course'
    student = db.Column(db.Integer,ForeignKey('Students.id'))
    course = db.Column(db.Integer,ForeignKey('Courses.id'))

class Project_Tasks(db.Model):
    """Project task model"""
    __tablename__ = 'Project_Tasks'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100), nullable=False,unique=False)
    course = db.Column(db.Integer,ForeignKey('Courses.id'))
    path_to_checks = db.Column(db.String(100), nullable=False,unique=False)

class Project_Submissions(db.Model):
    __tablename__ = 'Project_Submissions'
    student = db.Column(db.Integer,ForeignKey('Students.id'))
    project_task = db.Column(db.Integer,ForeignKey('Project_Tasks.id'))
    path_to_files = db.Column(db.String(100), nullable=False,unique=False)




# Create the database tables
with app.app_context():
    db.create_all()
