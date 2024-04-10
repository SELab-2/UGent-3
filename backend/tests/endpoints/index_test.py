"""Test the base routes of the application"""

import yaml


def test_home(client):
    """Test whether the index page is accesible"""
    response = client.get("/")
    assert response.status_code == 200


def test_openapi_spec(client):
    """Test whether the required fields of the openapi spec are present"""
    response = client.get("/")
    response_text = response.text
    response_yaml = yaml.safe_load(response_text)

    assert "openapi" in response_yaml
    assert "info" in response_yaml
