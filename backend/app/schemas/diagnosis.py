"""
Pydantic schemas สำหรับระบบวินิจฉัยโรค
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class DiagnosisInput(BaseModel):
    """ข้อมูลนำเข้าสำหรับการวินิจฉัย"""
    
    symptoms: List[str] = Field(
        ...,
        description="รายการอาการที่พบ",
        min_items=1
    )
    
    age: Optional[int] = Field(
        None,
        description="อายุของผู้ป่วย",
        ge=0,
        le=150
    )
    
    gender: Optional[str] = Field(
        None,
        description="เพศของผู้ป่วย",
        pattern="^(male|female|other)$"
    )
    
    duration_days: Optional[int] = Field(
        None,
        description="ระยะเวลาที่มีอาการ (วัน)",
        ge=0
    )
    
    medical_history: Optional[List[str]] = Field(
        None,
        description="ประวัติการรักษาที่เกี่ยวข้อง"
    )

class DiagnosisRequest(BaseModel):
    """ข้อมูลที่ใช้ในการวินิจฉัย"""
    symptoms: List[str]
    age: Optional[int] = None
    gender: Optional[str] = None
    duration_days: Optional[int] = None
    medical_history: Optional[List[str]] = None

class DiagnosisResult(BaseModel):
    """ผลลัพธ์การวินิจฉัย"""
    
    possible_conditions: List[str] = Field(
        ...,
        description="รายการโรคที่เป็นไปได้",
        min_items=1
    )
    
    confidence_score: float = Field(
        ...,
        description="ระดับความเชื่อมั่นของการวินิจฉัย",
        ge=0,
        le=1
    )
    
    recommendation: str = Field(
        ...,
        description="คำแนะนำเบื้องต้น"
    )
    
    warning_signs: List[str] = Field(
        default=[],
        description="สัญญาณอันตรายที่ตรวจพบ"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "possible_conditions": [
                    "ไข้หวัดทั่วไป",
                    "ภูมิแพ้",
                    "ไซนัสอักเสบ"
                ],
                "confidence_score": 0.85,
                "recommendation": "ควรพักผ่อนให้เพียงพอและดื่มน้ำมากๆ",
                "warning_signs": []
            }
        }

class DiagnosisHistoryResponse(BaseModel):
    """ข้อมูลประวัติการวินิจฉัยที่ส่งกลับให้ผู้ใช้"""
    id: int
    symptoms: List[str]
    age: Optional[int]
    gender: Optional[str]
    duration_days: Optional[int]
    medical_history: Optional[List[str]]
    possible_conditions: List[str]
    confidence_score: float
    recommendation: str
    warning_signs: Optional[List[str]]
    created_at: datetime

    class Config:
        orm_mode = True 