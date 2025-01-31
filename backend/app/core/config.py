from typing import List
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, validator
import secrets


class Settings(BaseSettings):
    # Application Settings
    APP_NAME: str = "MediTech HealthCheckup"
    APP_ENV: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1"]

    # API Configuration
    API_VERSION: str = "v1"
    API_PREFIX: str = f"/api/{API_VERSION}"
    API_HOST: str = "http://localhost"
    API_PORT: int = 8000

    # Database Configuration
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "meditech_healthcheckup"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = ""

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # JWT Settings
    JWT_SECRET_KEY: str = secrets.token_urlsafe(32)
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Redis Configuration
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str = ""

    @property
    def REDIS_URL(self) -> str:
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    # File Storage
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: List[str] = [".jpg", ".jpeg", ".png", ".pdf", ".docx"]

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"

    # CORS Settings
    CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Frontend Settings
    FRONTEND_URL: str = "http://localhost:3000"
    ASSETS_DIR: str = "./static/assets"

    # Security
    SSL_CERTIFICATE: str = ""
    SSL_KEY: str = ""

    # Feature Flags
    ENABLE_CACHE: bool = True
    ENABLE_NOTIFICATIONS: bool = True
    ENABLE_FILE_UPLOAD: bool = True
    ENABLE_AUDIT_LOG: bool = True

    # Performance
    MAX_WORKERS: int = 4
    TIMEOUT: int = 30
    KEEP_ALIVE: int = 5

    # Backup
    BACKUP_DIR: str = "./backups"
    BACKUP_RETENTION_DAYS: int = 30

    # Monitoring
    ENABLE_METRICS: bool = True
    PROMETHEUS_PORT: int = 9090

    class Config:
        case_sensitive = True
        env_file = ".env"


# Create settings instance
settings = Settings()

# Validate settings on startup
def validate_settings() -> None:
    """
    Validate critical settings on startup
    """
    required_dirs = [
        settings.UPLOAD_DIR,
        settings.ASSETS_DIR,
        settings.BACKUP_DIR,
        "logs",
        "static"
    ]

    for dir_path in required_dirs:
        import os
        os.makedirs(dir_path, exist_ok=True)

    if not settings.SECRET_KEY:
        raise ValueError("SECRET_KEY must be set")

    if not settings.DB_PASSWORD:
        raise ValueError("DB_PASSWORD must be set")

    if settings.APP_ENV == "production":
        if settings.DEBUG:
            raise ValueError("DEBUG should not be enabled in production")
        if not settings.SSL_CERTIFICATE or not settings.SSL_KEY:
            raise ValueError("SSL certificate and key are required in production") 