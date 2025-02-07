# 🏥 MediTech HealthCheckup System

<div align="center">
  <img src="docs/images/logo.png" alt="MediTech Logo" width="200"/>
  <br/>
  <p>ระบบตรวจสุขภาพและบันทึกข้อมูลทางการแพทย์ที่ทันสมัย</p>
  <p>
    <a href="#-คุณสมบัติ">คุณสมบัติ</a> •
    <a href="#-การติดตั้ง">การติดตั้ง</a> •
    <a href="#-การใช้งาน">การใช้งาน</a> •
    <a href="#-เทคโนโลยี">เทคโนโลยี</a> •
    <a href="#-การพัฒนา">การพัฒนา</a>
  </p>
</div>

## 📋 สารบัญ
- [คุณสมบัติ](#-คุณสมบัติ)
- [การติดตั้ง](#-การติดตั้ง)
- [การใช้งาน](#-การใช้งาน)
- [เทคโนโลยี](#-เทคโนโลยี)
- [การพัฒนา](#-การพัฒนา)
- [แผนพัฒนา](#-แผนพัฒนา)
- [ทีมงาน](#-ทีมงาน)
- [ลิขสิทธิ์](#-ลิขสิทธิ์)

## 📚 สำหรับนักศึกษา

### โครงสร้างโปรเจค
```
meditech/
├── backend/                 # ส่วน Backend API
│   ├── app/                # โค้ดหลัก
│   │   ├── api/           # API Endpoints
│   │   ├── core/          # Core functionality
│   │   ├── db/            # Database
│   │   ├── models/        # Data models
│   │   ├── schemas/       # Pydantic schemas
│   │   └── services/      # Business logic
│   └── tests/             # Unit tests
├── frontend/               # ส่วน Frontend UI
│   ├── src/
│   │   ├── components/    # UI Components
│   │   ├── styles/        # Stylesheets
│   │   ├── utils/         # Utilities
│   │   └── views/         # Page views
│   └── tests/             # UI tests
├── docs/                   # เอกสารประกอบ
│   ├── api/               # API Documentation
│   ├── database/          # Database Docs
│   └── user_guide/        # User Manual
└── tests/                 # Integration Tests
```

### คำอธิบายส่วนประกอบหลัก

#### 1. Backend (FastAPI)
- **api/**: จัดการ API endpoints และ routing
- **core/**: ฟังก์ชันพื้นฐานและการตั้งค่า
- **db/**: จัดการฐานข้อมูลและ migrations
- **models/**: โมเดลข้อมูลสำหรับ SQLAlchemy
- **schemas/**: กำหนดรูปแบบข้อมูล request/response
- **services/**: Business logic และการประมวลผล

#### 2. Frontend (PyQt6)
- **components/**: UI components ที่ใช้ซ้ำได้
- **styles/**: ธีมและการจัดรูปแบบ
- **utils/**: ฟังก์ชันช่วยเหลือ
- **views/**: หน้าจอหลักของแอพ

#### 3. Tests
- **Unit Tests**: ทดสอบฟังก์ชันย่อย
- **Integration Tests**: ทดสอบการทำงานร่วมกัน
- **UI Tests**: ทดสอบส่วนติดต่อผู้ใช้

### แนวทางการศึกษา

1. **เริ่มต้นที่ Backend**
   - ศึกษาโครงสร้าง FastAPI
   - เข้าใจการทำงานของ API
   - เรียนรู้การจัดการฐานข้อมูล

2. **ทำความเข้าใจ Frontend**
   - เรียนรู้ PyQt6 Components
   - ศึกษาการจัดการ State
   - เข้าใจการเชื่อมต่อกับ API

3. **การทดสอบ**
   - เขียน Unit Tests
   - ทดสอบ Integration
   - ตรวจสอบ UI/UX

4. **การ Deploy**
   - ใช้ Docker
   - ตั้งค่า Environment
   - จัดการ Dependencies

## ✨ คุณสมบัติ

### 🤖 AI Diagnosis System
- วินิจฉัยโรคเบื้องต้นด้วย Medical QA Model
- ตรวจจับสัญญาณอันตรายอัตโนมัติ
- ให้คำแนะนำเบื้องต้นและการปฏิบัติตัว
- บันทึกประวัติการวินิจฉัยและติดตามผล

### 👥 การจัดการผู้ป่วย
- ลงทะเบียนและจัดการข้อมูลผู้ป่วย
- ระบบนัดหมายอัจฉริยะ
- ติดตามประวัติการรักษา
- แจ้งเตือนการนัดหมายผ่าน LINE

### 📊 ระบบรายงาน
- รายงานผลตรวจสุขภาพ
- วิเคราะห์แนวโน้มสุขภาพ
- สถิติและกราฟแสดงผล
- ส่งออกรายงานหลายรูปแบบ

## 🚀 การติดตั้ง

### ความต้องการของระบบ
- Python 3.9+
- PostgreSQL 13+
- Git

### ขั้นตอนการติดตั้ง

1. Clone โปรเจค
```bash
git clone https://github.com/brxggroup/meditech.git
cd meditech
```

2. สร้าง Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. ติดตั้ง Dependencies
```bash
pip install -r requirements.txt
```

4. ตั้งค่า Environment Variables
```bash
cp .env.example .env
# แก้ไขค่าใน .env ตามการตั้งค่าของคุณ
```

5. สร้างฐานข้อมูล
```bash
python manage.py init-db
```

## 💻 การใช้งาน

### เริ่มต้นใช้งาน
1. รันเซิร์ฟเวอร์
```bash
python manage.py runserver
```

2. เปิดแอพพลิเคชัน
```bash
python src/main.py
```

### เอกสารประกอบ
- [คู่มือการใช้งาน](docs/user_guide.md)
- [คู่มือการพัฒนา](docs/development_guide.md)
- [API Documentation](docs/api/README.md)

## 🛠 เทคโนโลยี

### Backend
- FastAPI
- SQLAlchemy
- PostgreSQL
- Redis

### Frontend
- PyQt6
- Qt-Material
- Plotly

### AI/ML
- Hugging Face Transformers
- PyTorch
- Medical QA Models

### DevOps
- Docker
- GitHub Actions
- Prometheus
- Grafana

## 👨‍💻 การพัฒนา

### โครงสร้างโปรเจค
```
meditech/
├── backend/          # FastAPI Backend
├── frontend/         # PyQt6 Frontend
├── docs/            # เอกสารประกอบ
├── tests/           # Unit/Integration Tests
└── scripts/         # Utility Scripts
```

### การทดสอบ
```bash
# รันทดสอบทั้งหมด
pytest

# รันทดสอบเฉพาะส่วน
pytest tests/test_api.py
```

### Code Style
```bash
# ตรวจสอบ code style
flake8

# จัดรูปแบบโค้ด
black .
```

## 🔜 แผนพัฒนา

### ระยะสั้น
- Mobile Application
- ระบบแจ้งเตือนผ่าน LINE
- การชำระเงินออนไลน์

### ระยะกลาง
- เพิ่ม Caching
- Optimize Database
- Load Balancing
- Real-time Features

### ระยะยาว
- 2FA Authentication
- Audit Logging
- Enhanced Encryption
- Advanced Access Control

## 👥 ทีมงาน
- Project Manager: [ชื่อ-นามสกุล]
- Lead Developer: [ชื่อ-นามสกุล]
- UI/UX Designer: [ชื่อ-นามสกุล]
- AI Engineer: [ชื่อ-นามสกุล]

## 📝 ลิขสิทธิ์

© 2024 BRXG Co. สงวนลิขสิทธิ์

[MIT License](LICENSE) - ดูรายละเอียดเพิ่มเติมได้ที่ไฟล์ LICENSE

### ติดต่อ
- Website: [https://brxggroup.com](https://brxggroup.com)
- Facebook: [BRXG Group](https://www.facebook.com/brxggroup/?locale=th_TH) 