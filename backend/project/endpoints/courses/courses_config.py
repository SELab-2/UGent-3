"""
This file is used to configure the courses blueprint and the courses api.
It is used to define the routes for the courses blueprint and the
corresponding api endpoints.

The courses blueprint is used to define the routes for the courses api
endpoints and the courses api is used to define the routes for the courses
api endpoints.
"""

from flask import Blueprint
from flask_restful import Api

from  project.endpoints.courses.courses import CourseForUser
from  project.endpoints.courses.course_details import CourseByCourseId
from  project.endpoints.courses.course_admin_relation import CourseForAdmins
from  project.endpoints.courses.course_student_relation import CourseToAddStudents
from  project.endpoints.courses.join import CourseJoin

courses_bp = Blueprint("courses", __name__)
courses_api = Api(courses_bp)

courses_bp.add_url_rule("/courses",
                        view_func=CourseForUser.as_view('course_endpoint'))

courses_bp.add_url_rule("/courses/<int:course_id>",
                        view_func=CourseByCourseId.as_view('course_by_course_id'))

courses_bp.add_url_rule("/courses/<int:course_id>/admins",
                        view_func=CourseForAdmins.as_view('course_admins'))

courses_bp.add_url_rule("/courses/<int:course_id>/students",
                        view_func=CourseToAddStudents.as_view('course_students'))

courses_bp.add_url_rule("/courses/join", view_func=CourseJoin.as_view('course_join'))
