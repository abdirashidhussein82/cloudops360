
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


def test_create_service(client):
    response = client.post(
        "/services",
        json={
            "name": "Test Payment API",
            "description": "Testing service creation",
            "status": "active",
            "environment": "development"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Test Payment API"
    assert data["status"] == "active"
    assert data["environment"] == "development"
    assert "id" in data

def test_get_services(client):
    # Create a service first
    client.post(
        "/services",
        json={
            "name": "Monitoring Test API",
            "description": "Testing service retrieval",
            "status": "active",
            "environment": "development"
        }
    )

    # Retrieve all services
    response = client.get("/services")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "Monitoring Test API"
    assert data[0]["status"] == "active"


def test_update_service(client):
    # Create a service first
    create_response = client.post(
        "/services",
        json={
            "name": "Test API",
            "description": "Original description",
            "status": "active",
            "environment": "development"
        }
    )

    service_id = create_response.json()["id"]

    # Update the existing service
    update_response = client.put(
        f"/services/{service_id}",
        json={
            "name": "Test API",
            "description": "Updated description",
            "status": "maintenance",
            "environment": "production"
        }
    )

    assert update_response.status_code == 200

    data = update_response.json()

    assert data["id"] == service_id
    assert data["description"] == "Updated description"
    assert data["status"] == "maintenance"
    assert data["environment"] == "production"

def test_delete_service(client):
    # Create a service first
    create_response = client.post(
        "/services",
        json={
            "name": "Delete Test API",
            "description": "Testing service deletion",
            "status": "active",
            "environment": "development"
        }
    )

    service_id = create_response.json()["id"]

    # Delete the service
    delete_response = client.delete(
        f"/services/{service_id}"
    )

    assert delete_response.status_code == 204

    # Verify that the service no longer exists
    get_response = client.get("/services")

    assert get_response.status_code == 200
    assert len(get_response.json()) == 0

