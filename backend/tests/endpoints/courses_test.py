"""Here we will test all the courses endpoint related functionality"""

from project.models.course_relation import CourseStudent, CourseAdmin


from project.models.course import Course


class TestCourseEndpoint:
    """Class for testing the courses endpoint"""

    def test_post_courses(self, courses_init_db, client, course_data, invalid_course):
        """
        Test posting a course to the /courses endpoint
        """
        response = client.post("/courses?uid=Bart", json=course_data)  # valid user

        for x in range(3, 10):
            course = {"name": "Sel" + str(x), "teacher": "Bart"}
            response = client.post("/courses?uid=Bart", json=course)  # valid user
            assert response.status_code == 201
        assert response.status_code == 201  # succes post = 201

        course = courses_init_db.query(Course).filter_by(name="Sel2").first()
        assert course is not None
        assert course.teacher == "Bart"

        response = client.post(
            "/courses?uid=Bart", json=invalid_course
        )  # invalid course
        assert response.status_code == 400

    def test_post_courses_course_id_students_and_admins(self, db_with_course, client):
        """
        Test posting to courses/course_id/students and admins
        """
        course = db_with_course.query(Course).filter_by(name="Sel2").first()
        # Posting to /courses/course_id/students and admins test
        valid_students = {
            "students": ["student_sel2_0", "student_sel2_1", "student_sel2_2"]
        }
        bad_students = {"error": ["student_sel2_0", "student_sel2_1"]}
        sel2_students_link = "/courses/" + str(course.course_id)

        response = client.post(
            sel2_students_link + "/students?uid=student_sel2_0",
            json=valid_students,  # unauthorized user
        )
        assert response.status_code == 403

        assert course.teacher == "Bart"
        response = client.post(
            sel2_students_link + "/students?uid=Bart",
            json=valid_students,  # authorized user
        )

        assert response.status_code == 201  # succes post = 201
        users = [
            s.uid
            for s in CourseStudent.query.filter_by(course_id=course.course_id).all()
        ]
        assert users == valid_students["students"]

        response = client.post(
            sel2_students_link + "/students?uid=Bart",
            json=valid_students,  # already added students
        )
        assert response.status_code == 400

        response = client.post(
            sel2_students_link + "/students?uid=Bart",
            json=bad_students,  # bad request
        )
        assert response.status_code == 400

        sel2_admins_link = "/courses/" + str(course.course_id) + "/admins"

        course_admins = [
            s.uid
            for s in CourseAdmin.query.filter_by(course_id=course.course_id).all()
        ]
        assert course_admins == ["Bart"]

        response = client.post(
            sel2_admins_link + "?uid=Bart",  # authorized user
            json={"admin_uid": "Rin"},  # non existent user
        )
        assert response.status_code == 404

        response = client.post(
            sel2_admins_link + "?uid=Bart",  # authorized user
            json={"admin_uid": "Rien"},  # existing user
        )
        admins = [
            s.uid
            for s in CourseAdmin.query.filter_by(course_id=course.course_id).all()
        ]
        assert admins == ["Bart", "Rien"]

    def test_get_courses(self, courses_get_db, client, api_url):
        """
        Test all the getters for the courses endpoint
        """
        course = courses_get_db.query(Course).filter_by(name="Sel2").first()
        sel2_students_link = "/courses/" + str(course.course_id)

        for x in range(3, 10):
            response = client.get(f"/courses?name=Sel{str(x)}")
            assert response.status_code == 200
            link = response.json["url"]
            assert len(link) == len(f"{api_url}/courses")
            response = client.get(link + "?uid=Bart")
            assert response.status_code == 200

        sel2_students = [
            {"uid": f"{api_url}/users/" + s.uid}
            for s in CourseStudent.query.filter_by(course_id=course.course_id).all()
        ]

        response = client.get(sel2_students_link + "/students?uid=Bart")
        assert response.status_code == 200
        response_json = response.json  # the students ids are in the json without a key
        assert response_json["data"] == sel2_students

    def test_course_delete(self, courses_get_db, client):
        """Test all course endpoint related delete functionality"""

        course = courses_get_db.query(Course).filter_by(name="Sel2").first()
        sel2_students_link = "/courses/" + str(course.course_id)
        response = client.delete(
            sel2_students_link + "/students?uid=student_sel2_0",
            json={"students": ["student_sel2_0"]},
        )
        assert response.status_code == 403

        response = client.delete(
            sel2_students_link + "/students?uid=Bart",
            json={"students": ["student_sel2_0"]},
        )
        assert response.status_code == 200

        students = [
            s.uid
            for s in CourseStudent.query.filter_by(course_id=course.course_id).all()
        ]
        assert students == ["student_sel2_1", "student_sel2_2"]

        response = client.delete(
            sel2_students_link + "/students?uid=Bart", json={"error": ["invalid"]}
        )
        assert response.status_code == 400

        response = client.delete(
            sel2_students_link + "/admins?uid=Bart", json={"admin_uid": "error"}
        )
        assert response.status_code == 404

        assert (
            sel2_students_link + "/admins?uid=Bart"
            == "/courses/" + str(course.course_id) + "/admins?uid=Bart"
        )
        response = client.delete(
            sel2_students_link + "/admins?uid=Bart", json={"admin_ud": "Rien"}
        )
        assert response.status_code == 400

        response = client.delete(
            sel2_students_link + "/admins?uid=student_sel2_0",
            json={"admin_uid": "Rien"},
        )
        assert response.status_code == 403

        admins = [
            s.uid
            for s in CourseAdmin.query.filter_by(course_id=course.course_id).all()
        ]
        assert admins == ["Bart", "Rien"]
        response = client.delete(
            sel2_students_link + "/admins?uid=Bart", json={"admin_uid": "Rien"}
        )
        assert response.status_code == 204

        admins = [
            s.uid
            for s in CourseAdmin.query.filter_by(course_id=course.course_id).all()
        ]
        assert admins == ["Bart"]

        course = Course.query.filter_by(name="Sel2").first()
        assert course.teacher == "Bart"

    def test_course_patch(self, client, session):
        """
        Test the patching of a course
        """
        course = session.query(Course).filter_by(name="AD3").first()
        response = client.patch(f"/courses/{course.course_id}?uid=brinkmann", json={
            "name": "AD2"
        })
        data = response.json
        assert response.status_code == 200
        assert data["data"]["name"] == "AD2"
