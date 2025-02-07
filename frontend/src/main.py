# Frontend Main Application
# ====================
#
# ไฟล์นี้เป็นจุดเริ่มต้นของ Frontend Application โดยใช้ PyQt6
# เหมาะสำหรับการศึกษาเรื่อง:
# 1. การสร้าง Desktop Application
# 2. การออกแบบ UI/UX
# 3. การเชื่อมต่อกับ API
# 4. การจัดการ State
#
# การเรียนรู้:
# - ศึกษาการทำงานของ QApplication
# - เข้าใจระบบ Signal/Slot
# - วิธีการจัดการ UI Components
# - การทำ Responsive Design
#
# Tips:
# - ใช้ Qt Designer สำหรับออกแบบ UI
# - แยก Business Logic ออกจาก UI
# - ใช้ Threading สำหรับงานหนัก
# - จัดการ Error ให้ดี

import sys
import logging
import asyncio
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt, QThread, QTimer
from typing import Optional
import traceback

from .views.main_window import MainWindow
from .services.api import APIClient
from .utils.theme import Theme
from .utils.config import settings
from .utils.cache import Cache

# Setup logging with more detailed configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('frontend.log', encoding='utf-8')
    ]
)

logger = logging.getLogger(__name__)

class MediTechApp(QApplication):
    """
    แอพพลิเคชันหลักของระบบ MediTech
    
    คลาสนี้จัดการ:
    1. การเริ่มต้นระบบ
    2. การตั้งค่า Theme
    3. การเชื่อมต่อ API
    4. การจัดการ Window หลัก
    """
    
    def __init__(self, argv):
        """
        เริ่มต้นแอพพลิเคชัน
        
        Args:
            argv: Command line arguments
        """
        super().__init__(argv)
        
        # Global exception handler
        sys.excepthook = self.handle_exception
        
        # Initialize cache
        self.cache = Cache()
        
        # Performance monitoring
        self.start_time = None
        self.performance_timer = QTimer()
        self.performance_timer.timeout.connect(self.monitor_performance)
        self.performance_timer.start(60000)  # Monitor every minute
        
        try:
            self._init_services()
            self._init_theme()
            self._init_main_window()
            logger.info("Application initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize application: {str(e)}")
            self.handle_critical_error(e)
    
    def handle_exception(self, exc_type, exc_value, exc_traceback):
        """Global exception handler"""
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        
        logger.error("Uncaught exception:", exc_info=(exc_type, exc_value, exc_traceback))
    
    def handle_critical_error(self, error):
        """Handle critical errors that prevent app from starting"""
        from PyQt6.QtWidgets import QMessageBox
        
        error_msg = QMessageBox()
        error_msg.setIcon(QMessageBox.Icon.Critical)
        error_msg.setText("เกิดข้อผิดพลาดร้ายแรง")
        error_msg.setInformativeText(str(error))
        error_msg.setDetailedText(traceback.format_exc())
        error_msg.exec()
        
        self.quit()
    
    def monitor_performance(self):
        """Monitor application performance"""
        import psutil
        process = psutil.Process()
        
        # Log memory usage
        memory_info = process.memory_info()
        logger.info(f"Memory usage: {memory_info.rss / 1024 / 1024:.2f} MB")
        
        # Log CPU usage
        cpu_percent = process.cpu_percent()
        logger.info(f"CPU usage: {cpu_percent}%")
        
        # Check response time
        if hasattr(self, 'main_window'):
            response_time = self.main_window.get_average_response_time()
            logger.info(f"Average response time: {response_time:.2f}ms")
    
    async def _init_services(self):
        """Initialize services asynchronously"""
        try:
            self.api = await APIClient.create(settings.API_URL)
            logger.info("API client initialized successfully")
            
            # Warm up cache
            await self.cache.preload_common_data(self.api)
            logger.info("Cache warmed up successfully")
        except Exception as e:
            logger.error(f"Failed to initialize services: {str(e)}")
            raise
    
    def _init_theme(self):
        """Initialize application theme with error handling"""
        try:
            self.theme = Theme()
            self.setStyleSheet(self.theme.stylesheet)
            
            # Monitor theme changes
            self.theme.changed.connect(self.handle_theme_change)
            logger.info("Theme initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize theme: {str(e)}")
            raise
    
    def handle_theme_change(self):
        """Handle theme changes dynamically"""
        try:
            self.setStyleSheet(self.theme.stylesheet)
            if hasattr(self, 'main_window'):
                self.main_window.refresh_style()
        except Exception as e:
            logger.error(f"Failed to update theme: {str(e)}")
    
    def _init_main_window(self):
        """Initialize main window with performance monitoring"""
        try:
            self.start_time = self.currentTime()
            self.main_window = MainWindow(self.api, self.cache)
            self.main_window.show()
            
            # Log startup time
            startup_time = self.currentTime() - self.start_time
            logger.info(f"Main window initialized in {startup_time}ms")
        except Exception as e:
            logger.error(f"Failed to initialize main window: {str(e)}")
            raise
    
    def run(self) -> int:
        """Run application with comprehensive error handling"""
        try:
            logger.info("Starting application main loop")
            return self.exec()
        except Exception as e:
            logger.error(f"Application error: {str(e)}")
            self.handle_critical_error(e)
            return 1
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Cleanup resources before shutdown"""
        try:
            if hasattr(self, 'api'):
                asyncio.run(self.api.close())
            if hasattr(self, 'cache'):
                self.cache.clear()
            logger.info("Application cleanup completed")
        except Exception as e:
            logger.error(f"Cleanup error: {str(e)}")

def main():
    """Main entry point with proper initialization"""
    try:
        # Set application attributes
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling)
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)
        
        app = MediTechApp(sys.argv)
        return app.run()
    except Exception as e:
        logger.critical(f"Fatal error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 