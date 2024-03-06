"""
This module will handle the /courses/<course_id>/admins endpoint
It will allow the teacher of a course to add and remove admins from a course
"""

from os import getenv
from urllib.parse import urljoin
from dotenv import load_dotenv

from flask import jsonify, request
from flask_restful import Resource

from project.models.course_relations import CourseAdmin
from project.models.users import User
from project.endpoints.courses.courses_utils import (
    execute_query_abort_if_db_error,
    add_abort_if_error,
    commit_abort_if_error,
    delete_abort_if_error,
    get_course_abort_if_not_found,
    abort_if_not_teacher_or_none_assistant,
    json_message
)

load_dotenv()
API_URL = getenv("API_HOST")
RESPONSE_URL = urljoin(API_URL + "/", "courses")

class CourseForAdmins(Resource):
    """
    This class will handle post and delete queries to
    the /courses/course_id/admins url, only the teacher of a course can do this
    """

    def get(self, course_id):
        """
        This function will return all the admins of a course
        """
        abort_url = API_URL + "/courses/" + str(course_id) + "/admins"
        get_course_abort_if_not_found(course_id)

        query = CourseAdmin.query.filter_by(course_id=course_id)
        admin_uids = [
            API_URL + "/users/" + a.uid
            for a in execute_query_abort_if_db_error(query, abort_url, query_all=True)
        ]
        response = json_message(
            "Succesfully retrieved all admins of course " + str(course_id)
        )
        response["data"] = admin_uids
        response["url"] = abort_url
        return jsonify(admin_uids)

    def post(self, course_id):
        """
        Api endpoint for adding new admins to a course, can only be done by the teacher
        """
        abort_url = API_URL + "/courses/" + str(course_id) + "/admins"
        teacher = request.args.get("uid")
        data = request.get_json()
        assistant = data.get("admin_uid")
        abort_if_not_teacher_or_none_assistant(course_id, teacher, assistant)

        query = User.query.filter_by(uid=assistant)
        new_admin = execute_query_abort_if_db_error(query, abort_url)
        if not new_admin:
            message = (
                "User to make admin was not found, please request with a valid uid"
            )
            return json_message(message), 404

        admin_relation = CourseAdmin(uid=assistant, course_id=course_id)
        add_abort_if_error(admin_relation, abort_url)
        commit_abort_if_error(abort_url)
        response = json_message(
            f"Admin assistant added to course {course_id}"
        )
        response["url"] = abort_url
        data = {
            "course_id": API_URL + "/courses/" + str(course_id),
            "uid": API_URL + "/users/" + assistant,
        }
        response["data"] = data
        return response, 201

    def delete(self, course_id):
        """
        Api endpoint for removing admins of a course, can only be done by the teacher
        """
        abort_url = API_URL + "/courses/" + str(course_id) + "/admins"
        teacher = request.args.get("uid")
        data = request.get_json()
        assistant = data.get("admin_uid")
        abort_if_not_teacher_or_none_assistant(course_id, teacher, assistant)

        query = CourseAdmin.query.filter_by(uid=assistant, course_id=course_id)
        admin_relation = execute_query_abort_if_db_error(query, abort_url)
        if not admin_relation:
            message = "Course with given admin not found"
            return json_message(message), 404

        delete_abort_if_error(admin_relation, abort_url)
        commit_abort_if_error(abort_url)

        message = (
            f"Admin {assistant}"
            f" was succesfully removed from course {course_id}"
        )
        response = json_message(message)
        response["url"] = abort_url
        return response, 204
