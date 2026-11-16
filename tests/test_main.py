
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to CloudOps360",
        "platform": "Cloud Operations Platform",
        "status": "running"
    }


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["application"] == "cloudops360"
    assert "timestamp" in data
