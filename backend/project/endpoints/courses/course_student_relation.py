"""
This file contains the class CourseToAddStudents which is a
resource for the /courses/course_id/students link.
This class will allow admins of a course to assign and remove students from courses,
and everyone should be able to list all students assigned to a course.
"""

from os import getenv
from urllib.parse import urljoin

from dotenv import load_dotenv

from flask import request
from flask_restful import Resource

from project.db_in import db
from project.models.course_relation import CourseStudent
from project.endpoints.courses.courses_utils import (
    execute_query_abort_if_db_error,
    add_abort_if_error,
    commit_abort_if_error,
    delete_abort_if_error,
    get_course_abort_if_not_found,
    abort_if_none_uid_student_uids_or_non_existant_course_id,
    json_message,
)

from project.utils.query_agent import query_selected_from_model
from project.utils.authentication import login_required, authorize_teacher_or_course_admin

load_dotenv()
API_URL = getenv("API_HOST")
RESPONSE_URL = urljoin(API_URL + "/", "courses")

class CourseToAddStudents(Resource):
    """
    Class that will respond to the /courses/course_id/students link
    teachers should be able to assign and remove students from courses,
    and everyone should be able to list all students assigned to a course
    """

    @login_required
    def get(self, course_id):
        """
        Get function at /courses/course_id/students
        to get all the users assigned to a course
        everyone can get this data so no need to have uid query in the link
        """
        abort_url = f"{API_URL}/courses/{course_id}/students"
        get_course_abort_if_not_found(course_id)

        return query_selected_from_model(
            CourseStudent,
            abort_url,
            select_values=["uid"],
            url_mapper={"uid": urljoin(f"{API_URL}/", "users")},
            filters={"course_id": course_id}
        )

    @authorize_teacher_or_course_admin
    def post(self, course_id):
        """
        Allows admins of a course to assign new students by posting to:
        /courses/course_id/students with a list of uid in the request body under key "students"
        """
        abort_url = f"{API_URL}/courses/{course_id}/students"
        uid = request.args.get("uid")
        data = request.get_json()
        student_uids = data.get("students")
        abort_if_none_uid_student_uids_or_non_existant_course_id(
            course_id, uid, student_uids
        )

        for uid in student_uids:
            query = CourseStudent.query.filter_by(uid=uid, course_id=course_id)
            student_relation = execute_query_abort_if_db_error(query, abort_url)
            if student_relation:
                db.session.rollback()
                message = (
                    f"Student with uid {uid} is already assigned to the course"
                )
                return json_message(message), 400
            add_abort_if_error(CourseStudent(uid=uid, course_id=course_id), abort_url)
        commit_abort_if_error(abort_url)
        response = json_message("Users were succesfully added to the course")
        response["url"] = abort_url
        data = {"students": [f"{API_URL}/users/{uid}" for uid in student_uids]}
        response["data"] = data
        return response, 201

    @authorize_teacher_or_course_admin
    def delete(self, course_id):
        """
        This function allows admins of a course to remove students by sending a delete request to
        /courses/course_id/students with inside the request body
        a field "students" = [list of uids to unassign]
        """
        abort_url = f"{API_URL}/courses/{str(course_id)}/students"
        uid = request.args.get("uid")
        data = request.get_json()
        student_uids = data.get("students")
        abort_if_none_uid_student_uids_or_non_existant_course_id(
            course_id, uid, student_uids
        )

        for uid in student_uids:
            query = CourseStudent.query.filter_by(uid=uid, course_id=course_id)
            student_relation = execute_query_abort_if_db_error(query, abort_url)
            if student_relation:
                delete_abort_if_error(student_relation, abort_url)
        commit_abort_if_error(abort_url)

        response = json_message("Users were succesfully removed from the course")
        response["url"] = f"{API_URL}/courses/{str(course_id)}/students"
        return response
