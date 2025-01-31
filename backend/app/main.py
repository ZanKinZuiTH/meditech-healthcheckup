# Backend Main Application
# ===================
#
# ไฟล์นี้เป็นจุดเริ่มต้นของ Backend API โดยใช้ FastAPI
# เหมาะสำหรับการศึกษาเรื่อง:
# 1. การสร้าง REST API
# 2. การจัดการฐานข้อมูล
# 3. Authentication & Authorization
# 4. Dependency Injection
#
# การเรียนรู้:
# - ศึกษาโครงสร้าง FastAPI Application
# - เข้าใจการทำงานของ Middleware
# - วิธีการจัดการ Dependencies
# - การจัดการ Error Handling
#
# Tips:
# - ใช้ FastAPI docs ที่ /docs สำหรับทดสอบ API
# - ดู Logs เพื่อ Debug
# - ใช้ Pydantic สำหรับ Data Validation
# - แยก Business Logic ไว้ใน Services

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from prometheus_client import make_asgi_app
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from datetime import datetime

from app.core.config import settings
from app.core.logger import setup_logging
from app.api.v1.api import api_router
from app.db.session import engine, SessionLocal
from app.db.base import Base
from app.models import models
from app.schemas import schemas
from app.crud import crud
from app.auth import get_current_user
from app.services import create_patient_service, get_patients_service

# Setup logging
logger = setup_logging()

# Create FastAPI app
app = FastAPI(
    title="MediTech HealthCheckup API",
    description="API สำหรับระบบตรวจสุขภาพและบันทึกข้อมูลทางการแพทย์",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include API router
app.include_router(api_router, prefix=settings.API_PREFIX)

# Database Dependency
async def get_db() -> Session:
    """
    Get database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()

@app.on_event("startup")
async def startup_event() -> None:
    """
    Initialize application on startup
    """
    try:
        # Create database tables
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        logger.info("Successfully initialized database")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to initialize application"
        )

@app.on_event("shutdown")
async def shutdown_event() -> None:
    """
    Cleanup on application shutdown
    """
    try:
        await engine.dispose()
        logger.info("Successfully shutdown application")
    except Exception as e:
        logger.error(f"Error during shutdown: {str(e)}")

@app.get("/health", response_model=Dict[str, str])
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Any, exc: HTTPException) -> JSONResponse:
    """
    Handle HTTP exceptions
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "status_code": exc.status_code
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Any, exc: Exception) -> JSONResponse:
    """
    Handle general exceptions
    """
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
        }
    )

# Authentication
@app.post("/auth/token", response_model=schemas.Token)
async def login(db: Session = Depends(get_db)) -> schemas.Token:
    return {"access_token": "token", "token_type": "bearer"}

# Patients
@app.get("/patients", response_model=List[schemas.Patient])
async def get_patients(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
) -> List[schemas.Patient]:
    return await get_patients_service(db, skip, limit, search)

@app.post("/patients", response_model=schemas.Patient)
async def create_patient(
    patient: schemas.PatientCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
) -> schemas.Patient:
    return await create_patient_service(db, patient)

# Appointments
@app.get("/appointments", response_model=List[schemas.Appointment])
def get_appointments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    return crud.get_appointments(db, skip=skip, limit=limit)

@app.post("/appointments", response_model=schemas.Appointment)
def create_appointment(
    appointment: schemas.AppointmentCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    return crud.create_appointment(db, appointment=appointment)

# Examinations
@app.get("/examinations", response_model=List[schemas.Examination])
def get_examinations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    return crud.get_examinations(db, skip=skip, limit=limit)

@app.post("/examinations", response_model=schemas.Examination)
def create_examination(
    examination: schemas.ExaminationCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    return crud.create_examination(db, examination=examination)

# Reports
@app.get("/reports/health", response_model=List[schemas.Report])
def get_health_reports(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    return crud.get_health_reports(db, skip=skip, limit=limit)

@app.post("/reports/health", response_model=schemas.Report)
def create_health_report(
    report: schemas.ReportCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    return crud.create_health_report(db, report=report)

# UI Settings
@app.get("/settings/themes", response_model=List[schemas.Theme])
def get_themes(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    return crud.get_themes(db)

@app.put("/settings/accessibility", response_model=schemas.AccessibilitySettings)
def update_accessibility(
    settings: schemas.AccessibilitySettingsUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    return crud.update_accessibility_settings(db, current_user.id, settings)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        workers=settings.MAX_WORKERS
    ) 