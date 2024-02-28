"""Tests for project endpoints."""
from project.models.projects import Projects

def test_projects_home(client):
    """Test home project endpoint."""
    response = client.get("/projects")
    assert response.status_code == 200


def test_getting_all_projects(client):
    """Test getting all projects"""
    response = client.get("/projects")
    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_post_project(db_session, client, course, course_teacher, project_json):
    """Test posting a project to the datab and testing if it's present"""
    db_session.add(course_teacher)
    db_session.commit()

    db_session.add(course)
    db_session.commit()

    project_json["course_id"] = course.course_id

    # post the project
    print("project json")
    print(project_json)
    response = client.post("/projects", json=project_json)
    assert response.status_code == 201

    # check if the project with the id is present
    project_id = response.json["project_id"]
    response = client.get(f"/projects/{project_id}")
    assert response.status_code == 200


def test_remove_project(db_session, client, course, course_teacher, project_json):
    """Test removing a project to the datab and fetching it, testing if its not present anymore"""

    db_session.add(course_teacher)
    db_session.commit()

    db_session.add(course)
    db_session.commit()

    project_json["course_id"] = course.course_id

    # post the project
    response = client.post("/projects", json=project_json)
    assert response.status_code == 201

    # check if the project with the id is present
    project_id = response.json["project_id"]
    response = client.get(f"/projects/{project_id}")
    assert response.status_code == 200

    # check if the 204 status code is returned
    response = client.delete(f"/projects/{project_id}")
    assert response.status_code == 204

    # check if the project isn't present anymore and the delete indeed went through
    response = client.delete(f"/projects/{project_id}")
    assert response.status_code == 404


def test_update_project(db_session, client, course, course_teacher, project):
    """
    Test functionality of the PUT method for projects
    """

    db_session.add(course_teacher)
    db_session.commit()

    db_session.add(course)
    db_session.commit()

    project.course_id = course.course_id

    # post the project to edit
    db_session.add(project)
    db_session.commit()
    project_id = project.project_id

    new_title = "patched title"
    new_archieved = not project.archieved

    response = client.patch(f"/projects/{project_id}", json={
        "title": new_title, "archieved": new_archieved
    })
    db_session.commit()
    # print(project)
    print(response)
    updated_project = db_session.get(Projects, {"project_id": project.project_id})

    assert response.status_code == 200
    assert updated_project.title == new_title
    assert updated_project.archieved == new_archieved
