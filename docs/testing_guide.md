# คู่มือการทดสอบระบบ MediTech HealthCheckup

## สารบัญ
1. [บทนำ](#บทนำ)
2. [โครงสร้างการทดสอบ](#โครงสร้างการทดสอบ)
3. [การติดตั้งเครื่องมือ](#การติดตั้งเครื่องมือ)
4. [การทดสอบ Backend](#การทดสอบ-backend)
5. [การทดสอบ Frontend](#การทดสอบ-frontend)
6. [การทดสอบ Integration](#การทดสอบ-integration)
7. [แนวทางการพัฒนาต่อยอด](#แนวทางการพัฒนาต่อยอด)

## บทนำ

คู่มือนี้จะแนะนำวิธีการทดสอบระบบ MediTech HealthCheckup ทั้งในส่วนของ Backend, Frontend และการทดสอบแบบ Integration โดยใช้ pytest เป็นเครื่องมือหลักในการทดสอบ

## โครงสร้างการทดสอบ

โครงสร้างของการทดสอบแบ่งออกเป็น 3 ส่วนหลัก:

```
project/
├── backend/
│   └── tests/
│       ├── conftest.py
│       └── test_api.py
├── frontend/
│   └── tests/
│       ├── conftest.py
│       └── test_ui.py
└── tests/
    └── integration/
        ├── conftest.py
        └── test_integration.py
```

## การติดตั้งเครื่องมือ

1. ติดตั้ง Python (เวอร์ชัน 3.8 ขึ้นไป)
2. ติดตั้ง pytest และ plugins ที่จำเป็น:

```bash
pip install pytest pytest-asyncio pytest-qt pytest-cov
```

## การทดสอบ Backend

### การตั้งค่าฐานข้อมูลสำหรับการทดสอบ

ไฟล์ `backend/tests/conftest.py` จะกำหนดค่าเริ่มต้นสำหรับการทดสอบ:

```python
# สร้าง test database
SQLALCHEMY_DATABASE_URL = "sqlite://"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
```

### การทดสอบ API Endpoints

ตัวอย่างการทดสอบ API endpoint ใน `backend/tests/test_api.py`:

```python
def test_create_patient(self, auth_headers):
    data = {
        "first_name": "สมชาย",
        "last_name": "ใจดี",
        "date_of_birth": "1990-01-01",
        "gender": "male",
        "contact": {
            "phone": "0812345678",
            "email": "somchai@example.com"
        }
    }
    response = client.post("/patients", json=data, headers=auth_headers)
    assert response.status_code == 200
    result = response.json()
    assert result["first_name"] == data["first_name"]
```

### การรันการทดสอบ Backend

```bash
cd backend
pytest tests/ -v
```

## การทดสอบ Frontend

### การตั้งค่า QApplication

ไฟล์ `frontend/tests/conftest.py` จะกำหนดค่าเริ่มต้นสำหรับการทดสอบ UI:

```python
@pytest.fixture(scope="session")
def qapp():
    app = QApplication(sys.argv)
    yield app
    app.quit()
```

### การทดสอบ UI Components

ตัวอย่างการทดสอบ UI component ใน `frontend/tests/test_ui.py`:

```python
def test_base_button(self, app):
    button = BaseButton("Test Button")
    assert button.text() == "Test Button"
    assert button.isEnabled()
```

### การรันการทดสอบ Frontend

```bash
cd frontend
pytest tests/ -v
```

## การทดสอบ Integration

### การตั้งค่าการเชื่อมต่อ

ไฟล์ `tests/integration/conftest.py` จะกำหนดค่าเริ่มต้นสำหรับการทดสอบการเชื่อมต่อ:

```python
@pytest.fixture
async def api_client():
    client = APIClient(settings.API_BASE_URL)
    await client.login("test_user", "test_password")
    return client
```

### การทดสอบการทำงานร่วมกัน

ตัวอย่างการทดสอบการทำงานร่วมกันใน `tests/integration/test_integration.py`:

```python
async def test_create_and_fetch_patient(self, api_client, main_window):
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
    
    created_patient = await api_client.create_patient(patient_data)
    assert created_patient["first_name"] == patient_data["first_name"]
    
    main_window.patient_view.load_patient(created_patient["id"])
    displayed_data = main_window.patient_view.get_displayed_data()
    assert displayed_data["first_name"] == patient_data["first_name"]
```

### การรันการทดสอบ Integration

```bash
pytest tests/integration/ -v
```

## แนวทางการพัฒนาต่อยอด

### 1. เพิ่มการทดสอบ Edge Cases

- ทดสอบกรณีข้อมูลไม่ถูกต้อง
- ทดสอบกรณีการเชื่อมต่อล้มเหลว
- ทดสอบกรณีข้อมูลมีขนาดใหญ่

### 2. เพิ่มการทดสอบ Performance

```python
@pytest.mark.benchmark
def test_patient_list_performance(self, client):
    start_time = time.time()
    response = client.get("/patients")
    end_time = time.time()
    assert (end_time - start_time) < 1.0  # ต้องใช้เวลาน้อยกว่า 1 วินาที
```

### 3. เพิ่มการทดสอบ Security

```python
def test_unauthorized_access(self, client):
    response = client.get("/patients")
    assert response.status_code == 401
```

### 4. เพิ่มการทดสอบ Accessibility

```python
def test_screen_reader_compatibility(self, main_window):
    assert main_window.accessibility_manager.is_screen_reader_compatible()
```

### 5. เพิ่มการทดสอบ Localization

```python
def test_language_switch(self, main_window):
    main_window.change_language("th")
    assert main_window.windowTitle() == "ระบบตรวจสุขภาพ MediTech"
```

### 6. การใช้ Mock Objects

```python
@pytest.fixture
def mock_api_client(mocker):
    return mocker.patch("app.api.client.APIClient")
```

### 7. การทดสอบ Database Migrations

```python
def test_database_migration(self, test_db):
    from alembic.command import upgrade
    upgrade(test_db, "head")
    assert test_db.get_current_revision() == "latest_revision_id"
```

### 8. การวัด Code Coverage

รันการทดสอบพร้อมวัด coverage:

```bash
pytest --cov=app tests/
```

### 9. การทดสอบ Concurrent Access

```python
@pytest.mark.asyncio
async def test_concurrent_appointments(self, api_client):
    tasks = []
    for _ in range(10):
        tasks.append(api_client.create_appointment(appointment_data))
    results = await asyncio.gather(*tasks)
    assert len(results) == 10
```

### 10. การทดสอบ UI Responsiveness

```python
def test_window_resize(self, main_window):
    main_window.resize(800, 600)
    assert main_window.patient_view.is_responsive()
```

## เทคนิคการทดสอบเพิ่มเติม

1. **การใช้ Parameterized Tests**
```python
@pytest.mark.parametrize("input,expected", [
    ("สมชาย", True),
    ("", False),
    ("123", False)
])
def test_validate_name(self, input, expected):
    assert validate_name(input) == expected
```

2. **การทดสอบ Error Handling**
```python
def test_error_display(self, main_window):
    main_window.show_error("Test Error")
    error_dialog = main_window.findChild(QErrorMessage)
    assert error_dialog is not None
    assert error_dialog.isVisible()
```

3. **การทดสอบ State Management**
```python
def test_appointment_state_changes(self, main_window):
    appointment_view = main_window.appointment_view
    appointment_view.create_appointment()
    assert appointment_view.get_state() == "creating"
    appointment_view.save_appointment()
    assert appointment_view.get_state() == "viewing"
```

## คำแนะนำในการเขียน Test Cases ที่ดี

1. **ใช้ชื่อที่สื่อความหมาย**
```python
# ไม่ดี
def test_1(self):
    pass

# ดี
def test_patient_creation_with_valid_data(self):
    pass
```

2. **แยก Test Cases ให้เป็นหมวดหมู่**
```python
class TestPatientManagement:
    class TestCreation:
        def test_valid_data(self):
            pass
        
        def test_invalid_data(self):
            pass
    
    class TestUpdate:
        def test_valid_update(self):
            pass
```

3. **ใช้ Fixtures อย่างเหมาะสม**
```python
@pytest.fixture
def sample_patient_data():
    return {
        "first_name": "สมชาย",
        "last_name": "ใจดี",
        "age": 30
    }

def test_create_patient(self, sample_patient_data):
    result = create_patient(sample_patient_data)
    assert result.success
```

## การ Debug Tests

1. **ใช้ pytest -v -s**
```bash
pytest -v -s tests/  # แสดงผล print statements
```

2. **ใช้ pdb**
```python
def test_complex_scenario(self):
    import pdb; pdb.set_trace()
    # ทดสอบต่อ
```

3. **ใช้ pytest --pdb**
```bash
pytest --pdb  # หยุดทันทีที่ test fail
```

## Best Practices

1. **รักษาความเป็นอิสระของ Tests**
- แต่ละ test ควรทำงานได้โดยไม่ขึ้นกับ test อื่น
- ใช้ fixtures ในการ setup และ teardown

2. **ทดสอบให้ครอบคลุม**
- ทดสอบทั้ง positive และ negative cases
- ทดสอบ edge cases
- ทดสอบ error handling

3. **รักษาความเร็วของ Tests**
- ใช้ mock objects เมื่อเหมาะสม
- หลีกเลี่ยงการทำงานที่ใช้เวลานานโดยไม่จำเป็น

4. **เขียน Tests ที่อ่านง่าย**
- ใช้ชื่อที่สื่อความหมาย
- แบ่ง tests เป็นหมวดหมู่
- ใช้ comments อธิบายเมื่อจำเป็น 