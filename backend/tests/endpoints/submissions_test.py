"""Tests the submissions API endpoint"""

from typing import Any

from pytest import mark
from flask.testing import FlaskClient

from tests.endpoints.endpoint import (
    TestEndpoint,
    authentication_tests,
    authorization_tests,
    data_field_type_tests,
    query_parameter_tests
)
from project.models.user import User
from project.models.project import Project
from project.models.submission import Submission

class TestSubmissionsEndpoint(TestEndpoint):
    """Class to test the submissions API endpoint"""

    ### AUTHENTICATION ###
    # Where is login required
    authentication_tests = \
        authentication_tests("/submissions", ["get", "post"]) + \
        authentication_tests("/submissions/@submission_id", ["get", "patch"])

    @mark.parametrize("auth_test", authentication_tests, indirect=True)
    def test_authentication(self, auth_test: tuple[str, Any]):
        """Test the authentication"""
        super().authentication(auth_test)



    ### AUTHORIZATION ###
    # Who can access what
    authorization_tests = \
        authorization_tests("/submissions", "get",
            ["student", "student_other", "teacher", "teacher_other", "admin", "admin_other"],
            []
        ) + \
        authorization_tests("/submissions", "post",
            ["student"],
            ["student_other", "teacher", "teacher_other", "admin", "admin_other"]
        ) + \
        authorization_tests("/submissions/@submission_id", "get",
            ["student", "teacher", "admin"],
            ["student_other", "teacher_other", "admin_other"]
        ) + \
        authorization_tests("/submissions/@submission_id", "patch",
            ["teacher", "admin"],
            ["student", "student_other", "teacher_other", "admin_other"]
        )

    @mark.parametrize("auth_test", authorization_tests, indirect=True)
    def test_authorization(self, auth_test: tuple[str, Any, str, bool]):
        """Test the authorization"""
        super().authorization(auth_test)



    ### DATA FIELD TYPE ###
    # Test a data field by passing a list of values for which it should return bad request
    data_field_type_tests = \
        data_field_type_tests("/submissions", "post", "student",
            {"uid": "student", "project_id": "@project_id"},
            {"uid": [None, 0, "zero"], "project_id": [None, "zero", 0]}
        ) + \
        data_field_type_tests("/submissions/@submissions_id", "patch", "teacher",
            {"grading": 20},
            {"grading": ["zero", -1, 80]}
        )

    @mark.parametrize("data_field_type_test", data_field_type_tests, indirect=True)
    def test_data_fields(self, data_field_type_test: tuple[str, Any, str, dict[str, Any]]):
        """Test a data field typing"""
        super().data_field_type(data_field_type_test)



    ### QUERY PARAMETER ###
    # Test a query parameter, should return [] for wrong values
    query_parameter_tests = query_parameter_tests(
        "/submissions", "get", "student", ["uid", "project_id"]
    )

    @mark.parametrize("query_parameter_test", query_parameter_tests, indirect=True)
    def test_query_parameters(self, query_parameter_test: tuple[str, Any, str, bool]):
        """Test a query parameter"""
        super().query_parameter(query_parameter_test)



    ### GET SUBMISSIONS ###
    def test_get_submissions(self, client: FlaskClient, api_host: str, submission: Submission):
        """Test getting all submissions"""
        response = client.get("/submissions", headers = {"Authorization": "teacher"})
        assert response.status_code == 200
        assert response.json["data"][0]["submission_id"] == \
            f"{api_host}/submissions/{submission.submission_id}"



    ### POST SUBMISSIONS ###
    def test_post_submission(self, client: FlaskClient, student: User, project: Project):
        """Test posting a submission"""
        response = client.post(
            "/submissions",
            headers = {"Authorization": "student"},
            json = {
                "uid": student.uid,
                "project_id": project.project_id
            }
        )
        assert response.status_code == 201
        assert len(response.json["data"]) == 2



    ### GET SUBMISSION ###
    def test_get_submission(self, client: FlaskClient, api_host: str, submission: Submission):
        """Test getting a submission"""
        response = client.get(
            f"/submissions/{submission.submission_id}",
            headers = {"Authorization"}
        )
        assert response.status_code == 200
        assert response.json["data"]["submission_id"] == \
            f"{api_host}/submissions/{submission.submission_id}"



    ### PATCH SUBMISSION ###
    def test_patch_submission_correct_teacher(
            self, client: FlaskClient, api_host: str, submission: Submission
        ):
        """Test patching a submission"""
        response = client.patch(
            f"/submissions/{submission.submission_id}",
            headers = {"Authorization": "teacher"},
            json = {"grading": 20}
        )
        assert response.status_code == 200
        assert response.json["data"]["id"] == \
            f"{api_host}/submissions/{submission.submission_id}"
