"""Tests the courses API endpoint"""

from typing import Tuple, List, Dict
from pytest import mark
from flask.testing import FlaskClient
from tests.endpoints.endpoint import (
    TestEndpoint,
    authentication_tests,
    authorization_tests,
    data_field_type_tests
)
from project.models.user import User
from project.models.course import Course

class TestCourseEndpoint(TestEndpoint):
    """Class to test the courses API endpoint"""

    ### AUTHENTICATION & AUTHORIZATION ###
    # Where is login required
    # (endpoint, methods)
    authentication = authentication_tests([
        ("/courses", ["get", "post"]),
        ("/courses/@course_id", ["get", "patch", "delete"]),
        ("/courses/@course_id/students", ["get", "post", "delete"]),
        ("/courses/@course_id/admins", ["get", "post", "delete"])
    ])

    # Who can access what
    # (endpoint, method, allowed, disallowed)
    authorization = authorization_tests([
        ("/courses", "get", ["student", "teacher", "admin"], []),
        ("/courses", "post", ["teacher"], ["student", "admin"]),

        ("/courses/@course_id", "patch",
            ["teacher"], ["student", "teacher_other", "admin"]),
        ("/courses/@course_id", "delete",
            ["teacher"], ["student", "teacher_other", "admin"]),

        ("/courses/@course_id/students", "get",
            ["student", "teacher", "admin"], []),
        ("/courses/@course_id/students", "post",
            ["teacher", "admin"], ["student", "teacher_other", "admin_other"]),
        ("/courses/@course_id/students", "delete",
            ["teacher", "admin"], ["student", "teacher_other", "admin_other"]),

        ("/courses/@course_id/admins", "get",
            ["teacher", "admin"], ["student", "teacher_other", "admin_other"]),
        ("/courses/@course_id/admins", "post",
            ["teacher"], ["student", "admin"]),
        ("/courses/@course_id/admins", "delete",
            ["teacher"], ["student", "teacher_other", "admin"]),
    ])

    @mark.parametrize("auth_test", authentication, indirect=True)
    def test_authentication(self, auth_test: Tuple[str, any]):
        """Test the authentication"""
        super().authentication(auth_test)

    @mark.parametrize("auth_test", authorization, indirect=True)
    def test_authorization(self, auth_test: Tuple[str, any, str, bool]):
        """Test the authorization"""
        super().authorization(auth_test)



    ### DATA ###
    # Test a data field by passing a list of values for which it should return bad request
    # (endpoint, method, token, minimal_data, {key, [value]})
    data_fields = data_field_type_tests([
        ("/courses", "post", "teacher", {"name": "test", "ufora_id": "test"}, {
            "name": [None, 0],
            "ufora_id": [0],
        }),
        ("/courses/@course_id", "patch", "teacher", {}, {
            "name": [None, 0],
            "ufora_id": [0],
            "teacher": [None, 0, "student"],
        }),
        ("/courses/@course_id/students", "post", "teacher", {"students": ["student_other"]}, {
            "students": [None, [None], ["no_user"], ["student"]]
        }),
        ("/courses/@course_id/students", "delete", "teacher", {"students": ["student"]}, {
            "students": [None, [None], ["no_user"], ["student_other"]]
        }),
        ("/courses/@course_id/admins", "post", "teacher", {"admin_uid": "admin_other"}, {
            "admin_uid": [None, "no_user", "student", "admin"]
        }),
        ("/courses/@course_id/admins", "delete", "teacher", {"admin_uid": ["admin"]}, {
            "admin_uid": [None, "no_user", "admin_other"]
        })
    ])

    @mark.parametrize("data_field_type_test", data_fields, indirect=True)
    def test_data_fields(self, data_field_type_test: Tuple[str, any, str, Dict[str, any]]):
        """Test a data field"""
        super().data_field_type(data_field_type_test)



    ### GET COURSES ###
    def test_get_courses_all(self, client: FlaskClient, courses: List[Course]):
        """Test getting all courses"""
        response = client.get("/courses", headers = {"Authorization": "student"})
        assert response.status_code == 200
        data = [course["name"] for course in response.json["data"]]
        assert all(course.name in data for course in courses)

    def test_get_courses_wrong_argument(self, client: FlaskClient):
        """Test getting courses for a wrong parameter"""
        response = client.get("/courses?parameter=0", headers = {"Authorization": "student"})
        assert response.status_code == 400

    def test_get_courses_wrong_name(self, client: FlaskClient):
        """Test getting courses for a wrong course name"""
        response = client.get("/courses?name=no_name", headers = {"Authorization": "student"})
        assert response.status_code == 200
        assert response.json["data"] == []

    def test_get_courses_name(self, client: FlaskClient, course: Course):
        """Test getting courses for a given course name"""
        response = client.get(
            f"/courses?name={course.name}",
            headers = {"Authorization": "student"}
        )
        assert response.status_code == 200
        assert response.json["data"][0]["name"] == course.name

    def test_get_courses_wrong_ufora_id(self, client: FlaskClient):
        """Test getting courses for a wrong ufora_id"""
        response = client.get(
            "/courses?ufora_id=no_ufora_id",
            headers = {"Authorization": "student"}
        )
        assert response.status_code == 200
        assert response.json["data"] == []

    def test_get_courses_ufora_id(self, client: FlaskClient, course: Course):
        """Test getting courses for a given ufora_id"""
        response = client.get(
            f"/courses?ufora_id={course.ufora_id}",
            headers = {"Authorization": "student"}
        )
        assert response.status_code == 200
        assert response.json["data"][0]["ufora_id"] == course.ufora_id

    def test_get_courses_wrong_teacher(self, client: FlaskClient):
        """Test getting courses for a wrong teacher"""
        response = client.get(
            "/courses?teacher=no_teacher",
            headers = {"Authorization": "student"}
        )
        assert response.status_code == 200
        assert response.json["data"] == []

    def test_get_courses_teacher(self, client: FlaskClient, course: Course):
        """Test getting courses for a given teacher"""
        response = client.get(
            f"/courses?teacher={course.teacher}",
            headers = {"Authorization": "student"}
        )
        assert response.status_code == 200
        assert response.json["data"][0]["teacher"] == course.teacher

    def test_get_courses_name_ufora_id(self, client: FlaskClient, course: Course):
        """Test getting courses for a given course name and ufora_id"""
        response = client.get(
            f"/courses?name={course.name}&ufora_id={course.ufora_id}",
            headers = {"Authorization": "student"}
        )
        assert response.status_code == 200
        data = response.json["data"][0]
        assert data["name"] == course.name
        assert data["ufora_id"] == course.ufora_id

    def test_get_courses_name_teacher(self, client: FlaskClient, course: Course):
        """Test getting courses for a given course name and teacher"""
        response = client.get(
            f"/courses?name={course.name}&teacher={course.teacher}",
            headers = {"Authorization": "student"}
        )
        assert response.status_code == 200
        data = response.json["data"][0]
        assert data["name"] == course.name
        assert data["teacher"] == course.teacher

    def test_get_courses_ufora_id_teacher(self, client: FlaskClient, course: Course):
        """Test getting courses for a given ufora_id and teacher"""
        response = client.get(
            f"/courses?ufora_id={course.ufora_id}&teacher={course.teacher}",
            headers = {"Authorization": "student"}
        )
        assert response.status_code == 200
        data = response.json["data"][0]
        assert data["ufora_id"] == course.ufora_id
        assert data["teacher"] == course.teacher

    def test_get_courses_name_ufora_id_teacher(self, client: FlaskClient, course: Course):
        """Test getting courses for a given name, ufora_id and teacher"""
        response = client.get(
            f"/courses?name={course.name}&ufora_id={course.ufora_id}&teacher={course.teacher}",
            headers = {"Authorization": "student"}
        )
        assert response.status_code == 200
        data = response.json["data"][0]
        assert data["name"] == course.name
        assert data["ufora_id"] == course.ufora_id
        assert data["teacher"] == course.teacher



    ### POST COURSES ###
    def test_post_courses_correct(self, client: FlaskClient, teacher: User):
        """Test posting a course"""
        response = client.post("/courses", headers = {"Authorization": "teacher"},
            json = {
                "name": "test",
                "ufora_id": "test"
            }
        )
        assert response.status_code == 201
        response = client.get("/courses?name=test", headers = {"Authorization": "student"})
        assert response.status_code == 200
        data = response.json["data"][0]
        assert data["ufora_id"] == "test"
        assert data["teacher"] == teacher.uid



    ### GET COURSE ###
    def test_get_course_correct(self, client: FlaskClient, course: Course):
        """Test getting a course"""
        response = client.get(
            f"/courses/{course.course_id}",
            headers = {"Authorization": "student"}
        )
        assert response.status_code == 200
        data = response.json["data"]
        assert data["name"] == course.name
        assert data["ufora_id"] == course.ufora_id
        assert data["teacher"] == course.teacher



    ### PATCH COURSE ###
    def test_patch_course_correct(self, client: FlaskClient, course: Course):
        """Test patching a course"""
        response = client.patch(
            f"/courses/{course.course_id}",
            headers = {"Authorization": "teacher"},
            json = {"name": "test"}
        )
        assert response.status_code == 200
        assert response.json["data"]["name"] == "test"



    ### DELETE COURSE ###
    def test_delete_course_correct(self, client: FlaskClient, course: Course):
        """Test deleting a course"""
        response = client.delete(
            f"/courses/{course.course_id}",
            headers = {"Authorization": "teacher"}
        )
        assert response.status_code == 200
        response = client.get(
            f"/courses/{course.course_id}",
            headers = {"Authorization": "student"}
        )
        assert response.status_code == 404



    ### GET COURSE STUDENTS ###
    def test_get_students_correct(self, client: FlaskClient, api_host: str, course: Course):
        """Test getting the students fo a course"""
        response = client.get(
            f"/courses/{course.course_id}/students",
            headers = {"Authorization": "student"}
        )
        assert response.status_code == 200
        assert response.json["data"][0]["uid"] == f"{api_host}/users/student"



    ### POST COURSE STUDENTS ###
    def test_post_students_correct(
            self, client: FlaskClient, api_host: str, course: Course, student_other: User
        ):
        """Test adding students to a course"""
        response = client.post(
            f"/courses/{course.course_id}/students",
            headers = {"Authorization": "teacher"},
            json = {
                "students": [student_other.uid]
            }
        )
        assert response.status_code == 201
        assert response.json["data"]["students"][0] == f"{api_host}/users/student_other"



    ### DELETE COURSE STUDENTS ###
    def test_delete_students_correct(
            self, client: FlaskClient, course: Course, student: User
        ):
        """Test deleting students from a course"""
        response = client.delete(
            f"/courses/{course.course_id}/students",
            headers = {"Authorization": "teacher"},
            json = {
                "students": [student.uid]
            }
        )
        assert response.status_code == 200
        response = client.get(
            f"/courses/{course.course_id}/students",
            headers = {"Authorization": "student"}
        )
        assert response.status_code == 200
        assert response.json["data"] == []



    ### GET COURSE ADMINS ###
    def test_get_admins_correct(self, client: FlaskClient, api_host: str, course: Course):
        """Test getting the admins of a course"""
        response = client.get(
            f"/courses/{course.course_id}/admins",
            headers = {"Authorization": "teacher"}
        )
        assert response.status_code == 200
        assert response.json["data"][0]["uid"] == f"{api_host}/users/admin"



    ### POST COURSE ADMINS ###
    def test_post_admins_correct(self, client: FlaskClient, course: Course, admin: User):
        """Test adding an admin to a course"""
        response = client.post(
            f"/courses/{course.course_id}/admins",
            headers = {"Authorization": "teacher"},
            json = {
                "admin_uid": admin.uid
            }
        )
        assert response.status_code == 201
        assert response.json["data"]["uid"] == admin.uid



    ### DELETE COURSE ADMINS ###
    def test_delete_admins_correct(self, client: FlaskClient, course: Course, admin: User):
        """Test deleting an admin from a course"""
        response = client.delete(
            f"/courses/{course.course_id}/admins",
            headers = {"Authorization": "teacher"},
            json = {
                "admin_uid": admin.uid
            }
        )
        assert response.status_code == 204
        response = client.get(
            f"/courses/{course.course_id}/admins",
            headers = {"Authorization": "teacher"}
        )
        assert response.status_code == 200
        assert response.json["data"] == []
