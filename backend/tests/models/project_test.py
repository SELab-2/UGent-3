"""Project model tests"""

from sqlalchemy.orm import Session
from project.models.project import Project

class TestProjectModel:
    """Class to test the Project model"""

    def test_create_project(self, session: Session):
        """Test if a project can be created"""

    def test_query_project(self, session: Session):
        """Test if a project can be queried"""

    def test_update_project(self, session: Session):
        """Test if a project can be updated"""

    def test_delete_project(self, session: Session):
        """Test if a project can be deleted"""

    def test_title_required(self, session: Session):
        """Test if a title is given"""

    def test_description_required(self, session: Session):
        """Test if description is given"""

    def test_course_id_required(self, session: Session):
        """Test if course_id is given"""

    def test_visible_for_students_required(self, session: Session):
        """Test if visible_for_students is given"""

    def test_archived_required(self, session: Session):
        """Test if archived is given"""

    def test_foreign_key_course_id(self, session: Session):
        """Test the foreign key course_id"""
