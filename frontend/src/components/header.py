from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel,
    QPushButton, QFrame, QMenu
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from ..styles.theme import Theme

class Header(QWidget):
    """Header สำหรับแสดงชื่อหน้าและเครื่องมือต่างๆ"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        self.setObjectName("header")
        self.setFixedHeight(80)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(
            Theme.SPACING['xl'],
            Theme.SPACING['lg'],
            Theme.SPACING['xl'],
            Theme.SPACING['lg']
        )
        
        # ส่วนซ้าย (ชื่อหน้าและคำอธิบาย)
        left_container = QWidget()
        left_layout = QVBoxLayout(left_container)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(Theme.SPACING['xs'])
        
        self.title_label = QLabel()
        self.title_label.setObjectName("pageTitle")
        left_layout.addWidget(self.title_label)
        
        self.description_label = QLabel()
        self.description_label.setObjectName("pageDescription")
        left_layout.addWidget(self.description_label)
        
        layout.addWidget(left_container)
        
        # ส่วนขวา (ปุ่มและเครื่องมือ)
        right_container = QWidget()
        right_layout = QHBoxLayout(right_container)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(Theme.SPACING['base'])
        
        # ปุ่มแจ้งเตือน
        notification_btn = HeaderButton("resources/icons/notification.svg")
        notification_btn.setToolTip("การแจ้งเตือน")
        right_layout.addWidget(notification_btn)
        
        # ปุ่มโปรไฟล์
        profile_btn = HeaderButton("resources/icons/user.svg")
        profile_btn.setToolTip("โปรไฟล์")
        profile_menu = QMenu(profile_btn)
        profile_menu.setStyleSheet(f"""
            QMenu {{
                background-color: {Theme.COLORS['grey'][100]};
                border: 1px solid {Theme.COLORS['grey'][300]};
                border-radius: {Theme.BORDER_RADIUS['base']};
                padding: {Theme.SPACING['xs']}px;
            }}
            QMenu::item {{
                padding: {Theme.SPACING['sm']}px {Theme.SPACING['base']}px;
                border-radius: {Theme.BORDER_RADIUS['sm']};
            }}
            QMenu::item:selected {{
                background-color: {Theme.COLORS['primary']['light']};
                color: {Theme.COLORS['primary']['main']};
            }}
        """)
        profile_menu.addAction("ข้อมูลส่วนตัว")
        profile_menu.addAction("เปลี่ยนรหัสผ่าน")
        profile_menu.addSeparator()
        profile_menu.addAction("ออกจากระบบ")
        profile_btn.setMenu(profile_menu)
        right_layout.addWidget(profile_btn)
        
        layout.addWidget(right_container)
        
        # สไตล์
        self.setStyleSheet(f"""
            #header {{
                background-color: {Theme.COLORS['grey'][100]};
                border-bottom: 1px solid {Theme.COLORS['grey'][200]};
            }}
            
            #pageTitle {{
                color: {Theme.COLORS['grey'][900]};
                font-size: {Theme.TYPOGRAPHY['fontSize']['2xl']}px;
                font-weight: {Theme.TYPOGRAPHY['fontWeight']['bold']};
            }}
            
            #pageDescription {{
                color: {Theme.COLORS['grey'][600]};
                font-size: {Theme.TYPOGRAPHY['fontSize']['base']}px;
            }}
        """)
    
    def set_title(self, title, description=""):
        """ตั้งค่าชื่อและคำอธิบายของหน้า"""
        self.title_label.setText(title)
        self.description_label.setText(description)

class HeaderButton(QPushButton):
    """ปุ่มที่ใช้ใน Header"""
    
    def __init__(self, icon_path, parent=None):
        super().__init__(parent)
        self.setIcon(QIcon(icon_path))
        self.setup_style()
    
    def setup_style(self):
        size = Theme.SPACING['xl']
        self.setFixedSize(size, size)
        self.setIconSize(QIcon().actualSize(self.size()))
        
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                border-radius: {Theme.BORDER_RADIUS['full']};
                padding: {Theme.SPACING['xs']}px;
            }}
            
            QPushButton:hover {{
                background-color: {Theme.COLORS['grey'][200]};
            }}
            
            QPushButton:pressed {{
                background-color: {Theme.COLORS['grey'][300]};
            }}
        """) 