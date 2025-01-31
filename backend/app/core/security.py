from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Union

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.logger import log_security
from app.db.session import get_db
from app.models.user import User

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_PREFIX}/auth/login"
)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Hash a password
    """
    return pwd_context.hash(password)

def create_access_token(
    subject: Union[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create JWT access token
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    
    return encoded_jwt

def decode_token(token: str) -> Dict[str, Any]:
    """
    Decode and verify JWT token
    """
    try:
        decoded_token = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return decoded_token
    except JWTError as e:
        log_security("token_decode_failed", details={"error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    """
    Get current authenticated user
    """
    try:
        payload = decode_token(token)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
    except JWTError as e:
        log_security("token_validation_failed", details={"error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        log_security("user_not_found", details={"user_id": user_id})
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    return user

def check_permissions(user: User, required_permissions: list[str]) -> bool:
    """
    Check if user has required permissions
    """
    user_permissions = set(user.permissions)
    required = set(required_permissions)
    return required.issubset(user_permissions)

def require_permissions(permissions: list[str]):
    """
    Decorator to require specific permissions
    """
    async def permission_dependency(
        current_user: User = Depends(get_current_user),
    ):
        if not check_permissions(current_user, permissions):
            log_security(
                "permission_denied",
                user=current_user.username,
                details={"required_permissions": permissions}
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )
        return current_user
    
    return permission_dependency

def validate_password_strength(password: str) -> bool:
    """
    Validate password strength
    """
    import re
    
    if len(password) < 8:
        return False
    
    if not re.search(r"[A-Z]", password):
        return False
    
    if not re.search(r"[a-z]", password):
        return False
    
    if not re.search(r"[0-9]", password):
        return False
    
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    
    return True

def sanitize_input(input_str: str) -> str:
    """
    Sanitize user input
    """
    import html
    
    # Escape HTML
    sanitized = html.escape(input_str)
    
    # Remove potential SQL injection patterns
    sql_patterns = ["--", ";", "DROP", "DELETE", "UPDATE", "INSERT", "SELECT"]
    for pattern in sql_patterns:
        sanitized = sanitized.replace(pattern, "")
    
    return sanitized

def encrypt_sensitive_data(data: str) -> str:
    """
    Encrypt sensitive data
    """
    from cryptography.fernet import Fernet
    
    key = Fernet.generate_key()
    f = Fernet(key)
    encrypted_data = f.encrypt(data.encode())
    
    return encrypted_data.decode()

def decrypt_sensitive_data(encrypted_data: str, key: bytes) -> str:
    """
    Decrypt sensitive data
    """
    from cryptography.fernet import Fernet
    
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data.encode())
    
    return decrypted_data.decode()

def generate_secure_filename(filename: str) -> str:
    """
    Generate secure filename
    """
    import uuid
    from pathlib import Path
    
    # Get file extension
    ext = Path(filename).suffix
    
    # Generate random filename
    secure_filename = f"{uuid.uuid4().hex}{ext}"
    
    return secure_filename

def validate_file_type(filename: str) -> bool:
    """
    Validate file type
    """
    from pathlib import Path
    
    allowed_extensions = settings.ALLOWED_EXTENSIONS
    file_ext = Path(filename).suffix.lower()
    
    return file_ext in allowed_extensions

def rate_limit(requests: int, period: int):
    """
    Rate limiting decorator
    """
    from functools import wraps
    from fastapi import Request
    import time
    
    def decorator(func):
        # Store last request timestamps
        last_requests = []
        
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            now = time.time()
            
            # Remove old timestamps
            last_requests[:] = [t for t in last_requests if now - t < period]
            
            if len(last_requests) >= requests:
                log_security(
                    "rate_limit_exceeded",
                    details={"ip": request.client.host}
                )
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Too many requests",
                )
            
            last_requests.append(now)
            return await func(request, *args, **kwargs)
        
        return wrapper
    
    return decorator 