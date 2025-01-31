from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import enum
import os

Base = declarative_base()

# Enums
class Gender(enum.Enum):
    MALE = "ชาย"
    FEMALE = "หญิง"

class AppointmentStatus(enum.Enum):
    PENDING = "รอดำเนินการ"
    COMPLETED = "เสร็จสิ้น"
    CANCELLED = "ยกเลิก"

class AppointmentType(enum.Enum):
    GENERAL = "ตรวจทั่วไป"
    SPECIFIC = "ตรวจเฉพาะทาง"
    FOLLOW_UP = "ติดตามผล"
    EMERGENCY = "ฉุกเฉิน"

# Models
class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer)
    gender = Column(Enum(Gender))
    conditions = Column(String)
    
    appointments = relationship("Appointment", back_populates="patient")
    health_records = relationship("HealthRecord", back_populates="patient")

class Appointment(Base):
    __tablename__ = "appointments"
    
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    patient_id = Column(String, ForeignKey("patients.id"))
    type = Column(Enum(AppointmentType))
    status = Column(Enum(AppointmentStatus))
    
    patient = relationship("Patient", back_populates="appointments")

class HealthRecord(Base):
    __tablename__ = "health_records"
    
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    patient_id = Column(String, ForeignKey("patients.id"))
    blood_pressure = Column(Float)
    blood_sugar = Column(Float)
    cholesterol = Column(Float)
    
    patient = relationship("Patient", back_populates="health_records")

class Database:
    def __init__(self, use_real_db=False):
        """
        เริ่มต้นการเชื่อมต่อฐานข้อมูล
        
        Args:
            use_real_db (bool): True เพื่อใช้ฐานข้อมูลจริง, False เพื่อใช้ SQLite ในหน่วยความจำ
        """
        if use_real_db:
            # ใช้ค่าจาก Environment Variables สำหรับการเชื่อมต่อจริง
            db_user = os.getenv("DB_USER", "postgres")
            db_pass = os.getenv("DB_PASS", "")
            db_host = os.getenv("DB_HOST", "localhost")
            db_name = os.getenv("DB_NAME", "meditech")
            
            self.engine = create_engine(
                f"postgresql://{db_user}:{db_pass}@{db_host}/{db_name}"
            )
        else:
            # ใช้ SQLite ในหน่วยความจำสำหรับการสาธิต
            self.engine = create_engine("sqlite:///:memory:")
        
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    def get_session(self):
        """สร้าง session ใหม่สำหรับการทำงานกับฐานข้อมูล"""
        return self.Session()
    
    # Patient Operations
    def add_patient(self, id, name, age, gender, conditions):
        """เพิ่มข้อมูลผู้ป่วยใหม่"""
        with self.get_session() as session:
            patient = Patient(
                id=id,
                name=name,
                age=age,
                gender=Gender(gender),
                conditions=conditions
            )
            session.add(patient)
            session.commit()
    
    def get_patients(self, search=None):
        """ดึงข้อมูลผู้ป่วยทั้งหมดหรือค้นหาตามเงื่อนไข"""
        with self.get_session() as session:
            query = session.query(Patient)
            if search:
                query = query.filter(
                    (Patient.id.contains(search)) |
                    (Patient.name.contains(search))
                )
            return query.all()
    
    # Appointment Operations
    def add_appointment(self, date, patient_id, type, status="รอดำเนินการ"):
        """เพิ่มการนัดหมายใหม่"""
        with self.get_session() as session:
            appointment = Appointment(
                date=date,
                patient_id=patient_id,
                type=AppointmentType(type),
                status=AppointmentStatus(status)
            )
            session.add(appointment)
            session.commit()
    
    def get_appointments(self, date=None):
        """ดึงข้อมูลการนัดหมายตามวันที่"""
        with self.get_session() as session:
            query = session.query(Appointment)
            if date:
                query = query.filter(Appointment.date == date)
            return query.all()
    
    # Health Record Operations
    def add_health_record(self, patient_id, date, blood_pressure, blood_sugar, cholesterol):
        """เพิ่มผลตรวจสุขภาพใหม่"""
        with self.get_session() as session:
            record = HealthRecord(
                patient_id=patient_id,
                date=date,
                blood_pressure=blood_pressure,
                blood_sugar=blood_sugar,
                cholesterol=cholesterol
            )
            session.add(record)
            session.commit()
    
    def get_health_records(self, patient_id=None):
        """ดึงข้อมูลผลตรวจสุขภาพตามรหัสผู้ป่วย"""
        with self.get_session() as session:
            query = session.query(HealthRecord)
            if patient_id:
                query = query.filter(HealthRecord.patient_id == patient_id)
            return query.all() 