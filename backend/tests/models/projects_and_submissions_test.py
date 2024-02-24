"""This module tests the Projects and Submissions model"""
from datetime import datetime
import pytest
from sqlalchemy.exc import IntegrityError
from project.models.projects import Projects
from project.models.submissions import Submissions

class TestProjectsAndSubmissionsModel: # pylint: disable=too-few-public-methods
    """Test class for the database models of projects and submissions"""
    def test_deadline(self,db_session, # pylint: disable=too-many-arguments ; all arguments are needed for the test
                      course,
                      course_teacher,
                      valid_project,
                      valid_user):
        """Tests if the deadline is correctly set
        and if the submission is correctly connected to the project"""
        db_session.add(course_teacher)
        db_session.commit()
        db_session.add(course)
        db_session.commit()
        valid_project.course_id = course.course_id
        db_session.add(valid_project)
        db_session.commit()
        check_project = (
            db_session.query(Projects).filter_by(title=valid_project.title).first()
        )
        assert check_project.deadline == valid_project.deadline

        db_session.add(valid_user)
        db_session.commit()
        submission = Submissions(
            uid=valid_user.uid,
            project_id=check_project.project_id,
            submission_time=datetime.now(),
            submission_path="/test/submission/",
            submission_status=False,
        )
        db_session.add(submission)
        db_session.commit()

        submission_check = (
            db_session.query(Submissions)
            .filter_by(project_id=check_project.project_id)
            .first()
        )
        assert submission_check.uid == valid_user.uid

        with pytest.raises(
            IntegrityError
        ):
            submission_check.grading = 100
            db_session.commit()
        db_session.rollback()
        submission_check.grading = 15
        db_session.commit()
        submission_check = (
            db_session.query(Submissions)
            .filter_by(project_id=check_project.project_id)
            .first()
        )
        assert submission_check.grading == 15
        assert submission.grading == 15
        # Interesting! all the model objects are connected
