# คู่มือการตั้งค่าและเริ่มต้นเซิร์ฟเวอร์

## 1. การเตรียมสภาพแวดล้อม

### 1.1 ติดตั้ง Python
1. ดาวน์โหลด Python 3.8+ จาก https://www.python.org/downloads/
2. ติดตั้งและเพิ่มเข้า PATH
3. ตรวจสอบการติดตั้ง:
```bash
python --version
pip --version
```

### 1.2 ติดตั้ง Node.js (สำหรับ Frontend)
1. ดาวน์โหลด Node.js LTS จาก https://nodejs.org/
2. ติดตั้งและตรวจสอบ:
```bash
node --version
npm --version
```

### 1.3 สร้าง Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

## 2. การติดตั้งโปรเจค

### 2.1 Clone โปรเจค
```bash
git clone https://github.com/your-repo/meditech.git
cd meditech
```

### 2.2 ติดตั้ง Dependencies

#### Backend
```bash
cd backend
pip install -r requirements.txt
```

#### Frontend
```bash
cd frontend
npm install
```

## 3. การเริ่มต้นเซิร์ฟเวอร์

### 3.1 Development Mode

#### Backend Server
```bash
# ใน directory backend/
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Development Server
```bash
# ใน directory frontend/
npm run dev
```

### 3.2 Production Mode

#### Backend (using Gunicorn)
```bash
# ติดตั้ง gunicorn
pip install gunicorn

# รัน server
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

#### Frontend Production Build
```bash
# สร้าง production build
npm run build

# รัน production server (ใช้ serve)
npm install -g serve
serve -s build
```

### 3.3 Docker Mode

#### สร้าง Docker Images
```bash
# Build backend
docker build -t meditech-backend ./backend

# Build frontend
docker build -t meditech-frontend ./frontend
```

#### รันด้วย Docker Compose
```bash
docker-compose up -d
```

## 4. การกำหนดค่า Environment

### 4.1 Backend (.env)
```
# Server
API_V1_STR=/api/v1
PROJECT_NAME=MediTech
BACKEND_CORS_ORIGINS=["http://localhost:3000"]

# Security
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database
DB_CONNECTION=postgresql
DB_HOST=localhost
DB_PORT=5432
DB_DATABASE=meditech
DB_USERNAME=postgres
DB_PASSWORD=your_password
```

### 4.2 Frontend (.env)
```
REACT_APP_API_URL=http://localhost:8000/api/v1
REACT_APP_ENV=development
```

## 5. การ Deploy

### 5.1 การ Deploy บน Linux Server

#### ติดตั้ง Nginx
```bash
sudo apt update
sudo apt install nginx
```

#### ตั้งค่า Nginx Config
```nginx
# /etc/nginx/sites-available/meditech
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        root /var/www/meditech/frontend/build;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 5.2 การ Deploy ด้วย Docker

#### docker-compose.yml
```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DB_HOST=db
    depends_on:
      - db
  
  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
  
  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=meditech
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=your_password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## 6. การ Monitor และ Logging

### 6.1 Application Logging
```python
# backend/app/core/logging.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

### 6.2 Server Monitoring

#### ติดตั้ง Prometheus + Grafana
```bash
# ติดตั้ง Prometheus
docker run -d \
    -p 9090:9090 \
    -v /path/to/prometheus.yml:/etc/prometheus/prometheus.yml \
    prom/prometheus

# ติดตั้ง Grafana
docker run -d \
    -p 3000:3000 \
    grafana/grafana
```

## 7. การแก้ไขปัญหาที่พบบ่อย

### 7.1 ปัญหา CORS
1. ตรวจสอบ BACKEND_CORS_ORIGINS ใน .env
2. ยืนยัน frontend URL ถูกต้อง
3. ตรวจสอบ proxy settings ใน package.json

### 7.2 ปัญหา Performance
1. เพิ่ม worker processes ใน Gunicorn
2. ปรับแต่ง Nginx buffer sizes
3. เพิ่ม caching

### 7.3 ปัญหา Memory Leaks
1. ตรวจสอบ connection pools
2. Monitor memory usage
3. ตั้งค่า max_connections

## 8. การ Backup และ Restore

### 8.1 Backup System
```bash
# Backup database
pg_dump -U postgres meditech > backup.sql

# Backup uploads
tar -czf uploads.tar.gz /path/to/uploads

# Backup configs
cp .env .env.backup
```

### 8.2 Restore System
```bash
# Restore database
psql -U postgres meditech < backup.sql

# Restore uploads
tar -xzf uploads.tar.gz -C /path/to/uploads

# Restore configs
cp .env.backup .env
``` 