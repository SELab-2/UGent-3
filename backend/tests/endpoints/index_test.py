"""Test the base routes of the application"""

def test_home(client):
    """Test whether the index page is accesible"""
    response = client.get("/")
    assert response.status_code == 200
