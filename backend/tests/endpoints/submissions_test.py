"""Test the submissions API endpoint"""

from os import getenv
from flask.testing import FlaskClient
from sqlalchemy.orm import Session
from project.models.project import Project
from project.models.submission import Submission

API_HOST = getenv("API_HOST")

class TestSubmissionsEndpoint:
    """Class to test the submissions API endpoint"""

    ### GET SUBMISSIONS ###
    def test_get_submissions_wrong_user(self, client: FlaskClient):
        """Test getting submissions for a non-existing user"""
        response = client.get("/submissions?uid=-20", headers={"Authorization":"teacher1"})
        assert response.status_code == 400

    def test_get_submissions_wrong_project(self, client: FlaskClient):
        """Test getting submissions for a non-existing project"""
        response = client.get("/submissions?project_id=-1", headers={"Authorization":"teacher1"})
        assert response.status_code == 404 # can't find course of project in authorization
        assert "message" in response.json

    def test_get_submissions_wrong_project_type(self, client: FlaskClient):
        """Test getting submissions for a non-existing project of the wrong type"""
        response = client.get("/submissions?project_id=zero", headers={"Authorization":"teacher1"})
        assert response.status_code == 400
        assert "message" in response.json

    def test_get_submissions_all(self, client: FlaskClient):
        """Test getting the submissions"""
        response = client.get("/submissions", headers={"Authorization":"teacher2"})
        data = response.json
        assert response.status_code == 200
        assert "message" in data
        assert isinstance(data["data"], list)

    def test_get_submissions_user(self, client: FlaskClient, valid_submission_entry):
        """Test getting the submissions given a specific user"""
        response = client.get(f"/submissions?uid={valid_submission_entry.uid}", headers={"Authorization":"teacher2"})
        data = response.json
        assert response.status_code == 200
        assert "message" in data


    def test_get_submissions_project(self, client: FlaskClient, valid_submission_entry):
        """Test getting the submissions given a specific project"""
        response = client.get(f"/submissions?project_id={valid_submission_entry.project_id}", headers={"Authorization":"teacher2"})
        data = response.json
        assert response.status_code == 200
        assert "message" in data

    def test_get_submissions_user_project(self, client: FlaskClient, valid_submission_entry):
        """Test getting the submissions given a specific user and project"""
        response = client.get(
            f"/submissions? \
                uid={valid_submission_entry.uid}&\
                project_id={valid_submission_entry.project_id}", headers={"Authorization":"teacher2"})
        data = response.json
        assert response.status_code == 200
        assert "message" in data


    ### GET SUBMISSION ###
    def test_get_submission_wrong_id(self, client: FlaskClient, session: Session):
        """Test getting a submission for a non-existing submission id"""
        response = client.get("/submissions/0", headers={"Authorization":"ad3_teacher"})
        data = response.json
        assert response.status_code == 404
        assert data["message"] == "Submission with id: 0 not found"

    def test_get_submission_correct(self, client: FlaskClient, session: Session):
        """Test getting a submission"""
        project = session.query(Project).filter_by(title="B+ Trees").first()
        submission = session.query(Submission).filter_by(
            uid="student01", project_id=project.project_id
        ).first()
        response = client.get(f"/submissions/{submission.submission_id}", headers={"Authorization":"ad3_teacher"})
        data = response.json
        assert response.status_code == 200
        assert data["message"] == "Successfully fetched the submission"
        assert data["data"] == {
            "id": submission.submission_id,
            "user": f"{API_HOST}/users/student01",
            "project": f"{API_HOST}/projects/{project.project_id}",
            "grading": 16,
            "time": "Thu, 14 Mar 2024 12:00:00 GMT",
            "path": "/submissions/1",
            "status": True
        }

    ### PATCH SUBMISSION ###
    def test_patch_submission_wrong_id(self, client: FlaskClient, session: Session):
        """Test patching a submission for a non-existing submission id"""
        response = client.patch("/submissions/0", data={"grading": 20}, headers={"Authorization":"ad3_teacher"})
        data = response.json
        assert response.status_code == 404
        assert data["message"] == "Submission with id: 0 not found"

    def test_patch_submission_wrong_grading(self, client: FlaskClient, session: Session):
        """Test patching a submission with a wrong grading"""
        project = session.query(Project).filter_by(title="B+ Trees").first()
        submission = session.query(Submission).filter_by(
            uid="student02", project_id=project.project_id
        ).first()
        response = client.patch(f"/submissions/{submission.submission_id}", data={"grading": 100}, headers={"Authorization":"ad3_teacher"})
        data = response.json
        assert response.status_code == 400
        assert data["message"] == "Invalid grading (grading=0-20)"

    def test_patch_submission_wrong_grading_type(self, client: FlaskClient, session: Session):
        """Test patching a submission with a wrong grading type"""
        project = session.query(Project).filter_by(title="B+ Trees").first()
        submission = session.query(Submission).filter_by(
            uid="student02", project_id=project.project_id
        ).first()
        response = client.patch(f"/submissions/{submission.submission_id}",data={"grading": "zero"}, headers={"Authorization":"ad3_teacher"})
        data = response.json
        assert response.status_code == 400
        assert data["message"] == "Invalid grading (grading=0-20)"

    def test_patch_submission_correct_teacher(self, client: FlaskClient, session: Session):
        """Test patching a submission"""
        project = session.query(Project).filter_by(title="B+ Trees").first()
        submission = session.query(Submission).filter_by(
            uid="student02", project_id=project.project_id
        ).first()
        response = client.patch(f"/submissions/{submission.submission_id}", data={"grading": 20}, headers={"Authorization":"ad3_teacher"})
        data = response.json
        assert response.status_code == 200
        assert data["message"] == f"Submission (submission_id={submission.submission_id}) patched"
        assert data["url"] == f"{API_HOST}/submissions/{submission.submission_id}"
        assert data["data"] == {
            "id": submission.submission_id,
            "user": f"{API_HOST}/users/student02",
            "project": f"{API_HOST}/projects/{project.project_id}",
            "grading": 20,
            "time": 'Thu, 14 Mar 2024 23:59:59 GMT',
            "path": "/submissions/2",
            "status": False
        }
    
    # TODO test course admin (allowed) and student (not allowed) patch 

    ### DELETE SUBMISSION ###
    def test_delete_submission_wrong_id(self, client: FlaskClient, session: Session):
        """Test deleting a submission for a non-existing submission id"""
        response = client.delete("submissions/0", headers={"Authorization":"student01"})
        data = response.json
        assert response.status_code == 404
        assert data["message"] == "Submission with id: 0 not found"

    def test_delete_submission_correct(self, client: FlaskClient, session: Session):
        """Test deleting a submission"""
        project = session.query(Project).filter_by(title="B+ Trees").first()
        submission = session.query(Submission).filter_by(
            uid="student01", project_id=project.project_id
        ).first()
        response = client.delete(f"submissions/{submission.submission_id}", headers={"Authorization":"student01"})
        data = response.json
        assert response.status_code == 200
        assert data["message"] == f"Submission (submission_id={submission.submission_id}) deleted"
        assert submission.submission_id not in list(map(
            lambda s: s.submission_id, session.query(Submission).all()
        ))
