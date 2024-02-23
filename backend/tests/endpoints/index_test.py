"""Test the base routes of the application"""

def test_home(client):
    """Test whether the index page is accesible"""
    response = client.get("/")
    assert response.status_code == 200

def test_openapi_spec(client):
    "Test whether the required fields of the openapi spec are present"
    response = client.get("/")
    response_json = response.json
    assert response_json["openapi"] is not None
    assert response_json["info"] is not None