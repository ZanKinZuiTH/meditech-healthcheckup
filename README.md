# 🏥 MediTech HealthCheckup System

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68.0%2B-green.svg)](https://fastapi.tiangolo.com/)
[![PyQt6](https://img.shields.io/badge/PyQt-6.0%2B-orange.svg)](https://www.riverbankcomputing.com/software/pyqt/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

ระบบบริหารจัดการการตรวจสุขภาพและบันทึกข้อมูลทางการแพทย์ พัฒนาด้วย Python

[English](README_EN.md) | [ภาษาไทย](README.md)

![MediTech HealthCheckup Screenshot](docs/images/screenshot.png)

## 📖 คำอธิบายโปรเจค

MediTech HealthCheckup System เป็นระบบที่พัฒนาขึ้นเพื่อช่วยในการบริหารจัดการงานตรวจสุขภาพและบันทึกข้อมูลทางการแพทย์ โดยใช้เทคโนโลยีที่ทันสมัย:

- **Backend**: พัฒนาด้วย FastAPI ซึ่งเป็น framework ที่มีประสิทธิภาพสูงและรวดเร็ว
- **Frontend**: ใช้ PyQt6 สร้าง Desktop Application ที่ใช้งานง่ายและสวยงาม
- **Database**: PostgreSQL เป็นฐานข้อมูลหลักที่มีความเสถียรและปลอดภัย
- **Architecture**: ใช้ MVVM (Model-View-ViewModel) pattern เพื่อแยกส่วนการทำงานให้ชัดเจน

## ✨ คุณสมบัติหลัก

### 🏥 ระบบตรวจสุขภาพ (Health Checkup)
- จัดการงานตรวจสุขภาพ
  - สร้างและจัดการแพคเกจตรวจสุขภาพ
  - กำหนดรายการตรวจและราคา
  - จัดตารางนัดหมาย
- บันทึกและติดตามผลการตรวจ
  - บันทึกผลตรวจแบบ Real-time
  - ระบบแจ้งเตือนผลตรวจที่ผิดปกติ
  - ติดตามสถานะการตรวจ
- รายงานสรุปผลการตรวจ
  - สร้างรายงานในรูปแบบ PDF
  - กราฟแสดงผลเปรียบเทียบ
  - ส่งออกข้อมูลในรูปแบบต่างๆ
- จัดการข้อมูลบริษัทคู่สัญญา
  - ระบบสมาชิกองค์กร
  - จัดการสิทธิประโยชน์
  - ออกใบแจ้งหนี้อัตโนมัติ

### 📋 ระบบเวชระเบียน (EMR)
- บันทึกประวัติการรักษา
  - ประวัติการเจ็บป่วย
  - ประวัติการแพ้ยา
  - ประวัติครอบครัว
- จัดการข้อมูลผู้ป่วย
  - ข้อมูลส่วนตัว
  - ประวัติการนัดหมาย
  - การติดตามการรักษา
- บันทึกสัญญาณชีพ
  - วัดและบันทึกค่าต่างๆ
  - แจ้งเตือนค่าผิดปกติ
  - แสดงกราฟแนวโน้ม
- ติดตามประวัติการรักษา
  - Timeline การรักษา
  - ประวัติการใช้ยา
  - นัดหมายติดตามผล

## 🎓 สำหรับนักศึกษา

### แนวทางการศึกษาโค้ด
1. เริ่มจากการทำความเข้าใจโครงสร้างโปรเจค:
   - `backend/`: ศึกษา API endpoints และ business logic
   - `frontend/`: เรียนรู้การสร้าง UI และการจัดการ state
   - `Models/`: ศึกษาโครงสร้างข้อมูลและความสัมพันธ์
   - `ViewModels/`: เข้าใจการเชื่อมต่อระหว่าง Model และ View
   - `Services/`: ศึกษาการทำงานของ business services

2. ทำความเข้าใจ Design Patterns ที่ใช้:
   - MVVM Pattern
   - Repository Pattern
   - Factory Pattern
   - Observer Pattern
   - Dependency Injection

3. ศึกษาการใช้เทคโนโลยี:
   - FastAPI: การสร้าง API endpoints
   - PyQt6: การพัฒนา Desktop UI
   - SQLAlchemy: การจัดการฐานข้อมูล
   - Pydantic: การ validate ข้อมูล

### แนวทางการพัฒนาต่อยอด
1. เพิ่มฟีเจอร์ใหม่:
   - ระบบนัดหมายออนไลน์
   - การชำระเงินออนไลน์
   - ระบบแจ้งเตือนผ่าน LINE
   - Mobile Application

2. ปรับปรุงประสิทธิภาพ:
   - เพิ่ม Caching
   - Optimize Database Queries
   - Implement Load Balancing
   - Add Real-time Features

3. เพิ่มความปลอดภัย:
   - Implement 2FA
   - Add Audit Logging
   - Enhance Data Encryption
   - Improve Access Control

4. พัฒนา UI/UX:
   - สร้าง Responsive Design
   - เพิ่ม Dark Mode
   - ปรับปรุง Accessibility
   - สร้าง Interactive Reports

## 📝 ลิขสิทธิ์และการอ้างสิทธิ์

© 2024 BRXG Co. สงวนลิขสิทธิ์

โปรเจค MediTech HealthCheckup System และส่วนประกอบทั้งหมดเป็นลิขสิทธิ์ของ BRXG Co. แต่เพียงผู้เดียว การใช้งาน ทำซ้ำ ดัดแปลง หรือเผยแพร่ส่วนใดส่วนหนึ่งของโปรเจคนี้ จะต้องได้รับอนุญาตเป็นลายลักษณ์อักษรจาก BRXG Co. เท่านั้น

### ติดต่อบริษัท
- Website: https://brxggroup.com
- Facebook: https://www.facebook.com/brxggroup/?locale=th_TH

## 🚀 การติดตั้ง

### ความต้องการของระบบ
- Python 3.9+
- PostgreSQL 13+
- Git

### ขั้นตอนการติดตั้ง

1. Clone repository:
```bash
git clone https://github.com/BRXG/meditech-healthcheckup.git
cd meditech-healthcheckup
```

2. สร้าง virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. ติดตั้ง dependencies:
```bash
pip install -r requirements.txt
```

4. ตั้งค่า environment:
```bash
cp .env.example .env
# แก้ไขไฟล์ .env ตามความเหมาะสม
```

5. รัน Docker:
```bash
docker-compose up -d
```

## 📚 เอกสารประกอบ

- [คู่มือการติดตั้ง](docs/installation.md)
- [คู่มือการพัฒนา](docs/development_guide.md)
- [API Documentation](docs/api/README.md)

## 👥 ทีมพัฒนา

พัฒนาโดย BRXG Co.

## 📞 ติดต่อ

- Website: https://brxggroup.com
- Facebook: https://www.facebook.com/brxggroup/?locale=th_TH

## 🙏 กิตติกรรมประกาศ

ขอขอบคุณ:
- [FastAPI](https://fastapi.tiangolo.com/)
- [PyQt](https://www.riverbankcomputing.com/software/pyqt/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [และอื่นๆ](ACKNOWLEDGMENTS.md) 