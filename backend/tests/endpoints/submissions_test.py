"""Test the submissions API endpoint"""

from os import getenv
from flask.testing import FlaskClient
from sqlalchemy.orm import Session
from project.models.submissions import Submissions as m_submissions

API_HOST = getenv("API_HOST")

class TestSubmissionsEndpoint:
    """Class to test the submissions API endpoint"""

    ### GET SUBMISSIONS ###
    def test_get_submissions_wrong_user(self, client: FlaskClient, session: Session):
        """Test getting submissions for a non-existing user"""
        response = client.get("/submissions?uid=unknown")
        data = response.json
        assert response.status_code == 400
        assert data["url"] == f"{API_HOST}/submissions"
        assert data["message"] == "Invalid user (uid=unknown)"
        assert data["data"] == {}

    def test_get_submissions_wrong_project(self, client: FlaskClient, session: Session):
        """Test getting submissions for a non-existing project"""
        response = client.get("/submissions?project_id=-1")
        data = response.json
        assert response.status_code == 400
        assert data["url"] == f"{API_HOST}/submissions"
        assert data["message"] == "Invalid project (project_id=-1)"
        assert data["data"] == {}

    def test_get_submissions_wrong_project_type(self, client: FlaskClient, session: Session):
        """Test getting submissions for a non-existing project of the wrong type"""
        response = client.get("/submissions?project_id=zero")
        data = response.json
        assert response.status_code == 400
        assert data["url"] == f"{API_HOST}/submissions"
        assert data["message"] == "Invalid project (project_id=zero)"
        assert data["data"] == {}

    def test_get_submissions_all(self, client: FlaskClient, session: Session):
        """Test getting the submissions"""
        response = client.get("/submissions")
        data = response.json
        assert response.status_code == 200
        assert data["url"] == f"{API_HOST}/submissions"
        assert data["message"] == "Successfully fetched the submissions"
        assert data["data"]["submissions"] == [
            f"{API_HOST}/submissions/1",
            f"{API_HOST}/submissions/2",
            f"{API_HOST}/submissions/3"
        ]

    def test_get_submissions_user(self, client: FlaskClient, session: Session):
        """Test getting the submissions given a specific user"""
        response = client.get("/submissions?uid=student01")
        data = response.json
        assert response.status_code == 200
        assert data["url"] == f"{API_HOST}/submissions"
        assert data["message"] == "Successfully fetched the submissions"
        assert data["data"]["submissions"] == [
            f"{API_HOST}/submissions/1"
        ]

    def test_get_submissions_project(self, client: FlaskClient, session: Session):
        """Test getting the submissions given a specific project"""
        response = client.get("/submissions?project_id=1")
        data = response.json
        assert response.status_code == 200
        assert data["url"] == f"{API_HOST}/submissions"
        assert data["message"] == "Successfully fetched the submissions"
        assert data["data"]["submissions"] == [
            f"{API_HOST}/submissions/1",
            f"{API_HOST}/submissions/2"
        ]

    def test_get_submissions_user_project(self, client: FlaskClient, session: Session):
        """Test getting the submissions given a specific user and project"""
        response = client.get("/submissions?uid=student01&project_id=1")
        data = response.json
        assert response.status_code == 200
        assert data["url"] == f"{API_HOST}/submissions"
        assert data["message"] == "Successfully fetched the submissions"
        assert data["data"]["submissions"] == [
            f"{API_HOST}/submissions/1"
        ]

    ### POST SUBMISSIONS ###
    def test_post_submissions_no_user(self, client: FlaskClient, session: Session):
        """Test posting a submission without specifying a user"""
        response = client.post("/submissions", data={
            "project_id": 1
        })
        data = response.json
        assert response.status_code == 400
        assert data["url"] == f"{API_HOST}/submissions"
        assert data["message"] == "The uid data field is required"
        assert data["data"] == {}

    def test_post_submissions_wrong_user(self, client: FlaskClient, session: Session):
        """Test posting a submission for a non-existing user"""
        response = client.post("/submissions", data={
            "uid": "unknown",
            "project_id": 1
        })
        data = response.json
        assert response.status_code == 400
        assert data["url"] == f"{API_HOST}/submissions"
        assert data["message"] == "Invalid user (uid=unknown)"
        assert data["data"] == {}

    def test_post_submissions_no_project(self, client: FlaskClient, session: Session):
        """Test posting a submission without specifying a project"""
        response = client.post("/submissions", data={
            "uid": "student01"
        })
        data = response.json
        assert response.status_code == 400
        assert data["url"] == f"{API_HOST}/submissions"
        assert data["message"] == "The project_id data field is required"
        assert data["data"] == {}

    def test_post_submissions_wrong_project(self, client: FlaskClient, session: Session):
        """Test posting a submission for a non-existing project"""
        response = client.post("/submissions", data={
            "uid": "student01",
            "project_id": -1
        })
        data  = response.json
        assert response.status_code == 400
        assert data["url"] == f"{API_HOST}/submissions"
        assert data["message"] == "Invalid project (project_id=-1)"
        assert data["data"] == {}

    def test_post_submissions_wrong_project_type(self, client: FlaskClient, session: Session):
        """Test posting a submission for a non-existing project of the wrong type"""
        response = client.post("/submissions", data={
            "uid": "student01",
            "project_id": "zero"
        })
        data  = response.json
        assert response.status_code == 400
        assert data["url"] == f"{API_HOST}/submissions"
        assert data["message"] == "Invalid project (project_id=zero)"
        assert data["data"] == {}

    def test_post_submissions_wrong_grading(self, client: FlaskClient, session: Session):
        """Test posting a submission with a wrong grading"""
        response = client.post("/submissions", data={
            "uid": "student01",
            "project_id": 1,
            "grading": 80
        })
        data = response.json
        assert response.status_code == 400
        assert data["url"] == f"{API_HOST}/submissions"
        assert data["message"] == "Invalid grading (grading=0-20)"
        assert data["data"] == {}

    def test_post_submissions_wrong_grading_type(self, client: FlaskClient, session: Session):
        """Test posting a submission with a wrong grading type"""
        response = client.post("/submissions", data={
            "uid": "student01",
            "project_id": 1,
            "grading": "zero"
        })
        data = response.json
        assert response.status_code == 400
        assert data["url"] == f"{API_HOST}/submissions"
        assert data["message"] == "Invalid grading (grading=0-20)"
        assert data["data"] == {}

    def test_post_submissions_correct(self, client: FlaskClient, session: Session):
        """Test posting a submission"""
        response = client.post("/submissions", data={
            "uid": "student01",
            "project_id": 1,
            "grading": 16
        })
        data = response.json
        assert response.status_code == 201
        assert data["url"] == f"{API_HOST}/submissions"
        assert data["message"] == "Successfully fetched the submissions"

        submission_id = int(data["data"]["submission"].split("/")[-1])
        submission = session.get(m_submissions, submission_id)
        assert submission.uid == "student01" and submission.project_id == 1 \
            and submission.grading == 16

    ### GET SUBMISSION ###
    def test_get_submission_wrong_id(self, client: FlaskClient, session: Session):
        """Test getting a submission for a non-existing submission id"""
        response = client.get("/submissions/100")
        data = response.json
        assert response.status_code == 404
        assert data["url"] == f"{API_HOST}/submissions/100"
        assert data["message"] == "Submission (submission_id=100) not found"
        assert data["data"] == {}

    def test_get_submission_correct(self, client: FlaskClient, session: Session):
        """Test getting a submission"""
        response = client.get("/submissions/1")
        data = response.json
        assert response.status_code == 200
        assert data["url"] == f"{API_HOST}/submissions/1"
        assert data["message"] == "Successfully fetched the submission"
        assert data["data"]["submission"] == {
            "id": 1,
            "user": f"{API_HOST}/users/student01",
            "project": f"{API_HOST}/projects/1",
            "grading": 16,
            "time": "Thu, 14 Mar 2024 11:00:00 GMT",
            "path": "/submissions/1",
            "status": True
        }

    ### PATCH SUBMISSION ###
    def test_patch_submission_wrong_id(self, client: FlaskClient, session: Session):
        """Test patching a submission for a non-existing submission id"""
        response = client.patch("/submissions/100", data={"grading": 20})
        data = response.json
        assert response.status_code == 404
        assert data["url"] == f"{API_HOST}/submissions/100"
        assert data["message"] == "Submission (submission_id=100) not found"
        assert data["data"] == {}

    def test_patch_submission_wrong_grading(self, client: FlaskClient, session: Session):
        """Test patching a submission with a wrong grading"""
        response = client.patch("/submissions/2", data={"grading": 100})
        data = response.json
        assert response.status_code == 400
        assert data["url"] == f"{API_HOST}/submissions/2"
        assert data["message"] == "Invalid grading (grading=0-20)"
        assert data["data"] == {}

    def test_patch_submission_wrong_grading_type(self, client: FlaskClient, session: Session):
        """Test patching a submission with a wrong grading type"""
        response = client.patch("/submissions/2", data={"grading": "zero"})
        data = response.json
        assert response.status_code == 400
        assert data["url"] == f"{API_HOST}/submissions/2"
        assert data["message"] == "Invalid grading (grading=0-20)"
        assert data["data"] == {}

    def test_patch_submission_correct(self, client: FlaskClient, session: Session):
        """Test patching a submission"""
        response = client.patch("/submissions/2", data={"grading": 20})
        data = response.json
        assert response.status_code == 200
        assert data["url"] == f"{API_HOST}/submissions/2"
        assert data["message"] == "Submission (submission_id=2) patched"
        assert data["data"] == {}

        submission = session.get(m_submissions, 2)
        assert submission.grading == 20

    ### DELETE SUBMISSION ###
    def test_delete_submission_wrong_id(self, client: FlaskClient, session: Session):
        """Test deleting a submission for a non-existing submission id"""
        response = client.delete("submissions/100")
        data = response.json
        assert response.status_code == 404
        assert data["url"] == f"{API_HOST}/submissions/100"
        assert data["message"] == "Submission (submission_id=100) not found"
        assert data["data"] == {}

    def test_delete_submission_correct(self, client: FlaskClient, session: Session):
        """Test deleting a submission"""
        response = client.delete("submissions/1")
        data = response.json
        assert response.status_code == 200
        assert data["url"] == f"{API_HOST}/submissions/1"
        assert data["message"] == "Submission (submission_id=1) deleted"
        assert data["data"] == {}

        submission = session.get(m_submissions, 1)
        assert submission is None
