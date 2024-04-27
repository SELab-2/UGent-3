"""
This module tests user management endpoints.

- test_post_delete_user: Tests user creation, deletion, and error handling for deletion
    of non-existent user.
- test_get_users: Tests retrieval of all users, ensuring the response is a list.
- test_patch_user: Tests user update functionality and error handling for updating
    non-existent user.
"""
from dataclasses import asdict
import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from project.models.user import User,Role
from project.db_in import db
from tests import db_url
from tests.utils.auth_login import get_csrf_from_login

engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
@pytest.fixture
def user_db_session():
    """Create a new database session for the user tests.
    After the test, all changes are rolled back and the session is closed."""
    db.metadata.create_all(engine)
    session = Session()
    session.add_all(
        [User(uid="del", role=Role.TEACHER),
         User(uid="pat", role=Role.TEACHER),
         User(uid="u_get", role=Role.TEACHER),
         User(uid="query_user", role=Role.ADMIN)
         ]
    )
    session.commit()
    yield session
    session.rollback()
    session.close() # pylint: disable=duplicate-code;
    for table in reversed(db.metadata.sorted_tables):
        session.execute(table.delete())
    session.commit()


class TestUserEndpoint:
    """Class to test user management endpoints."""

    def test_delete_user(self, client, valid_user_entry):
        """Test deleting a user."""
        # Delete the user
        csrf = get_csrf_from_login(client, "student1")
        response = client.delete(f"/users/{valid_user_entry.uid}",
                                  headers={"X-CSRF-TOKEN":csrf})
        assert response.status_code == 200

        csrf = get_csrf_from_login(client, "teacher1")
        # If student 1 sends this request, he would get added again
        get_response = client.get(f"/users/{valid_user_entry.uid}",
                                  headers={"X-CSRF-TOKEN":csrf})

        assert get_response.status_code == 404

    def test_delete_user_not_yourself(self, client, valid_user_entry):
        """Test deleting a user that is not the user the authentication belongs to."""
        # Delete the user
        csrf = get_csrf_from_login(client, "teacher1")
        response = client.delete(f"/users/{valid_user_entry.uid}",
                                 headers={"X-CSRF-TOKEN":csrf})
        assert response.status_code == 403

        get_response = client.get(f"/users/{valid_user_entry.uid}",
                                  headers={"X-CSRF-TOKEN":csrf})

        assert get_response.status_code == 200

    def test_delete_not_present(self, client):
        """Test deleting a user that does not exist."""
        csrf = get_csrf_from_login(client, "teacher1")
        response = client.delete("/users/-20", headers={"X-CSRF-TOKEN":csrf})
        assert response.status_code == 403 # User does not exist, so you are not the user

    def test_post_no_authentication(self, client, user_invalid_field):
        """Test posting without authentication."""
        response = client.post("/users", json=user_invalid_field)
        assert response.status_code == 403 # POST to /users is not allowed

    def test_post_authenticated(self, client, valid_user):
        """Test posting with wrong authentication."""
        csrf = get_csrf_from_login(client, "teacher1")
        response = client.post("/users", data=valid_user,
                               headers={"X-CSRF-TOKEN":csrf})
        assert response.status_code == 403 # POST to /users is not allowed

    def test_wrong_form_post(self, client, user_invalid_field):
        """Test posting with a wrong form."""
        csrf = get_csrf_from_login(client, "teacher1")
        response = client.post("/users", data=user_invalid_field,
                               headers={"X-CSRF-TOKEN":csrf})
        assert response.status_code == 403

    def test_get_all_users(self, client, valid_user_entries):
        """Test getting all users."""
        csrf = get_csrf_from_login(client, "teacher1")
        response = client.get("/users", headers={"X-CSRF-TOKEN":csrf})
        assert response.status_code == 200
        # Check that the response is a list (even if it's empty)
        assert isinstance(response.json["data"], list)
        for valid_user in valid_user_entries:
            assert valid_user.uid in [user["uid"] for user in response.json["data"]]

    def test_get_all_users_no_authentication(self, client):
        """Test getting all users without authentication."""
        response = client.get("/users")
        assert response.status_code == 401

    def test_get_all_users_wrong_authentication(self, client):
        """Test getting all users with wrong authentication."""
        client.get("/auth?code=wrong")
        response = client.get("/users")
        assert response.status_code == 401

    def test_get_one_user(self, client, valid_user_entry):
        """Test getting a single user."""
        client.get("/auth?code=teacher1")
        response = client.get(f"users/{valid_user_entry.uid}")
        assert response.status_code == 200
        assert "data" in response.json

    def test_get_one_user_no_authentication(self, client, valid_user_entry):
        """Test getting a single user without authentication."""
        response = client.get(f"users/{valid_user_entry.uid}")
        assert response.status_code == 401

    def test_get_one_user_wrong_authentication(self, client, valid_user_entry):
        """Test getting a single user with wrong authentication."""
        res = client.get("/auth?code=wrong")
        assert res.status_code == 401
        response = client.get(f"users/{valid_user_entry.uid}")
        assert response.status_code == 401

    def test_patch_user_not_authorized(self, client, admin, valid_user_entry):
        """Test updating a user."""

        if valid_user_entry.role == Role.TEACHER:
            new_role = Role.ADMIN
        if valid_user_entry.role == Role.ADMIN:
            new_role = Role.STUDENT
        else:
            new_role = Role.TEACHER
        new_role = new_role.name
        csrf = get_csrf_from_login(client, "student01")
        response = client.patch(f"/users/{valid_user_entry.uid}", json={
            'role': new_role
        }, headers={'X-CSRF-TOKEN':csrf})
        assert response.status_code == 403 # Patching a user is not allowed as a not-admin

    def test_patch_user(self, client, admin, valid_user_entry):
        """Test updating a user."""

        if valid_user_entry.role == Role.TEACHER:
            new_role = Role.ADMIN
        if valid_user_entry.role == Role.ADMIN:
            new_role = Role.STUDENT
        else:
            new_role = Role.TEACHER
        new_role = new_role.name
        csrf = get_csrf_from_login(client, "admin")
        response = client.patch(f"/users/{valid_user_entry.uid}", json={
            'role': new_role
        }, headers={'X-CSRF-TOKEN':csrf})
        assert response.status_code == 200

    def test_patch_non_existent(self, client, admin):
        """Test updating a non-existent user."""
        csrf = get_csrf_from_login(client, "admin")
        response = client.patch("/users/-20", json={
            'role': Role.TEACHER.name
        }, headers={'X-CSRF-TOKEN':csrf})
        assert response.status_code == 404

    def test_patch_non_json(self, client, admin, valid_user_entry):
        """Test sending a non-JSON patch request."""
        valid_user_form = asdict(valid_user_entry)
        if valid_user_form["role"] == Role.TEACHER.name:
            valid_user_form["role"] = Role.STUDENT.name
        else:
            valid_user_form["role"] = Role.TEACHER.name
        csrf = get_csrf_from_login(client, "admin")
        response = client.patch(f"/users/{valid_user_form['uid']}", data=valid_user_form,
                                headers={'X-CSRF-TOKEN':csrf})
        assert response.status_code == 415

    def test_get_users_with_query(self, client, valid_user_entries):
        """Test getting users with a query."""
        get_csrf_from_login(client, "admin")
        # Send a GET request with query parameters, this is a nonsense entry but good for testing
        response = client.get("/users?role=ADMIN")
        assert response.status_code == 200

        # Check that the response contains only the user that matches the query
        users = response.json["data"]
        for user in users:
            assert Role[user["role"]] == Role.ADMIN
