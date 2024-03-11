"""Submission model tests"""

from datetime import datetime
from pytest import raises
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from project.models.project import Project
from project.models.submission import Submission

class TestSubmissionModel:
    """Class to test the Submission model"""

    def test_create_submission(self, session: Session):
        """Test if a submission can be created"""
        project = session.query(Project).filter_by(title="B+ Trees").first()
        submission = Submission(
            uid="student01",
            project_id=project.project_id,
            submission_time=datetime(2023,3,15,13,0,0),
            submission_path="/submissions",
            submission_status=True
        )
        session.add(submission)
        session.commit()
        assert submission.submission_id is not None
        assert session.query(Submission).count() == 4

    def test_query_submission(self, session: Session):
        """Test if a submission can be queried"""
        assert session.query(Submission).count() == 3
        submission = session.query(Submission).filter_by(uid="student01").first()
        assert submission is not None

    def test_update_submission(self, session: Session):
        """Test if a submission can be updated"""
        submission = session.query(Submission).filter_by(uid="student01").first()
        submission.uid = "student02"
        submission.grading = 20
        session.commit()
        assert submission.uid == "student02"
        assert submission.grading == 20

    def test_delete_submission(self, session: Session):
        """Test if a submission can be deleted"""
        submission = session.query(Submission).filter_by(uid="student01").first()
        session.delete(submission)
        session.commit()
        assert session.get(Submission, submission.submission_id) is None
        assert session.query(Submission).count() == 2

    def test_primary_key(self, session: Session):
        """Test the primary key"""
        submission = session.query(Submission).filter_by(uid="student01").first()
        submission_02 = session.query(Submission).filter_by(uid="student02").first()
        with raises(IntegrityError):
            submission.submission_id = submission_02.submission_id
            session.commit()
        session.rollback()
        with raises(IntegrityError):
            submission.submission_id = 0
            session.commit()

    def test_foreign_key_uid(self, session: Session):
        """Test the foreign key uid"""
        submission = session.query(Submission).filter_by(uid="student01").first()
        submission.uid = "student02"
        session.commit()
        assert submission.uid == "student02"
        with raises(IntegrityError):
            submission.uid = "unknown"
            session.commit()

    def test_foreign_key_project_id(self, session: Session):
        """Test the foreign key project_id"""
        submission = session.query(Submission).filter_by(uid="student01").first()
        project = session.query(Project).filter_by(title="Predicaten").first()
        submission.project_id = project.project_id
        session.commit()
        assert submission.project_id == project.project_id
        with raises(IntegrityError):
            submission.project_id = 0
            session.commit()

    def test_uid_required(self, session: Session):
        """Test if uid is given"""
        submission = session.query(Submission).filter_by(uid="student01").first()
        with raises(IntegrityError):
            submission.uid = None
            session.commit()

    def test_project_id_required(self, session: Session):
        """Test if project_id is given"""
        submission = session.query(Submission).filter_by(uid="student01").first()
        with raises(IntegrityError):
            submission.project_id = None
            session.commit()

    def test_submission_time_required(self, session: Session):
        """Test if submission_time is given"""
        submission = session.query(Submission).filter_by(uid="student01").first()
        with raises(IntegrityError):
            submission.submission_time = None
            session.commit()

    def test_submission_path_required(self, session: Session):
        """Test if submission_path is given"""
        submission = session.query(Submission).filter_by(uid="student01").first()
        with raises(IntegrityError):
            submission.submission_path = None
            session.commit()

    def test_submission_status_required(self, session: Session):
        """Test if submission_status is given"""
        submission = session.query(Submission).filter_by(uid="student01").first()
        with raises(IntegrityError):
            submission.submission_status = None
            session.commit()

    def test_grading_constraint(self, session: Session):
        """Test if the grading is between 0 and 20"""
        submission = session.query(Submission).filter_by(uid="student01").first()
        with raises(IntegrityError):
            submission.grading = 80
            session.commit()
