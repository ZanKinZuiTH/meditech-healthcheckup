from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from ...db.session import get_db
from ...services.ai_diagnosis import AIDiagnosisService
from ...schemas.diagnosis import DiagnosisInput, DiagnosisResult
from ...core.security import get_current_user
from ...schemas.user import User

router = APIRouter()
ai_diagnosis_service = AIDiagnosisService()

@router.post("/diagnose", response_model=DiagnosisResult)
async def get_diagnosis(
    input_data: DiagnosisInput,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> DiagnosisResult:
    """
    วินิจฉัยโรคเบื้องต้นจากอาการที่ระบุ
    
    Args:
        input_data: ข้อมูลอาการและรายละเอียดผู้ป่วย
        current_user: ข้อมูลผู้ใช้ที่กำลังใช้งาน
        db: Database session
        
    Returns:
        DiagnosisResult: ผลการวินิจฉัยเบื้องต้น
    """
    try:
        # ตรวจสอบสิทธิ์การใช้งาน
        if not current_user.can_use_ai_diagnosis:
            raise HTTPException(
                status_code=403,
                detail="ไม่มีสิทธิ์ใช้งานระบบวินิจฉัยด้วย AI"
            )
        
        # วินิจฉัยด้วย AI
        result = await ai_diagnosis_service.get_diagnosis(input_data)
        
        # บันทึกประวัติการวินิจฉัย
        await _save_diagnosis_history(
            db=db,
            user_id=current_user.id,
            input_data=input_data,
            result=result
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"เกิดข้อผิดพลาดในการวินิจฉัย: {str(e)}"
        )

@router.get("/history", response_model=List[DiagnosisResult])
async def get_diagnosis_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> List[DiagnosisResult]:
    """ดึงประวัติการวินิจฉัยของผู้ใช้"""
    try:
        history = await _get_user_diagnosis_history(db, current_user.id)
        return history
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"เกิดข้อผิดพลาดในการดึงประวัติ: {str(e)}"
        )

async def _save_diagnosis_history(
    db: Session,
    user_id: int,
    input_data: DiagnosisInput,
    result: DiagnosisResult
) -> None:
    """บันทึกประวัติการวินิจฉัยลงฐานข้อมูล"""
    # TODO: implement diagnosis history saving
    pass

async def _get_user_diagnosis_history(
    db: Session,
    user_id: int
) -> List[DiagnosisResult]:
    """ดึงประวัติการวินิจฉัยของผู้ใช้จากฐานข้อมูล"""
    # TODO: implement diagnosis history retrieval
    return [] 