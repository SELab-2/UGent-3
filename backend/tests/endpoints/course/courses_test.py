"""Tests the courses API endpoint"""

from typing import Tuple, List
from pytest import mark
from flask.testing import FlaskClient
from tests.endpoints.endpoint import TestEndpoint, authentication_tests, authorization_tests
from project.models.course import Course

class TestCourseEndpoint(TestEndpoint):
    """Class to test the courses API endpoint"""

    ### AUTHENTICATION & AUTHORIZATION ###
    # Where is login required
    # (endpoint, parameters, methods)
    authentication = authentication_tests([
        ("/courses", [], ["get", "post"]),
        ("/courses/@0", ["course_id"], ["get", "patch", "delete"]),
        ("/courses/@0/students", ["course_id"], ["get", "post", "delete"]),
        ("/courses/@0/admins", ["course_id"], ["get", "post", "delete"])
    ])

    # Who can access what
    # (endpoint, parameters, method, allowed, disallowed)
    authorization = authorization_tests([
        ("/courses", [], "get", ["student", "teacher", "admin"], []),
        ("/courses", [], "post", ["teacher"], ["student", "admin"]),

        ("/courses/@0", ["course_id"], "patch",
            ["teacher"], ["student", "teacher_other", "admin"]),
        ("/courses/@0", ["course_id"], "delete",
            ["teacher"], ["student", "teacher_other", "admin"]),

        ("/courses/@0/students", ["course_id"], "get",
            ["student", "teacher", "admin"], []),
        ("/courses/@0/students", ["course_id"], "post",
            ["teacher", "admin"], ["student", "teacher_other", "admin_other"]),
        ("/courses/@0/students", ["course_id"], "delete",
            ["teacher", "admin"], ["student", "teacher_other", "admin_other"]),

        ("/courses/@0/admins", ["course_id"], "get",
            ["teacher", "admin"], ["student", "teacher_other", "admin_other"]),
        ("/courses/@0/admins", ["course_id"], "post",
            ["teacher"], ["student", "teacher_other", "admin"]),
        ("/courses/@0/admins", ["course_id"], "delete",
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





    ### GET COURSES ###
    def test_get_courses_all(self, client: FlaskClient, valid_course_entries: List[Course]):
        """Test getting all courses"""
        response = client.get("/courses", headers = {"Authorization": "student"})
        assert response.status_code == 200
        data = [course["name"] for course in response.json["data"]]
        assert all(course.name in data for course in valid_course_entries)

    def test_get_courses_wrong_parameter(self, client: FlaskClient):
        """Test getting courses for a wrong parameter"""
        response = client.get("/courses?parameter=0", headers = {"Authorization": "student"})
        assert response.status_code == 400

    def test_get_courses_wrong_name(self, client: FlaskClient):
        """Test getting courses for a wrong course name"""
        response = client.get(
            "/courses?name=no_name",
            headers = {"Authorization": "student"}
        )
        assert response.status_code == 200
        assert response.json["data"] == []

    def test_get_courses_name(self, client: FlaskClient, valid_course_entry: Course):
        """Test getting courses for a given course name"""
        response = client.get(
            f"/courses?name={valid_course_entry.name}",
            headers = {"Authorization": "student"}
        )
        assert response.status_code == 200
        assert valid_course_entry.name in [course["name"] for course in response.json["data"]]

    def test_get_courses_wrong_ufora_id(self, client: FlaskClient):
        """Test getting courses for a wrong ufora_id"""
        response = client.get(
            "/courses?ufora_id=no_ufora_id",
            headers = {"Authorization": "student"}
        )
        assert response.status_code == 200
        assert response.json["data"] == []

    def test_get_courses_ufora_id(self, client: FlaskClient, valid_course_entry: Course):
        """Test getting courses for a given ufora_id"""
        response = client.get(
            f"/courses?ufora_id={valid_course_entry.ufora_id}",
            headers = {"Authorization": "student"}
        )
        assert response.status_code == 200
        assert valid_course_entry.ufora_id in \
            [course["ufora_id"] for course in response.json["data"]]

    def test_get_courses_wrong_teacher(self, client: FlaskClient):
        """Test getting courses for a wrong teacher"""
        response = client.get(
            "/courses?teacher=no_teacher",
            headers = {"Authorization": "student"}
        )
        assert response.status_code == 200
        assert response.json["data"] == []

    def test_get_courses_teacher(self, client: FlaskClient, valid_course_entry: Course):
        """Test getting courses for a given teacher"""
        response = client.get(
            f"/courses?teacher={valid_course_entry.teacher}",
            headers = {"Authorization": "student"}
        )
        assert response.status_code == 200
        assert valid_course_entry.teacher in [course["teacher"] for course in response.json["data"]]

    def test_get_courses_name_ufora_id(self, client: FlaskClient, valid_course_entry: Course):
        """Test getting courses for a given course name and ufora_id"""
        response = client.get(
            f"/courses?name={valid_course_entry.name}&ufora_id={valid_course_entry.ufora_id}",
            headers = {"Authorization": "student"}
        )
        assert response.status_code == 200
        assert valid_course_entry.name in [course["name"] for course in response.json["data"]]

    def test_get_courses_name_teacher(self, client: FlaskClient, valid_course_entry: Course):
        """Test getting courses for a given course name and teacher"""
        response = client.get(
            f"/courses?name={valid_course_entry.name}&teacher={valid_course_entry.teacher}",
            headers = {"Authorization": "student"}
        )
        assert response.status_code == 200
        assert valid_course_entry.name in [course["name"] for course in response.json["data"]]

    def test_get_courses_ufora_id_teacher(self, client: FlaskClient, valid_course_entry: Course):
        """Test getting courses for a given ufora_id and teacher"""
        response = client.get(
            f"/courses?ufora_id={valid_course_entry.ufora_id}&teacher={valid_course_entry.teacher}",
            headers = {"Authorization": "student"}
        )
        assert response.status_code == 200
        assert valid_course_entry.name in [course["name"] for course in response.json["data"]]

    def test_get_courses_name_ufora_id_teacher(
            self, client: FlaskClient, valid_course_entry: Course
        ):
        """Test getting courses for a given name, ufora_id and teacher"""
        response = client.get(
            f"/courses?name={valid_course_entry.name}&ufora_id={valid_course_entry.ufora_id}" \
                f"&teacher={valid_course_entry.teacher}",
            headers = {"Authorization": "student"}
        )
        assert response.status_code == 200
        assert valid_course_entry.name in [course["name"] for course in response.json["data"]]





    ### POST COURSES ###
    def test_post_courses_wrong_name_type(self, client: FlaskClient):
        """Test posting a course where the name does not have the correct type"""
        response = client.post("/courses", headers = {"Authorization": "teacher"},
            json = {
                "name": 0,
                "ufora_id": "test"
            }
        )
        assert response.status_code == 400

    def test_post_courses_wrong_ufora_id_type(self, client: FlaskClient):
        """Test posting a course where the ufora_id does not have the correct type"""
        response = client.post("/courses", headers = {"Authorization": "teacher"},
            json = {
                "name": "test",
                "ufora_id": 0
            }
        )
        assert response.status_code == 400

    def test_post_courses_incorrect_field(self, client: FlaskClient, valid_teacher_entry):
        """Test posting a course where a field that doesn't occur in the model is given"""
        response = client.post("/courses", headers = {"Authorization": "teacher"},
            json = {
                "name": "test",
                "ufora_id": "test",
                "teacher": valid_teacher_entry.uid
            }
        )
        assert response.status_code == 400

    def test_post_courses_correct(self, client: FlaskClient, valid_teacher_entry):
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
        data = response.json["data"]
        assert data[0]["ufora_id"] == "test"
        assert data[0]["teacher"] == valid_teacher_entry.uid





    ### GET COURSE ###
    def test_get_course_wrong_course_id(self, client: FlaskClient):
        """Test getting a non existing course by given a wrong course_id"""
        response = client.get("/courses/0", headers = {"Authorization": "student"})
        assert response.status_code == 404

    def test_get_course_correct(self, client: FlaskClient, valid_course_entry):
        """Test getting a course"""
        response = client.get(
            f"/courses/{valid_course_entry.course_id}",
            headers = {"Authorization": "student"}
        )
        assert response.status_code == 200
        data = response.json["data"]
        assert data["name"] == valid_course_entry.name
        assert data["ufora_id"] == valid_course_entry.ufora_id
        assert data["teacher"] == valid_course_entry.teacher





    ### PATCH COURSE ###
    def test_patch_course_wrong_course_id(self, client: FlaskClient, valid_course_entry):
        """Test patching a course that does not exist"""
        response = client.patch(
            "/courses/0",
            headers = {"Authorization": "teacher"}
        )
        assert response.status_code == 404

    def test_patch_course_wrong_name_type(self, client: FlaskClient, valid_course_entry):
        """Test patching a course given a wrong type for the course name"""
        response = client.patch(
            f"/courses/{valid_course_entry.course_id}",
            headers = {"Authorization": "teacher"},
            json = {"name": 0}
        )
        assert response.status_code == 400

    def test_patch_course_ufora_id_type(self, client: FlaskClient, valid_course_entry):
        """Test patching a course given a wrong type for the ufora_id"""
        response = client.patch(
            f"/courses/{valid_course_entry.course_id}",
            headers = {"Authorization": "teacher"},
            json = {"ufora_id": 0}
        )
        assert response.status_code == 400

    def test_patch_course_wrong_teacher_type(self, client: FlaskClient, valid_course_entry):
        """Test patching a course given a wrong type for the teacher"""
        response = client.patch(
            f"/courses/{valid_course_entry.course_id}",
            headers = {"Authorization": "teacher"},
            json = {"teacher": 0}
        )
        assert response.status_code == 400

    def test_patch_course_wrong_teacher(self, client: FlaskClient, valid_course_entry):
        """Test patching a course given a teacher that does not exist"""
        response = client.patch(
            f"/courses/{valid_course_entry.course_id}",
            headers = {"Authorization": "teacher"},
            json = {"teacher": "no_teacher"}
        )
        assert response.status_code == 400

    def test_patch_course_incorrect_field(self, client: FlaskClient, valid_course_entry):
        """Test patching a course with a field that doesn't occur in the course model"""
        response = client.patch(
            f"/courses/{valid_course_entry.course_id}",
            headers = {"Authorization": "teacher"},
            json = {"field": 0}
        )
        assert response.status_code == 400

    def test_patch_course_correct(self, client: FlaskClient, valid_course_entry):
        """Test patching a course"""
        response = client.patch(
            f"/courses/{valid_course_entry.course_id}",
            headers = {"Authorization": "teacher"},
            json = {"name": "test"}
        )
        assert response.status_code == 200
        assert response.json["data"]["name"] == "test"





    ### DELETE COURSE ###
    def test_delete_course_wrong_course_id(self, client: FlaskClient):
        """Test deleting a course that does not exist"""
        response = client.delete(
            "/courses/0",
            headers = {"Authorization": "teacher"}
        )
        assert response.status_code == 404

    def test_delete_course_correct(self, client: FlaskClient, valid_course_entry):
        """Test deleting a course"""
        response = client.delete(
            f"/courses/{valid_course_entry.course_id}",
            headers = {"Authorization": "teacher"}
        )
        assert response.status_code == 200
        response = client.get(
            f"/courses/{valid_course_entry.course_id}",
            headers = {"Authorization": "student"}
        )
        assert response.status_code == 404





    # ### GET COURSE STUDENTS ###
    # ### POST COURSE STUDENTS ###
    # ### DELETE COURSE STUDENTS ###
    # ### GET COURSE ADMINS ###
    # ### POST COURSE ADMINS ###
    # ### DELETE COURSE ADMINS ###
