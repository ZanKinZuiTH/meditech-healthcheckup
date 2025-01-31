import sys
import pytest
from PyQt6.QtWidgets import QApplication

from app.api.client import APIClient
from app.ui.main_window import MainWindow
from app.core.config import settings

@pytest.fixture(scope="session")
def qapp():
    app = QApplication(sys.argv)
    yield app
    app.quit()

@pytest.fixture
async def api_client():
    client = APIClient(settings.API_BASE_URL)
    await client.login("test_user", "test_password")
    return client

@pytest.fixture
def main_window(qapp, api_client):
    window = MainWindow()
    window.set_api_client(api_client)
    window.show()
    return window

@pytest.fixture
def test_data():
    return {
        "patient": {
            "first_name": "สมชาย",
            "last_name": "ใจดี",
            "date_of_birth": "1990-01-01",
            "gender": "male",
            "contact": {
                "phone": "0812345678",
                "email": "somchai@example.com"
            }
        },
        "appointment": {
            "patient_id": "test_patient_id",
            "package_id": "test_package_id",
            "datetime": "2024-02-01T10:00:00",
            "notes": "ตรวจสุขภาพประจำปี"
        },
        "examination": {
            "appointment_id": "test_appointment_id",
            "type": "vital_signs",
            "values": {
                "blood_pressure": "120/80",
                "heart_rate": 72,
                "temperature": 36.5
            },
            "notes": "ผลปกติ"
        },
        "report": {
            "patient_id": "test_patient_id",
            "type": "health_summary",
            "date_range": {
                "start": "2024-01-01",
                "end": "2024-01-31"
            },
            "format": "pdf"
        },
        "theme": {
            "dark_mode": True,
            "accent_color": "#007AFF"
        },
        "accessibility": {
            "font_size": 16,
            "high_contrast": True,
            "screen_reader": True
        }
    } 