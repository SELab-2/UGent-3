"""Here we will test all the courses endpoint related functionality"""

class TestCourseEndpoint:
    """Class for testing the courses endpoint"""

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

    def test_post_with_invalid_fields(self, client, course_invalid_field):
        """
        Test posting a course with invalid fields
        """

        response = client.post("/courses", json=course_invalid_field,
                               headers={"Authorization":"teacher2"})
        assert response.status_code == 201

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
