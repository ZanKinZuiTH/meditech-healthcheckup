from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel,
    QScrollArea, QWidget, QPushButton, QCalendarWidget
)
from PyQt6.QtCore import Qt, QDate, pyqtSignal
from PyQt6.QtGui import QIcon

from ...styles.theme import Theme

class AppointmentItem(QFrame):
    """รายการนัดหมาย"""
    
    clicked = pyqtSignal(dict)
    
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data
        self.setup_ui()
    
    def setup_ui(self):
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(f"""
            QFrame {{
                background: white;
                border: 1px solid {Theme.COLORS['grey'][200]};
                border-radius: {Theme.BORDER_RADIUS['md']};
                padding: {Theme.SPACING['md']}px;
                margin-bottom: {Theme.SPACING['sm']}px;
            }}
            QFrame:hover {{
                border-color: {Theme.COLORS['primary']['main']};
                background: {Theme.COLORS['primary'][50]};
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(Theme.SPACING['sm'])
        
        # เวลา
        time = QLabel(self.data['time'])
        time.setStyleSheet(f"""
            color: {Theme.COLORS['primary']['main']};
            font-size: {Theme.TYPOGRAPHY['fontSize']['sm']}px;
            font-weight: {Theme.TYPOGRAPHY['fontWeight']['medium']};
        """)
        layout.addWidget(time)
        
        # ชื่อผู้ป่วย
        patient = QLabel(self.data['patient_name'])
        patient.setStyleSheet(f"""
            color: {Theme.COLORS['grey'][900]};
            font-size: {Theme.TYPOGRAPHY['fontSize']['base']}px;
            font-weight: {Theme.TYPOGRAPHY['fontWeight']['medium']};
        """)
        layout.addWidget(patient)
        
        # รายละเอียด
        details = QLabel(self.data['details'])
        details.setStyleSheet(f"""
            color: {Theme.COLORS['grey'][600]};
            font-size: {Theme.TYPOGRAPHY['fontSize']['sm']}px;
        """)
        layout.addWidget(details)
        
        # สถานะ
        status_layout = QHBoxLayout()
        status_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        status = QLabel(self.data['status'])
        status.setStyleSheet(f"""
            color: {Theme.COLORS[self.data['status_color']]['main']};
            font-size: {Theme.TYPOGRAPHY['fontSize']['sm']}px;
            font-weight: {Theme.TYPOGRAPHY['fontWeight']['medium']};
            padding: {Theme.SPACING['xs']}px {Theme.SPACING['sm']}px;
            background: {Theme.COLORS[self.data['status_color']][50]};
            border-radius: {Theme.BORDER_RADIUS['full']};
        """)
        status_layout.addWidget(status)
        
        layout.addLayout(status_layout)
    
    def mousePressEvent(self, event):
        self.clicked.emit(self.data)

class AppointmentCalendar(QFrame):
    """ปฏิทินนัดหมาย"""
    
    date_selected = pyqtSignal(QDate)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        self.setStyleSheet(f"""
            QFrame {{
                background: white;
                border: 1px solid {Theme.COLORS['grey'][200]};
                border-radius: {Theme.BORDER_RADIUS['lg']};
                padding: {Theme.SPACING['md']}px;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(Theme.SPACING['md'])
        
        # หัวข้อ
        title = QLabel("ปฏิทินนัดหมาย")
        title.setStyleSheet(f"""
            color: {Theme.COLORS['grey'][900]};
            font-size: {Theme.TYPOGRAPHY['fontSize']['lg']}px;
            font-weight: {Theme.TYPOGRAPHY['fontWeight']['medium']};
        """)
        layout.addWidget(title)
        
        # ปฏิทิน
        calendar = QCalendarWidget()
        calendar.setStyleSheet(f"""
            QCalendarWidget QWidget {{
                alternate-background-color: {Theme.COLORS['grey'][50]};
            }}
            QCalendarWidget QAbstractItemView:enabled {{
                color: {Theme.COLORS['grey'][900]};
                selection-background-color: {Theme.COLORS['primary']['main']};
                selection-color: white;
            }}
            QCalendarWidget QAbstractItemView:disabled {{
                color: {Theme.COLORS['grey'][400]};
            }}
        """)
        calendar.clicked.connect(self.date_selected.emit)
        layout.addWidget(calendar)

class AppointmentList(QFrame):
    """รายการนัดหมาย"""
    
    def __init__(self, appointments=None, parent=None):
        super().__init__(parent)
        self.appointments = appointments or []
        self.setup_ui()
    
    def setup_ui(self):
        self.setStyleSheet(f"""
            QFrame {{
                background: white;
                border: 1px solid {Theme.COLORS['grey'][200]};
                border-radius: {Theme.BORDER_RADIUS['lg']};
                padding: {Theme.SPACING['md']}px;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(Theme.SPACING['md'])
        
        # หัวข้อ
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        title = QLabel("การนัดหมายวันนี้")
        title.setStyleSheet(f"""
            color: {Theme.COLORS['grey'][900]};
            font-size: {Theme.TYPOGRAPHY['fontSize']['lg']}px;
            font-weight: {Theme.TYPOGRAPHY['fontWeight']['medium']};
        """)
        header_layout.addWidget(title)
        
        add_button = QPushButton("เพิ่มนัดหมาย")
        add_button.setStyleSheet(f"""
            QPushButton {{
                background: {Theme.COLORS['primary']['main']};
                color: white;
                border: none;
                padding: {Theme.SPACING['sm']}px {Theme.SPACING['lg']}px;
                border-radius: {Theme.BORDER_RADIUS['md']};
                font-weight: {Theme.TYPOGRAPHY['fontWeight']['medium']};
            }}
            QPushButton:hover {{
                background: {Theme.COLORS['primary']['dark']};
            }}
        """)
        header_layout.addWidget(add_button)
        
        layout.addWidget(header)
        
        # รายการนัดหมาย
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
            }
        """)
        
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        for appointment in self.appointments:
            item = AppointmentItem(appointment)
            content_layout.addWidget(item)
        
        if not self.appointments:
            empty = QLabel("ไม่มีการนัดหมาย")
            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty.setStyleSheet(f"""
                color: {Theme.COLORS['grey'][500]};
                padding: {Theme.SPACING['xl']}px;
            """)
            content_layout.addWidget(empty)
        
        content_layout.addStretch()
        scroll.setWidget(content)
        layout.addWidget(scroll)
    
    def add_appointment(self, appointment):
        """เพิ่มการนัดหมายใหม่"""
        item = AppointmentItem(appointment)
        content = self.findChild(QScrollArea).widget()
        
        # ลบข้อความ "ไม่มีการนัดหมาย" ถ้ามี
        if content.layout().count() == 2:  # มีแค่ข้อความว่างและ stretch
            content.layout().itemAt(0).widget().deleteLater()
        
        content.layout().insertWidget(content.layout().count() - 1, item)
    
    def clear_appointments(self):
        """ล้างการนัดหมายทั้งหมด"""
        content = self.findChild(QScrollArea).widget()
        
        # ลบทุกรายการยกเว้น stretch
        for i in reversed(range(content.layout().count() - 1)):
            content.layout().itemAt(i).widget().deleteLater()
        
        # เพิ่มข้อความว่าง
        empty = QLabel("ไม่มีการนัดหมาย")
        empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        empty.setStyleSheet(f"""
            color: {Theme.COLORS['grey'][500]};
            padding: {Theme.SPACING['xl']}px;
        """)
        content.layout().insertWidget(0, empty) 