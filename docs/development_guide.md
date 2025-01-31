# คู่มือการพัฒนาระบบ MediTech HealthCheckup ด้วย Python

## 🎓 สำหรับนักศึกษา

### การเริ่มต้นศึกษาโค้ด

1. **ทำความเข้าใจพื้นฐาน**
   - Python: ศึกษาการเขียนโปรแกรมเชิงวัตถุ (OOP)
   - SQL: เรียนรู้การออกแบบและจัดการฐานข้อมูล
   - HTTP/REST API: เข้าใจหลักการทำงานของ Web API
   - Git: ศึกษาการใช้ Version Control

2. **ศึกษาโครงสร้างโปรเจค**
   ```
   meditech_healthcheckup/
   ├── backend/                 # ส่วน API และ Business Logic
   ├── frontend/               # ส่วนติดต่อผู้ใช้
   ├── Models/                # โครงสร้างข้อมูล
   ├── ViewModels/           # ตัวเชื่อมระหว่าง Model และ View
   └── Services/            # Business Services
   ```

3. **เริ่มจากส่วนที่เข้าใจง่าย**
   - ศึกษาโมเดลข้อมูลใน `Models/`
   - ดูตัวอย่าง UI ใน `frontend/`
   - อ่าน API Documentation

### ตัวอย่างการพัฒนา

1. **การเพิ่มฟีเจอร์ใหม่**

   ตัวอย่าง: เพิ่มระบบแจ้งเตือนผลตรวจผิดปกติ

   a. สร้างโมเดล:
   ```python
   # Models/alert.py
   from sqlalchemy import Column, Integer, String, ForeignKey
   from sqlalchemy.orm import relationship
   
   class AlertConfig(Base):
       __tablename__ = "alert_configs"
       
       id = Column(Integer, primary_key=True)
       test_name = Column(String)  # ชื่อรายการตรวจ
       min_value = Column(Float)   # ค่าต่ำสุดปกติ
       max_value = Column(Float)   # ค่าสูงสุดปกติ
       
       def is_abnormal(self, value: float) -> bool:
           """ตรวจสอบว่าค่าผิดปกติหรือไม่"""
           return value < self.min_value or value > self.max_value
   ```

   b. สร้าง ViewModel:
   ```python
   # ViewModels/alert_vm.py
   from PyQt6.QtCore import QObject, pyqtSignal
   
   class AlertViewModel(QObject):
       alert_triggered = pyqtSignal(str)  # สัญญาณแจ้งเตือน
       
       def check_result(self, test_name: str, value: float):
           """ตรวจสอบผลและส่งการแจ้งเตือน"""
           config = AlertConfig.get_by_test_name(test_name)
           if config and config.is_abnormal(value):
               message = f"ผลตรวจ {test_name} มีค่า {value} ผิดปกติ"
               self.alert_triggered.emit(message)
   ```

   c. สร้าง View:
   ```python
   # Views/alert_view.py
   from PyQt6.QtWidgets import QWidget, QMessageBox
   
   class AlertView(QWidget):
       def __init__(self, view_model: AlertViewModel):
           super().__init__()
           self.view_model = view_model
           self.setup_ui()
           
       def setup_ui(self):
           # เชื่อมต่อสัญญาณแจ้งเตือน
           self.view_model.alert_triggered.connect(self.show_alert)
           
       def show_alert(self, message: str):
           """แสดงกล่องข้อความแจ้งเตือน"""
           QMessageBox.warning(self, "แจ้งเตือน", message)
   ```

2. **การแก้ไขบัค**

   ตัวอย่าง: แก้ไขการคำนวณอายุผิดพลาด

   ```python
   # ก่อนแก้ไข
   def calculate_age(birthdate: date) -> int:
       today = date.today()
       return today.year - birthdate.year
   
   # หลังแก้ไข
   def calculate_age(birthdate: date) -> int:
       today = date.today()
       age = today.year - birthdate.year
       # ตรวจสอบว่าผ่านวันเกิดปีนี้หรือยัง
       if today.month < birthdate.month or \
          (today.month == birthdate.month and today.day < birthdate.day):
           age -= 1
       return age
   ```

3. **การเพิ่มการทดสอบ**

   ```python
   # tests/test_age_calculation.py
   import pytest
   from datetime import date
   
   def test_calculate_age():
       # เตรียมข้อมูลทดสอบ
       birthdate = date(1990, 6, 15)
       today = date(2024, 1, 1)
       
       # เรียกใช้ฟังก์ชันที่ต้องการทดสอบ
       age = calculate_age(birthdate)
       
       # ตรวจสอบผลลัพธ์
       assert age == 33
   ```

### เทคนิคการเรียนรู้

1. **การอ่านโค้ด**
   - เริ่มจากไฟล์หลัก (`main.py`)
   - ติดตามการทำงานทีละส่วน
   - ใช้ debugger ช่วยดูการทำงาน
   - จดบันทึกสิ่งที่ไม่เข้าใจ

2. **การทดลองแก้ไข**
   - สร้าง branch ใหม่ก่อนแก้ไข
   - เพิ่ม print หรือ logging
   - ทดสอบการทำงานทุกครั้ง
   - ถ้าไม่เวิร์ก ย้อนกลับได้

3. **การขอความช่วยเหลือ**
   - ค้นหาใน Documentation
   - ถามใน Stack Overflow
   - ปรึกษาเพื่อนร่วมทีม
   - สร้าง Issue ใน GitHub

## 1. ภาพรวมของระบบ

ระบบ MediTech HealthCheckup เป็นระบบสำหรับการตรวจสุขภาพและบันทึกข้อมูลทางการแพทย์ ประกอบด้วย 2 ส่วนหลัก:
1. ระบบตรวจสุขภาพ (Health Checkup System)
2. ระบบบันทึกข้อมูลทางการแพทย์ (EMR - Electronic Medical Record)

## 2. เทคโนโลยีที่ใช้ในการพัฒนา

### 2.1 Backend
- Python 3.9+
- FastAPI สำหรับ Web API
- SQLAlchemy สำหรับ ORM
- PostgreSQL สำหรับฐานข้อมูล
- Pydantic สำหรับ Data Validation
- JWT สำหรับ Authentication

### 2.2 Frontend
- Python + PyQt6 สำหรับ Desktop Application
- Qt Designer สำหรับออกแบบ UI
- Matplotlib สำหรับแสดงกราฟ
- ReportLab สำหรับสร้างรายงาน PDF

## 3. โครงสร้างโปรเจค

```
meditech_healthcheckup/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── v1/
│   │   │   │   ├── checkup.py
│   │   │   │   ├── emr.py
│   │   │   │   └── auth.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── security.py
│   │   ├── db/
│   │   │   ├── base.py
│   │   │   └── session.py
│   │   ├── models/
│   │   │   ├── checkup.py
│   │   │   └── emr.py
│   │   └── schemas/
│   │       ├── checkup.py
│   │       └── emr.py
│   └── tests/
├── frontend/
│   ├── app/
│   │   ├── views/
│   │   │   ├── checkup/
│   │   │   └── emr/
│   │   ├── viewmodels/
│   │   │   ├── checkup/
│   │   │   └── emr/
│   │   ├── models/
│   │   └── services/
│   ├── resources/
│   │   ├── ui/
│   │   └── icons/
│   └── tests/
└── docs/
    ├── api/
    ├── database/
    └── user_guide/
```

## 4. ขั้นตอนการพัฒนา

### 4.1 การเตรียมสภาพแวดล้อม

1. ติดตั้ง Python 3.9+
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

2. ติดตั้ง Dependencies
```bash
pip install -r requirements.txt
```

### 4.2 การพัฒนา Backend

1. สร้างโมเดลฐานข้อมูล (models/checkup.py):
```python
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class CheckupJob(Base):
    __tablename__ = "checkup_jobs"
    
    id = Column(Integer, primary_key=True)
    job_number = Column(String)
    company_name = Column(String)
    start_date = Column(DateTime)
    # ... เพิ่มเติมตามต้องการ
```

2. สร้าง Schema (schemas/checkup.py):
```python
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CheckupJobBase(BaseModel):
    job_number: str
    company_name: str
    start_date: datetime
```

3. สร้าง API (api/v1/checkup.py):
```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.checkup import CheckupJobBase

router = APIRouter()

@router.get("/jobs/")
def get_checkup_jobs(db: Session = Depends(get_db)):
    # Logic to get checkup jobs
    pass
```

### 4.3 การพัฒนา Frontend

1. สร้าง UI ด้วย Qt Designer:
- ออกแบบหน้าจอตามตัวอย่างจากไฟล์ XAML เดิม
- แปลง UI เป็น Python code

2. สร้าง ViewModel (viewmodels/checkup.py):
```python
from PyQt6.QtCore import QObject, pyqtSignal
from datetime import datetime

class CheckupSummaryViewModel(QObject):
    data_changed = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self._header_text = "ตารางแสดงผลการตรวจสุขภาพประจำปี"
        self._company_name = ""
        # ... เพิ่มเติมตามต้องการ
```

3. สร้าง View (views/checkup/summary.py):
```python
from PyQt6.QtWidgets import QWidget
from .ui.summary_ui import Ui_Summary

class CheckupSummaryView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Summary()
        self.ui.setupUi(self)
        self.setup_connections()
```

### 4.4 การสร้างรายงาน

1. ใช้ ReportLab สร้างรายงาน PDF:
```python
from reportlab.pdfgen import canvas
from reportlab.lib import colors

def create_checkup_summary_report(data, filename):
    c = canvas.Canvas(filename)
    # Logic to create report
    c.save()
```

## 5. การทดสอบ

### 5.1 Unit Tests
```python
import pytest
from app.models.checkup import CheckupJob

def test_create_checkup_job():
    job = CheckupJob(
        job_number="TEST001",
        company_name="Test Company"
    )
    assert job.job_number == "TEST001"
```

### 5.2 Integration Tests
```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_checkup_jobs():
    response = client.get("/api/v1/checkup/jobs/")
    assert response.status_code == 200
```

## 6. การ Deploy

1. Backend:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

2. Frontend:
```bash
pyinstaller --onefile --windowed frontend/main.py
```

## 7. แนวทางการศึกษาเพิ่มเติม

1. Python
   - [Python Official Documentation](https://docs.python.org/3/)
   - [Real Python Tutorials](https://realpython.com/)

2. FastAPI
   - [FastAPI Documentation](https://fastapi.tiangolo.com/)
   - [SQLAlchemy Tutorial](https://docs.sqlalchemy.org/en/14/tutorial/)

3. PyQt6
   - [PyQt6 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
   - [Qt for Python](https://doc.qt.io/qtforpython-6/)

4. Database
   - [PostgreSQL Tutorial](https://www.postgresqltutorial.com/)
   - [SQLAlchemy ORM](https://docs.sqlalchemy.org/en/14/orm/tutorial.html)

## 8. Best Practices

1. การเขียนโค้ด
   - ใช้ Type Hints
   - ทำ Documentation
   - ใช้ Black formatter
   - ใช้ Flake8 linter

2. การจัดการ Version Control
   - ใช้ Git
   - แยก Branch ตาม Feature
   - ทำ Code Review

3. การทำ Testing
   - Unit Tests ครอบคลุม
   - Integration Tests
   - End-to-End Tests

4. Security
   - ใช้ Environment Variables
   - Implement Authentication
   - Validate Input Data
   - Sanitize Output Data

## 9. ตัวอย่างโค้ดเพิ่มเติม

### 9.1 การเชื่อมต่อฐานข้อมูล
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/db_name"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

### 9.2 การสร้าง API Endpoint
```python
@router.post("/checkup/jobs/", response_model=schemas.CheckupJob)
def create_checkup_job(
    job: schemas.CheckupJobCreate,
    db: Session = Depends(get_db)
):
    db_job = models.CheckupJob(**job.dict())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job
```

### 9.3 การสร้าง GUI Form
```python
class CheckupForm(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Add form elements
        self.job_number = QLineEdit()
        self.company_name = QLineEdit()
        self.date_edit = QDateEdit()
        
        # Add to layout
        layout.addWidget(QLabel("Job Number:"))
        layout.addWidget(self.job_number)
        layout.addWidget(QLabel("Company Name:"))
        layout.addWidget(self.company_name)
        
        self.setLayout(layout)
```

## 10. การแก้ไขปัญหาที่พบบ่อย

1. การติดตั้ง Dependencies
```bash
# หากมีปัญหากับ pip
python -m pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

2. การแก้ไขปัญหา Database Connection
```python
# ตรวจสอบการเชื่อมต่อ
try:
    db.execute("SELECT 1")
except Exception as e:
    print(f"Database connection error: {e}")
```

3. การแก้ไขปัญหา GUI
```python
# Debug PyQt signals
@pyqtSlot()
def on_button_clicked(self):
    try:
        # Your logic here
        pass
    except Exception as e:
        print(f"GUI error: {e}")
```

## 11. การบำรุงรักษาโค้ด

1. การทำ Documentation
```python
def process_checkup_data(data: dict) -> CheckupResult:
    """
    Process checkup data and return results.
    
    Args:
        data (dict): Raw checkup data
        
    Returns:
        CheckupResult: Processed checkup results
        
    Raises:
        ValueError: If data is invalid
    """
    pass
```

2. การทำ Logging
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
```

## 12. แผนการพัฒนาในอนาคต

1. Phase 1: Core Features
   - ระบบพื้นฐาน
   - การจัดการผู้ใช้
   - การบันทึกข้อมูล

2. Phase 2: Advanced Features
   - การสร้างรายงาน
   - การวิเคราะห์ข้อมูล
   - การแสดงกราฟ

3. Phase 3: Integration
   - เชื่อมต่อกับระบบอื่น
   - API Gateway
   - Mobile Application 