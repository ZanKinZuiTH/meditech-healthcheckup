from datetime import datetime, date
from typing import Optional
from sqlalchemy import Column, String, Integer, Date, DateTime, ForeignKey, Boolean, JSON, Text, Numeric
from sqlalchemy.orm import relationship

from app.db.base import Base, FullAuditMixin

class Patient(Base, FullAuditMixin):
    """
    Model for patient information
    """
    # Basic information
    hn = Column(String, unique=True, nullable=False, index=True)
    title = Column(String)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    first_name_en = Column(String)
    last_name_en = Column(String)
    
    # Personal information
    birth_date = Column(Date, nullable=False)
    gender = Column(String, nullable=False)  # male, female
    blood_type = Column(String)
    nationality = Column(String)
    religion = Column(String)
    marital_status = Column(String)
    
    # Contact information
    phone = Column(String)
    email = Column(String)
    line_id = Column(String)
    emergency_contact = Column(JSON)  # Name and phone number
    
    # Address
    address = Column(JSON)  # Structured address data
    
    # Work information
    company_id = Column(Integer, ForeignKey("company.id"))
    employee_id = Column(String)
    department = Column(String)
    position = Column(String)
    work_start_date = Column(Date)
    
    # Insurance
    insurance_info = Column(JSON)  # Insurance details
    
    # Medical information
    allergies = Column(JSON)  # List of allergies
    chronic_conditions = Column(JSON)  # List of chronic conditions
    current_medications = Column(JSON)  # List of current medications
    family_history = Column(JSON)  # Family medical history
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Relationships
    company = relationship("Company", back_populates="employees")
    medical_records = relationship("MedicalRecord", back_populates="patient", cascade="all, delete-orphan")
    vital_signs = relationship("VitalSign", back_populates="patient", cascade="all, delete-orphan")
    checkup_results = relationship("CheckupResult", back_populates="patient")

    @property
    def age(self) -> Optional[int]:
        """
        Calculate patient age
        """
        if not self.birth_date:
            return None
        today = date.today()
        return today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )

    @property
    def full_name(self) -> str:
        """
        Get patient full name
        """
        return f"{self.title or ''} {self.first_name} {self.last_name}".strip()

    @property
    def full_name_en(self) -> str:
        """
        Get patient full name in English
        """
        if not self.first_name_en or not self.last_name_en:
            return self.full_name
        return f"{self.first_name_en} {self.last_name_en}".strip()

    def to_dict(self) -> dict:
        """
        Convert patient to dictionary
        """
        return {
            "id": self.id,
            "hn": self.hn,
            "full_name": self.full_name,
            "full_name_en": self.full_name_en,
            "age": self.age,
            "gender": self.gender,
            "birth_date": self.birth_date.isoformat() if self.birth_date else None,
            "blood_type": self.blood_type,
            "nationality": self.nationality,
            "phone": self.phone,
            "email": self.email,
            "company": self.company.name if self.company else None,
            "employee_id": self.employee_id,
            "department": self.department,
            "position": self.position,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

class MedicalRecord(Base, FullAuditMixin):
    """
    Model for patient medical records
    """
    # Record information
    patient_id = Column(Integer, ForeignKey("patient.id"), nullable=False)
    visit_date = Column(DateTime(timezone=True), nullable=False)
    visit_type = Column(String)  # OPD, IPD, Emergency
    
    # Clinical information
    chief_complaint = Column(Text)
    present_illness = Column(Text)
    past_history = Column(Text)
    physical_exam = Column(Text)
    diagnosis = Column(JSON)  # List of diagnoses with ICD codes
    treatment = Column(Text)
    medications = Column(JSON)  # Prescribed medications
    lab_orders = Column(JSON)  # Ordered laboratory tests
    imaging_orders = Column(JSON)  # Ordered imaging studies
    
    # Doctor information
    doctor_id = Column(Integer, ForeignKey("doctor.id"))
    doctor_notes = Column(Text)
    
    # Follow-up
    follow_up_date = Column(Date)
    follow_up_notes = Column(Text)
    
    # Relationships
    patient = relationship("Patient", back_populates="medical_records")
    doctor = relationship("Doctor", back_populates="medical_records")
    vital_signs = relationship("VitalSign", back_populates="medical_record", uselist=False)

    def to_dict(self) -> dict:
        """
        Convert medical record to dictionary
        """
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "visit_date": self.visit_date.isoformat() if self.visit_date else None,
            "visit_type": self.visit_type,
            "chief_complaint": self.chief_complaint,
            "diagnosis": self.diagnosis,
            "treatment": self.treatment,
            "doctor": self.doctor.full_name if self.doctor else None,
            "follow_up_date": self.follow_up_date.isoformat() if self.follow_up_date else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

class VitalSign(Base, FullAuditMixin):
    """
    Model for patient vital signs
    """
    # Record information
    patient_id = Column(Integer, ForeignKey("patient.id"), nullable=False)
    medical_record_id = Column(Integer, ForeignKey("medicalrecord.id"))
    measured_at = Column(DateTime(timezone=True), nullable=False)
    
    # Vital signs
    temperature = Column(Numeric(4, 1))  # Celsius
    pulse_rate = Column(Integer)  # Beats per minute
    respiratory_rate = Column(Integer)  # Breaths per minute
    blood_pressure_systolic = Column(Integer)  # mmHg
    blood_pressure_diastolic = Column(Integer)  # mmHg
    oxygen_saturation = Column(Integer)  # Percentage
    
    # Additional measurements
    height = Column(Numeric(5, 2))  # cm
    weight = Column(Numeric(5, 2))  # kg
    bmi = Column(Numeric(4, 1))
    pain_score = Column(Integer)  # 0-10
    
    # Notes
    notes = Column(Text)
    
    # Relationships
    patient = relationship("Patient", back_populates="vital_signs")
    medical_record = relationship("MedicalRecord", back_populates="vital_signs")

    @property
    def blood_pressure(self) -> str:
        """
        Get formatted blood pressure
        """
        if not self.blood_pressure_systolic or not self.blood_pressure_diastolic:
            return None
        return f"{self.blood_pressure_systolic}/{self.blood_pressure_diastolic}"

    def calculate_bmi(self) -> None:
        """
        Calculate BMI if height and weight are available
        """
        if self.height and self.weight:
            height_m = float(self.height) / 100
            self.bmi = round(float(self.weight) / (height_m * height_m), 1)

    def to_dict(self) -> dict:
        """
        Convert vital signs to dictionary
        """
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "medical_record_id": self.medical_record_id,
            "measured_at": self.measured_at.isoformat() if self.measured_at else None,
            "temperature": float(self.temperature) if self.temperature else None,
            "pulse_rate": self.pulse_rate,
            "respiratory_rate": self.respiratory_rate,
            "blood_pressure": self.blood_pressure,
            "oxygen_saturation": self.oxygen_saturation,
            "height": float(self.height) if self.height else None,
            "weight": float(self.weight) if self.weight else None,
            "bmi": float(self.bmi) if self.bmi else None,
            "pain_score": self.pain_score,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None
        } 