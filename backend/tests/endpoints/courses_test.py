"""Here we will test all the courses endpoint related functionality"""

from project.models.course_relations import CourseStudents, CourseAdmins


from project.models.courses import Courses


class TestCoursesEndpoint:
    """Class for testing the courses endpoint"""

    def test_courses(self, courses_init_db, client):
        """
        First i test posting, then getting then deleting of all the courses related data
        """
        course_data = {"name": "Sel2", "teacher": "Bart"}
        invalid_course = {"invalid": "error"}

        # Posting to /courses test
        response = client.post("/courses?uid=Bart", json=course_data)  # valid user

        assert response.status_code == 201  # succes post = 201

        course = courses_init_db.query(Courses).filter_by(name="Sel2").first()
        assert course is not None
        assert course.teacher == "Bart"

        response = client.post(
            "/courses?uid=Jef", json=course_data
        )  # non existant user
        assert response.status_code == 404

        response = client.post(
            "/courses?uid=student_sel2_0", json=course_data
        )  # existant user but no rights
        assert response.status_code == 403

        response = client.post("/courses", json=course_data)  # bad link, no uid passed
        assert response.status_code == 400

        response = client.post(
            "/courses?uid=Bart", json=invalid_course
        )  # invalid course
        assert response.status_code == 400

        # Posting to /courses/course_id/students and admins test
        valid_students = {
            "students": ["student_sel2_0", "student_sel2_1", "student_sel2_2"]
        }
        invalid_students = {"students": ["invalid"]}
        bad_students = {"error": ["student_sel2_0", "student_sel2_1"]}
        sel2_students_link = "/courses/" + str(course.course_id)

        response = client.post(
            sel2_students_link + "/students?uid=student_sel2_0",
            json=valid_students,  # unauthorized user
        )
        assert response.status_code == 403

        response = client.post(
            sel2_students_link + "/students?uid=Bart",
            json=valid_students,  # authorized user
        )

        assert response.status_code == 201  # succes post = 201
        users = [
            s.uid
            for s in CourseStudents.query.filter_by(course_id=course.course_id).all()
        ]
        assert users == valid_students["students"]

        response = client.post(
            sel2_students_link + "/students?uid=Bart",
            json=valid_students,  # already added students
        )
        assert response.status_code == 400
        response = client.post(
            sel2_students_link + "/students?uid=Bart",
            json=invalid_students,  # invalid students
        )
        assert (
            response.status_code == 500
        )  # internal server error because of invalid students uid

        response = client.post(
            sel2_students_link + "/students?uid=Bart",
            json=bad_students,  # bad request
        )
        assert response.status_code == 400

        # Now we have a course, a teacher and some students assigned to the course,
        # lets try to assign an assistent

        sel2_admins_link = "/courses/" + str(course.course_id) + "/admins"

        response = client.post(
            sel2_admins_link + "?uid=student_sel2_0",  # unauthorized user
            json={"admin_uid": "Rien"},
        )
        assert response.status_code == 403
        course_admins = [
            s.uid
            for s in CourseAdmins.query.filter_by(course_id=course.course_id).all()
        ]
        assert course_admins == ["Bart"]

        response = client.post(
            sel2_admins_link + "?uid=Bart",  # authorized user
            json={"admin_uid": "Rin"},  # non existant user
        )
        assert response.status_code == 404

        response = client.post(
            sel2_admins_link + "?uid=Bart",  # authorized user
            json={"admin_uid": "Rien"},  # existing user
        )
        admins = [
            s.uid
            for s in CourseAdmins.query.filter_by(course_id=course.course_id).all()
        ]
        assert admins == ["Bart", "Rien"]

        # Now we have a course with a teacher, students and an assistent lets try to get some info

        sel2_students = [
            s.uid
            for s in CourseStudents.query.filter_by(course_id=course.course_id).all()
        ]

        response = client.get(sel2_students_link + "/students?uid=Bart")
        assert response.status_code == 200
        response_json = response.json  # the students ids are in the json without a key
        assert response_json == sel2_students

        # Now we test the deleting

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
            for s in CourseStudents.query.filter_by(course_id=course.course_id).all()
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
            for s in CourseAdmins.query.filter_by(course_id=course.course_id).all()
        ]
        assert admins == ["Bart", "Rien"]
        response = client.delete(
            sel2_students_link + "/admins?uid=Bart", json={"admin_uid": "Rien"}
        )
        assert response.status_code == 204

        admins = [
            s.uid
            for s in CourseAdmins.query.filter_by(course_id=course.course_id).all()
        ]
        assert admins == ["Bart"]

        course = Courses.query.filter_by(name="Sel2").first()
        assert course.teacher == "Bart"
        response = client.delete(
            "/courses/" + str(course.course_id) + "?uid=" + course.teacher
        )
        assert response.status_code == 200

        course = courses_init_db.query(Courses).filter_by(name="Sel2").first()
        assert course is None
