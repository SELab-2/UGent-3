"""Test the submissions API endpoint"""

from os import getenv

class TestSubmissionsEndpoint:
    """Class to test the submissions API endpoint"""

    ### GET SUBMISSIONS ###
    def test_get_submissions_wrong_user(self, client):
        """Test getting submissions for a non-existing user"""
        response = client.get("/submissions?uid=unknown")
        data = response.json
        assert response.status_code == 400
        assert data["message"] == "Invalid user (uid=unknown)"

    def test_get_submissions_wrong_project(self, client):
        """Test getting submissions for a non-existing project"""
        response = client.get("/submissions?project_id=-1")
        data = response.json
        assert response.status_code == 400
        assert data["message"] == "Invalid project (project_id=-1)"

    def test_get_submissions_all(self, client):
        """Test getting the submissions"""
        response = client.get("/submissions")
        data = response.json
        assert response.status_code == 200
        assert data["submissions"] == [
            f"{getenv('HOSTNAME')}/submissions/1",
            f"{getenv('HOSTNAME')}/submissions/2"
        ]

    def test_get_submissions_user(self, client):
        """Test getting the submissions given a specific user"""
        response = client.get("/submissions?uid=user4")
        data = response.json
        assert response.status_code == 200
        assert data["submissions"] == [
            f"{getenv('HOSTNAME')}/submissions/1"
        ]

    def test_get_submissions_project(self, client):
        """Test getting the submissions given a specific project"""
        response = client.get("/submissions?project_id=1")
        data = response.json
        assert response.status_code == 200
        assert data["submissions"] == [
            f"{getenv('HOSTNAME')}/submissions/1"
        ]

    def test_get_submissions_user_project(self, client):
        """Test getting the submissions given a specific user and project"""
        response = client.get("/submissions?uid=user4&project_id=1")
        data = response.json
        assert response.status_code == 200
        assert data["submissions"] == [
            f"{getenv('HOSTNAME')}/submissions/1"
        ]

    ### POST SUBMISSIONS ###
    def test_post_submissions_wrong_user(self, client, session):
        """Test posting a submission for a non-existing user"""

    def test_post_submissions_wrong_project(self, client, session):
        """Test posting a submission for a non-existing project"""

    def test_post_submissions_wrong_grading(self, client, session):
        """Test posting a submission with a wrong grading"""

    def test_post_submissions_wrong_form(self, client, session):
        """Test posting a submission with a wrong data form"""

    def test_post_submissions_wrong_files(self, client, session):
        """Test posting a submission with no or wrong files"""

    def test_post_submissions_database_issue(self, client, session):
        """Test posting the submissions with a faulty database"""

    def test_post_submissions_correct(self, client, session):
        """Test posting a submission"""

    ### GET SUBMISSION ###
    def test_get_submission_wrong_id(self, client, session):
        """Test getting a submission for a non-existing submission id"""

    def test_get_submission_database_issue(self, client, session):
        """Test getting a submission with a faulty database"""

    def test_get_submission_correct(self, client, session):
        """Test getting a submission"""

    ### PATCH SUBMISSION ###
    def test_patch_submission_wrong_id(self, client, session):
        """Test patching a submission for a non-existing submission id"""

    def test_patch_submission_wrong_grading(self, client, session):
        """Test patching a submission with a wrong grading"""

    def test_patch_submission_wrong_form(self, client, session):
        """Test patching a submisson with a wrong data form"""

    def test_patch_submission_database_issue(self, client, session):
        """Test patching a submission with a faulty database"""

    def test_patch_submission_correct(self, client, session):
        """Test patching a submission"""

    ### DELETE SUBMISSION ###
    def test_delete_submission_wrong_id(self, client, session):
        """Test deleting a submission for a non-existing submission id"""

    def test_delete_submission_database_issue(self, client, session):
        """Test deleting a submission with a faulty database"""

    def test_delete_submission_correct(self, client, session):
        """Test deleting a submission"""
