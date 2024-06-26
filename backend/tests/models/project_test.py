"""Project model tests"""

from datetime import datetime
from pytest import raises, mark
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from project.models.course import Course
from project.models.project import Project

class TestProjectModel:
    """Class to test the Project model"""

    def test_create_project(self, session: Session):
        """Test if a project can be created"""
        course = session.query(Course).first()
        project = Project(
            title="Pigeonhole",
            description="A new project",
            deadlines=[("Deadline 1", datetime(2024,12,31,23,59,59))],
            course_id=course.course_id,
            visible_for_students=True,
            archived=False,
            regex_expressions=[r".*"]
        )
        session.add(project)
        session.commit()
        assert project.project_id is not None
        assert session.query(Project).count() == 3

    def test_query_project(self, session: Session):
        """Test if a project can be queried"""
        assert session.query(Project).count() == 2
        project = session.query(Project).filter_by(title="Predicaten").first()
        assert project is not None
        assert project.course_id == session.query(Course).filter_by(name="RAF").first().course_id

    def test_update_project(self, session: Session):
        """Test if a project can be updated"""
        project = session.query(Project).filter_by(title="B+ Trees").first()
        project.title = "Trees"
        project.description = "Implement 3 trees of your choosing"
        session.commit()
        updated_project = session.get(Project, project.project_id)
        assert updated_project.title == "Trees"
        assert updated_project.description == "Implement 3 trees of your choosing"

    def test_delete_project(self, session: Session):
        """Test if a project can be deleted"""
        project = session.query(Project).first()
        session.delete(project)
        session.commit()
        assert session.get(Project, project.project_id) is None
        assert session.query(Project).count() == 1

    def test_foreign_key_course_id(self, session: Session):
        """Test the foreign key course_id"""
        course = session.query(Course).filter_by(name="RAF").first()
        project = session.query(Project).filter_by(title="B+ Trees").first()
        project.course_id = course.course_id
        session.commit()
        assert project.course_id == course.course_id
        with raises(IntegrityError):
            project.course_id = 0
            session.commit()
        session.rollback()

    @mark.parametrize("property_name",
        ["title","description","course_id","visible_for_students","archived"]
    )
    def test_property_not_nullable(self, session: Session, property_name: str):
        """Test if the property is not nullable"""
        project = session.query(Project).first()
        with raises(IntegrityError):
            setattr(project, property_name, None)
            session.commit()
        session.rollback()
