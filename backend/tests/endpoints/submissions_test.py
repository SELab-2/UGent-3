"""Test the submissions API endpoint"""

class TestSubmissionsEndpoint:
    """Class to test the submissions API endpoint"""

    ### GET SUBMISSIONS ###
    def test_get_submissions_wrong_user(self, client, session):
        """Test getting submissions for a non-existing user"""

    def test_get_submissions_wrong_project(self, client, session):
        """Test getting submissions for a non-existing project"""

    def test_get_submissions_database_issue(self, client, session):
        """Test getting the submissions with a faulty database"""

    def test_get_submissions_correct(self, client, session):
        """Test getting the submissions"""

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
