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
from project.models.user import User
from project.db_in import db
from tests import db_url

engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
@pytest.fixture
def user_db_session():
    """Create a new database session for the user tests.
    After the test, all changes are rolled back and the session is closed."""
    db.metadata.create_all(engine)
    session = Session()
    session.add_all(
            [User(uid="del", is_admin=False, is_teacher=True),
             User(uid="pat", is_admin=False, is_teacher=True),
             User(uid="u_get", is_admin=False, is_teacher=True),
             User(uid="query_user", is_admin=True, is_teacher=False)
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
        response = client.delete(f"/users/{valid_user_entry.uid}")
        assert response.status_code == 200

        get_response = client.get(f"/users/{valid_user_entry.uid}")
        assert get_response.status_code == 404

    def test_delete_not_present(self, client):
        """Test deleting a user that does not exist."""
        response = client.delete("/users/-20")
        assert response.status_code == 404

    def test_wrong_form_post(self, client, user_invalid_field):
        """Test posting with a wrong form."""
        response = client.post("/users", json=user_invalid_field)
        assert response.status_code == 400

    def test_wrong_datatype_post(self, client, valid_user):
        """Test posting with a wrong content type."""
        response = client.post("/users", data=valid_user)
        assert response.status_code == 415

    def test_get_all_users(self, client, valid_user_entries):
        """Test getting all users."""
        response = client.get("/users", headers={"Authorization":"teacher1"})
        assert response.status_code == 200
        # Check that the response is a list (even if it's empty)
        assert isinstance(response.json["data"], list)
        for valid_user in valid_user_entries:
            assert valid_user.uid in \
                [user["uid"] for user in response.json["data"]]

    def test_get_one_user(self, client, valid_user_entry):
        """Test getting a single user."""
        response = client.get(f"users/{valid_user_entry.uid}")
        assert response.status_code == 200
        assert "data" in response.json

    def test_patch_user(self, client, valid_user_entry):
        """Test updating a user."""

        new_is_teacher = not valid_user_entry.is_teacher

        response = client.patch(f"/users/{valid_user_entry.uid}", json={
            'is_teacher': new_is_teacher,
            'is_admin': not valid_user_entry.is_admin
        })
        assert response.status_code == 200
        assert response.json["message"] == "User updated successfully!"

        get_response = client.get(f"/users/{valid_user_entry.uid}")
        assert get_response.status_code == 200
        assert get_response.json["data"]["is_teacher"] == new_is_teacher

    def test_patch_non_existent(self, client):
        """Test updating a non-existent user."""
        response = client.patch("/users/-20", json={
            'is_teacher': False,
            'is_admin': True
        })
        assert response.status_code == 403 # Patching is not allowed

    def test_patch_non_json(self, client, valid_user_entry):
        """Test sending a non-JSON patch request."""
        valid_user_form = asdict(valid_user_entry)
        valid_user_form["is_teacher"] = not valid_user_form["is_teacher"]
        response = client.patch(f"/users/{valid_user_form['uid']}", data=valid_user_form)
        assert response.status_code == 415

    def test_get_users_with_query(self, client, valid_user_entries):
        """Test getting users with a query."""
        # Send a GET request with query parameters, this is a nonsense entry but good for testing
        response = client.get("/users?is_admin=true&is_teacher=false", headers={"Authorization":"teacher1"})
        assert response.status_code == 200

        # Check that the response contains only the user that matches the query
        users = response.json["data"]
        for user in users:
            assert user["is_admin"] is True
            assert user["is_teacher"] is False
