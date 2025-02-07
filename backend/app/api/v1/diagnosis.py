"""
API endpoints สำหรับระบบวินิจฉัยโรคเบื้องต้น
"""

from datetime import datetime
from typing import List, Optional
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.models.diagnosis import DiagnosisHistory
from app.models.user import User
from app.schemas.diagnosis import DiagnosisRequest, DiagnosisResult, DiagnosisHistoryResponse
from app.services.ai_diagnosis import AIDiagnosisService

router = APIRouter(prefix="/api/v1")

@router.post("/diagnosis", response_model=DiagnosisResult)
async def get_diagnosis(
    request: DiagnosisRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> DiagnosisResult:
    """
    วินิจฉัยโรคเบื้องต้นจากอาการและข้อมูลผู้ป่วย
    """
    try:
        # สร้างและเริ่มต้น AI service
        service = AIDiagnosisService()
        await service.initialize()
        
        # ทำการวินิจฉัย
        result = await service.get_diagnosis(request)
        
        # บันทึกประวัติ
        history = DiagnosisHistory(
            user_id=current_user.id,
            symptoms=request.symptoms,
            age=request.age,
            gender=request.gender,
            duration_days=request.duration_days,
            medical_history=request.medical_history,
            possible_conditions=result.possible_conditions,
            confidence_score=result.confidence_score,
            recommendation=result.recommendation,
            warning_signs=result.warning_signs,
            created_at=datetime.utcnow()
        )
        
        try:
            db.add(history)
            await db.commit()
            await db.refresh(history)
        except Exception as db_error:
            await db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"ไม่สามารถบันทึกประวัติการวินิจฉัย: {str(db_error)}"
            )
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"เกิดข้อผิดพลาดในการวินิจฉัย: {str(e)}"
        )

@router.get("/diagnosis/history", response_model=List[DiagnosisHistoryResponse])
async def get_diagnosis_history(
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> List[DiagnosisHistoryResponse]:
    """
    ดึงประวัติการวินิจฉัยของผู้ใช้
    """
    try:
        history = await db.query(DiagnosisHistory)\
            .filter(DiagnosisHistory.user_id == current_user.id)\
            .order_by(DiagnosisHistory.created_at.desc())\
            .offset(skip)\
            .limit(limit)\
            .all()
        return history
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"เกิดข้อผิดพลาดในการดึงประวัติ: {str(e)}"
        ) 