# 🏥 MediTech HealthCheckup System

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68.0%2B-green.svg)](https://fastapi.tiangolo.com/)
[![PyQt6](https://img.shields.io/badge/PyQt-6.0%2B-orange.svg)](https://www.riverbankcomputing.com/software/pyqt/)
[![GitHub license](https://img.shields.io/github/license/BRXG/meditech-healthcheckup)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/BRXG/meditech-healthcheckup)](https://github.com/BRXG/meditech-healthcheckup/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/BRXG/meditech-healthcheckup)](https://github.com/BRXG/meditech-healthcheckup/network)
[![GitHub issues](https://img.shields.io/github/issues/BRXG/meditech-healthcheckup)](https://github.com/BRXG/meditech-healthcheckup/issues)

ระบบบริหารจัดการการตรวจสุขภาพและบันทึกข้อมูลทางการแพทย์ พัฒนาด้วย Python

[English](README_EN.md) | [ภาษาไทย](README.md)

![MediTech HealthCheckup Screenshot](docs/images/screenshot.png)

## 📋 สารบัญ

- [ภาพรวมระบบ](#ภาพรวมระบบ)
- [การติดตั้ง](#การติดตั้ง)
- [โครงสร้างโปรเจค](#โครงสร้างโปรเจค)
- [การพัฒนา](#การพัฒนา)
- [การทดสอบ](#การทดสอบ)
- [เอกสารเพิ่มเติม](#เอกสารเพิ่มเติม)

## 🔍 ภาพรวมระบบ

ระบบประกอบด้วย 3 ส่วนหลัก:

1. **Backend (FastAPI)**
   - RESTful API
   - ฐานข้อมูล PostgreSQL
   - ระบบ Authentication
   - การจัดการข้อมูล

2. **Frontend (PyQt6)**
   - UI ที่ใช้งานง่าย
   - การแสดงผลข้อมูล
   - กราฟและรายงาน
   - ระบบแจ้งเตือน

3. **Database**
   - PostgreSQL
   - SQLAlchemy ORM
   - Data Migration
   - Backup System

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

### 🎨 ระบบ UI/UX (User Interface/Experience)
- ธีมและการออกแบบ
  - ธีมสีที่ปรับแต่งได้
  - Dark Mode รองรับการใช้งานในที่มืด
  - การจัดวางที่เป็นระเบียบและใช้งานง่าย
- คอมโพเนนต์พื้นฐาน
  - ปุ่มกดที่ปรับแต่งได้หลายรูปแบบ
  - ฟอร์มกรอกข้อมูลที่ตรวจสอบความถูกต้อง
  - ตารางข้อมูลที่จัดการได้ง่าย
  - Dropdown และ Combo box ที่ใช้งานสะดวก
- การแสดงผลข้อมูล
  - กราฟเส้นแสดงแนวโน้ม
  - กราฟแท่งเปรียบเทียบข้อมูล
  - กราฟวงกลมแสดงสัดส่วน
  - Heat map แสดงความเข้มข้นของข้อมูล
- ความสามารถในการเข้าถึง
  - รองรับการปรับขนาดตัวอักษร
  - โหมดความคมชัดสูง
  - รองรับโปรแกรมอ่านหน้าจอ
  - การนำทางด้วยแป้นพิมพ์
  - รองรับหลายภาษา

### 📊 ระบบรายงาน (Reporting System)
- รายงานผลตรวจสุขภาพ
  - สร้างรายงานแบบ Real-time
  - แสดงผลในรูปแบบตาราง
  - วิเคราะห์ด้วยกราฟหลายรูปแบบ
  - เปรียบเทียบผลกับค่ามาตรฐาน
- การส่งออกรายงาน
  - ส่งออกเป็น PDF แบบกำหนดเองได้
  - ส่งออกเป็น Excel สำหรับวิเคราะห์เพิ่มเติม
  - พิมพ์รายงานโดยตรงจากระบบ
  - บันทึกและแชร์รายงานได้
- การวิเคราะห์ข้อมูล
  - แนวโน้มตามช่วงเวลา
  - การเปรียบเทียบระหว่างกลุ่ม
  - สัดส่วนตามประเภทการตรวจ
  - สถิติและการวิเคราะห์เชิงลึก

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

## 🤝 การมีส่วนร่วมพัฒนา

เรายินดีต้อนรับการมีส่วนร่วมจากชุมชน! หากคุณต้องการมีส่วนร่วมในการพัฒนา:

1. Fork repository
2. สร้าง feature branch (`git checkout -b feature/amazing-feature`)
3. Commit การเปลี่ยนแปลง (`git commit -m 'Add amazing feature'`)
4. Push ไปยัง branch (`git push origin feature/amazing-feature`)
5. เปิด Pull Request

โปรดอ่านรายละเอียดเพิ่มเติมที่ [CONTRIBUTING.md](CONTRIBUTING.md)

## 📝 ลิขสิทธิ์

© 2024 BRXG Co.

โปรเจคนี้เผยแพร่ภายใต้ลิขสิทธิ์ MIT License - ดูรายละเอียดได้ที่ [LICENSE](LICENSE)

## 👥 ทีมพัฒนา

พัฒนาโดย BRXG Co.

## 📞 ติดต่อ

- Website: https://brxggroup.com
- Facebook: https://www.facebook.com/brxggroup/?locale=th_TH
- GitHub Issues: https://github.com/BRXG/meditech-healthcheckup/issues

## 🙏 กิตติกรรมประกาศ

ขอขอบคุณ:
- [FastAPI](https://fastapi.tiangolo.com/)
- [PyQt](https://www.riverbankcomputing.com/software/pyqt/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [และอื่นๆ](ACKNOWLEDGMENTS.md)

## 📁 โครงสร้างโปรเจค

```
meditech-healthcheckup/
├── backend/                 # Backend API
│   ├── app/                # โค้ดหลัก
│   ├── tests/             # Unit Tests
│   └── alembic/           # Database Migrations
├── frontend/               # Frontend Application
│   ├── src/               # Source Code
│   └── tests/             # UI Tests
├── docs/                   # เอกสาร
├── tests/                  # Integration Tests
└── tools/                  # Development Tools
```

## 🛠️ การพัฒนา

### การตั้งค่าสภาพแวดล้อม

1. ติดตั้ง Development Tools:
```bash
pip install -r requirements-dev.txt
```

2. ตั้งค่า Pre-commit:
```bash
pre-commit install
```

### แนวทางการพัฒนา

1. **Backend**
   - ใช้ FastAPI Best Practices
   - มี Type Hints ครบถ้วน
   - เขียน Unit Tests
   - ใช้ Async/Await

2. **Frontend**
   - ใช้ PyQt6 Widgets
   - แยก Business Logic
   - ใช้ Signal/Slot
   - รองรับ Themes

3. **Database**
   - ใช้ Migrations
   - Optimize Queries
   - มี Indexes
   - Backup Strategy

## 🧪 การทดสอบ

ระบบมีการทดสอบครอบคลุมทุกส่วน:

1. **Integration Tests**
```bash
pytest tests/integration/test_system.py -v
```

2. **Frontend Tests**
```bash
pytest frontend/tests/test_ui.py -v
```

3. **Backend Tests**
```bash
pytest backend/tests/test_api.py -v
```

### ส่วนที่ทดสอบ

1. **Workflow ทั้งระบบ**
   - การล็อกอิน
   - การจัดการข้อมูลผู้ป่วย
   - การนัดหมาย
   - การบันทึกผลตรวจ
   - การสร้างรายงาน

2. **UI และการนำทาง**
   - การเปลี่ยนหน้า
   - การใช้แป้นพิมพ์
   - การทำงานของปุ่ม

3. **การจัดการข้อมูล**
   - การบันทึก
   - การอัพเดท
   - การลบ

4. **การจัดการข้อผิดพลาด**
   - การล็อกอินผิดพลาด
   - การส่งข้อมูลไม่ครบ
   - API ไม่ถูกต้อง

5. **ประสิทธิภาพ**
   - การโหลดข้อมูลจำนวนมาก
   - การทำงานพร้อมกัน

6. **การเข้าถึง**
   - ขนาดตัวอักษร
   - โหมดกลางคืน
   - ความคมชัดสูง

## 📚 เอกสารเพิ่มเติม

- [คู่มือการใช้งาน](docs/user_guide/README.md)
- [คู่มือการพัฒนา](docs/development_guide.md)
- [คู่มือการทดสอบ](docs/testing_guide.md)
- [เอกสารการนำเสนอ](docs/presentation.md)

## 🤝 การมีส่วนร่วม

โปรดอ่าน [CONTRIBUTING.md](CONTRIBUTING.md) สำหรับรายละเอียดเพิ่มเติม

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 