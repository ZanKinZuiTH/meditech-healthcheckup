import pytest
import asyncio
from PyQt6.QtWidgets import QApplication, QPushButton, QPalette
from PyQt6.QtTest import QTest
from PyQt6.QtCore import Qt

from app.main import MediTechApp
from app.ui.main_window import MainWindow
from app.api.client import APIClient

class TestSystemIntegration:
    """ทดสอบการทำงานร่วมกันของระบบทั้งหมด"""

    @pytest.mark.asyncio
    async def test_full_workflow(self, qapp, api_client, test_data):
        """ทดสอบการทำงานทั้งระบบตั้งแต่ต้นจนจบ"""
        
        # 1. เริ่มต้นแอพพลิเคชัน
        app = MediTechApp(qapp)
        main_window = MainWindow()
        main_window.set_api_client(api_client)
        main_window.show()
        
        # 2. ทดสอบการล็อกอิน
        success = await api_client.login("test_user", "test_password")
        assert success, "ล็อกอินไม่สำเร็จ"
        
        # 3. ทดสอบการเพิ่มผู้ป่วย
        patient_data = test_data["patient"]
        response = await api_client.create_patient(patient_data)
        assert response["first_name"] == patient_data["first_name"]
        patient_id = response["id"]
        
        # 4. ทดสอบการนัดหมาย
        appointment_data = test_data["appointment"]
        appointment_data["patient_id"] = patient_id
        response = await api_client.create_appointment(appointment_data)
        assert response["patient_id"] == patient_id
        appointment_id = response["id"]
        
        # 5. ทดสอบการบันทึกผลตรวจ
        examination_data = test_data["examination"]
        examination_data["appointment_id"] = appointment_id
        response = await api_client.create_examination(examination_data)
        assert response["appointment_id"] == appointment_id
        
        # 6. ทดสอบการสร้างรายงาน
        report_data = test_data["report"]
        report_data["patient_id"] = patient_id
        response = await api_client.create_health_report(report_data)
        assert response["patient_id"] == patient_id
        
        # 7. ทดสอบการตั้งค่าธีม
        theme_data = test_data["theme"]
        response = await api_client.update_theme(theme_data)
        assert response["dark_mode"] == theme_data["dark_mode"]
        
        # 8. ทดสอบการตั้งค่าการเข้าถึง
        accessibility_data = test_data["accessibility"]
        response = await api_client.update_accessibility(accessibility_data)
        assert response["font_size"] == accessibility_data["font_size"]

    def test_ui_navigation(self, main_window):
        """ทดสอบการนำทางในส่วน UI"""
        
        # 1. ทดสอบการเปลี่ยนหน้า
        pages = ["patients", "appointments", "examinations", "reports", "settings"]
        for page in pages:
            main_window.show_page(page)
            assert main_window.current_page == page
        
        # 2. ทดสอบการใช้แป้นพิมพ์
        QTest.keyClick(main_window, Qt.Key.Key_Tab)
        assert main_window.focusWidget() is not None
        
        # 3. ทดสอบการคลิกปุ่มต่างๆ
        buttons = main_window.findChildren(QPushButton)
        for button in buttons:
            if button.isEnabled():
                QTest.mouseClick(button, Qt.MouseButton.LeftButton)

    @pytest.mark.asyncio
    async def test_data_persistence(self, api_client, test_data):
        """ทดสอบการเก็บข้อมูลและการดึงข้อมูล"""
        
        # 1. ทดสอบการบันทึกข้อมูลผู้ป่วย
        patient_data = test_data["patient"]
        created_patient = await api_client.create_patient(patient_data)
        retrieved_patient = await api_client.get_patient(created_patient["id"])
        assert created_patient == retrieved_patient
        
        # 2. ทดสอบการอัพเดทข้อมูล
        updated_data = patient_data.copy()
        updated_data["first_name"] = "ทดสอบ"
        updated_patient = await api_client.update_patient(created_patient["id"], updated_data)
        assert updated_patient["first_name"] == "ทดสอบ"
        
        # 3. ทดสอบการลบข้อมูล
        await api_client.delete_patient(created_patient["id"])
        with pytest.raises(Exception):
            await api_client.get_patient(created_patient["id"])

    @pytest.mark.asyncio
    async def test_error_handling(self, main_window, api_client):
        """ทดสอบการจัดการข้อผิดพลาด"""
        
        # 1. ทดสอบการล็อกอินด้วยข้อมูลไม่ถูกต้อง
        with pytest.raises(Exception):
            await api_client.login("wrong_user", "wrong_pass")
        
        # 2. ทดสอบการส่งข้อมูลไม่ครบ
        with pytest.raises(Exception):
            await api_client.create_patient({})
        
        # 3. ทดสอบการเรียก API ที่ไม่มีอยู่
        with pytest.raises(Exception):
            await api_client.get("/not_exist")

    @pytest.mark.asyncio
    async def test_performance(self, api_client):
        """ทดสอบประสิทธิภาพของระบบ"""
        
        # 1. ทดสอบการโหลดข้อมูลจำนวนมาก
        patients = await api_client.get_patients(limit=1000)
        assert len(patients) <= 1000
        
        # 2. ทดสอบการทำงานพร้อมกัน
        tasks = []
        for _ in range(10):
            tasks.append(api_client.get_patients())
        results = await asyncio.gather(*tasks)
        assert all(isinstance(r, list) for r in results)

    def test_accessibility(self, main_window):
        """ทดสอบการเข้าถึงระบบ"""
        
        # 1. ทดสอบการเปลี่ยนขนาดตัวอักษร
        main_window.accessibility_manager.change_font_size(16)
        assert main_window.font().pointSize() == 16
        
        # 2. ทดสอบโหมดกลางคืน
        main_window.accessibility_manager.toggle_dark_mode(True)
        assert main_window.palette().color(QPalette.ColorRole.Window).name() in ["#2d2d2d", "#1e1e1e"]
        
        # 3. ทดสอบความคมชัดสูง
        main_window.accessibility_manager.toggle_high_contrast(True)
        assert main_window.palette().color(QPalette.ColorRole.WindowText).name() == "#ffffff" 