# Database Configuration
# ====================
#
# ไฟล์นี้จัดการการเชื่อมต่อและการตั้งค่าฐานข้อมูล
# เหมาะสำหรับการศึกษาเรื่อง:
# 1. การเชื่อมต่อฐานข้อมูล
# 2. การใช้ SQLAlchemy ORM
# 3. การจัดการ Connection Pool
# 4. การทำ Migration
#
# การเรียนรู้:
# - ศึกษาการตั้งค่า Database URL
# - เข้าใจการทำงานของ Session
# - วิธีการจัดการ Connection Pool
# - การใช้ Async Database
#
# Tips:
# - ใช้ Environment Variables
# - ตั้งค่า Pool Size ให้เหมาะสม
# - ใช้ Alembic สำหรับ Migration
# - จัดการ Connection ให้ดี

import logging
from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import QueuePool
from typing import Generator

from .config import settings

# Setup logging
logger = logging.getLogger(__name__)

# สร้าง Database URL
# -----------------
# Format: postgresql://user:password@host:port/dbname
# สามารถกำหนดค่าผ่าน Environment Variables ได้
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# สร้าง Engine
# -----------
# Engine เป็นตัวจัดการการเชื่อมต่อกับฐานข้อมูล
# สามารถกำหนดค่าต่างๆ เช่น:
# - Pool Size
# - Timeout
# - Echo SQL
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,  # เพิ่มจำนวน connections
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,  # รีเซ็ต connection ทุก 30 นาที
    echo=settings.DEBUG
)

# เพิ่ม Event Listeners
@event.listens_for(engine, "connect")
def connect(dbapi_connection, connection_record):
    logger.info("Database connection established")

@event.listens_for(engine, "checkout")
def checkout(dbapi_connection, connection_record, connection_proxy):
    logger.debug("Database connection checked out")

@event.listens_for(engine, "checkin")
def checkin(dbapi_connection, connection_record):
    logger.debug("Database connection checked in")

# สร้าง SessionLocal
# -----------------
# SessionLocal ใช้สำหรับติดต่อกับฐานข้อมูล
# แต่ละ Request ควรใช้ Session แยกกัน
SessionLocal = scoped_session(
    sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False
    )
)

# สร้าง Base Class
# ---------------
# Base Class สำหรับสร้าง Model
# ใช้เป็น Parent Class ของทุก Model
Base = declarative_base()
Base.query = SessionLocal.query_property()

# Dependency
# ---------
# ฟังก์ชันสำหรับสร้าง Database Session
# ใช้เป็น Dependency ใน FastAPI
def get_db() -> Generator:
    """
    สร้าง Database Session สำหรับแต่ละ Request
    
    Yields:
        Session: Database Session
    
    Example:
        @app.get("/items/")
        def read_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        SessionLocal.remove()  # ทำความสะอาด thread-local storage

# Database Utilities
# -----------------

def init_db() -> None:
    """
    สร้างตารางทั้งหมดในฐานข้อมูล
    ใช้สำหรับเริ่มต้นระบบครั้งแรก
    
    Warning:
        ควรใช้ Alembic สำหรับ Production
    """
    Base.metadata.create_all(bind=engine)

def drop_db() -> None:
    """
    ลบตารางทั้งหมดในฐานข้อมูล
    ใช้สำหรับ Testing เท่านั้น
    
    Warning:
        อย่าใช้ใน Production
    """
    Base.metadata.drop_all(bind=engine)

# Database Events
# --------------

def connect_db() -> None:
    """
    เชื่อมต่อกับฐานข้อมูล
    ใช้เมื่อ Application เริ่มทำงาน
    """
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        logger.info("Database connected successfully")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
    finally:
        db.close()

def disconnect_db() -> None:
    """
    ตัดการเชื่อมต่อกับฐานข้อมูล
    ใช้เมื่อ Application หยุดทำงาน
    """
    engine.dispose()
    logger.info("Database disconnected") 