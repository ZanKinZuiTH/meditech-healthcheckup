# คู่มือการติดตั้ง MediTech HealthCheckup System

## 📋 ความต้องการของระบบ

### 1. ฮาร์ดแวร์
- CPU: Intel Core i5 หรือสูงกว่า
- RAM: 8GB ขึ้นไป
- พื้นที่ว่าง: 20GB ขึ้นไป
- การ์ดจอ: รองรับ OpenGL 2.0

### 2. ซอฟต์แวร์
- Windows 10/11 หรือ Linux (Ubuntu 20.04+)
- Python 3.8 หรือสูงกว่า
- PostgreSQL 12 หรือสูงกว่า
- Git

### 3. การเชื่อมต่อ
- อินเทอร์เน็ตความเร็ว 10Mbps ขึ้นไป
- พอร์ตที่ต้องเปิด: 80, 443, 5432

## 🚀 ขั้นตอนการติดตั้ง

### 1. การเตรียมระบบ

#### a. ติดตั้ง Python
```bash
# Windows
# ดาวน์โหลดและติดตั้งจาก python.org

# Linux
sudo apt update
sudo apt install python3.8 python3.8-venv python3-pip
```

#### b. ติดตั้ง PostgreSQL
```bash
# Windows
# ดาวน์โหลดและติดตั้งจาก postgresql.org

# Linux
sudo apt install postgresql postgresql-contrib
```

#### c. ติดตั้ง Git
```bash
# Windows
# ดาวน์โหลดและติดตั้งจาก git-scm.com

# Linux
sudo apt install git
```

### 2. การตั้งค่าฐานข้อมูล

#### a. สร้างฐานข้อมูล
```sql
CREATE DATABASE meditech;
CREATE USER meditech_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE meditech TO meditech_user;
```

#### b. ตั้งค่าการเข้าถึง
```bash
# แก้ไขไฟล์ pg_hba.conf
host    meditech        meditech_user    127.0.0.1/32    md5
```

### 3. การติดตั้งแอพพลิเคชัน

#### a. Clone Repository
```bash
git clone https://github.com/your-org/meditech.git
cd meditech
```

#### b. สร้าง Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux
python3 -m venv venv
source venv/bin/activate
```

#### c. ติดตั้ง Dependencies
```bash
pip install -r requirements.txt
```

#### d. ตั้งค่า Environment Variables
```bash
# สร้างไฟล์ .env
cp .env.example .env

# แก้ไขการตั้งค่าใน .env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=meditech
DB_USER=meditech_user
DB_PASSWORD=your_password
```

### 4. การ Initialize ระบบ

#### a. รัน Database Migrations
```bash
alembic upgrade head
```

#### b. โหลดข้อมูลเริ่มต้น
```bash
python scripts/load_initial_data.py
```

#### c. สร้าง Admin User
```bash
python scripts/create_admin.py
```

## 🔧 การตั้งค่าระบบ

### 1. การตั้งค่า Backend

#### a. การตั้งค่า API
```python
# config/api.py
API_HOST = "0.0.0.0"
API_PORT = 8000
DEBUG = False
```

#### b. การตั้งค่า Security
```python
# config/security.py
SECRET_KEY = "your-secret-key"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

### 2. การตั้งค่า Frontend

#### a. การตั้งค่า UI
```python
# config/ui.py
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
THEME = "light"
```

#### b. การตั้งค่า API Connection
```python
# config/connection.py
API_BASE_URL = "http://localhost:8000"
TIMEOUT = 30
```

## 🚀 การรันระบบ

### 1. รัน Backend
```bash
# Development
uvicorn backend.main:app --reload

# Production
gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### 2. รัน Frontend
```bash
# Development
python frontend/main.py

# Production
pyinstaller frontend/main.py
```

## 📦 การ Deploy

### 1. การ Deploy Backend

#### a. ใช้ Docker
```bash
# Build image
docker build -t meditech-api .

# Run container
docker run -d -p 8000:8000 meditech-api
```

#### b. ใช้ Docker Compose
```yaml
version: '3'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
  db:
    image: postgres:12
    environment:
      POSTGRES_DB: meditech
      POSTGRES_USER: meditech_user
      POSTGRES_PASSWORD: your_password
```

### 2. การ Deploy Frontend

#### a. สร้าง Executable
```bash
pyinstaller --onefile --windowed frontend/main.py
```

#### b. สร้าง Installer
```bash
# ใช้ Inno Setup (Windows)
iscc setup.iss
```

## 🔒 การตั้งค่าความปลอดภัย

### 1. SSL/TLS

#### a. สร้าง Certificate
```bash
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

#### b. ตั้งค่า HTTPS
```python
# main.py
ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.load_cert_chain('cert.pem', 'key.pem')
```

### 2. Firewall

#### a. UFW (Linux)
```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 5432/tcp
```

#### b. Windows Firewall
```powershell
New-NetFirewallRule -DisplayName "MediTech API" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 8000
```

## 🔄 การอัพเดทระบบ

### 1. การอัพเดท Backend

#### a. อัพเดท Code
```bash
git pull origin main
pip install -r requirements.txt
alembic upgrade head
```

#### b. Restart Services
```bash
sudo systemctl restart meditech-api
```

### 2. การอัพเดท Frontend

#### a. อัพเดท Application
```bash
# ดาวน์โหลด update
wget https://meditech.com/updates/latest.exe

# ติดตั้ง update
./latest.exe
```

## 🔍 การแก้ไขปัญหา

### 1. ปัญหาการติดตั้ง

#### a. Database Connection
```bash
# ตรวจสอบ PostgreSQL service
sudo systemctl status postgresql

# ตรวจสอบ connection
psql -h localhost -U meditech_user -d meditech
```

#### b. Dependencies
```bash
# ตรวจสอบ versions
pip freeze

# ติดตั้ง dependencies ที่หายไป
pip install -r requirements.txt
```

### 2. ปัญหาการรัน

#### a. Backend Issues
```bash
# ตรวจสอบ logs
tail -f logs/api.log

# ตรวจสอบ port
netstat -tulpn | grep 8000
```

#### b. Frontend Issues
```bash
# ตรวจสอบ error logs
cat logs/frontend.log

# รีเซ็ต settings
rm -rf ~/.meditech/settings.json
```

## 📝 การบำรุงรักษา

### 1. การ Backup

#### a. Database Backup
```bash
# Backup
pg_dump meditech > backup.sql

# Restore
psql meditech < backup.sql
```

#### b. File Backup
```bash
# Backup uploads
tar -czf uploads.tar.gz uploads/

# Backup configs
cp .env .env.backup
```

### 2. การ Monitoring

#### a. System Monitoring
```bash
# ตรวจสอบ CPU/Memory
top

# ตรวจสอบ disk space
df -h
```

#### b. Application Monitoring
```bash
# ตรวจสอบ API status
curl http://localhost:8000/health

# ตรวจสอบ logs
tail -f logs/*.log
```

## 📚 แหล่งข้อมูลเพิ่มเติม

### 1. เอกสารอ้างอิง
- [Python Documentation](https://docs.python.org)
- [PostgreSQL Documentation](https://www.postgresql.org/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [PyQt6 Documentation](https://doc.qt.io/qtforpython)

### 2. Community Support
- GitHub Issues
- Stack Overflow
- Discord Channel

### 3. Commercial Support
- Email: support@meditech.com
- Phone: xxx-xxx-xxxx
- Website: https://meditech.com/support 