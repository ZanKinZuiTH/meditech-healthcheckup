from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QStackedWidget, QLabel, QErrorMessage, QMessageBox, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QFont
from typing import Optional, List, Dict, Any, cast
from ..styles.theme import Theme
from ..components.base import BaseButton, ResponsiveWidget, Card
from ..components.reports import ReportGenerator
from .patient_view import PatientView
from .appointment_view import AppointmentView
from .examination_view import ExaminationView
from ..services.api import APIError, APIClient
from ..components.sidebar import Sidebar
from ..components.header import Header

class MainWindow(QMainWindow):
    error_occurred = pyqtSignal(str)  # Signal for error handling
    state_changed = pyqtSignal(str)   # Signal for state changes

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("MediTech HealthCheckup System")
        self.current_state = "idle"
        self.api_client: Optional[APIClient] = None
        self.content_stack: Optional[QStackedWidget] = None
        self.patient_view: Optional[PatientView] = None
        self.appointment_view: Optional[AppointmentView] = None
        self.examination_view: Optional[ExaminationView] = None
        self.report_view: Optional[ReportGenerator] = None
        self.error_message: Optional[QErrorMessage] = None
        
        self.setup_error_handling()
        self.setup_ui()

    def setup_error_handling(self) -> None:
        self.error_occurred.connect(self.show_error_dialog)
        self.error_message = QErrorMessage(self)
        self.error_message.setMinimumSize(400, 200)

    def show_error_dialog(self, message: str) -> None:
        if self.error_message:
            self.error_message.showMessage(message)

    def show_confirmation_dialog(self, message: str) -> bool:
        reply = QMessageBox.question(
            self,
            'ยืนยัน',
            message,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        return reply == QMessageBox.StandardButton.Yes

    def set_state(self, new_state: str) -> None:
        if new_state != self.current_state:
            self.current_state = new_state
            self.state_changed.emit(new_state)

    def setup_ui(self) -> None:
        try:
            # ตั้งค่าขนาดหน้าจอ
            self.resize(1280, 800)
            self.setMinimumSize(1024, 768)
            
            # สร้าง Central Widget
            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            
            # Layout หลัก
            main_layout = QHBoxLayout(central_widget)
            main_layout.setContentsMargins(0, 0, 0, 0)
            main_layout.setSpacing(0)
            
            # Sidebar
            self.sidebar = Sidebar(self)
            main_layout.addWidget(self.sidebar)
            
            # Container สำหรับ content
            content_container = QWidget()
            content_layout = QVBoxLayout(content_container)
            content_layout.setContentsMargins(0, 0, 0, 0)
            content_layout.setSpacing(0)
            main_layout.addWidget(content_container)
            
            # Header
            self.header = Header(self)
            content_layout.addWidget(self.header)
            
            # Content Area
            content_area = QWidget()
            content_area.setObjectName("contentArea")
            content_area_layout = QVBoxLayout(content_area)
            content_area_layout.setContentsMargins(
                Theme.SPACING['xl'],
                Theme.SPACING['xl'],
                Theme.SPACING['xl'],
                Theme.SPACING['xl']
            )
            content_layout.addWidget(content_area)
            
            # Stacked Widget สำหรับหน้าต่างๆ
            self.stacked_widget = QStackedWidget()
            content_area_layout.addWidget(self.stacked_widget)
            
            # สไตล์
            self.setup_style()
            
            self.setup_content_views()

        except Exception as e:
            self.error_occurred.emit(f"เกิดข้อผิดพลาดในการสร้าง UI: {str(e)}")

    def setup_style(self):
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {Theme.COLORS['grey'][100]};
            }}
            
            #contentArea {{
                background-color: {Theme.COLORS['grey'][100]};
            }}
            
            QLabel#pageTitle {{
                color: {Theme.COLORS['grey'][900]};
                font-size: {Theme.TYPOGRAPHY['fontSize']['2xl']}px;
                font-weight: {Theme.TYPOGRAPHY['fontWeight']['bold']};
            }}
            
            QLabel#pageDescription {{
                color: {Theme.COLORS['grey'][600]};
                font-size: {Theme.TYPOGRAPHY['fontSize']['base']}px;
            }}
        """)

    def add_page(self, widget, name):
        """เพิ่มหน้าใหม่เข้าไปใน stacked widget"""
        self.stacked_widget.addWidget(widget)
        widget.setObjectName(name)
    
    def show_page(self, name):
        """แสดงหน้าตามชื่อที่กำหนด"""
        for i in range(self.stacked_widget.count()):
            if self.stacked_widget.widget(i).objectName() == name:
                self.stacked_widget.setCurrentIndex(i)
                break
    
    def set_page_title(self, title, description=""):
        """ตั้งค่าชื่อและคำอธิบายของหน้า"""
        self.header.set_title(title, description)

    def setup_content_views(self) -> None:
        try:
            # สร้าง Views
            self.patient_view = PatientView()
            self.appointment_view = AppointmentView()
            self.examination_view = ExaminationView()
            self.report_view = ReportGenerator()
            
            if self.stacked_widget:
                # เพิ่มเข้า Stack
                self.stacked_widget.addWidget(self.patient_view)
                self.stacked_widget.addWidget(self.appointment_view)
                self.stacked_widget.addWidget(self.examination_view)
                self.stacked_widget.addWidget(self.report_view)

                # เชื่อมต่อ error signals
                self.patient_view.error_occurred.connect(self.show_error_dialog)
                self.appointment_view.error_occurred.connect(self.show_error_dialog)
                self.examination_view.error_occurred.connect(self.show_error_dialog)
                self.report_view.error_occurred.connect(self.show_error_dialog)

        except Exception as e:
            self.error_occurred.emit(f"เกิดข้อผิดพลาดในการสร้าง Content Views: {str(e)}")

    def set_api_client(self, client: APIClient) -> None:
        self.api_client = client
        if self.patient_view:
            self.patient_view.set_api_client(client)
        if self.appointment_view:
            self.appointment_view.set_api_client(client)
        if self.examination_view:
            self.examination_view.set_api_client(client)
        if self.report_view:
            self.report_view.set_api_client(client)

    # Slot functions with error handling
    def show_patients(self) -> None:
        try:
            if self.stacked_widget and self.patient_view:
                self.stacked_widget.setCurrentWidget(self.patient_view)
                self.set_state("viewing_patients")
        except Exception as e:
            self.error_occurred.emit(f"เกิดข้อผิดพลาดในการแสดงรายการผู้ป่วย: {str(e)}")

    def show_appointments(self) -> None:
        try:
            if self.stacked_widget and self.appointment_view:
                self.stacked_widget.setCurrentWidget(self.appointment_view)
                self.set_state("viewing_appointments")
        except Exception as e:
            self.error_occurred.emit(f"เกิดข้อผิดพลาดในการแสดงการนัดหมาย: {str(e)}")

    def show_examinations(self) -> None:
        try:
            if self.stacked_widget and self.examination_view:
                self.stacked_widget.setCurrentWidget(self.examination_view)
                self.set_state("viewing_examinations")
        except Exception as e:
            self.error_occurred.emit(f"เกิดข้อผิดพลาดในการแสดงผลการตรวจ: {str(e)}")

    def show_reports(self) -> None:
        try:
            if self.stacked_widget and self.report_view:
                self.stacked_widget.setCurrentWidget(self.report_view)
                self.set_state("viewing_reports")
        except Exception as e:
            self.error_occurred.emit(f"เกิดข้อผิดพลาดในการแสดงรายงาน: {str(e)}")

    def show_settings(self) -> None:
        try:
            # TODO: Implement settings view
            self.set_state("viewing_settings")
        except Exception as e:
            self.error_occurred.emit(f"เกิดข้อผิดพลาดในการแสดงการตั้งค่า: {str(e)}")

    def closeEvent(self, event: Any) -> None:
        """Handle application shutdown"""
        try:
            if self.show_confirmation_dialog("ต้องการปิดโปรแกรมหรือไม่?"):
                # Cleanup code here
                if self.api_client:
                    event.accept()
            else:
                event.ignore()
        except Exception as e:
            self.error_occurred.emit(f"เกิดข้อผิดพลาดในการปิดโปรแกรม: {str(e)}")
            event.accept() 