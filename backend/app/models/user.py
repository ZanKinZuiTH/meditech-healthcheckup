from typing import List
from sqlalchemy import Boolean, Column, String, JSON, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base, FullAuditMixin

class Role(Base, FullAuditMixin):
    """
    Role model for user roles
    """
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    permissions = Column(JSON, default=list)

    # Relationships
    users = relationship("User", back_populates="role")

    def __str__(self):
        return self.name

class User(Base, FullAuditMixin):
    """
    User model for authentication and authorization
    """
    # Basic information
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    full_name = Column(String)
    hashed_password = Column(String, nullable=False)
    
    # User status
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    
    # Additional information
    phone = Column(String)
    department = Column(String)
    position = Column(String)
    employee_id = Column(String, unique=True)
    
    # Security
    last_login = Column(String)
    failed_login_attempts = Column(Integer, default=0)
    password_changed_at = Column(String)
    
    # Preferences
    language = Column(String, default="th")
    theme = Column(String, default="light")
    notifications_enabled = Column(Boolean, default=True)
    
    # Role and permissions
    role_id = Column(Integer, ForeignKey("role.id"))
    role = relationship("Role", back_populates="users")
    custom_permissions = Column(JSON, default=list)

    @property
    def permissions(self) -> List[str]:
        """
        Get combined permissions from role and custom permissions
        """
        role_permissions = self.role.permissions if self.role else []
        return list(set(role_permissions + self.custom_permissions))

    def has_permission(self, permission: str) -> bool:
        """
        Check if user has specific permission
        """
        if self.is_superuser:
            return True
        return permission in self.permissions

    def has_permissions(self, permissions: List[str]) -> bool:
        """
        Check if user has all specified permissions
        """
        if self.is_superuser:
            return True
        return all(self.has_permission(p) for p in permissions)

    def add_permission(self, permission: str) -> None:
        """
        Add custom permission to user
        """
        if permission not in self.custom_permissions:
            self.custom_permissions.append(permission)

    def remove_permission(self, permission: str) -> None:
        """
        Remove custom permission from user
        """
        if permission in self.custom_permissions:
            self.custom_permissions.remove(permission)

    def increment_failed_login(self) -> None:
        """
        Increment failed login attempts
        """
        self.failed_login_attempts += 1

    def reset_failed_login(self) -> None:
        """
        Reset failed login attempts
        """
        self.failed_login_attempts = 0

    def update_last_login(self) -> None:
        """
        Update last login timestamp
        """
        from datetime import datetime
        self.last_login = datetime.utcnow().isoformat()

    def update_password(self, hashed_password: str) -> None:
        """
        Update user password
        """
        from datetime import datetime
        self.hashed_password = hashed_password
        self.password_changed_at = datetime.utcnow().isoformat()
        self.failed_login_attempts = 0

    def to_dict(self) -> dict:
        """
        Convert user to dictionary
        """
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name,
            "is_active": self.is_active,
            "is_superuser": self.is_superuser,
            "department": self.department,
            "position": self.position,
            "employee_id": self.employee_id,
            "role": self.role.name if self.role else None,
            "permissions": self.permissions,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_login": self.last_login
        }

    def __str__(self):
        return f"{self.username} ({self.full_name})"

    class Config:
        orm_mode = True 