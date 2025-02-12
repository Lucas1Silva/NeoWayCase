# tests/test_api.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_status():
    response = client.get("/status")
    assert response.status_code == 200
    data = response.json()
    assert "uptime" in data
    assert "request_count" in data
