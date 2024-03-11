"""Project model tests"""

from datetime import datetime
from pytest import raises
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from project.models.course import Course
from project.models.project import Project

class TestProjectModel:
    """Class to test the Project model"""

    def test_create_project(self, session: Session):
        """Test if a project can be created"""
        course = session.query(Course).filter_by(name="AD3").first()
        project = Project(
            title="Pigeonhole",
            descriptions="A new project",
            assignment_file="assignment.pdf",
            deadline=datetime(2024,12,31,23,59,59),
            course_id=course.course_id,
            visible_for_students=True,
            archieved=False,
            test_path="/test",
            script_name="script",
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
        project.descriptions = "Implement 3 trees of your choosing"
        session.commit()
        assert project.title == "Trees"
        assert project.descriptions == "Implement 3 trees of your choosing"

    def test_delete_project(self, session: Session):
        """Test if a project can be deleted"""

    def test_primary_key(self, session: Session):
        """Test the primary key"""
        project_ad3 = session.query(Project).filter_by(title="B+ Trees").first()
        project_raf = session.query(Project).filter_by(title="Predicaten").first()
        with raises(IntegrityError):
            project_raf.project_id = project_ad3.project_id
            session.commit()
        session.rollback()
        with raises(IntegrityError):
            project_raf.project_id = 0
            session.commit()

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

    def test_title_required(self, session: Session):
        """Test if a title is given"""
        project = session.query(Project).filter_by(title="B+ Trees").first()
        with raises(IntegrityError):
            project.title = None
            session.commit()

    def test_description_required(self, session: Session):
        """Test if description is given"""
        project = session.query(Project).filter_by(title="B+ Trees").first()
        with raises(IntegrityError):
            project.descriptions = None
            session.commit()

    def test_course_id_required(self, session: Session):
        """Test if course_id is given"""
        project = session.query(Project).filter_by(title="B+ Trees").first()
        with raises(IntegrityError):
            project.course_id = None
            session.commit()

    def test_visible_for_students_required(self, session: Session):
        """Test if visible_for_students is given"""
        project = session.query(Project).filter_by(title="B+ Trees").first()
        with raises(IntegrityError):
            project.visible_for_students = None
            session.commit()

    def test_archived_required(self, session: Session):
        """Test if archived is given"""
        project = session.query(Project).filter_by(title="B+ Trees").first()
        with raises(IntegrityError):
            project.archieved = None
            session.commit()
