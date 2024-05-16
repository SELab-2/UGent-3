"""Test the submissions API endpoint"""

from os import getenv
from typing import Any

from pytest import mark
from flask.testing import FlaskClient

from project.models.user import User
from project.models.project import Project
from project.models.submission import Submission
from tests.utils.auth_login import get_csrf_from_login
from tests.endpoints.endpoint import (
    TestEndpoint,
    authentication_tests,
    authorization_tests,
    data_field_type_tests,
    query_parameter_tests
)

API_HOST = getenv("API_HOST")

class TestSubmissionsEndpoint(TestEndpoint):
    """Class to test the submissions API endpoint"""

    ### AUTHENTICATION ###
    # Where is login required
    authentication_tests = \
        authentication_tests("/submissions", ["get", "post"]) + \
        authentication_tests("/submissions/@submission_id", ["get", "patch"]) + \
        authentication_tests("/submissions/@submission_id/download", ["get"])

    @mark.parametrize("auth_test", authentication_tests, indirect=True)
    def test_authentication(self, auth_test: tuple[str, Any, str, bool, dict[str, Any]]):
        """Test the authentication"""
        super().authentication(auth_test)



    ### AUTHORIZATION ###
    # Who can access what
    authorization_tests = \
        authorization_tests("/submissions", "get",
            ["student", "student_other", "teacher", "teacher_other", "admin", "admin_other"],
            []) + \
        authorization_tests("/submissions", "post",
            ["student"],
            ["student_other", "teacher", "teacher_other", "admin", "admin_other"]) + \
        authorization_tests("/submissions/@submission_id", "get",
            ["student", "teacher", "admin"],
            ["student_other", "teacher_other", "admin_other"]) + \
        authorization_tests("submissions/@submission_id", "patch",
            ["teacher", "admin"],
            ["student", "student_other", "teacher_other", "admin_other"]) + \
        authorization_tests("submissions/@submission_id/download", "get",
            ["student", "teacher", "admin"],
            ["student_other", "teacher_other", "admin_other"])

    @mark.parametrize("auth_test", authorization_tests, indirect=True)
    def test_authorization(self, auth_test: tuple[str, Any, str, bool, dict[str, Any]]):
        """Test the authorization"""
        super().authorization(auth_test)



    ### QUERY PARAMETER ###
    # Test a query parameter, should return [] for wrong values
    query_parameter_tests = \
        query_parameter_tests("/submissions", "get", "student", ["uid", "project_id"])

    @mark.parametrize("query_parameter_test", query_parameter_tests, indirect=True)
    def test_query_parameters(self, query_parameter_test: tuple[str, Any, str, bool]):
        """Test a query parameter"""
        super().query_parameter(query_parameter_test)



    ### SUBMISSIONS ###
    def test_get_submissions(self, client: FlaskClient, api_host: str, submission: Submission):
        """Test getting all submissions"""
        response = client.get(
            "/submissions",
            headers = {"X-CSRF-TOKEN":get_csrf_from_login(client, "student")}
        )
        assert response.status_code == 200
        data = response.json["data"][0]
        assert data["submission_id"] == f"{api_host}/submissions/{submission.submission_id}"

    def test_get_submissions_user(
            self, client: FlaskClient, api_host: str, student: User, submission: Submission
        ):
        """Test getting all submissions for a given user"""
        response = client.get(
            f"/submissions?uid={student.uid}",
            headers = {"X-CSRF-TOKEN":get_csrf_from_login(client, "student")}
        )
        assert response.status_code == 200
        data = response.json["data"][0]
        assert data["submission_id"] == f"{api_host}/submissions/{submission.submission_id}"
        assert data["uid"] == f"{api_host}/users/{student.uid}"

    def test_get_submissions_project(
            self, client: FlaskClient, api_host: str, project: Project, submission: Submission
        ):
        """Test getting all submissions for a given project"""
        response = client.get(
            f"/submissions?project_id={project.project_id}",
            headers = {"X-CSRF-TOKEN":get_csrf_from_login(client, "student")}
        )
        assert response.status_code == 200
        data = response.json["data"][0]
        assert data["submission_id"] == f"{api_host}/submissions/{submission.submission_id}"
        assert data["project_id"] == f"{api_host}/projects/{project.project_id}"

    def test_get_submissions_user_project(
            self, client: FlaskClient, api_host: str,
            student: User, project: Project, submission: Submission
        ):
        """Test getting all submissions for a given user and project"""
        response = client.get(
            f"/submissions?uid={student.uid}&project_id={project.project_id}",
            headers = {"X-CSRF-TOKEN":get_csrf_from_login(client, "student")}
        )
        assert response.status_code == 200
        data = response.json["data"][0]
        assert data["submission_id"] == f"{api_host}/submissions/{submission.submission_id}"
        assert data["uid"] == f"{api_host}/users/{student.uid}"
        assert data["project_id"] == f"{api_host}/projects/{project.project_id}"

    def test_post_submissions(self, client: FlaskClient, project: Project, files):
        """Test posting a submission"""
        csrf = get_csrf_from_login(client, "student")
        response = client.post(
            "/submissions",
            headers = {"X-CSRF-TOKEN":csrf},
            data = {"project_id":project.project_id, "files": files}
        )
        assert response.status_code == 201
        submission_id = response.json["data"]["submission_id"].split("/")[-1]
        response = client.get(
            f"/submissions/{submission_id}",
            headers = {"X-CSRF-TOKEN":csrf}
        )
        assert response.status_code == 200

    def test_post_submissions_invalid_project_id(self, client: FlaskClient, files):
        """Test posting a submission when given an invalid project"""
        response = client.post(
            "/submissions",
            headers = {"X-CSRF-TOKEN":get_csrf_from_login(client, "student")},
            data = {"project_id":"zero", "files": files}
        )
        assert response.status_code == 400

    def test_post_submissions_invalid_file(self, client: FlaskClient, file_no_name):
        """Test posting a submission when given a file with no name"""
        response = client.post(
            "/submissions",
            headers = {"X-CSRF-TOKEN":get_csrf_from_login(client, "student")},
            data = {"project_id":"zero", "files": file_no_name}
        )
        assert response.status_code == 400



    ### SUBMISSION ###
    def test_get_submission(self, client: FlaskClient, api_host: str, submission: Submission):
        """Test getting a submission"""
        response = client.get(
            f"/submissions/{submission.submission_id}",
            headers = {"X-CSRF-TOKEN":get_csrf_from_login(client, "student")}
        )
        assert response.status_code == 200
        data = response.json["data"]
        assert data["submission_id"] == f"{api_host}/submissions/{submission.submission_id}"

    def test_patch_submission_grading(
            self, client: FlaskClient, api_host: str, submission: Submission
        ):
        """Test patching the grading to a submission"""
        response = client.patch(
            f"/submissions/{submission.submission_id}",
            headers = {"X-CSRF-TOKEN":get_csrf_from_login(client, "teacher")},
            data = {"grading":20}
        )
        assert response.status_code == 200
        data = response.json["data"]
        assert data["submission_id"] == f"{api_host}/submissions/{submission.submission_id}"
        assert data["grading"] == 20.0

    def test_patch_submission_invalid_grading(self, client: FlaskClient, submission: Submission):
        """Test posting a submission when given an invalid project"""
        response = client.patch(
            f"/submissions/{submission.submission_id}",
            headers = {"X-CSRF-TOKEN":get_csrf_from_login(client, "teacher")},
            data = {"grading":"zero"}
        )
        assert response.status_code == 400



    ### SUBMISSION DOWNLOAD ###
    def test_get_submission_download(
            self, client: FlaskClient, project: Project, files
        ):
        """Test downloading a submission"""
        csrf = get_csrf_from_login(client, "student")
        response = client.post(
            "/submissions",
            headers = {"X-CSRF-TOKEN":csrf},
            data = {"project_id":project.project_id, "files": files}
        )
        assert response.status_code == 201
        submission_id = response.json["data"]["submission_id"].split("/")[-1]
        response = client.get(
            f"/submissions/{submission_id}/download",
            headers = {"X-CSRF-TOKEN":csrf}
        )
        assert response.status_code == 200
