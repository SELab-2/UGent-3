"""Tests for project endpoints."""

def test_assignment_download(client, valid_project):
    """
    Method for assignment download
    """

    with open("tests/resources/testzip.zip", "rb") as zip_file:
        valid_project["assignment_file"] = zip_file
        # post the project
        response = client.post(
            "/projects",
            data=valid_project,
            content_type='multipart/form-data',
            headers={"Authorization":"teacher2"}
        )
    assert response.status_code == 201
    project_id = response.json["data"]["project_id"]
    response = client.get(f"/projects/{project_id}/assignment",
                          headers={"Authorization":"teacher2"})
    # file downloaded succesfully
    assert response.status_code == 200


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


def test_post_project(client, valid_project):
    """Test posting a project to the database and testing if it's present"""

    with open("tests/resources/testzip.zip", "rb") as zip_file:
        valid_project["assignment_file"] = zip_file
        # post the project
        response = client.post(
            "/projects",
            data=valid_project,
            content_type='multipart/form-data', headers={"Authorization":"teacher2"}
        )

    assert response.status_code == 201

    # check if the project with the id is present
    project_id = response.json["data"]["project_id"]
    response = client.get(f"/projects/{project_id}", headers={"Authorization":"teacher2"})

    assert response.status_code == 200

def test_remove_project(client, valid_project_entry):
    """Test removing a project to the datab and fetching it, testing if it's not present anymore"""

    project_id = valid_project_entry.project_id
    response = client.delete(f"/projects/{project_id}", headers={"Authorization":"teacher2"})
    assert response.status_code == 200

    # check if the project isn't present anymore and the delete indeed went through
    response = client.get(f"/projects/{project_id}", headers={"Authorization":"teacher2"})
    assert response.status_code == 404

def test_patch_project(client, valid_project_entry):
    """Test functionality of the PATCH method for projects"""

    project_id = valid_project_entry.project_id

    new_title = valid_project_entry.title + "hallo"
    new_archived = not valid_project_entry.archived

    response = client.patch(f"/projects/{project_id}", json={
        "title": new_title, "archived": new_archived
    }, headers={"Authorization":"teacher2"})

    assert response.status_code == 200
