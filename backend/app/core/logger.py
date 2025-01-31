import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any, Dict

from app.core.config import settings

# Custom formatter with Thai time
class ThaiFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        import datetime
        import pytz

        tz = pytz.timezone('Asia/Bangkok')
        dt = datetime.datetime.fromtimestamp(record.created, tz)
        if datefmt:
            return dt.strftime(datefmt)
        return dt.strftime('%Y-%m-%d %H:%M:%S %z')

def setup_logging() -> logging.Logger:
    """
    Setup logging configuration
    """
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Create logger
    logger = logging.getLogger("meditech")
    logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))

    # Log format
    log_format = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    formatter = ThaiFormatter(log_format)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler
    file_handler = RotatingFileHandler(
        settings.LOG_FILE,
        maxBytes=10485760,  # 10MB
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

def get_logger() -> logging.Logger:
    """
    Get logger instance
    """
    return logging.getLogger("meditech")

def log_request(request: Any, response: Any = None, error: Exception = None) -> None:
    """
    Log HTTP request details
    """
    logger = get_logger()
    
    request_info: Dict[str, Any] = {
        "method": request.method,
        "url": str(request.url),
        "client_host": request.client.host if request.client else None,
        "headers": dict(request.headers),
    }

    if response:
        request_info["status_code"] = response.status_code
        request_info["response_headers"] = dict(response.headers)

    if error:
        request_info["error"] = str(error)
        logger.error(f"Request failed: {request_info}")
    else:
        logger.info(f"Request processed: {request_info}")

def log_database_query(query: str, params: Any = None, duration: float = None) -> None:
    """
    Log database query details
    """
    logger = get_logger()
    
    query_info = {
        "query": query,
        "parameters": params,
        "duration": f"{duration:.2f}s" if duration else None
    }
    
    logger.debug(f"Database query executed: {query_info}")

def log_error(error: Exception, context: Dict[str, Any] = None) -> None:
    """
    Log error with context
    """
    logger = get_logger()
    
    error_info = {
        "error_type": type(error).__name__,
        "error_message": str(error),
        "context": context
    }
    
    logger.error(f"Error occurred: {error_info}", exc_info=True)

def log_audit(user: str, action: str, resource: str, details: Dict[str, Any] = None) -> None:
    """
    Log audit trail
    """
    logger = get_logger()
    
    audit_info = {
        "user": user,
        "action": action,
        "resource": resource,
        "details": details
    }
    
    logger.info(f"Audit trail: {audit_info}")

def log_performance(operation: str, duration: float, context: Dict[str, Any] = None) -> None:
    """
    Log performance metrics
    """
    logger = get_logger()
    
    performance_info = {
        "operation": operation,
        "duration": f"{duration:.2f}s",
        "context": context
    }
    
    logger.info(f"Performance metric: {performance_info}")

def log_security(event: str, user: str = None, details: Dict[str, Any] = None) -> None:
    """
    Log security events
    """
    logger = get_logger()
    
    security_info = {
        "event": event,
        "user": user,
        "details": details
    }
    
    logger.warning(f"Security event: {security_info}")

def log_startup() -> None:
    """
    Log application startup information
    """
    logger = get_logger()
    
    startup_info = {
        "app_name": settings.APP_NAME,
        "environment": settings.APP_ENV,
        "debug_mode": settings.DEBUG,
        "api_version": settings.API_VERSION,
        "database": f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}",
        "features": {
            "cache": settings.ENABLE_CACHE,
            "notifications": settings.ENABLE_NOTIFICATIONS,
            "file_upload": settings.ENABLE_FILE_UPLOAD,
            "audit_log": settings.ENABLE_AUDIT_LOG
        }
    }
    
    logger.info(f"Application starting: {startup_info}")

def log_shutdown() -> None:
    """
    Log application shutdown information
    """
    logger = get_logger()
    logger.info("Application shutting down") 