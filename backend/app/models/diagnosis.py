"""
โมเดลสำหรับเก็บข้อมูลการวินิจฉัยโรค
"""

from datetime import datetime
from pathlib import Path
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import AsyncAttrs

from app.db.base_class import Base

class DiagnosisHistory(AsyncAttrs, Base):
    """ตารางเก็บประวัติการวินิจฉัย"""
    
    __tablename__ = "diagnosis_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    
    # ข้อมูลนำเข้า
    symptoms = Column(JSON, nullable=False)  # List[str]
    age = Column(Integer)
    gender = Column(String)
    duration_days = Column(Integer)
    medical_history = Column(JSON)  # List[str]
    
    # ผลการวินิจฉัย
    possible_conditions = Column(JSON, nullable=False)  # List[str]
    confidence_score = Column(Float, nullable=False)
    recommendation = Column(String, nullable=False)
    warning_signs = Column(JSON)  # List[str]
    
    # Metadata
    created_at = Column(DateTime, nullable=False, index=True)
    
    # Relationships
    user = relationship(
        "User",
        back_populates="diagnosis_history",
        lazy="selectin",
        cascade="all, delete"
    )
    
    class Config:
        orm_mode = True
        
    def __repr__(self):
        return f"<DiagnosisHistory(id={self.id}, user_id={self.user_id}, created_at={self.created_at})>" 