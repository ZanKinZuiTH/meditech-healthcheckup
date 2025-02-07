from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QComboBox, QSpinBox, QCheckBox,
    QPushButton, QTabWidget, QWidget, QFormLayout,
    QColorDialog, QFileDialog
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QColor

from ...styles.theme import Theme

class SettingsTab(QWidget):
    """แท็บตั้งค่าพื้นฐาน"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QFormLayout(self)
        layout.setSpacing(Theme.SPACING['lg'])
        layout.setContentsMargins(
            Theme.SPACING['xl'],
            Theme.SPACING['xl'],
            Theme.SPACING['xl'],
            Theme.SPACING['xl']
        )
        
        # ชื่อคลินิก
        clinic_name = QLineEdit()
        clinic_name.setStyleSheet(self.get_input_style())
        layout.addRow(self.create_label("ชื่อคลินิก"), clinic_name)
        
        # ที่อยู่
        address = QLineEdit()
        address.setStyleSheet(self.get_input_style())
        layout.addRow(self.create_label("ที่อยู่"), address)
        
        # เบอร์โทรศัพท์
        phone = QLineEdit()
        phone.setStyleSheet(self.get_input_style())
        layout.addRow(self.create_label("เบอร์โทรศัพท์"), phone)
        
        # อีเมล
        email = QLineEdit()
        email.setStyleSheet(self.get_input_style())
        layout.addRow(self.create_label("อีเมล"), email)
        
        # โลโก้
        logo_layout = QHBoxLayout()
        logo_preview = QLabel("ไม่ได้เลือกไฟล์")
        logo_preview.setStyleSheet(f"""
            color: {Theme.COLORS['grey'][500]};
        """)
        logo_layout.addWidget(logo_preview)
        
        logo_button = QPushButton("เลือกไฟล์")
        logo_button.setStyleSheet(self.get_button_style())
        logo_button.clicked.connect(lambda: QFileDialog.getOpenFileName(
            self, "เลือกโลโก้", "", "Images (*.png *.jpg *.jpeg)"
        ))
        logo_layout.addWidget(logo_button)
        
        layout.addRow(self.create_label("โลโก้"), logo_layout)
    
    def create_label(self, text):
        """สร้างป้ายกำกับ"""
        label = QLabel(text)
        label.setStyleSheet(f"""
            color: {Theme.COLORS['grey'][700]};
            font-weight: {Theme.TYPOGRAPHY['fontWeight']['medium']};
        """)
        return label
    
    def get_input_style(self):
        """สไตล์สำหรับ input"""
        return f"""
            padding: {Theme.SPACING['sm']}px;
            border: 1px solid {Theme.COLORS['grey'][300]};
            border-radius: {Theme.BORDER_RADIUS['md']};
            background: white;
            min-width: 300px;
        """
    
    def get_button_style(self):
        """สไตล์สำหรับปุ่ม"""
        return f"""
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
        """

class AppearanceTab(QWidget):
    """แท็บตั้งค่าการแสดงผล"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QFormLayout(self)
        layout.setSpacing(Theme.SPACING['lg'])
        layout.setContentsMargins(
            Theme.SPACING['xl'],
            Theme.SPACING['xl'],
            Theme.SPACING['xl'],
            Theme.SPACING['xl']
        )
        
        # ธีม
        theme = QComboBox()
        theme.addItems(["สว่าง", "มืด", "ระบบ"])
        theme.setStyleSheet(self.get_input_style())
        layout.addRow(self.create_label("ธีม"), theme)
        
        # สีหลัก
        color_layout = QHBoxLayout()
        color_preview = QLabel()
        color_preview.setStyleSheet(f"""
            background: {Theme.COLORS['primary']['main']};
            min-width: 24px;
            min-height: 24px;
            border-radius: {Theme.BORDER_RADIUS['sm']};
        """)
        color_layout.addWidget(color_preview)
        
        color_button = QPushButton("เลือกสี")
        color_button.setStyleSheet(self.get_button_style())
        color_button.clicked.connect(lambda: QColorDialog.getColor())
        color_layout.addWidget(color_button)
        
        layout.addRow(self.create_label("สีหลัก"), color_layout)
        
        # ขนาดตัวอักษร
        font_size = QSpinBox()
        font_size.setRange(12, 24)
        font_size.setValue(16)
        font_size.setStyleSheet(self.get_input_style())
        layout.addRow(self.create_label("ขนาดตัวอักษร"), font_size)
        
        # การแจ้งเตือน
        notifications = QCheckBox("เปิดการแจ้งเตือน")
        notifications.setStyleSheet(f"""
            color: {Theme.COLORS['grey'][700]};
        """)
        layout.addRow("", notifications)
        
        # เสียงแจ้งเตือน
        sound = QCheckBox("เปิดเสียงแจ้งเตือน")
        sound.setStyleSheet(f"""
            color: {Theme.COLORS['grey'][700]};
        """)
        layout.addRow("", sound)
    
    def create_label(self, text):
        """สร้างป้ายกำกับ"""
        label = QLabel(text)
        label.setStyleSheet(f"""
            color: {Theme.COLORS['grey'][700]};
            font-weight: {Theme.TYPOGRAPHY['fontWeight']['medium']};
        """)
        return label
    
    def get_input_style(self):
        """สไตล์สำหรับ input"""
        return f"""
            padding: {Theme.SPACING['sm']}px;
            border: 1px solid {Theme.COLORS['grey'][300]};
            border-radius: {Theme.BORDER_RADIUS['md']};
            background: white;
            min-width: 300px;
        """
    
    def get_button_style(self):
        """สไตล์สำหรับปุ่ม"""
        return f"""
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
        """

class SettingsDialog(QFrame):
    """หน้าต่างตั้งค่า"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        self.setStyleSheet(f"""
            QFrame {{
                background: white;
                border: 1px solid {Theme.COLORS['grey'][200]};
                border-radius: {Theme.BORDER_RADIUS['lg']};
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # แท็บ
        tabs = QTabWidget()
        tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border: none;
            }}
            QTabBar::tab {{
                padding: {Theme.SPACING['md']}px {Theme.SPACING['lg']}px;
                color: {Theme.COLORS['grey'][600]};
                border: none;
                background: transparent;
            }}
            QTabBar::tab:selected {{
                color: {Theme.COLORS['primary']['main']};
                border-bottom: 2px solid {Theme.COLORS['primary']['main']};
            }}
            QTabBar::tab:hover {{
                color: {Theme.COLORS['primary']['main']};
            }}
        """)
        
        tabs.addTab(SettingsTab(), "ตั้งค่าทั่วไป")
        tabs.addTab(AppearanceTab(), "การแสดงผล")
        
        layout.addWidget(tabs)
        
        # ปุ่มดำเนินการ
        buttons = QWidget()
        buttons.setStyleSheet(f"""
            background: {Theme.COLORS['grey'][50]};
            border-top: 1px solid {Theme.COLORS['grey'][200]};
        """)
        
        button_layout = QHBoxLayout(buttons)
        button_layout.setContentsMargins(
            Theme.SPACING['xl'],
            Theme.SPACING['lg'],
            Theme.SPACING['xl'],
            Theme.SPACING['lg']
        )
        
        save = QPushButton("บันทึก")
        save.setStyleSheet(f"""
            QPushButton {{
                background: {Theme.COLORS['primary']['main']};
                color: white;
                border: none;
                padding: {Theme.SPACING['sm']}px {Theme.SPACING['xl']}px;
                border-radius: {Theme.BORDER_RADIUS['md']};
                font-weight: {Theme.TYPOGRAPHY['fontWeight']['medium']};
            }}
            QPushButton:hover {{
                background: {Theme.COLORS['primary']['dark']};
            }}
        """)
        button_layout.addWidget(save)
        
        cancel = QPushButton("ยกเลิก")
        cancel.setStyleSheet(f"""
            QPushButton {{
                background: white;
                color: {Theme.COLORS['grey'][700]};
                border: 1px solid {Theme.COLORS['grey'][300]};
                padding: {Theme.SPACING['sm']}px {Theme.SPACING['xl']}px;
                border-radius: {Theme.BORDER_RADIUS['md']};
            }}
            QPushButton:hover {{
                background: {Theme.COLORS['grey'][50]};
            }}
        """)
        button_layout.addWidget(cancel)
        
        layout.addWidget(buttons) 