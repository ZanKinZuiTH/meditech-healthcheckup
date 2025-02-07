"""
Test Suite สำหรับ AI Diagnosis System

คำอธิบายสำหรับนักศึกษา:
1. การทดสอบแบ่งเป็น 3 ส่วนหลัก:
   - Unit Tests: ทดสอบการทำงานของแต่ละฟังก์ชัน
   - API Tests: ทดสอบการเรียกใช้ API
   - UI Tests: ทดสอบส่วนติดต่อผู้ใช้

2. หลักการเขียน Test:
   - ใช้ pytest framework
   - แยก test cases ให้ชัดเจน
   - ครอบคลุมทั้ง positive และ negative cases
   - ใช้ fixtures เพื่อเตรียมข้อมูลทดสอบ

3. การรัน Tests:
   pytest tests/test_ai_diagnosis.py -v
"""

import pytest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient

from app.main import app
from app.services.ai_diagnosis import AIDiagnosisService
from app.schemas.diagnosis import DiagnosisInput, DiagnosisResult

@pytest.fixture
def test_diagnosis_input():
    """Fixture สำหรับเตรียมข้อมูลนำเข้าในการทดสอบ
    
    คำอธิบาย:
    - สร้างข้อมูลตัวอย่างสำหรับการวินิจฉัย
    - ใช้ข้อมูลที่ครอบคลุมฟิลด์ที่จำเป็น
    """
    return DiagnosisInput(
        symptoms=["ไข้", "ปวดหัว", "ไอ"],
        age=30,
        gender="male",
        duration_days=2
    )

@pytest.fixture
def mock_ai_service():
    """Fixture สำหรับ mock AI service
    
    คำอธิบาย:
    - ใช้ unittest.mock เพื่อจำลองการทำงานของ AI
    - กำหนดค่าที่คาดว่าจะได้รับจากการวินิจฉัย
    """
    with patch("app.services.ai_diagnosis.AIDiagnosisService") as mock:
        service = Mock()
        service.get_diagnosis.return_value = DiagnosisResult(
            possible_conditions=["ไข้หวัดใหญ่", "ไข้หวัดธรรมดา"],
            confidence_score=0.85,
            recommendation="ควรพักผ่อนให้เพียงพอและดื่มน้ำมากๆ",
            warning_signs=[]
        )
        mock.return_value = service
        yield service

class TestAIDiagnosisService:
    """ทดสอบ AI Diagnosis Service
    
    คำอธิบายสำหรับนักศึกษา:
    - ทดสอบการทำงานของ service โดยตรง
    - ครอบคลุมฟังก์ชันหลักทั้งหมด
    - ตรวจสอบการจัดการข้อผิดพลาด
    """
    
    @pytest.mark.asyncio
    async def test_initialization(self):
        """ทดสอบการเริ่มต้นบริการ
        
        Steps:
        1. สร้าง instance ของ service
        2. ตรวจสอบสถานะเริ่มต้น
        3. เรียกใช้ initialize
        4. ตรวจสอบการโหลดโมเดล
        """
        service = AIDiagnosisService()
        assert not service.initialized
        
        await service.initialize()
        assert service.initialized
        assert service.model is not None
        assert service.tokenizer is not None
    
    @pytest.mark.asyncio
    async def test_diagnosis(self, test_diagnosis_input):
        """ทดสอบการวินิจฉัย
        
        Steps:
        1. เตรียม service
        2. ส่งข้อมูลเข้าวินิจฉัย
        3. ตรวจสอบผลลัพธ์
        """
        service = AIDiagnosisService()
        await service.initialize()
        
        result = await service.get_diagnosis(test_diagnosis_input)
        
        assert isinstance(result, DiagnosisResult)
        assert len(result.possible_conditions) > 0
        assert 0 <= result.confidence_score <= 1
        assert result.recommendation
    
    def test_warning_signs(self):
        """ทดสอบการตรวจจับสัญญาณอันตราย
        
        Steps:
        1. ทดสอบกับอาการปกติ
        2. ทดสอบกับอาการอันตราย
        3. ตรวจสอบการแจ้งเตือน
        """
        service = AIDiagnosisService()
        
        # ทดสอบอาการปกติ
        normal_symptoms = ["ไข้", "ปวดหัว"]
        warnings = service._check_warning_signs(normal_symptoms)
        assert len(warnings) == 0
        
        # ทดสอบอาการอันตราย
        dangerous_symptoms = ["เจ็บหน้าอกรุนแรง", "หายใจลำบาก"]
        warnings = service._check_warning_signs(dangerous_symptoms)
        assert len(warnings) == 2

class TestDiagnosisAPI:
    """ทดสอบ API endpoints
    
    คำอธิบายสำหรับนักศึกษา:
    - ใช้ TestClient จาก FastAPI
    - ทดสอบการเรียก API ในรูปแบบต่างๆ
    - ตรวจสอบ response codes และ data
    """
    
    def test_diagnosis_endpoint(self, mock_ai_service, test_diagnosis_input):
        """ทดสอบ endpoint การวินิจฉัย
        
        Steps:
        1. เตรียม test client
        2. ส่ง request ไปที่ endpoint
        3. ตรวจสอบ response
        """
        client = TestClient(app)
        
        response = client.post(
            "/api/v1/diagnosis/diagnose",
            json=test_diagnosis_input.dict()
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "possible_conditions" in data
        assert "confidence_score" in data
        assert "recommendation" in data
    
    def test_missing_symptoms(self, mock_ai_service):
        """ทดสอบกรณีไม่ระบุอาการ
        
        Steps:
        1. ส่ง request โดยไม่ระบุอาการ
        2. ตรวจสอบ error response
        """
        client = TestClient(app)
        
        response = client.post(
            "/api/v1/diagnosis/diagnose",
            json={"symptoms": []}
        )
        
        assert response.status_code == 422
    
    def test_unauthorized_access(self, mock_ai_service, test_diagnosis_input):
        """ทดสอบกรณีไม่มีสิทธิ์ใช้งาน
        
        Steps:
        1. ส่ง request โดยไม่มี token
        2. ตรวจสอบ error response
        """
        client = TestClient(app)
        
        response = client.post(
            "/api/v1/diagnosis/diagnose",
            json=test_diagnosis_input.dict()
        )
        
        assert response.status_code == 401

class TestDiagnosisUI:
    """ทดสอบส่วน UI
    
    คำอธิบายสำหรับนักศึกษา:
    - ใช้ qtbot สำหรับจำลองการใช้งาน UI
    - ทดสอบการทำงานของ components
    - ตรวจสอบการแสดงผลข้อมูล
    """
    
    def test_input_validation(self, qtbot):
        """ทดสอบการตรวจสอบข้อมูลนำเข้า
        
        Steps:
        1. สร้าง widget สำหรับรับข้อมูล
        2. ทดสอบกรณีไม่กรอกข้อมูล
        3. ทดสอบกรณีกรอกข้อมูลถูกต้อง
        """
        from frontend.src.views.diagnosis_view import SymptomInput
        
        widget = SymptomInput()
        qtbot.addWidget(widget)
        
        # ทดสอบกรณีไม่กรอกข้อมูล
        data = widget.get_input_data()
        assert len(data["symptoms"]) == 0
        
        # ทดสอบกรอกข้อมูล
        widget.symptom_input.setPlainText("ไข้, ปวดหัว")
        data = widget.get_input_data()
        assert len(data["symptoms"]) == 2
        assert "ไข้" in data["symptoms"]
    
    def test_result_display(self, qtbot):
        """ทดสอบการแสดงผลลัพธ์
        
        Steps:
        1. สร้าง widget แสดงผล
        2. ส่งข้อมูลตัวอย่าง
        3. ตรวจสอบการแสดงผล
        """
        from frontend.src.views.diagnosis_view import DiagnosisResult
        
        widget = DiagnosisResult()
        qtbot.addWidget(widget)
        
        test_data = {
            "possible_conditions": ["ไข้หวัด", "ภูมิแพ้"],
            "confidence_score": 0.85,
            "recommendation": "ควรพักผ่อน",
            "warning_signs": ["ควรพบแพทย์ด่วน"]
        }
        
        widget.update_result(test_data)
        
        assert "ไข้หวัด" in widget.conditions_list.text()
        assert "85.0%" in widget.confidence_value.text()
        assert widget.warning_frame.isVisible() 