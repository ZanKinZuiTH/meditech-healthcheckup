# คู่มือการทดสอบระบบ MediTech HealthCheckup

## 📋 ภาพรวมการทดสอบ

ระบบมีการทดสอบครอบคลุม 3 ส่วนหลัก:
1. Integration Tests
2. Frontend Tests
3. Backend Tests

## 🔧 การเตรียมสภาพแวดล้อม

1. ติดตั้ง Dependencies สำหรับการทดสอบ:
```bash
pip install -r requirements.txt
```

2. ตั้งค่าฐานข้อมูลสำหรับทดสอบ:
```bash
# สร้างไฟล์ .env.test
cp .env.example .env.test
# แก้ไขการตั้งค่าให้ใช้ฐานข้อมูลสำหรับทดสอบ
```

## 🧪 การรันทดสอบ

### 1. Integration Tests
```bash
pytest tests/integration/test_system.py -v
```

รายละเอียดการทดสอบ:

#### a. Workflow ทั้งระบบ (`test_full_workflow`)
- การล็อกอิน
- การจัดการข้อมูลผู้ป่วย
- การนัดหมาย
- การบันทึกผลตรวจ
- การสร้างรายงาน
- การตั้งค่าระบบ

#### b. UI และการนำทาง (`test_ui_navigation`)
- การเปลี่ยนหน้า
- การใช้แป้นพิมพ์
- การทำงานของปุ่ม

#### c. การจัดการข้อมูล (`test_data_persistence`)
- การบันทึกข้อมูล
- การอัพเดทข้อมูล
- การลบข้อมูล

#### d. การจัดการข้อผิดพลาด (`test_error_handling`)
- การล็อกอินผิดพลาด
- การส่งข้อมูลไม่ครบ
- การเรียก API ที่ไม่มี

#### e. ประสิทธิภาพ (`test_performance`)
- การโหลดข้อมูลจำนวนมาก
- การทำงานพร้อมกัน

#### f. การเข้าถึง (`test_accessibility`)
- การปรับขนาดตัวอักษร
- โหมดกลางคืน
- โหมดความคมชัดสูง

### 2. Frontend Tests
```bash
pytest frontend/tests/test_ui.py -v
```

รายละเอียดการทดสอบ:
- Components
- Events
- State Management
- UI Rendering
- User Interactions

### 3. Backend Tests
```bash
pytest backend/tests/test_api.py -v
```

รายละเอียดการทดสอบ:
- API Endpoints
- Database Operations
- Authentication
- Error Handling
- Data Validation

## 📊 การวิเคราะห์ผลทดสอบ

### 1. Test Coverage
```bash
pytest --cov=app tests/
```

### 2. Performance Metrics
```bash
pytest --benchmark-only tests/
```

### 3. Error Logs
- ตรวจสอบ logs/test.log
- วิเคราะห์ error patterns
- ติดตามการแก้ไข

## 🔍 การแก้ไขปัญหาที่พบบ่อย

1. **Database Connection Issues**
   - ตรวจสอบการตั้งค่าใน .env.test
   - เช็คสถานะ PostgreSQL
   - ล้างข้อมูล cache

2. **UI Test Failures**
   - ตรวจสอบ screen resolution
   - เช็ค Qt dependencies
   - รีเซ็ต app state

3. **API Test Timeouts**
   - เพิ่ม timeout ใน pytest.ini
   - ลดจำนวน concurrent requests
   - ตรวจสอบ network latency

## ✅ Checklist ก่อน Commit

1. รันทดสอบทั้งหมด:
```bash
pytest
```

2. ตรวจสอบ code coverage:
```bash
pytest --cov=app --cov-report=html
```

3. รัน linter:
```bash
flake8
black .
isort .
```

4. ตรวจสอบ type hints:
```bash
mypy .
```

## 📝 การเขียน Tests ใหม่

### 1. โครงสร้างไฟล์
```
tests/
├── integration/
│   └── test_system.py
├── frontend/
│   └── test_ui.py
└── backend/
    └── test_api.py
```

### 2. Naming Conventions
- ชื่อไฟล์: `test_*.py`
- ชื่อฟังก์ชัน: `test_*`
- ชื่อคลาส: `Test*`

### 3. Best Practices
- ใช้ fixtures
- แยก test cases
- ทำ cleanup
- ใช้ meaningful assertions

## 🔄 Continuous Integration

### 1. GitHub Actions
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Tests
        run: |
          pip install -r requirements.txt
          pytest
```

### 2. การตั้งค่า CI/CD
- Automated testing
- Coverage reports
- Performance benchmarks
- Linting checks

## 📈 การติดตามคุณภาพ

1. **Metrics ที่สำคัญ**
   - Test coverage
   - Pass/fail ratio
   - Performance trends
   - Bug detection rate

2. **การรายงานผล**
   - Daily test reports
   - Weekly coverage analysis
   - Monthly quality metrics

3. **การปรับปรุง**
   - Code review feedback
   - Test optimization
   - Documentation updates 

## 1. การทดสอบระบบ AI

### 1.1 Unit Testing
```python
import pytest
from app.services.ai_diagnosis import AIDiagnosisService

def test_diagnosis_initialization():
    service = AIDiagnosisService()
    assert not service.initialized
    
    await service.initialize()
    assert service.initialized
    assert service.model is not None

def test_diagnosis_result():
    service = AIDiagnosisService()
    result = await service.get_diagnosis({
        "symptoms": ["ไข้", "ไอ"],
        "age": 30,
        "gender": "male"
    })
    
    assert len(result.possible_conditions) > 0
    assert 0 <= result.confidence_score <= 1
    assert result.recommendation
```

### 1.2 Integration Testing
```python
from fastapi.testclient import TestClient
from app.main import app

def test_diagnosis_api():
    client = TestClient(app)
    response = client.post(
        "/api/v1/diagnose",
        json={
            "symptoms": ["ไข้", "ปวดหัว"],
            "age": 25,
            "gender": "female"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "possible_conditions" in data
```

### 1.3 Performance Testing
```python
import time

def test_diagnosis_performance():
    service = AIDiagnosisService()
    
    start_time = time.time()
    result = service.get_diagnosis({"symptoms": ["ไข้"]})
    end_time = time.time()
    
    assert (end_time - start_time) < 2.0  # ต้องใช้เวลาน้อยกว่า 2 วินาที
```

## 2. การทดสอบ Frontend

### 2.1 Component Testing
```python
def test_diagnosis_form(qtbot):
    form = DiagnosisForm()
    qtbot.addWidget(form)
    
    # ทดสอบการกรอกข้อมูล
    qtbot.keyClicks(form.symptom_input, "ไข้")
    qtbot.mouseClick(form.add_button, Qt.LeftButton)
    
    assert "ไข้" in form.get_symptoms()
```

### 2.2 UI Testing
```python
def test_result_display(qtbot):
    display = DiagnosisResult()
    qtbot.addWidget(display)
    
    test_data = {
        "possible_conditions": ["ไข้หวัด", "ภูมิแพ้"],
        "confidence_score": 0.85,
        "recommendation": "ควรพักผ่อน"
    }
    
    display.update_result(test_data)
    assert "ไข้หวัด" in display.conditions_list.text()
```

## 3. การทดสอบ Backend

### 3.1 API Testing
```python
def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_protected_endpoint():
    response = client.get(
        "/api/v1/patients",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
```

### 3.2 Database Testing
```python
def test_patient_crud():
    db = TestingSessionLocal()
    
    # Create
    patient = Patient(name="ทดสอบ", age=30)
    db.add(patient)
    db.commit()
    
    # Read
    saved_patient = db.query(Patient).first()
    assert saved_patient.name == "ทดสอบ"
```

## 4. การทดสอบความปลอดภัย

### 4.1 Authentication Testing
```python
def test_invalid_token():
    response = client.get(
        "/api/v1/patients",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401

def test_expired_token():
    expired_token = create_expired_token()
    response = client.get(
        "/api/v1/patients",
        headers={"Authorization": f"Bearer {expired_token}"}
    )
    assert response.status_code == 401
```

### 4.2 Authorization Testing
```python
def test_user_permissions():
    # ทดสอบผู้ใช้ทั่วไป
    response = client.post(
        "/api/v1/admin/settings",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 403
    
    # ทดสอบผู้ดูแลระบบ
    response = client.post(
        "/api/v1/admin/settings",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
```

## 5. การทดสอบประสิทธิภาพ

### 5.1 Load Testing
```python
from locust import HttpUser, task, between

class MediTechUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def diagnose(self):
        self.client.post(
            "/api/v1/diagnose",
            json={"symptoms": ["ไข้", "ไอ"]}
        )
```

### 5.2 Stress Testing
```python
def test_concurrent_requests():
    async def make_request():
        async with AsyncClient() as client:
            return await client.post("/api/v1/diagnose")
    
    # ทดสอบ 100 requests พร้อมกัน
    tasks = [make_request() for _ in range(100)]
    results = await asyncio.gather(*tasks)
    
    # ตรวจสอบว่าทุก request สำเร็จ
    assert all(r.status_code == 200 for r in results)
```

## 6. การทดสอบการใช้งานจริง

### 6.1 End-to-End Testing
```python
def test_complete_workflow():
    # 1. Login
    token = client.post("/auth/token").json()["access_token"]
    
    # 2. Create patient
    patient = client.post(
        "/api/v1/patients",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "ทดสอบ"}
    ).json()
    
    # 3. Create appointment
    appointment = client.post(
        "/api/v1/appointments",
        headers={"Authorization": f"Bearer {token}"},
        json={"patient_id": patient["id"]}
    ).json()
    
    # 4. Record examination
    examination = client.post(
        "/api/v1/examinations",
        headers={"Authorization": f"Bearer {token}"},
        json={"appointment_id": appointment["id"]}
    ).json()
    
    assert examination["status"] == "completed"
```

### 6.2 Acceptance Testing
```python
def test_user_scenarios():
    # ทดสอบการใช้งานตามสถานการณ์จริง
    scenarios = [
        test_new_patient_registration,
        test_appointment_scheduling,
        test_examination_recording,
        test_report_generation
    ]
    
    for scenario in scenarios:
        scenario()
```

## 7. การรายงานผลการทดสอบ

### 7.1 Test Coverage
```bash
# Generate coverage report
pytest --cov=app --cov-report=html

# View report
open htmlcov/index.html
```

### 7.2 Test Results
```python
def generate_test_report():
    """สร้างรายงานผลการทดสอบ"""
    report = TestReport()
    
    # รวบรวมผลการทดสอบ
    report.add_section("Unit Tests", run_unit_tests())
    report.add_section("Integration Tests", run_integration_tests())
    report.add_section("Performance Tests", run_performance_tests())
    
    # สร้าง PDF report
    report.generate_pdf("test_report.pdf")
```

## 8. การแก้ไขข้อผิดพลาด

### 8.1 Debugging Tools
```python
import pdb
import logging

def debug_diagnosis():
    logging.debug("Starting diagnosis")
    pdb.set_trace()
    
    result = ai_service.diagnose(symptoms)
    logging.debug(f"Diagnosis result: {result}")
    
    return result
```

### 8.2 Error Handling
```python
try:
    result = ai_service.diagnose(symptoms)
except ModelNotFoundError:
    logger.error("AI model not found")
    raise HTTPException(status_code=500, detail="AI service unavailable")
except ValidationError as e:
    logger.error(f"Invalid input: {e}")
    raise HTTPException(status_code=400, detail=str(e)) 