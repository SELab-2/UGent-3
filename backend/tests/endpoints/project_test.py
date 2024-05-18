"""Tests for project endpoints."""

import json
from typing import Any

from pytest import mark

from tests.utils.auth_login import get_csrf_from_login
from tests.endpoints.endpoint import (
    TestEndpoint,
    authentication_tests,
    authorization_tests
)

class TestProjectsEndpoint(TestEndpoint):
    """Class to test the projects API endpoint"""

    ### AUTHENTICATION ###
    # Where is login required
    authentication_tests = \
        authentication_tests("/projects", ["get", "post"]) + \
        authentication_tests("/projects/@project_id", ["get", "patch", "delete"]) + \
        authentication_tests("/projects/@project_id/assignment", ["get"]) + \
        authentication_tests("/projects/@project_id/submissions-download", ["get"]) + \
        authentication_tests("/projects/@project_id/latest-per-user", ["get"])

    @mark.parametrize("auth_test", authentication_tests, indirect=True)
    def test_authentication(self, auth_test: tuple[str, Any, str, bool]):
        """Test the authentication"""
        super().authentication(auth_test)



    ### AUTHORIZATION ###
    # Who can access what
    authorization_tests = \
        authorization_tests("/projects", "get",
            ["student", "student_other", "teacher", "teacher_other", "admin", "admin_other"],
            []) + \
        authorization_tests("/projects", "post",
            ["teacher"],
            ["student", "student_other", "teacher_other", "admin", "admin_other"]) + \
        authorization_tests("/projects/@project_id", "get",
            ["student", "teacher", "admin"],
            ["student_other", "teacher_other", "admin_other"]) + \
        authorization_tests("/projects/@project_id", "patch",
            ["teacher", "admin"],
            ["student", "student_other", "teacher_other", "admin_other"]) + \
        authorization_tests("/projects/@project_id", "delete",
            ["teacher"],
            ["student", "student_other", "teacher_other", "admin", "admin_other"]) + \
        authorization_tests("/projects/@project_id/assignment", "get",
            ["student", "teacher", "admin"],
            ["student_other", "teacher_other", "admin_other"]) + \
        authorization_tests("/projects/@project_id/submissions-download", "get",
            ["teacher", "admin"],
            ["student", "student_other", "teacher_other", "admin_other"]) + \
        authorization_tests("/projects/@project_id/latest-per-user", "get",
            ["teacher", "admin"],
            ["student_other", "teacher_other", "admin_other"])

    @mark.parametrize("auth_test", authorization_tests, indirect=True)
    def test_authorization(self, auth_test: tuple[str, Any, str, bool]):
        """Test the authorization"""
        super().authorization(auth_test)

def test_assignment_download(client, valid_project):
    """
    Method for assignment download
    """

    valid_project["deadlines"] = json.dumps(valid_project["deadlines"])
    with open("tests/resources/testzip.zip", "rb") as zip_file:
        valid_project["assignment_file"] = zip_file
        # post the project
        csrf = get_csrf_from_login(client, "teacher")
        response = client.post(
            "/projects",
            headers = {"X-CSRF-TOKEN":csrf},
            data=valid_project,
            content_type='multipart/form-data',
        )
        assert response.status_code == 201
        project_id = response.json["data"]["project_id"]
        response = client.get(f"/projects/{project_id}/assignment", headers = {"X-CSRF-TOKEN":csrf})
        # 404 because the file is not found, no assignment.md in zip file
        assert response.status_code == 404


def test_not_found_download(client):
    """
    Test a not present project download
    """
    csrf = get_csrf_from_login(client, "teacher2")
    response = client.get("/projects", headers = {"X-CSRF-TOKEN":csrf})
    # get an index that doesnt exist
    response = client.get("/projects/-1/assignments", headers = {"X-CSRF-TOKEN":csrf})
    assert response.status_code == 404


def test_projects_home(client):
    """Test home project endpoint."""
    csrf = get_csrf_from_login(client, "teacher1")
    response = client.get("/projects", headers = {"X-CSRF-TOKEN":csrf})
    assert response.status_code == 200


def test_getting_all_projects(client):
    """Test getting all projects"""
    csrf = get_csrf_from_login(client, "teacher1")
    response = client.get("/projects", headers = {"X-CSRF-TOKEN":csrf})
    assert response.status_code == 200
    assert isinstance(response.json['data'], list)


def test_post_project(client, valid_project):
    """Test posting a project to the database and testing if it's present"""
    valid_project["deadlines"] = json.dumps(valid_project["deadlines"])
    csrf = get_csrf_from_login(client, "teacher")
    with open("tests/resources/testzip.zip", "rb") as zip_file:
        valid_project["assignment_file"] = zip_file
        # post the project
        response = client.post(
            "/projects",
            data=valid_project,
            content_type='multipart/form-data', headers = {"X-CSRF-TOKEN":csrf}
        )

    assert response.status_code == 201

    # check if the project with the id is present
    project_id = response.json["data"]["project_id"]
    response = client.get(f"/projects/{project_id}", headers = {"X-CSRF-TOKEN":csrf})

    assert response.status_code == 200

def test_remove_project(client, valid_project_entry):
    """Test removing a project to the datab and fetching it, testing if it's not present anymore"""
    csrf = get_csrf_from_login(client, "teacher")
    project_id = valid_project_entry.project_id
    response = client.delete(f"/projects/{project_id}", headers = {"X-CSRF-TOKEN":csrf})
    assert response.status_code == 200

    # check if the project isn't present anymore and the delete indeed went through
    response = client.get(f"/projects/{project_id}", headers = {"X-CSRF-TOKEN":csrf})
    assert response.status_code == 404

def test_patch_project(client, valid_project_entry):
    """Test functionality of the PATCH method for projects"""
    csrf = get_csrf_from_login(client, "teacher")
    project_id = valid_project_entry.project_id

    new_title = valid_project_entry.title + "hallo"
    new_archived = not valid_project_entry.archived

    response = client.patch(f"/projects/{project_id}", json={
        "title": new_title, "archived": new_archived
    }, headers = {"X-CSRF-TOKEN":csrf})

    assert response.status_code == 200
