from sqlalchemy import Column, String, Integer, Boolean, JSON, Text, ForeignKey, Date
from sqlalchemy.orm import relationship

from app.db.base import Base, FullAuditMixin

class Doctor(Base, FullAuditMixin):
    """
    Model for doctors
    """
    # Basic information
    title = Column(String)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    first_name_en = Column(String)
    last_name_en = Column(String)
    
    # Professional information
    license_number = Column(String, unique=True, nullable=False)
    specialty = Column(String, nullable=False)
    sub_specialty = Column(String)
    position = Column(String)
    
    # Education and certification
    education = Column(JSON)  # List of education history
    certifications = Column(JSON)  # List of certifications
    training = Column(JSON)  # List of training history
    
    # Contact information
    phone = Column(String)
    email = Column(String)
    line_id = Column(String)
    
    # Work information
    department = Column(String)
    office_hours = Column(JSON)  # Weekly schedule
    consultation_fee = Column(Integer)
    
    # Professional memberships
    memberships = Column(JSON)  # Professional organization memberships
    
    # Status
    is_active = Column(Boolean, default=True)
    status = Column(String, default="active")  # active, inactive, on_leave
    remarks = Column(Text)
    
    # Document information
    documents = Column(JSON)  # List of document paths (license, certificates, etc.)
    signature = Column(String)  # Path to signature image
    
    # Relationships
    medical_records = relationship("MedicalRecord", back_populates="doctor")
    checkup_results = relationship("CheckupResult", back_populates="doctor")
    specialties = relationship("DoctorSpecialty", back_populates="doctor", cascade="all, delete-orphan")
    schedules = relationship("DoctorSchedule", back_populates="doctor", cascade="all, delete-orphan")

    @property
    def full_name(self) -> str:
        """
        Get doctor full name
        """
        return f"{self.title or ''} {self.first_name} {self.last_name}".strip()

    @property
    def full_name_en(self) -> str:
        """
        Get doctor full name in English
        """
        if not self.first_name_en or not self.last_name_en:
            return self.full_name
        return f"{self.first_name_en} {self.last_name_en}".strip()

    def to_dict(self) -> dict:
        """
        Convert doctor to dictionary
        """
        return {
            "id": self.id,
            "full_name": self.full_name,
            "full_name_en": self.full_name_en,
            "license_number": self.license_number,
            "specialty": self.specialty,
            "sub_specialty": self.sub_specialty,
            "position": self.position,
            "department": self.department,
            "phone": self.phone,
            "email": self.email,
            "is_active": self.is_active,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

class DoctorSpecialty(Base, FullAuditMixin):
    """
    Model for doctor specialties
    """
    # Specialty information
    doctor_id = Column(Integer, ForeignKey("doctor.id"), nullable=False)
    specialty_name = Column(String, nullable=False)
    certification_number = Column(String)
    certification_date = Column(Date)
    expiry_date = Column(Date)
    
    # Additional information
    issuing_authority = Column(String)
    certification_details = Column(JSON)
    
    # Status
    is_primary = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    remarks = Column(Text)
    
    # Relationships
    doctor = relationship("Doctor", back_populates="specialties")

    def to_dict(self) -> dict:
        """
        Convert specialty to dictionary
        """
        return {
            "id": self.id,
            "doctor_id": self.doctor_id,
            "specialty_name": self.specialty_name,
            "certification_number": self.certification_number,
            "certification_date": self.certification_date.isoformat() if self.certification_date else None,
            "expiry_date": self.expiry_date.isoformat() if self.expiry_date else None,
            "issuing_authority": self.issuing_authority,
            "is_primary": self.is_primary,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

class DoctorSchedule(Base, FullAuditMixin):
    """
    Model for doctor schedules
    """
    # Schedule information
    doctor_id = Column(Integer, ForeignKey("doctor.id"), nullable=False)
    day_of_week = Column(Integer)  # 0-6 (Monday-Sunday)
    start_time = Column(String)
    end_time = Column(String)
    
    # Schedule details
    location = Column(String)
    service_type = Column(String)  # regular, special, emergency
    max_patients = Column(Integer)
    
    # Break time
    break_start = Column(String)
    break_end = Column(String)
    
    # Status
    is_active = Column(Boolean, default=True)
    remarks = Column(Text)
    
    # Relationships
    doctor = relationship("Doctor", back_populates="schedules")

    def to_dict(self) -> dict:
        """
        Convert schedule to dictionary
        """
        return {
            "id": self.id,
            "doctor_id": self.doctor_id,
            "day_of_week": self.day_of_week,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "location": self.location,
            "service_type": self.service_type,
            "max_patients": self.max_patients,
            "break_start": self.break_start,
            "break_end": self.break_end,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        } 