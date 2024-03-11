"""Submission model tests"""

from sqlalchemy.orm import Session
from project.models.submission import Submission

class TestSubmissionModel:
    """Class to test the Submission model"""

    def test_create_submission(self, session: Session):
        """Test if a submission can be created"""

    def test_query_submission(self, session: Session):
        """Test if a submission can be queried"""

    def test_update_submission(self, session: Session):
        """Test if a submission can be updated"""

    def test_delete_submission(self, session: Session):
        """Test if a submission can be deleted"""

    def test_uid_required(self, session: Session):
        """Test if uid is given"""

    def test_project_id_required(self, session: Session):
        """Test if project_id is given"""

    def test_submission_time_required(self, session: Session):
        """Test if submission_time is given"""

    def test_submission_path_required(self, session: Session):
        """Test if submission_path is given"""

    def test_submission_status_required(self, session: Session):
        """Test if submission_status is given"""

    def test_foreign_key_uid(self, session: Session):
        """Test the foreign key uid"""

    def test_foreign_key_project_id(self, session: Session):
        """Test the foreign key project_id"""

    def test_grading_constraint(self, session: Session):
        """Test if the grading is between 0 and 20"""
