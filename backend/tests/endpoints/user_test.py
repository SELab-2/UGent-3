def test_post_delete_user(client):
    """Test whether the users page is accessible"""
    response = client.post("/users", json={
        'uid': 'del',
        'is_teacher': True,
        'is_admin': False
    })
    assert response.status_code == 200
    # Delete the user
    response = client.delete("/users", json={'uid': 'del'})
    assert response.status_code == 200
    assert response.json == {"Message": f"User with id: del deleted successfully!"}

    # Try to delete the user again
    response = client.delete("/users", json={'uid': 'del'})
    assert response.status_code == 404
    # a test that should fail
    response = client.post("/users", json={
        'uid': '12',
        'is_student': True, #wrong field name
        'is_admin': False
    })
    assert response.status_code == 400

def test_get_users(client):
    """Test the get method of the Users class"""
    response = client.get("/users")
    assert response.status_code == 200
    # Check that the response is a list (even if it's empty)
    assert isinstance(response.json, list)

def test_patch_user(client):
    """Test the update method of the Users class"""
    # First, create a user to update
    client.post("/users", json={
        'uid': 'pat',
        'is_teacher': True,
        'is_admin': False
    })

    # Then, update the user
    response = client.patch("/users", json={
        'uid': 'pat',
        'is_teacher': False,
        'is_admin': True
    })
    assert response.status_code == 200
    assert response.json == {"Message": "User updated successfully!"}

    # Try to update a non-existent user
    response = client.patch("/users", json={
        'uid': 'non',
        'is_teacher': False,
        'is_admin': True
    })
    assert response.status_code == 404