from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QStackedWidget, QLabel, QErrorMessage, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from typing import Optional, List, Dict, Any, cast
from ..components.base import BaseButton, ResponsiveWidget
from ..components.reports import ReportGenerator
from .patient_view import PatientView
from .appointment_view import AppointmentView
from .examination_view import ExaminationView
from ..services.api import APIError, APIClient

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
            # สร้าง Central Widget
            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            
            # Layout หลัก
            main_layout = QHBoxLayout(central_widget)
            
            # Sidebar
            sidebar = self.create_sidebar()
            main_layout.addWidget(sidebar)
            
            # Content Area
            self.content_stack = QStackedWidget()
            self.setup_content_views()
            main_layout.addWidget(self.content_stack)
            
            # อัตราส่วน Sidebar:Content = 1:4
            main_layout.setStretch(0, 1)
            main_layout.setStretch(1, 4)

        except Exception as e:
            self.error_occurred.emit(f"เกิดข้อผิดพลาดในการสร้าง UI: {str(e)}")

    def create_sidebar(self) -> QWidget:
        try:
            sidebar = QWidget()
            sidebar.setObjectName("sidebar")
            layout = QVBoxLayout(sidebar)
            
            # Logo
            logo = QLabel("MediTech")
            logo.setObjectName("logo")
            layout.addWidget(logo)
            
            # Menu Buttons
            self.create_menu_buttons(layout)
            
            # Settings Button
            settings_btn = BaseButton("ตั้งค่า", variant="secondary")
            settings_btn.clicked.connect(self.show_settings)
            layout.addWidget(settings_btn)
            
            layout.addStretch()
            return sidebar
        except Exception as e:
            self.error_occurred.emit(f"เกิดข้อผิดพลาดในการสร้าง Sidebar: {str(e)}")
            return QWidget()

    def create_menu_buttons(self, layout: QVBoxLayout) -> None:
        try:
            # ปุ่มเมนูหลัก
            buttons = [
                ("ผู้ป่วย", self.show_patients),
                ("นัดหมาย", self.show_appointments),
                ("ผลตรวจ", self.show_examinations),
                ("รายงาน", self.show_reports)
            ]
            
            for text, slot in buttons:
                btn = BaseButton(text, variant="primary")
                btn.clicked.connect(slot)
                layout.addWidget(btn)
        except Exception as e:
            self.error_occurred.emit(f"เกิดข้อผิดพลาดในการสร้างปุ่มเมนู: {str(e)}")

    def setup_content_views(self) -> None:
        try:
            # สร้าง Views
            self.patient_view = PatientView()
            self.appointment_view = AppointmentView()
            self.examination_view = ExaminationView()
            self.report_view = ReportGenerator()
            
            if self.content_stack:
                # เพิ่มเข้า Stack
                self.content_stack.addWidget(self.patient_view)
                self.content_stack.addWidget(self.appointment_view)
                self.content_stack.addWidget(self.examination_view)
                self.content_stack.addWidget(self.report_view)

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
            if self.content_stack and self.patient_view:
                self.content_stack.setCurrentWidget(self.patient_view)
                self.set_state("viewing_patients")
        except Exception as e:
            self.error_occurred.emit(f"เกิดข้อผิดพลาดในการแสดงรายการผู้ป่วย: {str(e)}")

    def show_appointments(self) -> None:
        try:
            if self.content_stack and self.appointment_view:
                self.content_stack.setCurrentWidget(self.appointment_view)
                self.set_state("viewing_appointments")
        except Exception as e:
            self.error_occurred.emit(f"เกิดข้อผิดพลาดในการแสดงการนัดหมาย: {str(e)}")

    def show_examinations(self) -> None:
        try:
            if self.content_stack and self.examination_view:
                self.content_stack.setCurrentWidget(self.examination_view)
                self.set_state("viewing_examinations")
        except Exception as e:
            self.error_occurred.emit(f"เกิดข้อผิดพลาดในการแสดงผลการตรวจ: {str(e)}")

    def show_reports(self) -> None:
        try:
            if self.content_stack and self.report_view:
                self.content_stack.setCurrentWidget(self.report_view)
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