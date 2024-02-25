def test_simple(client):
    """Test whether the users page is accessible"""
    response = client.post("/users", json={
        'uid': '12',
        'is_teacher': True,
        'is_admin': False
    })
    assert response.status_code == 200
    # a test that should fail
    response = client.post("/users", json={
        'uid': '12',
        'is_student': True, #wrong field name
        'is_admin': False
    })
    assert response.status_code == 400