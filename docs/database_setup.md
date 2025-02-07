# คู่มือการตั้งค่าฐานข้อมูลและการเชื่อมต่อ

## 1. การติดตั้งฐานข้อมูล PostgreSQL

### 1.1 Windows
1. ดาวน์โหลด PostgreSQL จาก https://www.postgresql.org/download/windows/
2. ติดตั้งโปรแกรมโดยเลือกคอมโพเนนต์:
   - PostgreSQL Server
   - pgAdmin 4
   - Command Line Tools
3. กำหนดรหัสผ่าน superuser และพอร์ต (ค่าเริ่มต้น 5432)

### 1.2 Linux (Ubuntu)
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### 1.3 macOS
```bash
brew install postgresql
brew services start postgresql
```

## 2. การสร้างฐานข้อมูล

### 2.1 ใช้ pgAdmin 4
1. เปิด pgAdmin 4
2. คลิกขวาที่ Databases > Create > Database
3. ตั้งชื่อ: meditech
4. กำหนด Owner: postgres

### 2.2 ใช้ Command Line
```bash
# เข้าสู่ PostgreSQL shell
psql -U postgres

# สร้างฐานข้อมูล
CREATE DATABASE meditech;

# ตรวจสอบการสร้าง
\l
```

## 3. การตั้งค่าการเชื่อมต่อ

### 3.1 ไฟล์ .env
สร้างไฟล์ `.env` ในโฟลเดอร์หลักของโปรเจค:
```
DB_CONNECTION=postgresql
DB_HOST=localhost
DB_PORT=5432
DB_DATABASE=meditech
DB_USERNAME=postgres
DB_PASSWORD=your_password
```

### 3.2 ตั้งค่า SQLAlchemy
ไฟล์ `backend/app/core/config.py`:
```python
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.DB_USERNAME}:"
    f"{settings.DB_PASSWORD}@{settings.DB_HOST}:"
    f"{settings.DB_PORT}/{settings.DB_DATABASE}"
)
```

## 4. การ Migrate ฐานข้อมูล

### 4.1 สร้าง Migration
```bash
# สร้าง migration ใหม่
alembic revision --autogenerate -m "initial migration"

# รัน migration
alembic upgrade head
```

### 4.2 ตรวจสอบสถานะ
```bash
# ดูประวัติ migration
alembic history

# ดูสถานะปัจจุบัน
alembic current
```

## 5. การทดสอบการเชื่อมต่อ

### 5.1 ทดสอบผ่าน Python Shell
```python
from app.db.session import SessionLocal

db = SessionLocal()
try:
    # ทดสอบการเชื่อมต่อ
    db.execute("SELECT 1")
    print("เชื่อมต่อสำเร็จ!")
except Exception as e:
    print(f"เกิดข้อผิดพลาด: {e}")
finally:
    db.close()
```

### 5.2 ทดสอบผ่าน API
```bash
# รัน server
uvicorn app.main:app --reload

# ทดสอบ health check endpoint
curl http://localhost:8000/health
```

## 6. การแก้ไขปัญหาที่พบบ่อย

### 6.1 ปัญหาการเชื่อมต่อ
1. ตรวจสอบ PostgreSQL service กำลังทำงาน
2. ยืนยันพอร์ตและ credentials ถูกต้อง
3. ตรวจสอบ firewall อนุญาตการเชื่อมต่อ

### 6.2 ปัญหา Migration
1. ล้าง cache: `alembic stamp head`
2. รีเซ็ต migration: `alembic downgrade base`
3. สร้าง migration ใหม่

## 7. การสำรองข้อมูล

### 7.1 Backup Database
```bash
# Backup
pg_dump -U postgres meditech > backup.sql

# Restore
psql -U postgres meditech < backup.sql
```

### 7.2 Automated Backup
สร้างไฟล์ `backup.sh`:
```bash
#!/bin/bash
BACKUP_DIR="/path/to/backups"
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump -U postgres meditech > "$BACKUP_DIR/backup_$DATE.sql"
```

## 8. การตั้งค่าความปลอดภัย

### 8.1 SSL/TLS
1. เปิดใช้งาน SSL ใน postgresql.conf
2. กำหนดค่าในไฟล์ .env:
```
DB_SSL_MODE=require
DB_SSL_CERT=/path/to/cert
```

### 8.2 Firewall Rules
```bash
# อนุญาตเฉพาะ IP ที่กำหนด
sudo ufw allow from 192.168.1.0/24 to any port 5432
```

## 9. การ Monitor ฐานข้อมูล

### 9.1 pgAdmin Monitoring
1. Server Statistics
2. Activity Monitor
3. Log Files

### 9.2 Prometheus + Grafana
1. ติดตั้ง postgres_exporter
2. กำหนดค่า prometheus.yml
3. สร้าง dashboard ใน Grafana 