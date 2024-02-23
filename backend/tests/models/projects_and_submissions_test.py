from datetime import datetime
import pytest
from sqlalchemy.exc import IntegrityError
from project.models.courses import Courses
from project.models.course_relations import CourseAdmins, CourseStudents
from project.models.projects import Projects
from project.models.submissions import Submissions
from project.models.users import Users

class TestProjectsAndSubmissionsModel:
    def test_deadline(self,db_session,course,course_teacher,valid_project,valid_user):
        db_session.add(course_teacher)
        db_session.commit()
        db_session.add(course)
        db_session.commit()
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
            IntegrityError,
            match="Submissions model should throw an error on grades out of [0,20] range",
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