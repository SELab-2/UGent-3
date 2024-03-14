"""Tests for project endpoints."""
from project.models.project import Project

def test_assignment_download(db_session, client, course_ad, course_teacher_ad, project_json):
    """
    Method for assignment download
    """
    db_session.add(course_teacher_ad)
    db_session.commit()

    db_session.add(course_ad)
    db_session.commit()
    project_json["course_id"] = course_ad.course_id

    with open("testzip.zip", "rb") as zip_file:
        project_json["assignment_file"] = zip_file
        # post the project
        response = client.post(
            "/projects",
            data=project_json,
            content_type='multipart/form-data',
            headers={"Authorization":"teacher1"}
        )

    project_id = response.json["data"]["project_id"]
    response = client.get(f"/projects/{project_id}/assignments", headers={"Authorization":"teacher1"})
    # file downloaded succesfully
    assert response.status_code == 200


def test_not_found_download(client):
    """
    Test a not present project download
    """
    response = client.get("/projects")
    # get an index that doesnt exist
    project_id = len(response.data)+1
    response = client.get(f"/projects/{project_id}/assignments", headers={"Authorization":"teacher2"})
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


def test_getting_all_projects_no_authentication(client):
    """Test getting all projects without authentication"""
    response = client.get("/projects")
    assert response.status_code == 401


def test_getting_all_projects_not_authorized(client):
    """Test getting all projects without authorization"""
    response = client.get("/projects", headers={"Authorization":"student1"})
    assert response.status_code == 403


def test_post_project(client, course_ad, project_json):
    """Test posting a project to the database and testing if it's present"""

    project_json["course_id"] = course_ad.course_id
    # cant be done with 'with' because it autocloses then
    # pylint: disable=R1732
    with open("testzip.zip", "rb") as zip_file:
        project_json["assignment_file"] = zip_file
        # post the project
        response = client.post(
            "/projects",
            data=project_json,
            content_type='multipart/form-data',
            headers={"Authorization":"teacher1"}
        )

    assert response.status_code == 201

    # check if the project with the id is present
    project_id = response.json["data"]["project_id"]
    response = client.get(f"/projects/{project_id}", headers={"Authorization":"teacher1"})

    assert response.status_code == 200

def test_post_project_not_authorized(db_session, client, course_ad, course_teacher_ad, project_json):
    """Test posting a project to the database and testing if it's not present"""

    project_json["course_id"] = course_ad.course_id
    # cant be done with 'with' because it autocloses then
    # pylint: disable=R1732
    with open("testzip.zip", "rb") as zip_file:
        project_json["assignment_file"] = zip_file
        # post the project
        response = client.post(
            "/projects",
            data=project_json,
            content_type='multipart/form-data',
            headers={"Authorization":"student1"}
        )

    assert response.status_code == 403

def test_project_no_authentication(db_session, client, course_ad, course_teacher_ad, project_json):
    """Test posting a project to the database and testing if it's not present"""
    db_session.add(course_teacher_ad)
    db_session.commit()

    db_session.add(course_ad)
    db_session.commit()

    project_json["course_id"] = course_ad.course_id
    # cant be done with 'with' because it autocloses then
    # pylint: disable=R1732
    with open("testzip.zip", "rb") as zip_file:
        project_json["assignment_file"] = zip_file
        # post the project
        response = client.post(
            "/projects",
            data=project_json,
            content_type='multipart/form-data',
        )

    assert response.status_code == 401


def test_remove_project(db_session, client, course_ad, course_teacher_ad, project_json):
    """Test removing a project to the datab and fetching it, testing if it's not present anymore"""

    db_session.add(course_teacher_ad)
    db_session.commit()

    db_session.add(course_ad)
    db_session.commit()

    project_json["course_id"] = course_ad.course_id

    # post the project
    with open("testzip.zip", "rb") as zip_file:
        project_json["assignment_file"] = zip_file
        response = client.post("/projects", data=project_json, headers={"Authorization":"teacher1"})

    # check if the project with the id is present
    assert response.status_code == 201
    project_id = response.json["data"]["project_id"]

    response = client.delete(f"/projects/{project_id}", headers={"Authorization":"teacher1"})
    assert response.status_code == 200

    # check if the project isn't present anymore and the delete indeed went through
    response = client.delete(f"/projects/{project_id}", headers={"Authorization":"teacher1"})
    assert response.status_code == 404


def test_remove_project_wrong_teacher(db_session, client, course_ad, course_teacher_ad, project_json):
    """Test removing a project to the datab and fetching it, testing if it's not present anymore"""

    db_session.add(course_teacher_ad)
    db_session.commit()

    db_session.add(course_ad)
    db_session.commit()

    project_json["course_id"] = course_ad.course_id

    # post the project
    with open("testzip.zip", "rb") as zip_file:
        project_json["assignment_file"] = zip_file
        response = client.post("/projects", data=project_json, headers={"Authorization":"teacher1"})

    # check if the project with the id is present
    assert response.status_code == 201
    project_id = response.json["data"]["project_id"]

    response = client.delete(f"/projects/{project_id}", headers={"Authorization":"teacher2"})
    assert response.status_code == 403

    # check if the project is still present
    response = client.get(f"/projects/{project_id}", headers={"Authorization":"teacher1"})
    assert response.status_code == 200


def test_remove_project_student(db_session, client, course_ad, course_teacher_ad, project_json):
    """Test removing a project to the datab and fetching it, testing if it's not present anymore"""

    db_session.add(course_teacher_ad)
    db_session.commit()

    db_session.add(course_ad)
    db_session.commit()

    project_json["course_id"] = course_ad.course_id

    # post the project
    with open("testzip.zip", "rb") as zip_file:
        project_json["assignment_file"] = zip_file
        response = client.post("/projects", data=project_json, headers={"Authorization":"teacher1"})

    # check if the project with the id is present
    assert response.status_code == 201
    project_id = response.json["data"]["project_id"]

    response = client.delete(f"/projects/{project_id}", headers={"Authorization":"student1"})
    assert response.status_code == 403

    # check if the project is still present
    response = client.get(f"/projects/{project_id}", headers={"Authorization":"teacher1"})
    assert response.status_code == 200


def test_remove_project_course_admin(db_session, client, course_ad, course_teacher_ad, project_json):
    """Test removing a project to the datab and fetching it, testing if it's not present anymore"""

    db_session.add(course_teacher_ad)
    db_session.commit()

    db_session.add(course_ad)
    db_session.commit()

    project_json["course_id"] = course_ad.course_id

    # post the project
    with open("testzip.zip", "rb") as zip_file:
        project_json["assignment_file"] = zip_file
        response = client.post("/projects", data=project_json, headers={"Authorization":"teacher1"})

    # check if the project with the id is present
    assert response.status_code == 201
    project_id = response.json["data"]["project_id"]

    response = client.delete(f"/projects/{project_id}", headers={"Authorization":"course_admin1"})
    assert response.status_code == 403

    # check if the project is still present
    response = client.get(f"/projects/{project_id}", headers={"Authorization":"teacher1"})
    assert response.status_code == 200


def test_remove_project_no_authentication(db_session, client, course_ad, course_teacher_ad, project_json):
    """Test removing a project to the datab and fetching it, testing if it's not present anymore"""

    db_session.add(course_teacher_ad)
    db_session.commit()

    db_session.add(course_ad)
    db_session.commit()

    project_json["course_id"] = course_ad.course_id

    # post the project
    with open("testzip.zip", "rb") as zip_file:
        project_json["assignment_file"] = zip_file
        response = client.post("/projects", data=project_json)

    # check if the project with the id is present
    assert response.status_code == 401
    

def test_patch_project_teacher(db_session, client, course_ad, course_teacher_ad, project):
    """
    Test functionality of the PUT method for projects
    """

    db_session.add(course_teacher_ad)
    db_session.commit()

    db_session.add(course_ad)
    db_session.commit()

    project.course_id = course_ad.course_id

    # post the project to edit
    db_session.add(project)
    db_session.commit()
    project_id = project.project_id

    new_title = "patched title"
    new_archived = not project.archived

    response = client.patch(f"/projects/{project_id}", json={
        "title": new_title, "archived": new_archived
    }, headers={"Authorization":"teacher1"})
    db_session.commit()
    updated_project = db_session.get(Project, {"project_id": project.project_id})

    assert response.status_code == 200
    assert updated_project.title == new_title
    assert updated_project.archived == new_archived


def test_patch_project_course_admin(db_session, client, course_ad, course_teacher_ad, project):
    """
    Test functionality of the PUT method for projects
    """

    db_session.add(course_teacher_ad)
    db_session.commit()

    db_session.add(course_ad)
    db_session.commit()

    project.course_id = course_ad.course_id

    # post the project to edit
    db_session.add(project)
    db_session.commit()
    project_id = project.project_id

    new_title = "patched title"
    new_archived = not project.archived

    response = client.patch(f"/projects/{project_id}", json={
        "title": new_title, "archived": new_archived
    }, headers={"Authorization":"course_admin1"})
    db_session.commit()
    updated_project = db_session.get(Project, {"project_id": project.project_id})

    assert response.status_code == 200
    assert updated_project.title == new_title
    assert updated_project.archived == new_archived


def test_patch_project_student(db_session, client, course_ad, course_teacher_ad, project):
    """
    Test functionality of the PUT method for projects
    """

    db_session.add(course_teacher_ad)
    db_session.commit()

    db_session.add(course_ad)
    db_session.commit()

    project.course_id = course_ad.course_id

    # post the project to edit
    db_session.add(project)
    db_session.commit()
    project_id = project.project_id

    new_title = "patched title"
    new_archived = not project.archived

    response = client.patch(f"/projects/{project_id}", json={
        "title": new_title, "archived": new_archived
    }, headers={"Authorization":"student1"})
    db_session.commit()
    updated_project = db_session.get(Project, {"project_id": project.project_id})

    assert response.status_code == 403
    assert updated_project.title == project.title
    assert updated_project.archived == project.archived


def test_patch_project_wrong_teacher(db_session, client, course_ad, course_teacher_ad, project):
    """
    Test functionality of the PUT method for projects
    """

    db_session.add(course_teacher_ad)
    db_session.commit()

    db_session.add(course_ad)
    db_session.commit()

    project.course_id = course_ad.course_id

    # post the project to edit
    db_session.add(project)
    db_session.commit()
    project_id = project.project_id

    new_title = "patched title"
    new_archived = not project.archived

    response = client.patch(f"/projects/{project_id}", json={
        "title": new_title, "archived": new_archived
    }, headers={"Authorization":"teacher2"})
    db_session.commit()
    updated_project = db_session.get(Project, {"project_id": project.project_id})

    assert response.status_code == 403
    assert updated_project.title == project.title
    assert updated_project.archived == project.archived