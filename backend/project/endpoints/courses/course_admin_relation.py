"""
This module will handle the /courses/<course_id>/admins endpoint
It will allow the teacher of a course to add and remove admins from a course
"""

from os import getenv
from urllib.parse import urljoin
from dotenv import load_dotenv

from flask import abort, request
from flask_restful import Resource

from utils.authentication import add_user_if_not_in_database, get_user_info

from project.models.course_relations import CourseAdmin
from project.models.users import User
from project.endpoints.courses.courses_utils import (
    execute_query_abort_if_db_error,
    commit_abort_if_error,
    delete_abort_if_error,
    get_course_abort_if_not_found,
    abort_if_not_teacher_or_none_assistant,
    json_message
)
from project.utils.query_agent import query_selected_from_model, insert_into_model

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
        # geen authorization meegegeven
        if not request.headers.get("Authorization"):
            abort(401)
        
        user_info = get_user_info(request.headers.get("Authorization"))
        # probleem met access_token
        if user_info: # mogelijke error code bekijken?
            abort(401)
        
        # hier checken of user bestaat en toevoegen indien nodig
        add_user_if_not_in_database(user_info)

        abort_url = urljoin(f"{RESPONSE_URL}/" , f"{str(course_id)}/", "admins")
        course = get_course_abort_if_not_found(course_id)

        # hier controleren of persoon teacher/admin is van huidige course
        

        return query_selected_from_model(
            CourseAdmin,
            abort_url,
            select_values=["uid"],
            url_mapper={"uid": urljoin(f"{API_URL}/", "users")},
            filters={"course_id": course_id},
        )

    def post(self, course_id):
        """
        Api endpoint for adding new admins to a course, can only be done by the teacher
        """
        abort_url = urljoin(f"{RESPONSE_URL}/" , f"{str(course_id)}/", "admins")
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

        return insert_into_model(
            CourseAdmin,
            {"uid": assistant, "course_id": course_id},
            abort_url,
            "uid"
        )

    def delete(self, course_id):
        """
        Api endpoint for removing admins of a course, can only be done by the teacher
        """
        abort_url = urljoin(f"{RESPONSE_URL}/" , f"{str(course_id)}/", "admins")
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
