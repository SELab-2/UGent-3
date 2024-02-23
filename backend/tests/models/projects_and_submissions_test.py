from project.models.courses import Courses
from project.models.course_relations import CourseAdmins, CourseStudents
from project.models.projects import Projects
from project.models.submissions import Submissions
from project.models.users import Users

class TestProjectsAndSubmissionsModel:
    def test_projects_and_submissions(self,db_session):
        """
        In this test function i will test the
        creation of projects and submissions
        """

        teacher = Users(uid="teacher", is_teacher=True)
        db_session.add(teacher)
        db_session.commit()
        course = Courses(name="course", teacher=teacher.uid)
        db_session.add(course)
        db_session.commit()
        deadline = datetime(2024, 2, 25, 12, 0, 0)  # February 25, 2024, 12:00 PM
        project = Projects(
            title="Project",
            descriptions="Test project",
            deadline=deadline,
            course_id=course.course_id,
            visible_for_students=True,
            archieved=False,
        )

        db_session.add(project)
        db_session.commit()

        check_project = (
            db_session.query(Projects).filter_by(title=project.title).first()
        )
        self.assertEqual(check_project.deadline, project.deadline)

        submittor = Users(uid="student")
        self.assertFalse(submittor.is_teacher)
        db_session.add(submittor)
        db_session.commit()

        submission = Submissions(
            uid=submittor.uid,
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
        self.assertEqual(submission_check.uid, submittor.uid)
        with self.assertRaises(
            IntegrityError,
            msg="Submissions model should throw an error on grades out of [0,20] range",
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
        self.assertEqual(submission_check.grading, 15)
        self.assertEqual(
            submission.grading, 15
        )  # Interesting! all the model objects are connected