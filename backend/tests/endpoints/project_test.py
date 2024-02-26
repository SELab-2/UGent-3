"""Tests for project endpoints."""

def test_projects_home(client):
    """Test home project endpoint."""
    response = client.get("/projects")
    assert response.status_code == 200

def test_getting_all_projects(client):
    """Test getting all projects"""
    response = client.get("/projects")
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_post_remove_project(db_session, client, course, course_teacher):
    """Test adding a user to the datab and fetching it"""

    db_session.add(course_teacher)
    db_session.add(course)
    db_session.commit()

    data = {
        "title": "YourProject for testing purposes 123451",
        "descriptions": ["YourProjectDescription"],
        "assignment_file": "@/path/to/your/file.txt",
        "deadline": "2024-02-25T12:00:00+00:00",
        "course_id": course.course_id,
        "visible_for_students": 'true',
        "archieved": 'false',
        "test_path": "YourTestPath",
        "script_name": "YourTestScriptName",
        "regex_expressions": "Y"
    }

    response = client.post("/projects", json=data)
    assert response.status_code == 201

    response = client.get("/projects", json={"title": data["title"]})
    assert response.status_code == 200

    json_data = response.json

    to_rem = {}
    for json in json_data:
        if json["title"] == data["title"]:
            to_rem = json
    response = client.delete(f"/projects/{to_rem['project_id']}")

    assert response.status_code == 204
    response = client.delete(f"/projects/{to_rem['project_id']}")
    assert response.status_code == 404

def test_update_project(db_session, client, course, course_teacher):
    """
    Test functionality of the PUT method for projects
    """

    db_session.add(course_teacher)
    db_session.commit()
    db_session.add(course)
    db_session.commit()

    # dummy data for testing
    data = {
        "title": "YourProject for testing purposes 123451",
        "descriptions": ["YourProjectDescription"],
        "assignment_file": "@/path/to/your/file.txt",
        "deadline": "2024-02-25T12:00:00+00:00",
        "course_id": course.course_id,
        "visible_for_students": 'true',
        "archieved": 'false',
        "test_path": "YourTestPath",
        "script_name": "YourTestScriptName",
        "regex_expressions": "Y"
    }

    # post it so it can be edited later on
    response = client.post("/projects", json=data)

    # get the newly added project is no other is present
    response = client.get("/projects")
    assert response.status_code == 200
    json_data = response.json[0]

    # set a new title and flit the archieved boolean
    new_archieved = not json_data["archieved"]
    new_title = "just patched title"

    # edit the project
    response = client.put(f"/projects/{json_data['project_id']}", json={
        "title": new_title, "archieved": new_archieved
    })

    assert response.status_code == 200

    # fetch the project again and check if the values are the newly edited values
    response = client.get(f"/projects/{json_data['project_id']}")
    data = response.json
    assert response.status_code == 200
    assert data['title'] == new_title
    assert data['archieved'] == new_archieved
