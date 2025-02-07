from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QSpacerItem,
    QSizePolicy, QPushButton
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QPixmap
from ..styles.theme import Theme

class MenuButton(QPushButton):
    """ปุ่มเมนูที่มีการออกแบบเฉพาะสำหรับ Sidebar"""
    
    def __init__(self, text, icon_path=None, parent=None):
        super().__init__(text, parent)
        if icon_path:
            self.setIcon(QIcon(icon_path))
        self.setCheckable(True)
        self.setup_style()
    
    def setup_style(self):
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {Theme.COLORS['grey'][300]};
                text-align: left;
                padding: {Theme.SPACING['base']}px;
                border: none;
                border-radius: {Theme.BORDER_RADIUS['base']};
                font-size: {Theme.TYPOGRAPHY['fontSize']['base']}px;
                font-weight: {Theme.TYPOGRAPHY['fontWeight']['medium']};
            }}
            QPushButton:hover {{
                background-color: {Theme.COLORS['grey'][800]};
                color: {Theme.COLORS['grey'][100]};
            }}
            QPushButton:checked {{
                background-color: {Theme.COLORS['primary']['main']};
                color: {Theme.COLORS['primary']['contrast']};
            }}
        """)

class Sidebar(QWidget):
    """Sidebar สำหรับการนำทางในแอปพลิเคชัน"""
    
    page_changed = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        self.setFixedWidth(280)
        self.setObjectName("sidebar")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            Theme.SPACING['lg'],
            Theme.SPACING['xl'],
            Theme.SPACING['lg'],
            Theme.SPACING['xl']
        )
        layout.setSpacing(Theme.SPACING['lg'])
        
        # Logo
        logo_container = QWidget()
        logo_layout = QVBoxLayout(logo_container)
        logo_layout.setContentsMargins(0, 0, 0, Theme.SPACING['xl'])
        
        logo = QLabel()
        logo.setPixmap(QPixmap("resources/images/logo.png").scaledToWidth(180, Qt.TransformationMode.SmoothTransformation))
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.addWidget(logo)
        
        app_name = QLabel("MediTech")
        app_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        app_name.setStyleSheet(f"""
            color: {Theme.COLORS['grey'][100]};
            font-size: {Theme.TYPOGRAPHY['fontSize']['xl']}px;
            font-weight: {Theme.TYPOGRAPHY['fontWeight']['bold']};
        """)
        logo_layout.addWidget(app_name)
        
        layout.addWidget(logo_container)
        
        # เมนูหลัก
        menu_label = QLabel("เมนูหลัก")
        menu_label.setStyleSheet(f"""
            color: {Theme.COLORS['grey'][500]};
            font-size: {Theme.TYPOGRAPHY['fontSize']['sm']}px;
            font-weight: {Theme.TYPOGRAPHY['fontWeight']['medium']};
            padding-left: {Theme.SPACING['sm']}px;
        """)
        layout.addWidget(menu_label)
        
        # ปุ่มเมนู
        self.menu_buttons = {}
        menu_items = [
            ("dashboard", "แดชบอร์ด", "resources/icons/dashboard.svg"),
            ("patients", "ผู้ป่วย", "resources/icons/patients.svg"),
            ("appointments", "นัดหมาย", "resources/icons/calendar.svg"),
            ("examinations", "ผลตรวจ", "resources/icons/examination.svg"),
            ("reports", "รายงาน", "resources/icons/report.svg"),
        ]
        
        for page_id, text, icon in menu_items:
            btn = MenuButton(text, icon)
            btn.clicked.connect(lambda checked, p=page_id: self.handle_page_change(p))
            layout.addWidget(btn)
            self.menu_buttons[page_id] = btn
        
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        # เมนูล่าง
        bottom_menu_label = QLabel("ระบบ")
        bottom_menu_label.setStyleSheet(f"""
            color: {Theme.COLORS['grey'][500]};
            font-size: {Theme.TYPOGRAPHY['fontSize']['sm']}px;
            font-weight: {Theme.TYPOGRAPHY['fontWeight']['medium']};
            padding-left: {Theme.SPACING['sm']}px;
        """)
        layout.addWidget(bottom_menu_label)
        
        # ปุ่มตั้งค่าและออกจากระบบ
        settings_btn = MenuButton("ตั้งค่า", "resources/icons/settings.svg")
        settings_btn.clicked.connect(lambda: self.handle_page_change("settings"))
        layout.addWidget(settings_btn)
        
        logout_btn = MenuButton("ออกจากระบบ", "resources/icons/logout.svg")
        logout_btn.clicked.connect(self.handle_logout)
        layout.addWidget(logout_btn)
        
        self.setStyleSheet(f"""
            #sidebar {{
                background-color: {Theme.COLORS['grey'][900]};
                border-right: 1px solid {Theme.COLORS['grey'][800]};
            }}
        """)
    
    def handle_page_change(self, page_id):
        """จัดการการเปลี่ยนหน้า"""
        # ยกเลิกการเลือกปุ่มอื่นๆ
        for btn in self.menu_buttons.values():
            btn.setChecked(False)
        
        # เลือกปุ่มปัจจุบัน
        if page_id in self.menu_buttons:
            self.menu_buttons[page_id].setChecked(True)
        
        self.page_changed.emit(page_id)
    
    def handle_logout(self):
        """จัดการการออกจากระบบ"""
        # TODO: เพิ่มการจัดการออกจากระบบ
        pass 