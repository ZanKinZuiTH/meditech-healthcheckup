from datetime import datetime
from typing import Any
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.sql import func

@as_declarative()
class Base:
    """
    Base class for all database models
    """
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

class TimestampMixin:
    """
    Mixin for adding created_at and updated_at timestamps
    """
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

class UserMixin:
    """
    Mixin for adding created_by and updated_by fields
    """
    created_by = Column(String, nullable=True)
    updated_by = Column(String, nullable=True)

class SoftDeleteMixin:
    """
    Mixin for soft delete functionality
    """
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    deleted_by = Column(String, nullable=True)

    def soft_delete(self, user: str = None):
        self.deleted_at = datetime.utcnow()
        self.deleted_by = user

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None

class AuditMixin:
    """
    Mixin for audit trail
    """
    version = Column(Integer, nullable=False, default=1)
    last_modified_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
    last_modified_by = Column(String, nullable=True)

    def update_audit(self, user: str = None):
        self.version += 1
        self.last_modified_at = datetime.utcnow()
        self.last_modified_by = user

class FullAuditMixin(TimestampMixin, UserMixin, SoftDeleteMixin, AuditMixin):
    """
    Mixin combining all audit functionality
    """
    pass

# Import all models here
from app.models.user import User  # noqa
from app.models.checkup import CheckupJob, CheckupTask, CheckupResult  # noqa
from app.models.patient import Patient, MedicalRecord, VitalSign  # noqa
from app.models.company import InsuranceCompany  # noqa
from app.models.doctor import Doctor  # noqa 