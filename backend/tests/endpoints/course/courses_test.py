"""Tests the courses API endpoint"""

from flask.testing import FlaskClient

AUTH_TOKEN_BAD = ""
AUTH_TOKEN_TEACHER = "teacher2"
AUTH_TOKEN_STUDENT = "student1"

class TestCourseEndpoint:
    """Class to test the courses API endpoint"""

    ### GET COURSES ###
    def test_get_courses_not_authenticated(self, client: FlaskClient):
        """Test getting courses when not authenticated"""
        response = client.get("/courses")
        assert response.status_code == 401

    def test_get_courses_bad_authentication_token(self, client: FlaskClient):
        """Test getting courses for a bad authentication token"""
        response = client.get("/courses", headers = {"Authorization": AUTH_TOKEN_BAD})
        assert response.status_code == 401

    def test_get_courses_all(self, client: FlaskClient, valid_course_entries):
        """Test getting all courses"""
        response = client.get("/courses", headers = {"Authorization": AUTH_TOKEN_TEACHER})
        assert response.status_code == 200
        data = [course["name"] for course in response.json["data"]]
        assert all(course.name in data for course in valid_course_entries)

    def test_get_courses_wrong_parameter(self, client: FlaskClient):
        """Test getting courses for a wrong parameter"""
        response = client.get(
            "/courses?parameter=0",
            headers = {"Authorization": AUTH_TOKEN_TEACHER}
        )
        assert response.status_code == 400

    def test_get_courses_wrong_name(self, client: FlaskClient):
        """Test getting courses for a wrong course name"""
        response = client.get(
            "/courses?name=no_name",
            headers = {"Authorization": AUTH_TOKEN_TEACHER}
        )
        assert response.status_code == 200
        assert response.json["data"] == []

    def test_get_courses_name(self, client: FlaskClient, valid_course_entry):
        """Test getting courses for a given course name"""
        response = client.get(
            f"/courses?name={valid_course_entry.name}",
            headers = {"Authorization": AUTH_TOKEN_TEACHER}
        )
        assert response.status_code == 200
        assert valid_course_entry.name in [course["name"] for course in response.json["data"]]

    def test_get_courses_wrong_ufora_id(self, client: FlaskClient):
        """Test getting courses for a wrong ufora_id"""
        response = client.get(
            "/courses?ufora_id=no_ufora_id",
            headers = {"Authorization": AUTH_TOKEN_TEACHER}
        )
        assert response.status_code == 200
        assert response.json["data"] == []

    def test_get_courses_ufora_id(self, client: FlaskClient, valid_course_entry):
        """Test getting courses for a given ufora_id"""
        response = client.get(
            f"/courses?ufora_id={valid_course_entry.ufora_id}",
            headers = {"Authorization": AUTH_TOKEN_TEACHER}
        )
        assert response.status_code == 200
        assert valid_course_entry.ufora_id in \
            [course["ufora_id"] for course in response.json["data"]]

    def test_get_courses_wrong_teacher(self, client: FlaskClient):
        """Test getting courses for a wrong teacher"""
        response = client.get(
            "/courses?teacher=no_teacher",
            headers = {"Authorization": AUTH_TOKEN_TEACHER}
        )
        assert response.status_code == 200
        assert response.json["data"] == []

    def test_get_courses_teacher(self, client: FlaskClient, valid_course_entry):
        """Test getting courses for a given teacher"""
        response = client.get(
            f"/courses?teacher={valid_course_entry.teacher}",
            headers = {"Authorization": AUTH_TOKEN_TEACHER}
        )
        assert response.status_code == 200
        assert valid_course_entry.teacher in [course["teacher"] for course in response.json["data"]]

    def test_get_courses_name_ufora_id(self, client: FlaskClient, valid_course_entry):
        """Test getting courses for a given course name and ufora_id"""
        response = client.get(
            f"/courses?name={valid_course_entry.name}&ufora_id={valid_course_entry.ufora_id}",
            headers = {"Authorization": AUTH_TOKEN_TEACHER}
        )
        assert response.status_code == 200
        assert valid_course_entry.name in [course["name"] for course in response.json["data"]]

    def test_get_courses_name_teacher(self, client: FlaskClient, valid_course_entry):
        """Test getting courses for a given course name and teacher"""
        response = client.get(
            f"/courses?name={valid_course_entry.name}&teacher={valid_course_entry.teacher}",
            headers = {"Authorization": AUTH_TOKEN_TEACHER}
        )
        assert response.status_code == 200
        assert valid_course_entry.name in [course["name"] for course in response.json["data"]]

    def test_get_courses_ufora_id_teacher(self, client: FlaskClient, valid_course_entry):
        """Test getting courses for a given ufora_id and teacher"""
        response = client.get(
            f"/courses?ufora_id={valid_course_entry.ufora_id}&teacher={valid_course_entry.teacher}",
            headers = {"Authorization": AUTH_TOKEN_TEACHER}
        )
        assert response.status_code == 200
        assert valid_course_entry.name in [course["name"] for course in response.json["data"]]

    def test_get_courses_name_ufora_id_teacher(self, client: FlaskClient, valid_course_entry):
        """Test getting courses for a given name, ufora_id and teacher"""
        response = client.get(
            f"/courses?name={valid_course_entry.name}&ufora_id={valid_course_entry.ufora_id}" \
                f"&teacher={valid_course_entry.teacher}",
            headers = {"Authorization": AUTH_TOKEN_TEACHER}
        )
        assert response.status_code == 200
        assert valid_course_entry.name in [course["name"] for course in response.json["data"]]

    ### POST COURSES ###
    def test_post_courses_not_authenticated(self, client: FlaskClient):
        """Test posting a course when not authenticated"""
        response = client.post("/courses")
        assert response.status_code == 401

    def test_post_courses_bad_authentication_token(self, client: FlaskClient):
        """Test posting a course when given a bad authentication token"""
        response = client.post("/courses", headers = {"Authorization": AUTH_TOKEN_BAD})
        assert response.status_code == 401

    def test_post_courses_no_authorization(self, client: FlaskClient):
        """Test posting a course when not having the correct authorization"""
        response = client.post("/courses", headers = {"Authorization": AUTH_TOKEN_STUDENT})
        assert response.status_code == 403

    def test_post_courses_wrong_name_type(self, client: FlaskClient):
        """Test posting a course where the name does not have the correct type"""
        response = client.post(
            "/courses",
            headers = {"Authorization": AUTH_TOKEN_TEACHER},
            json = {
                "name": 0,
                "ufora_id": "test"
            }
        )
        assert response.status_code == 400

    def test_post_courses_wrong_ufora_id_type(self, client: FlaskClient):
        """Test posting a course where the ufora_id does not have the correct type"""
        response = client.post(
            "/courses",
            headers = {"Authorization": AUTH_TOKEN_TEACHER},
            json = {
                "name": "test",
                "ufora_id": 0
            }
        )
        assert response.status_code == 400

    def test_post_courses_incorrect_field(self, client: FlaskClient, valid_teacher_entry):
        """Test posting a course where a field that doesn't occur in the model is given"""
        response = client.post(
            "/courses",
            headers = {"Authorization": AUTH_TOKEN_TEACHER},
            json = {
                "name": "test",
                "ufora_id": "test",
                "teacher": valid_teacher_entry.uid
            }
        )
        assert response.status_code == 400

    def test_post_courses_correct(self, client: FlaskClient):
        """Test posting a course"""
        response = client.post(
            "/courses",
            headers = {"Authorization": AUTH_TOKEN_TEACHER},
            json = {
                "name": "test",
                "ufora_id": "test"
            }
        )
        assert response.status_code == 201
        response = client.get("/courses?name=test", headers = {"Authorization": AUTH_TOKEN_TEACHER})
        assert response.status_code == 200
        assert response.json["data"][0]["ufora_id"] == "test"

    ### GET COURSE ###
    ### PATCH COURSE ###
    ### DELETE COURSE ###
    ### GET COURSE ADMINS ###
    ### POST COURSE ADMINS ###
    ### DELETE COURSE ADMINS ###
    ### GET COURSE STUDENTS ###
    ### POST COURSE STUDENTS ###
    ### DELETE COURSE STUDENTS ###

    def test_post_courses(self, client, valid_course):
        """
        Test posting a course to the /courses endpoint
        """

        response = client.post("/courses", json=valid_course, headers={"Authorization":"teacher2"})
        assert response.status_code == 201
        data = response.json
        assert data["data"]["name"] == "Sel"
        assert data["data"]["teacher"] == valid_course["teacher"]

        # Is reachable using the API
        get_response = client.get(f"/courses/{data['data']['course_id']}",
                                  headers={"Authorization":"teacher2"})
        assert get_response.status_code == 200


    def test_post_courses_course_id_students_and_admins(
            self, client, valid_course_entry, valid_students_entries):
        """
        Test posting to courses/course_id/students and admins
        """

        # Posting to /courses/course_id/students and admins test
        sel2_students_link = "/courses/" + str(valid_course_entry.course_id)

        valid_students = [s.uid for s in valid_students_entries]

        response = client.post(
            sel2_students_link + f"/students?uid={valid_course_entry.teacher}",
            json={"students": valid_students}, headers={"Authorization":"teacher2"}
        )

        assert response.status_code == 403


    def test_get_courses(self, valid_course_entries, client):
        """
        Test all the getters for the courses endpoint
        """

        response = client.get("/courses", headers={"Authorization":"teacher1"})
        assert response.status_code == 200
        data = response.json
        for course in valid_course_entries:
            assert course.name in [c["name"] for c in data["data"]]

    def test_course_delete(self, valid_course_entry, client):
        """Test all course endpoint related delete functionality"""

        response = client.delete(
            "/courses/" + str(valid_course_entry.course_id), headers={"Authorization":"teacher2"}
        )
        assert response.status_code == 200

        # Is not reachable using the API
        get_response = client.get(f"/courses/{valid_course_entry.course_id}",
                                  headers={"Authorization":"teacher2"})
        assert get_response.status_code == 404

    def test_course_patch(self, valid_course_entry, client):
        """
        Test the patching of a course
        """
        response = client.patch(f"/courses/{valid_course_entry.course_id}", json={
            "name": "TestTest"
        }, headers={"Authorization":"teacher2"})
        data = response.json
        assert response.status_code == 200
        assert data["data"]["name"] == "TestTest"
