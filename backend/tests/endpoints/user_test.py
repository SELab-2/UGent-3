"""
This module tests user management endpoints.

- test_post_delete_user: Tests user creation, deletion, and error handling for deletion
    of non-existent user.
- test_get_users: Tests retrieval of all users, ensuring the response is a list.
- test_patch_user: Tests user update functionality and error handling for updating
    non-existent user.
"""
class TestUserEndpoint:
    """Class to test user management endpoints."""

    def test_delete_user(self, client,user_db_session):  # pylint:  disable=unused-argument ; pytest uses it
        """Test deleting a user."""
        # Delete the user
        response = client.delete("/users/del")
        assert response.status_code == 200
        assert response.json == {"Message": "User deleted successfully!"}

    def test_delete_not_present(self, client,user_db_session): # pylint:  disable=unused-argument ; pytest uses it
        """Test deleting a user that does not exist."""
        response = client.delete("/users/non")
        assert response.status_code == 404

    def test_wrong_form_post(self, client,user_db_session): # pylint:  disable=unused-argument ; pytest uses it
        """Test posting with a wrong form."""
        response = client.post("/users", json={
            'uid': '12',
            'is_student': True,  # wrong field name
            'is_admin': False
        })
        assert response.status_code == 400

    def test_wrong_datatype_post(self, client,user_db_session): # pylint:  disable=unused-argument ; pytest uses it
        """Test posting with a wrong data type."""
        response = client.post("/users", data={
            'uid': '12',
            'is_teacher': True,
            'is_admin': False
        })
        assert response.status_code == 415

    def test_get_all_users(self, client,user_db_session): # pylint:  disable=unused-argument ; pytest uses it
        """Test getting all users."""
        response = client.get("/users")
        assert response.status_code == 200
        # Check that the response is a list (even if it's empty)
        assert isinstance(response.json, list)

    def test_get_one_user(self, client,user_db_session): # pylint:  disable=unused-argument ; pytest uses it
        """Test getting a single user."""
        response = client.get("users/u_get")
        assert response.status_code == 200
        assert response.json == {
            'uid': 'u_get',
            'is_teacher': True,
            'is_admin': False
        }

    def test_patch_user(self, client, user_db_session): # pylint:  disable=unused-argument ; pytest uses it
        """Test updating a user."""
        response = client.patch("/users/pat", json={
            'is_teacher': False,
            'is_admin': True
        })
        assert response.status_code == 200
        assert response.json == {"Message": "User updated successfully!"}

    def test_patch_non_existent(self, client,user_db_session): # pylint:  disable=unused-argument ; pytest uses it
        """Test updating a non-existent user."""
        response = client.patch("/users/non", json={
            'is_teacher': False,
            'is_admin': True
        })
        assert response.status_code == 404

    def test_patch_non_json(self, client,user_db_session): # pylint:  disable=unused-argument ; pytest uses it
        """Test sending a non-JSON patch request."""
        response = client.post("/users", data={
            'uid': '12',
            'is_teacher': True,
            'is_admin': False
        })
        assert response.status_code == 415
