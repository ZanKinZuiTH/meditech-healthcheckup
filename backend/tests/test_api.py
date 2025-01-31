import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta

from app.main import app
from app.core.config import settings
from app.tests.utils.utils import get_test_db, get_test_token

client = TestClient(app)

@pytest.fixture
def test_db():
    return get_test_db()

@pytest.fixture
def auth_headers():
    token = get_test_token()
    return {"Authorization": f"Bearer {token}"}

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

class TestPatients:
    def test_create_patient(self, auth_headers):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": "1990-01-01",
            "gender": "male",
            "contact": {
                "phone": "0812345678",
                "email": "john@example.com"
            }
        }
        response = client.post("/patients", json=data, headers=auth_headers)
        assert response.status_code == 200
        result = response.json()
        assert result["first_name"] == data["first_name"]
        assert result["last_name"] == data["last_name"]

    def test_get_patients(self, auth_headers):
        response = client.get("/patients", headers=auth_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

class TestAppointments:
    def test_create_appointment(self, auth_headers):
        data = {
            "patient_id": "123",
            "package_id": "456",
            "datetime": (datetime.now() + timedelta(days=1)).isoformat(),
            "notes": "Test appointment"
        }
        response = client.post("/appointments", json=data, headers=auth_headers)
        assert response.status_code == 200
        result = response.json()
        assert result["patient_id"] == data["patient_id"]
        assert result["status"] == "scheduled"

    def test_get_appointments(self, auth_headers):
        response = client.get("/appointments", headers=auth_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

class TestExaminations:
    def test_create_examination(self, auth_headers):
        data = {
            "appointment_id": "789",
            "type": "blood_pressure",
            "values": {
                "systolic": 120,
                "diastolic": 80
            },
            "notes": "Normal range"
        }
        response = client.post("/examinations", json=data, headers=auth_headers)
        assert response.status_code == 200
        result = response.json()
        assert result["type"] == data["type"]
        assert result["values"] == data["values"]

    def test_get_examinations(self, auth_headers):
        response = client.get("/examinations", headers=auth_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

class TestReports:
    def test_create_health_report(self, auth_headers):
        data = {
            "patient_id": "123",
            "type": "comprehensive",
            "date_range": {
                "start": "2024-01-01",
                "end": "2024-01-31"
            },
            "format": "pdf"
        }
        response = client.post("/reports/health", json=data, headers=auth_headers)
        assert response.status_code == 200
        result = response.json()
        assert result["patient_id"] == data["patient_id"]
        assert result["type"] == data["type"]
        assert "download_url" in result

    def test_get_health_reports(self, auth_headers):
        response = client.get("/reports/health", headers=auth_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

class TestUISettings:
    def test_get_themes(self, auth_headers):
        response = client.get("/settings/themes", headers=auth_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_update_accessibility(self, auth_headers):
        data = {
            "font_size": 16,
            "high_contrast": True,
            "dark_mode": True,
            "screen_reader": False
        }
        response = client.put("/settings/accessibility", json=data, headers=auth_headers)
        assert response.status_code == 200
        result = response.json()
        assert result["font_size"] == data["font_size"]
        assert result["high_contrast"] == data["high_contrast"] 