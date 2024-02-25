"""
This module tests user management endpoints.

- test_post_delete_user: Tests user creation, deletion, and error handling for deletion
    of non-existent user.
- test_get_users: Tests retrieval of all users, ensuring the response is a list.
- test_patch_user: Tests user update functionality and error handling for updating
    non-existent user.
"""
def test_post_delete_user(client):
    """Test whether the users page is accessible"""
    response = client.post("/users", json={
        'uid': 'del',
        'is_teacher': True,
        'is_admin': False
    })
    assert response.status_code == 201 or response.status_code == 400 # already present
    # Delete the user
    response = client.delete("/users/del")
    assert response.status_code == 200
    assert response.json == {"Message": "User deleted successfully!"}

    # Try to delete the user again
    response = client.delete("/users/del")
    assert response.status_code == 404
    # a test that should fail
    response = client.post("/users", json={
        'uid': '12',
        'is_student': True, # wrong field name
        'is_admin': False
    })
    assert response.status_code == 400

    # Send a request with a media type that's not JSON
    response = client.post("/users", data={
        'uid': '12',
        'is_teacher': True,
        'is_admin': False
    })
    assert response.status_code == 415

def test_get_users(client):
    """Test the get method of the Users class"""
    response = client.get("/users")
    assert response.status_code == 200
    # Check that the response is a list (even if it's empty)
    assert isinstance(response.json, list)

    response = client.post("/users", json={
        'uid': 'u_get',
        'is_teacher': True,
        'is_admin': False
    })
    assert response.status_code == 201 or response.status_code == 400
    response = client.get("users/u_get")
    assert response.status_code == 200
    assert response.json == {
        'uid': 'u_get',
        'is_teacher': True,
        'is_admin': False
    }


def test_patch_user(client):
    """Test the update method of the Users class"""
    # First, create a user to update
    client.post("/users", json={
        'uid': 'pat',
        'is_teacher': True,
        'is_admin': False
    })

    # Then, update the user
    response = client.patch("/users/pat", json={
        'is_teacher': False,
        'is_admin': True
    })
    assert response.status_code == 200
    assert response.json == {"Message": "User updated successfully!"}

    # Try to update a non-existent user
    response = client.patch("/users/non", json={
        'is_teacher': False,
        'is_admin': True
    })
    assert response.status_code == 404

    # Send a request with a media type that's not JSON
    response = client.post("/users", data={
        'uid': '12',
        'is_teacher': True,
        'is_admin': False
    })
    assert response.status_code == 415 
