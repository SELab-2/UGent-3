"""Tests for project endpoints."""

def test_assignment_download(client, valid_project, valid_project_entry):
    """
    Method for assignment download
    """

    data, status_code = valid_project_entry
    assert status_code == 201
    project_id = data["project_id"]
    response = client.get(f"/projects/{project_id}/assignment",
                          headers={"Authorization":"teacher2"})
    # 404 because the file is not found, no assignment.md in zip file
    assert response.status_code == 404


def test_not_found_download(client):
    """
    Test a not present project download
    """
    response = client.get("/projects")
    # get an index that doesnt exist
    response = client.get("/projects/-1/assignments", headers={"Authorization":"teacher2"})
    assert response.status_code == 404


def test_projects_home(client):
    """Test home project endpoint."""
    response = client.get("/projects", headers={"Authorization":"teacher1"})
    assert response.status_code == 200


def test_getting_all_projects(client):
    """Test getting all projects"""
    response = client.get("/projects", headers={"Authorization":"teacher1"})
    assert response.status_code == 200
    assert isinstance(response.json['data'], list)


def test_post_project(client, valid_project_entry):
    """Test posting a project to the database and testing if it's present"""

    data, status_code = valid_project_entry

    assert status_code == 201

    # check if the project with the id is present
    project_id = data["project_id"]
    response = client.get(f"/projects/{project_id}", headers={"Authorization":"teacher2"})

    assert response.status_code == 200

def test_remove_project(client, valid_project_entry):
    """Test removing a project to the datab and fetching it, testing if it's not present anymore"""
    data, _ = valid_project_entry
    project_id = data["project_id"]
    response = client.delete(f"/projects/{project_id}", headers={"Authorization":"teacher2"})
    assert response.status_code == 200

    # check if the project isn't present anymore and the delete indeed went through
    response = client.get(f"/projects/{project_id}", headers={"Authorization":"teacher2"})
    assert response.status_code == 404

def test_patch_project(client, valid_project_entry):
    """Test functionality of the PATCH method for projects"""
    data, _ = valid_project_entry

    project_id = data['project_id']

    new_title = data['title'] + "hallo"
    new_archived = not data['archived']

    response = client.patch(f"/projects/{project_id}", json={
        "title": new_title, "archived": new_archived
    }, headers={"Authorization":"teacher2"})

    assert response.status_code == 200
