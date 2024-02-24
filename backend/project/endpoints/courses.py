"""Courses api point"""
from flask import Blueprint, jsonify
from flask_restful import Resource
from project import db
from project.models.course_relations import CourseAdmins,CourseStudents
from project.models.users import Users

courses_bp = Blueprint("courses", __name__)


class CoursesForUser(Resource):
    """Api endpoint for the users/uid/courses link, returns all the courses of a related users"""

    def get(self, uid):
        """
        Get function for /users/uid/courses
        """

        student_courses = CourseStudents.query.filter_by(uid=uid).all()
        admin_courses = CourseAdmins.query.filter_by(uid=uid).all()

        courses_data = {
            "student": [course.course_id for course in student_courses],
            "admin": [course.course_id for course in admin_courses]
        }

        return jsonify(courses_data)


courses_bp.add_url_rule("/users/<string:uid>/courses", view_func=CoursesForUser.as_view("index"))