# คู่มือการทดสอบ MediTech HealthCheckup System

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