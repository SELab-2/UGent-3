"""Test the submissions API endpoint"""

from os import getenv
from flask.testing import FlaskClient
from sqlalchemy.orm import Session
from project.models.submissions import Submissions as m_submissions

class TestSubmissionsEndpoint:
    """Class to test the submissions API endpoint"""

    ### GET SUBMISSIONS ###
    def test_get_submissions_wrong_user(self, client: FlaskClient, session: Session):
        """Test getting submissions for a non-existing user"""
        response = client.get("/submissions?uid=unknown")
        data = response.json
        assert response.status_code == 400
        assert data["message"] == "Invalid user (uid=unknown)"

    def test_get_submissions_wrong_project(self, client: FlaskClient, session: Session):
        """Test getting submissions for a non-existing project"""
        response = client.get("/submissions?project_id=-1")
        data = response.json
        assert response.status_code == 400
        assert data["message"] == "Invalid project (project_id=-1)"

    def test_get_submissions_all(self, client: FlaskClient, session: Session):
        """Test getting the submissions"""
        response = client.get("/submissions")
        data = response.json
        assert response.status_code == 200
        assert data["submissions"] == [
            f"{getenv('HOSTNAME')}/submissions/1",
            f"{getenv('HOSTNAME')}/submissions/2",
            f"{getenv('HOSTNAME')}/submissions/3"
        ]

    def test_get_submissions_user(self, client: FlaskClient, session: Session):
        """Test getting the submissions given a specific user"""
        response = client.get("/submissions?uid=student01")
        data = response.json
        assert response.status_code == 200
        assert data["submissions"] == [
            f"{getenv('HOSTNAME')}/submissions/1"
        ]

    def test_get_submissions_project(self, client: FlaskClient, session: Session):
        """Test getting the submissions given a specific project"""
        response = client.get("/submissions?project_id=1")
        data = response.json
        assert response.status_code == 200
        assert data["submissions"] == [
            f"{getenv('HOSTNAME')}/submissions/1",
            f"{getenv('HOSTNAME')}/submissions/2"
        ]

    def test_get_submissions_user_project(self, client: FlaskClient, session: Session):
        """Test getting the submissions given a specific user and project"""
        response = client.get("/submissions?uid=student01&project_id=1")
        data = response.json
        assert response.status_code == 200
        assert data["submissions"] == [
            f"{getenv('HOSTNAME')}/submissions/1"
        ]

    ### POST SUBMISSIONS ###
    def test_post_submissions_no_user(self, client: FlaskClient, session: Session):
        """Test posting a submission without specifying a user"""
        response = client.post("/submissions", data={
            "project_id": 1
        })
        data = response.json
        assert response.status_code == 400
        assert data["message"] == "The uid data field is required"

    def test_post_submissions_wrong_user(self, client: FlaskClient, session: Session):
        """Test posting a submission for a non-existing user"""
        response = client.post("/submissions", data={
            "uid": "unknown",
            "project_id": 1
        })
        data = response.json
        assert response.status_code == 400
        assert data["message"] == "Invalid user (uid=unknown)"

    def test_post_submissions_no_project(self, client: FlaskClient, session: Session):
        """Test posting a submission without specifying a project"""
        response = client.post("/submissions", data={
            "uid": "student01"
        })
        data = response.json
        assert response.status_code == 400
        assert data["message"] == "The project_id data field is required"

    def test_post_submissions_wrong_project(self, client: FlaskClient, session: Session):
        """Test posting a submission for a non-existing project"""
        response = client.post("/submissions", data={
            "uid": "student01",
            "project_id": -1
        })
        data  = response.json
        assert response.status_code == 400
        assert data["message"] == "Invalid project (project_id=-1)"

    def test_post_submissions_wrong_grading(self, client: FlaskClient, session: Session):
        """Test posting a submission with a wrong grading"""
        response = client.post("/submissions", data={
            "uid": "student01",
            "project_id": 1,
            "grading": 80
        })
        data = response.json
        assert response.status_code == 400
        assert data["message"] == "Invalid grading (grading=0-20)"

    def test_post_submissions_wrong_files(self, client: FlaskClient, session: Session):
        """Test posting a submission with no or wrong files"""

    def test_post_submissions_correct(self, client: FlaskClient, session: Session):
        """Test posting a submission"""
        response = client.post("/submissions", data={
            "uid": "student01",
            "project_id": 1,
            "grading": 16
        })
        data = response.json
        assert response.status_code == 201
        assert data["message"] == "Successfully fetched the submissions"

        submission = session.query(m_submissions).filter_by(
            uid="student01", project_id=1, grading=16
        ).first()
        assert submission is not None

    ### GET SUBMISSION ###
    def test_get_submission_wrong_id(self, client: FlaskClient, session: Session):
        """Test getting a submission for a non-existing submission id"""
        response = client.get("/submissions/100")
        data = response.json
        assert response.status_code == 404
        assert data["message"] == "Submission (submission_id=100) not found"

    def test_get_submission_correct(self, client: FlaskClient, session: Session):
        """Test getting a submission"""
        response = client.get("/submissions/1")
        data = response.json
        assert response.status_code == 200
        assert data["submission"] == {
            "submission_id": 1,
            "uid": "student01",
            "project_id": 1,
            "grading": 16,
            "submission_time": "Thu, 14 Mar 2024 11:00:00 GMT",
            "submission_path": "/submissions/1",
            "submission_status": True
        }

    ### PATCH SUBMISSION ###
    def test_patch_submission_wrong_id(self, client: FlaskClient, session: Session):
        """Test patching a submission for a non-existing submission id"""
        response = client.patch("/submissions/100", data={"grading": 20})
        data = response.json
        assert response.status_code == 404
        assert data["message"] == "Submission (submission_id=100) not found"

    def test_patch_submission_wrong_grading(self, client: FlaskClient, session: Session):
        """Test patching a submission with a wrong grading"""
        response = client.patch("/submissions/2", data={"grading": 100})
        data = response.json
        assert response.status_code == 400
        assert data["message"] == "Invalid grading (grading=0-20)"

    def test_patch_submission_correct(self, client: FlaskClient, session: Session):
        """Test patching a submission"""
        response = client.patch("/submissions/2", data={"grading": 20})
        data = response.json
        assert response.status_code == 200
        assert data["message"] == "Successfully patched submission (submission_id=2)"

        submission = session.get(m_submissions, 2)
        assert submission.grading == 20

    ### DELETE SUBMISSION ###
    def test_delete_submission_wrong_id(self, client: FlaskClient, session: Session):
        """Test deleting a submission for a non-existing submission id"""

    def test_delete_submission_database_issue(self, client: FlaskClient, session: Session):
        """Test deleting a submission with a faulty database"""

    def test_delete_submission_correct(self, client: FlaskClient, session: Session):
        """Test deleting a submission"""
