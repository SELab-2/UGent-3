"""Tests the courses API endpoint"""

from typing import Any
from dataclasses import fields
from pytest import mark
from flask.testing import FlaskClient
from tests.utils.auth_login import get_csrf_from_login
from tests.endpoints.endpoint import (
    TestEndpoint,
    authentication_tests,
    authorization_tests,
    data_field_type_tests,
    query_parameter_tests
)
from project.models.user import User
from project.models.course import Course

class TestCourseEndpoint(TestEndpoint):
    """Class to test the courses API endpoint"""

    ### AUTHENTICATION ###
    # Where is login required
    authentication_tests = \
        authentication_tests("/courses", ["get", "post"]) + \
        authentication_tests("/courses/@course_id", ["get", "patch", "delete"]) + \
        authentication_tests("/courses/@course_id/students", ["get", "post", "delete"]) + \
        authentication_tests("/courses/@course_id/admins", ["get", "post", "delete"])

    @mark.parametrize("auth_test", authentication_tests, indirect=True)
    def test_authentication(self, auth_test: tuple[str, Any, str, bool]):
        """Test the authentication"""
        super().authentication(auth_test)



    ### AUTHORIZATION ###
    # Who can access what
    authorization_tests = \
        authorization_tests("/courses", "get",
            ["student", "student_other", "teacher", "teacher_other", "admin", "admin_other"],
            []) + \
        authorization_tests("/courses", "post",
            ["teacher", "teacher_other"],
            ["student", "student_other", "admin", "admin_other"]) + \
        authorization_tests("/courses/@course_id", "patch",
            ["teacher"],
            ["student", "student_other", "teacher_other", "admin", "admin_other"]) + \
        authorization_tests("/courses/@course_id", "delete",
            ["teacher"],
            ["student", "student_other", "teacher_other", "admin", "admin_other"]) + \
        authorization_tests("/courses/@course_id/students", "get",
            ["student", "student_other", "teacher", "teacher_other", "admin", "admin_other"],
            []) + \
        authorization_tests("/courses/@course_id/students", "post",
            ["teacher", "admin"],
            ["student", "student_other", "teacher_other", "admin_other"]) + \
        authorization_tests("/courses/@course_id/students", "delete",
            ["teacher", "admin"],
            ["student", "student_other", "teacher_other", "admin_other"]) + \
        authorization_tests("/courses/@course_id/admins", "get",
            ["teacher", "admin"],
            ["student", "student_other", "teacher_other", "admin_other"]) + \
        authorization_tests("/courses/@course_id/admins", "post",
            ["teacher"],
            ["student", "student_other", "teacher_other", "admin", "admin_other"]) + \
        authorization_tests("/courses/@course_id/admins", "delete",
            ["teacher"],
            ["student", "student_other", "teacher_other", "admin", "admin_other"])

    @mark.parametrize("auth_test", authorization_tests, indirect=True)
    def test_authorization(self, auth_test: tuple[str, Any, str, bool]):
        """Test the authorization"""
        super().authorization(auth_test)



    ### DATA FIELD TYPE ###
    # Test a data field by passing a list of values for which it should return bad request
    data_field_type_tests = \
        data_field_type_tests("/courses", "post", "teacher",
            {"name": "test", "ufora_id": "test"},
            {"name": [None, 0], "ufora_id": [0]}
        ) + \
        data_field_type_tests("/courses/@course_id", "patch", "teacher",
            {},
            {"name": [None, 0], "ufora_id": [0], "teacher": [None, 0, "student"]}
        ) + \
        data_field_type_tests("/courses/@course_id/students", "post", "teacher",
            {"students": ["student_other"]},
            {"students": [None, [None], ["no_user"], ["student"]]}
        ) + \
        data_field_type_tests("/courses/@course_id/students", "delete", "teacher",
            {"students": ["student"]},
            {"students": [None, [None], ["no_user"], ["student_other"]]}
        ) + \
        data_field_type_tests("/courses/@course_id/admins", "post", "teacher",
            {"admin_uid": "admin_other"},
            {"admin_uid": [None, "no_user", "admin"]}
        ) + \
        data_field_type_tests("/courses/@course_id/admins", "delete", "teacher",
            {"admin_uid": ["admin"]},
            {"admin_uid": [None, "no_user", "admin_other"]}
        )

    @mark.parametrize("data_field_type_test", data_field_type_tests, indirect=True)
    def test_data_fields(self, data_field_type_test: tuple[str, Any, str, dict[str, Any]]):
        """Test a data field typing"""
        super().data_field_type(data_field_type_test)



    ### QUERY PARAMETER ###
    # Test a query parameter, should return [] for wrong values
    query_parameter_tests = \
        query_parameter_tests("/courses", "get", "student", [f.name for f in fields(Course)])

    @mark.parametrize("query_parameter_test", query_parameter_tests, indirect=True)
    def test_query_parameters(self, query_parameter_test: tuple[str, Any, str, bool]):
        """Test a query parameter"""
        super().query_parameter(query_parameter_test)



    ### COURSES ###
    def test_get_courses(self, client: FlaskClient, courses: list[Course]):
        """Test getting all courses"""
        csrf = get_csrf_from_login(client, "student")
        response = client.get("/courses", headers = {"X-CSRF-TOKEN":csrf})
        assert response.status_code == 200
        data = [course["name"] for course in response.json["data"]]
        assert all(course.name in data for course in courses)

    def test_get_courses_name(self, client: FlaskClient, course: Course):
        """Test getting courses for a given course name"""
        csrf = get_csrf_from_login(client, "student")
        response = client.get(
            f"/courses?name={course.name}",
            headers = {"X-CSRF-TOKEN":csrf}
        )
        assert response.status_code == 200
        assert response.json["data"][0]["name"] == course.name

    def test_get_courses_ufora_id(self, client: FlaskClient, course: Course):
        """Test getting courses for a given ufora_id"""
        csrf = get_csrf_from_login(client, "student")
        response = client.get(
            f"/courses?ufora_id={course.ufora_id}",
            headers = {"X-CSRF-TOKEN":csrf}
        )
        assert response.status_code == 200
        assert response.json["data"][0]["ufora_id"] == course.ufora_id

    def test_get_courses_teacher(self, client: FlaskClient, course: Course):
        """Test getting courses for a given teacher"""
        csrf = get_csrf_from_login(client, "student")
        response = client.get(
            f"/courses?teacher={course.teacher}",
            headers = {"X-CSRF-TOKEN":csrf}
        )
        assert response.status_code == 200
        assert response.json["data"][0]["teacher"] == course.teacher

    def test_get_courses_name_ufora_id(self, client: FlaskClient, course: Course):
        """Test getting courses for a given course name and ufora_id"""
        csrf = get_csrf_from_login(client, "student")
        response = client.get(
            f"/courses?name={course.name}&ufora_id={course.ufora_id}",
            headers = {"X-CSRF-TOKEN":csrf}
        )
        assert response.status_code == 200
        data = response.json["data"][0]
        assert data["name"] == course.name
        assert data["ufora_id"] == course.ufora_id

    def test_get_courses_name_teacher(self, client: FlaskClient, course: Course):
        """Test getting courses for a given course name and teacher"""
        csrf = get_csrf_from_login(client, "student")
        response = client.get(
            f"/courses?name={course.name}&teacher={course.teacher}",
            headers = {"X-CSRF-TOKEN":csrf}
        )
        assert response.status_code == 200
        data = response.json["data"][0]
        assert data["name"] == course.name
        assert data["teacher"] == course.teacher

    def test_get_courses_ufora_id_teacher(self, client: FlaskClient, course: Course):
        """Test getting courses for a given ufora_id and teacher"""
        csrf = get_csrf_from_login(client, "student")
        response = client.get(
            f"/courses?ufora_id={course.ufora_id}&teacher={course.teacher}",
            headers = {"X-CSRF-TOKEN":csrf}
        )
        assert response.status_code == 200
        data = response.json["data"][0]
        assert data["ufora_id"] == course.ufora_id
        assert data["teacher"] == course.teacher

    def test_get_courses_name_ufora_id_teacher(self, client: FlaskClient, course: Course):
        """Test getting courses for a given name, ufora_id and teacher"""
        csrf = get_csrf_from_login(client, "student")
        response = client.get(
            f"/courses?name={course.name}&ufora_id={course.ufora_id}&teacher={course.teacher}",
            headers = {"X-CSRF-TOKEN":csrf}
        )
        assert response.status_code == 200
        data = response.json["data"][0]
        assert data["name"] == course.name
        assert data["ufora_id"] == course.ufora_id
        assert data["teacher"] == course.teacher

    def test_post_courses(self, client: FlaskClient, teacher: User):
        """Test posting a course"""
        csrf = get_csrf_from_login(client, "teacher")
        response = client.post("/courses", headers = {"X-CSRF-TOKEN":csrf},
            json = {
                "name": "test",
                "ufora_id": "test"
            }
        )
        assert response.status_code == 201
        csrf = get_csrf_from_login(client, "student")
        response = client.get("/courses?name=test", headers = {"X-CSRF-TOKEN":csrf})
        assert response.status_code == 200
        data = response.json["data"][0]
        assert data["ufora_id"] == "test"
        assert data["teacher"] == teacher.uid



    ### COURSE ###
    def test_get_course(self, client: FlaskClient, course: Course):
        """Test getting a course"""
        csrf = get_csrf_from_login(client, "student")
        response = client.get(
            f"/courses/{course.course_id}",
            headers = {"X-CSRF-TOKEN":csrf}
        )
        assert response.status_code == 200
        data = response.json["data"]
        assert data["name"] == course.name
        assert data["ufora_id"] == course.ufora_id
        assert data["teacher"] == course.teacher

    def test_patch_course(self, client: FlaskClient, course: Course):
        """Test patching a course"""
        csrf = get_csrf_from_login(client, "teacher")
        response = client.patch(
            f"/courses/{course.course_id}",
            headers = {"X-CSRF-TOKEN":csrf},
            json = {"name": "test"}
        )
        assert response.status_code == 200
        assert response.json["data"]["name"] == "test"

    def test_delete_course(self, client: FlaskClient, course: Course):
        """Test deleting a course"""
        csrf = get_csrf_from_login(client, "teacher")
        response = client.delete(
            f"/courses/{course.course_id}",
            headers = {"X-CSRF-TOKEN":csrf}
        )
        assert response.status_code == 200
        csrf = get_csrf_from_login(client, "student")
        response = client.get(
            f"/courses/{course.course_id}",
            headers = {"X-CSRF-TOKEN":csrf}
        )
        assert response.status_code == 404



    ### COURSE STUDENTS ###
    def test_get_students(self, client: FlaskClient, api_host: str, course: Course):
        """Test getting the students fo a course"""
        csrf = get_csrf_from_login(client, "student")
        response = client.get(
            f"/courses/{course.course_id}/students",
            headers = {"X-CSRF-TOKEN":csrf}
        )
        assert response.status_code == 200
        assert response.json["data"][0]["uid"] == f"{api_host}/users/student"

    def test_post_students(
            self, client: FlaskClient, api_host: str, course: Course, student_other: User
        ):
        """Test adding students to a course"""
        csrf = get_csrf_from_login(client, "teacher")
        response = client.post(
            f"/courses/{course.course_id}/students",
            headers = {"X-CSRF-TOKEN":csrf},
            json = {
                "students": [student_other.uid]
            }
        )
        assert response.status_code == 201
        assert response.json["data"]["students"][0] == f"{api_host}/users/student_other"

    def test_delete_students(
            self, client: FlaskClient, course: Course, student: User
        ):
        """Test deleting students from a course"""
        csrf = get_csrf_from_login(client, "teacher")
        response = client.delete(
            f"/courses/{course.course_id}/students",
            headers = {"X-CSRF-TOKEN":csrf},
            json = {
                "students": [student.uid]
            }
        )
        assert response.status_code == 200
        csrf = get_csrf_from_login(client, "student")
        response = client.get(
            f"/courses/{course.course_id}/students",
            headers = {"X-CSRF-TOKEN":csrf}
        )
        assert response.status_code == 200
        assert response.json["data"] == []



    ### COURSE ADMINS ###
    def test_get_admins(self, client: FlaskClient, api_host: str, course: Course):
        """Test getting the admins of a course"""
        csrf = get_csrf_from_login(client, "teacher")
        response = client.get(
            f"/courses/{course.course_id}/admins",
            headers = {"X-CSRF-TOKEN":csrf}
        )
        assert response.status_code == 200
        assert response.json["data"][0]["uid"] == f"{api_host}/users/admin"

    def test_post_admins(self, client: FlaskClient, course: Course, admin_other: User):
        """Test adding an admin to a course"""
        csrf = get_csrf_from_login(client, "teacher")
        response = client.post(
            f"/courses/{course.course_id}/admins",
            headers = {"X-CSRF-TOKEN":csrf},
            json = {
                "admin_uid": admin_other.uid
            }
        )
        assert response.status_code == 201
        assert response.json["data"]["uid"] == admin_other.uid

    def test_delete_admins(self, client: FlaskClient, course: Course, admin: User):
        """Test deleting an admin from a course"""
        csrf = get_csrf_from_login(client, "teacher")
        response = client.delete(
            f"/courses/{course.course_id}/admins",
            headers = {"X-CSRF-TOKEN":csrf},
            json = {
                "admin_uid": admin.uid
            }
        )
        assert response.status_code == 204
        response = client.get(
            f"/courses/{course.course_id}/admins",
            headers = {"X-CSRF-TOKEN":csrf}
        )
        assert response.status_code == 200
        assert response.json["data"] == []
