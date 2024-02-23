import pytest
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import ForeignKeyViolation
from project.models.courses import Courses
from project.models.users import Users
from project.models.course_relations import CourseAdmins, CourseStudents


class TestCoursesModel:
    """Test class for the database models"""

    def test_foreignkey_courses_teacher(self, db_session, course: Courses):
        """Tests the foreign key relation between courses and the teacher uid"""
        with pytest.raises(
            IntegrityError
        ):
            db_session.add(course)
            db_session.commit()

    def test_correct_course(self, db_session, course: Courses, course_teacher: Users):
        """Tests wether added course and a teacher are correctly connected"""
        db_session.add(course_teacher)
        db_session.commit()

        db_session.add(course)
        db_session.commit()
        assert (
            db_session.query(Courses).filter_by(name=course.name).first().teacher
            == course_teacher.uid
        )

    def test_foreignkey_coursestudents_uid(
        self, db_session, course, course_teacher, course_students_relation
    ):
        """Test the foreign key of the CourseStudent related to the student uid"""
        db_session.add(course_teacher)
        db_session.commit()

        db_session.add(course)
        db_session.commit()
        for s in course_students_relation:
            s.course_id = course.course_id

        with pytest.raises(
            IntegrityError
        ):
            db_session.add_all(course_students_relation)
            db_session.commit()

    def test_correct_courserelations(
        self,
        db_session,
        course,
        course_teacher,
        course_students,
        course_students_relation,
        assistent,
        course_admin,
    ):
        """Tests if we get the expected results for correct usage of CourseStudents and CourseAdmins"""
        db_session.add(course_teacher)
        db_session.commit()

        db_session.add(course)
        db_session.commit()

        db_session.add_all(course_students)
        db_session.commit()

        for s in course_students_relation:
            s.course_id = course.course_id
        db_session.add_all(course_students_relation)
        db_session.commit()

        student_check = [
            s.uid
            for s in db_session.query(CourseStudents)
            .filter_by(course_id=course.course_id)
            .all()
        ]
        student_uids = [s.uid for s in course_students]
        assert student_check == student_uids

        db_session.add(assistent)
        db_session.commit()
        course_admin.course_id = course.course_id
        db_session.add(course_admin)
        db_session.commit()

        assert (
            db_session.query(CourseAdmins)
            .filter_by(course_id=course.course_id)
            .first()
            .uid
            == assistent.uid
        )