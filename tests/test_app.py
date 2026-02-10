import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_remove_participant():
    # Sign up a new participant
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    signup_resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup_resp.status_code == 200 or signup_resp.status_code == 400
    # Try to remove participant
    delete_resp = client.delete(f"/activities/{activity}/participants/{email}")
    assert delete_resp.status_code == 204 or delete_resp.status_code == 404

def test_signup_duplicate():
    email = "alex@mergington.edu"
    activity = "Basketball Club"
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Student already signed up for this activity"

def test_remove_nonexistent_participant():
    email = "notfound@mergington.edu"
    activity = "Chess Club"
    resp = client.delete(f"/activities/{activity}/participants/{email}")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Participant not found in this activity"
