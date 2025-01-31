from datetime import datetime
from typing import List
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean, JSON, Text, Numeric
from sqlalchemy.orm import relationship

from app.db.base import Base, FullAuditMixin

class CheckupJob(Base, FullAuditMixin):
    """
    Model for health checkup jobs
    """
    # Basic information
    job_number = Column(String, unique=True, nullable=False, index=True)
    company_name = Column(String, nullable=False)
    branch_name = Column(String)
    
    # Schedule
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    
    # Status
    status = Column(String, default="draft")  # draft, scheduled, in_progress, completed, cancelled
    is_active = Column(Boolean, default=True)
    
    # Contract details
    contract_number = Column(String)
    contract_date = Column(DateTime(timezone=True))
    insurance_company_id = Column(Integer, ForeignKey("insurancecompany.id"))
    
    # Additional information
    total_employees = Column(Integer, default=0)
    completed_checkups = Column(Integer, default=0)
    remarks = Column(Text)
    
    # Relationships
    insurance_company = relationship("InsuranceCompany", back_populates="checkup_jobs")
    tasks = relationship("CheckupTask", back_populates="job", cascade="all, delete-orphan")
    results = relationship("CheckupResult", back_populates="job", cascade="all, delete-orphan")

    @property
    def progress(self) -> float:
        """
        Calculate job progress
        """
        if not self.total_employees:
            return 0
        return (self.completed_checkups / self.total_employees) * 100

    def update_progress(self) -> None:
        """
        Update completed checkups count
        """
        self.completed_checkups = sum(1 for result in self.results if result.is_completed)

    def to_dict(self) -> dict:
        """
        Convert job to dictionary
        """
        return {
            "id": self.id,
            "job_number": self.job_number,
            "company_name": self.company_name,
            "branch_name": self.branch_name,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "status": self.status,
            "progress": self.progress,
            "total_employees": self.total_employees,
            "completed_checkups": self.completed_checkups,
            "insurance_company": self.insurance_company.name if self.insurance_company else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

class CheckupTask(Base, FullAuditMixin):
    """
    Model for checkup tasks within a job
    """
    # Task information
    job_id = Column(Integer, ForeignKey("checkupjob.id"), nullable=False)
    task_name = Column(String, nullable=False)
    group_result_name = Column(String)
    description = Column(Text)
    
    # Configuration
    is_required = Column(Boolean, default=True)
    order = Column(Integer, default=0)
    reference_values = Column(JSON)  # Normal ranges, units, etc.
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Relationships
    job = relationship("CheckupJob", back_populates="tasks")
    results = relationship("CheckupResult", back_populates="task", cascade="all, delete-orphan")

    def to_dict(self) -> dict:
        """
        Convert task to dictionary
        """
        return {
            "id": self.id,
            "job_id": self.job_id,
            "task_name": self.task_name,
            "group_result_name": self.group_result_name,
            "description": self.description,
            "is_required": self.is_required,
            "order": self.order,
            "reference_values": self.reference_values,
            "is_active": self.is_active
        }

class CheckupResult(Base, FullAuditMixin):
    """
    Model for checkup results
    """
    # Result information
    job_id = Column(Integer, ForeignKey("checkupjob.id"), nullable=False)
    task_id = Column(Integer, ForeignKey("checkuptask.id"), nullable=False)
    patient_id = Column(Integer, ForeignKey("patient.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctor.id"))
    
    # Result values
    result_value = Column(Text)
    numeric_value = Column(Numeric(10, 2))
    result_status = Column(String)  # normal, abnormal, critical
    doctor_comment = Column(Text)
    
    # Status
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime(timezone=True))
    verified_at = Column(DateTime(timezone=True))
    verified_by = Column(String)
    
    # Additional data
    attachments = Column(JSON)  # List of file paths
    metadata = Column(JSON)  # Additional result metadata
    
    # Relationships
    job = relationship("CheckupJob", back_populates="results")
    task = relationship("CheckupTask", back_populates="results")
    patient = relationship("Patient", back_populates="checkup_results")
    doctor = relationship("Doctor", back_populates="checkup_results")

    def complete(self, user: str = None) -> None:
        """
        Mark result as completed
        """
        self.is_completed = True
        self.completed_at = datetime.utcnow()
        self.updated_by = user

    def verify(self, user: str = None) -> None:
        """
        Verify result by doctor
        """
        self.verified_at = datetime.utcnow()
        self.verified_by = user

    def to_dict(self) -> dict:
        """
        Convert result to dictionary
        """
        return {
            "id": self.id,
            "job_id": self.job_id,
            "task_id": self.task_id,
            "patient_id": self.patient_id,
            "doctor_id": self.doctor_id,
            "result_value": self.result_value,
            "numeric_value": float(self.numeric_value) if self.numeric_value else None,
            "result_status": self.result_status,
            "doctor_comment": self.doctor_comment,
            "is_completed": self.is_completed,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "verified_at": self.verified_at.isoformat() if self.verified_at else None,
            "verified_by": self.verified_by,
            "attachments": self.attachments,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        } 