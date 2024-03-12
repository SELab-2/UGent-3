"""Course relation tests"""

from pytest import raises, mark
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from project.models.course import Course
from project.models.course_relation import CourseAdmin

class TestCourseRelationModel:
    """Class to test the CourseRelation model"""

    def test_create_course_relation(self, session: Session):
        """Test if a course relation can be created"""
        course_id = session.query(Course).filter_by(name="AD3").first().course_id
        relation = CourseAdmin(course_id=course_id, uid="laermans")
        session.add(relation)
        session.commit()
        assert session.get(CourseAdmin, (course_id, "laermans")) is not None

    def test_query_course_relation(self, session: Session):
        """Test if a course relation can be queried"""
        assert session.query(CourseAdmin).count() == 2
        relation = session.query(CourseAdmin).filter_by(uid="brinkmann").first()
        assert relation is not None
        assert relation.course_id == \
            session.query(Course).filter_by(name="AD3").first().course_id

    def test_update_course_relation(self, session: Session):
        """Test if a course relation can be updated"""
        relation = session.query(CourseAdmin).filter_by(uid="brinkmann").first()
        course = session.query(Course).filter_by(name="RAF").first()
        relation.course_id = course.course_id
        session.commit()
        assert session.get(CourseAdmin, (course.course_id, "brinkmann")) is not None

    def test_delete_course_relation(self, session: Session):
        """Test if a course relation can be deleted"""
        relation = session.query(CourseAdmin).filter_by(uid="brinkmann").first()
        session.delete(relation)
        session.commit()
        assert session.get(CourseAdmin, (relation.course_id,relation.uid)) is None
        assert session.query(CourseAdmin).count() == 1

    def test_primary_key(self, session: Session):
        """Test the primary key"""
        relations = session.query(CourseAdmin).all()
        with raises(IntegrityError):
            relations[0].course_id = relations[1].course_id
            relations[0].uid = relations[1].uid
            session.commit()
        session.rollback()

    def test_foreign_key_course_id(self, session: Session):
        """Test the foreign key course_id"""
        course = session.query(Course).filter_by(name="RAF").first()
        relation = session.query(CourseAdmin).filter_by(uid="brinkmann").first()
        relation.course_id = course.course_id
        session.commit()
        assert session.get(CourseAdmin, (course.course_id, "brinkmann")) is not None
        with raises(IntegrityError):
            relation.course_id = 0
            session.commit()
        session.rollback()

    def test_foreign_key_uid(self, session: Session):
        """Test the foreign key uid"""
        relation = session.query(CourseAdmin).filter_by(uid="brinkmann").first()
        relation.uid = "laermans"
        session.commit()
        assert session.get(CourseAdmin, (relation.course_id,relation.uid)) is not None
        with raises(IntegrityError):
            relation.uid = "unknown"
            session.commit()
        session.rollback()

    @mark.parametrize("property_name", ["course_id", "uid"])
    def test_property_not_nullable(self, session: Session, property_name: str):
        """Test if the property is not nullable"""
        relation = session.query(CourseAdmin).first()
        with raises(IntegrityError):
            setattr(relation, property_name, None)
            session.commit()
        session.rollback()
