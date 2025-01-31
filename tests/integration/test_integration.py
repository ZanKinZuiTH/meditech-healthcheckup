import pytest
import asyncio
from datetime import datetime, timedelta

from app.api.client import APIClient
from app.ui.main_window import MainWindow
from app.core.config import settings

@pytest.fixture
async def api_client():
    client = APIClient(settings.API_BASE_URL)
    await client.login("test_user", "test_password")
    return client

@pytest.fixture
def main_window(api_client):
    window = MainWindow()
    window.set_api_client(api_client)
    return window

class TestAuthentication:
    @pytest.mark.asyncio
    async def test_login(self, api_client):
        token = await api_client.login("test_user", "test_password")
        assert token is not None
        assert len(token) > 0

    @pytest.mark.asyncio
    async def test_invalid_login(self, api_client):
        with pytest.raises(Exception):
            await api_client.login("invalid_user", "invalid_password")

class TestPatientManagement:
    @pytest.mark.asyncio
    async def test_create_and_fetch_patient(self, api_client, main_window):
        # สร้างข้อมูลผู้ป่วย
        patient_data = {
            "first_name": "สมชาย",
            "last_name": "ใจดี",
            "date_of_birth": "1990-01-01",
            "gender": "male",
            "contact": {
                "phone": "0812345678",
                "email": "somchai@example.com"
            }
        }
        
        # บันทึกข้อมูลผ่าน API
        created_patient = await api_client.create_patient(patient_data)
        assert created_patient["first_name"] == patient_data["first_name"]
        
        # ดึงข้อมูลมาแสดงใน UI
        main_window.patient_view.load_patient(created_patient["id"])
        displayed_data = main_window.patient_view.get_displayed_data()
        assert displayed_data["first_name"] == patient_data["first_name"]

class TestAppointmentManagement:
    @pytest.mark.asyncio
    async def test_create_and_manage_appointment(self, api_client, main_window):
        # สร้างการนัดหมาย
        appointment_data = {
            "patient_id": "test_patient_id",
            "package_id": "test_package_id",
            "datetime": (datetime.now() + timedelta(days=1)).isoformat(),
            "notes": "ตรวจสุขภาพประจำปี"
        }
        
        created_appointment = await api_client.create_appointment(appointment_data)
        assert created_appointment["status"] == "scheduled"
        
        # ตรวจสอบการแสดงผลในปฏิทิน
        main_window.calendar_view.load_appointments()
        calendar_items = main_window.calendar_view.get_appointments()
        assert any(item["id"] == created_appointment["id"] for item in calendar_items)

class TestExaminationRecords:
    @pytest.mark.asyncio
    async def test_record_examination_results(self, api_client, main_window):
        # บันทึกผลการตรวจ
        exam_data = {
            "appointment_id": "test_appointment_id",
            "type": "vital_signs",
            "values": {
                "blood_pressure": "120/80",
                "heart_rate": 72,
                "temperature": 36.5
            },
            "notes": "ผลปกติ"
        }
        
        recorded_exam = await api_client.create_examination(exam_data)
        assert recorded_exam["type"] == exam_data["type"]
        
        # ตรวจสอบการแสดงผลในหน้าประวัติการตรวจ
        main_window.exam_history_view.load_examination(recorded_exam["id"])
        displayed_exam = main_window.exam_history_view.get_displayed_exam()
        assert displayed_exam["values"] == exam_data["values"]

class TestReportGeneration:
    @pytest.mark.asyncio
    async def test_generate_and_download_report(self, api_client, main_window):
        # สร้างรายงาน
        report_data = {
            "patient_id": "test_patient_id",
            "type": "health_summary",
            "date_range": {
                "start": "2024-01-01",
                "end": "2024-01-31"
            },
            "format": "pdf"
        }
        
        generated_report = await api_client.create_health_report(report_data)
        assert "download_url" in generated_report
        
        # ตรวจสอบการดาวน์โหลด
        download_success = main_window.report_view.download_report(generated_report["id"])
        assert download_success

class TestUISync:
    @pytest.mark.asyncio
    async def test_theme_sync(self, api_client, main_window):
        # อัพเดทธีม
        theme_settings = {
            "dark_mode": True,
            "accent_color": "#007AFF"
        }
        
        updated_settings = await api_client.update_theme_settings(theme_settings)
        assert updated_settings["dark_mode"] == theme_settings["dark_mode"]
        
        # ตรวจสอบการอัพเดท UI
        main_window.apply_theme_settings(updated_settings)
        current_theme = main_window.get_current_theme()
        assert current_theme["dark_mode"] == theme_settings["dark_mode"]

    @pytest.mark.asyncio
    async def test_accessibility_sync(self, api_client, main_window):
        # อัพเดทการตั้งค่าการเข้าถึง
        accessibility_settings = {
            "font_size": 16,
            "high_contrast": True,
            "screen_reader": True
        }
        
        updated_settings = await api_client.update_accessibility_settings(accessibility_settings)
        assert updated_settings["font_size"] == accessibility_settings["font_size"]
        
        # ตรวจสอบการอัพเดท UI
        main_window.apply_accessibility_settings(updated_settings)
        current_settings = main_window.get_accessibility_settings()
        assert current_settings["font_size"] == accessibility_settings["font_size"] 