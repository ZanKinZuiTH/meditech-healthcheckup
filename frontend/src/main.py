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
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt, QThread
from typing import Optional

from .views.main_window import MainWindow
from .services.api import APIClient
from .utils.theme import Theme
from .utils.config import settings

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
        
        # ตั้งค่า Application
        self.setApplicationName("MediTech")
        self.setApplicationVersion("1.0.0")
        
        # เตรียม Services
        self._init_services()
        
        # ตั้งค่า Theme
        self._init_theme()
        
        # สร้าง Main Window
        self.main_window: Optional[MainWindow] = None
        self._init_main_window()
    
    def _init_services(self):
        """
        เตรียม Services ต่างๆ:
        - API Client
        - Database Connection
        - Authentication
        """
        self.api = APIClient(settings.API_URL)
    
    def _init_theme(self):
        """
        ตั้งค่า Theme ของแอพพลิเคชัน:
        - สี
        - ฟอนต์
        - ไอคอน
        - สไตล์
        """
        self.theme = Theme()
        self.setStyleSheet(self.theme.stylesheet)
    
    def _init_main_window(self):
        """
        สร้างและแสดง Main Window:
        - ตั้งค่า UI
        - เชื่อมต่อ Signals
        - จัดการ Layout
        """
        self.main_window = MainWindow(self.api)
        self.main_window.show()
    
    def run(self) -> int:
        """
        รันแอพพลิเคชัน
        
        Returns:
            int: Exit code
        """
        return self.exec()

def main():
    """
    ฟังก์ชันหลักสำหรับเริ่มต้นแอพพลิเคชัน
    
    Flow การทำงาน:
    1. สร้าง Application Instance
    2. ตั้งค่าระบบ
    3. แสดง UI
    4. รันแอพพลิเคชัน
    """
    app = MediTechApp(sys.argv)
    return app.run()

if __name__ == "__main__":
    sys.exit(main()) 