"""Course model tests"""

from pytest import raises, mark
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from project.models.course import Course

class TestCourseModel:
    """Class to test the Course model"""

    def test_create_course(self, session: Session):
        """Test if a course can be created"""
        course = Course(name="SEL2", ufora_id="C003784A_2023", teacher="brinkmann")
        session.add(course)
        session.commit()
        assert session.get(Course, course.course_id) is not None
        assert session.query(Course).count() == 3

    def test_query_course(self, session: Session):
        """Test if a course can be queried"""
        assert session.query(Course).count() == 2
        course = session.query(Course).filter_by(name="AD3").first()
        assert course is not None
        assert course.teacher == "brinkmann"

    def test_update_course(self, session: Session):
        """Test if a course can be updated"""
        course = session.query(Course).filter_by(name="AD3").first()
        course.name = "AD2"
        session.commit()
        assert session.get(Course, course.course_id).name == "AD2"

    def test_delete_course(self, session: Session):
        """Test if a course can be deleted"""

    def test_foreign_key_teacher(self, session: Session):
        """Test the foreign key teacher"""
        course = session.query(Course).filter_by(name="AD3").first()
        course.teacher = "laermans"
        session.commit()
        assert session.get(Course, course.course_id).teacher == "laermans"
        with raises(IntegrityError):
            course.teacher = "unknown"
            session.commit()
        session.rollback()

    @mark.parametrize("property_name", ["name","teacher"])
    def test_property_not_nullable(self, session: Session, property_name: str):
        """Test if the property is not nullable"""
        course = session.query(Course).first()
        with raises(IntegrityError):
            setattr(course, property_name, None)
            session.commit()
        session.rollback()
