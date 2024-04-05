"""Tests the courses API endpoint"""

from typing import Tuple, List
from pytest import mark
from flask.testing import FlaskClient
from tests.endpoints.endpoint import TestEndpoint, authentication_tests, authorization_tests
from project.models.user import User
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

    def test_post_courses_incorrect_field(self, client: FlaskClient, teacher: User):
        """Test posting a course where a field that doesn't occur in the model is given"""
        response = client.post("/courses", headers = {"Authorization": "teacher"},
            json = {
                "name": "test",
                "ufora_id": "test",
                "teacher": teacher.uid
            }
        )
        assert response.status_code == 400

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
    def test_get_course_wrong_course_id(self, client: FlaskClient):
        """Test getting a non existing course by giving a wrong course_id"""
        response = client.get("/courses/0", headers = {"Authorization": "student"})
        assert response.status_code == 404

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
    def test_patch_course_wrong_course_id(self, client: FlaskClient):
        """Test patching a course that does not exist"""
        response = client.patch("/courses/0", headers = {"Authorization": "teacher"})
        assert response.status_code == 404

    def test_patch_course_wrong_name_type(self, client: FlaskClient, course: Course):
        """Test patching a course given a wrong type for the course name"""
        response = client.patch(
            f"/courses/{course.course_id}",
            headers = {"Authorization": "teacher"},
            json = {"name": 0}
        )
        assert response.status_code == 400

    def test_patch_course_ufora_id_type(self, client: FlaskClient, course: Course):
        """Test patching a course given a wrong type for the ufora_id"""
        response = client.patch(
            f"/courses/{course.course_id}",
            headers = {"Authorization": "teacher"},
            json = {"ufora_id": 0}
        )
        assert response.status_code == 400

    def test_patch_course_wrong_teacher_type(self, client: FlaskClient, course: Course):
        """Test patching a course given a wrong type for the teacher"""
        response = client.patch(
            f"/courses/{course.course_id}",
            headers = {"Authorization": "teacher"},
            json = {"teacher": 0}
        )
        assert response.status_code == 400

    def test_patch_course_wrong_teacher(self, client: FlaskClient, course: Course):
        """Test patching a course given a teacher that does not exist"""
        response = client.patch(
            f"/courses/{course.course_id}",
            headers = {"Authorization": "teacher"},
            json = {"teacher": "no_teacher"}
        )
        assert response.status_code == 400

    def test_patch_course_incorrect_field(self, client: FlaskClient, course: Course):
        """Test patching a course with a field that doesn't occur in the course model"""
        response = client.patch(
            f"/courses/{course.course_id}",
            headers = {"Authorization": "teacher"},
            json = {"incorrect": 0}
        )
        assert response.status_code == 400

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
    def test_delete_course_wrong_course_id(self, client: FlaskClient):
        """Test deleting a course that does not exist"""
        response = client.delete(
            "/courses/0",
            headers = {"Authorization": "teacher"}
        )
        assert response.status_code == 404

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
    def test_get_students_wrong_course_id(self, client: FlaskClient):
        """Test getting the students of a non existing course by giving a wrong course_id"""
        response = client.get("/courses/0/students", headers = {"Authorization": "student"})
        assert response.status_code == 404

    def test_get_students_correct(self, client: FlaskClient, api_host: str, course: Course):
        """Test getting the students fo a course"""
        response = client.get(
            f"/courses/{course.course_id}/students",
            headers = {"Authorization": "student"}
        )
        assert response.status_code == 200
        assert response.json["data"][0]["uid"] == f"{api_host}/users/student"



    ### POST COURSE STUDENTS ###
    def test_post_students_wrong_course_id(self, client: FlaskClient):
        """Test adding students to a non existing course"""
        response = client.post("/courses/0/students", headers = {"Authorization": "teacher"})
        assert response.status_code == 404

    def test_post_students_wrong_students_type(
            self, client: FlaskClient, course: Course, student_other: User
        ):
        """Test adding a student without putting it in a list"""
        response = client.post(
            f"/courses/{course.course_id}/students",
            headers = {"Authorization": "teacher"},
            json = {
                "students": student_other.uid
            }
        )
        assert response.status_code == 400

    def test_post_students_wrong_students(self, client: FlaskClient, course: Course):
        """Test adding students with invalid uid values in the list"""
        response = client.post(
            f"/courses/{course.course_id}/students",
            headers = {"Authorization": "teacher"},
            json = {
                "students": [None, "no_user"]
            }
        )
        assert response.status_code == 400

    def test_post_students_incorrect_field(
            self, client: FlaskClient, course: Course, student_other: User
        ):
        """Test adding students but give unnecessary fields to the data"""
        response = client.post(
            f"/courses/{course.course_id}/students",
            headers = {"Authorization": "teacher"},
            json = {
                "incorrect": [student_other.uid]
            }
        )
        assert response.status_code == 400

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
    def test_delete_students_wrong_course_id(self, client: FlaskClient):
        """Test deleting students from a non existing course"""
        response = client.delete("/courses/0/students", headers = {"Authorization": "teacher"})
        assert response.status_code == 404

    def test_delete_students_wrong_students_type(
            self, client: FlaskClient, course: Course, student_other: User
        ):
        """Test deleting a student without putting it in a list"""
        response = client.delete(
            f"/courses/{course.course_id}/students",
            headers = {"Authorization": "teacher"},
            json = {
                "students": student_other.uid
            }
        )
        assert response.status_code == 400

    def test_delete_students_wrong_students(self, client: FlaskClient, course: Course):
        """Test deleting students with invalid uid values in the list"""
        response = client.delete(
            f"/courses/{course.course_id}/students",
            headers = {"Authorization": "teacher"},
            json = {
                "students": [None, "no_user"]
            }
        )
        assert response.status_code == 400

    def test_delete_students_incorrect_field(
            self, client: FlaskClient, course: Course, student: User
        ):
        """Test deleting students with an extra field that should not be there"""
        response = client.delete(
            f"/courses/{course.course_id}/students",
            headers = {"Authorization": "teacher"},
            json = {
                "incorrect": [student.uid]
            }
        )
        assert response.status_code == 400

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
    def test_get_admins_wrong_course_id(self, client: FlaskClient):
        """Test getting the admins of a non existing course"""
        response = client.get("/courses/0/admins", headers = {"Authorization": "teacher"})
        assert response.status_code == 404

    def test_get_admins_correct(self, client: FlaskClient, api_host: str, course: Course):
        """Test getting the admins of a course"""
        response = client.get(
            f"/courses/{course.course_id}/admins",
            headers = {"Authorization": "teacher"}
        )
        assert response.status_code == 200
        assert response.json["data"][0]["uid"] == f"{api_host}/users/admin"



    ### POST COURSE ADMINS ###
    def test_post_admins_wrong_course_id(self, client: FlaskClient):
        """Test adding admins to a non existing course"""
        response = client.post("/courses/0/admins", headers = {"Authorization": "teacher"})
        assert response.status_code == 404

    def test_post_admins_wrong_admin_uid_type(self, client: FlaskClient, course: Course):
        """Test adding an admin where the uid has a wrong typing"""
        response = client.post(
            f"/courses/{course.course_id}/admins",
            headers = {"Authorization": "teacher"},
            json = {
                "admin_uid": None
            }
        )
        assert response.status_code == 400

    def test_post_admins_wrong_user(self, client: FlaskClient, course: Course, student: User):
        """Test adding a student as an admin"""
        response = client.post(
            f"/courses/{course.course_id}/admins",
            headers = {"Authorization": "teacher"},
            json = {
                "admin_uid": student.uid
            }
        )
        assert response.status_code == 400

    def test_post_admins_incorrect_field(self, client: FlaskClient, course: Course, admin: User):
        """Test adding an admin but the data has an incorrect field"""
        response = client.post(
            f"/courses/{course.course_id}/admins",
            headers = {"Authorization": "teacher"},
            json = {
                "incorrect": admin.uid
            }
        )
        assert response.status_code == 400

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
    def test_delete_admins_wrong_course_id(self, client: FlaskClient):
        """Test deleting an admin from a non existing course"""
        response = client.delete("/courses/0/admins", headers = {"Authorization": "teacher"})
        assert response.status_code == 404

    def test_delete_admins_wrong_admin_uid_type(self, client: FlaskClient, course: Course):
        """Test deleting an admin where the uid has the wrong typing"""
        response = client.delete(
            f"/courses/{course.course_id}/admins",
            headers = {"Authorization": "teacher"},
            json = {
                "admin_uid": None
            }
        )
        assert response.status_code == 400

    def test_delete_admins_wrong_user(self, client: FlaskClient, course: Course, student: User):
        """Test deleting an user that is not an admin for this course"""
        response = client.delete(
            f"/courses/{course.course_id}/admins",
            headers = {"Authorization": "teacher"},
            json = {
                "admin_uid": student.uid
            }
        )
        assert response.status_code == 400

    def test_delete_admins_incorrect_field(self, client: FlaskClient, course: Course, admin: User):
        """Test deleting an admin but the data has an incorrect field"""
        response = client.delete(
            f"/courses/{course.course_id}/admins",
            headers = {"Authorization": "teacher"},
            json = {
                "incorrect": admin.uid
            }
        )
        assert response.status_code == 400

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
