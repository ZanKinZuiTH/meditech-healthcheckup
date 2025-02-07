from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel,
    QScrollArea, QWidget, QPushButton
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon

from ...styles.theme import Theme

class NotificationItem(QFrame):
    """รายการแจ้งเตือน"""
    
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
                border-bottom: 1px solid {Theme.COLORS['grey'][200]};
                padding: {Theme.SPACING['md']}px;
            }}
            QFrame:hover {{
                background: {Theme.COLORS['grey'][50]};
            }}
        """)
        
        layout = QHBoxLayout(self)
        layout.setSpacing(Theme.SPACING['md'])
        
        # ไอคอน
        if self.data.get('icon'):
            icon = QLabel()
            icon.setPixmap(self.data['icon'].pixmap(24, 24))
            layout.addWidget(icon)
        
        # เนื้อหา
        content = QVBoxLayout()
        content.setSpacing(Theme.SPACING['xs'])
        
        title = QLabel(self.data['title'])
        title.setStyleSheet(f"""
            color: {Theme.COLORS['grey'][900]};
            font-weight: {Theme.TYPOGRAPHY['fontWeight']['medium']};
        """)
        content.addWidget(title)
        
        if self.data.get('message'):
            message = QLabel(self.data['message'])
            message.setStyleSheet(f"""
                color: {Theme.COLORS['grey'][600]};
                font-size: {Theme.TYPOGRAPHY['fontSize']['sm']}px;
            """)
            content.addWidget(message)
        
        layout.addLayout(content)
        
        # เวลา
        if self.data.get('time'):
            time = QLabel(self.data['time'])
            time.setStyleSheet(f"""
                color: {Theme.COLORS['grey'][500]};
                font-size: {Theme.TYPOGRAPHY['fontSize']['sm']}px;
            """)
            layout.addWidget(time)
    
    def mousePressEvent(self, event):
        self.clicked.emit(self.data)

class NotificationList(QFrame):
    """รายการแจ้งเตือนทั้งหมด"""
    
    def __init__(self, notifications=None, parent=None):
        super().__init__(parent)
        self.notifications = notifications or []
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
        
        # หัวข้อ
        header = QWidget()
        header.setStyleSheet(f"""
            background: {Theme.COLORS['grey'][50]};
            border-bottom: 1px solid {Theme.COLORS['grey'][200]};
            padding: {Theme.SPACING['md']}px;
        """)
        
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(
            Theme.SPACING['md'],
            Theme.SPACING['md'],
            Theme.SPACING['md'],
            Theme.SPACING['md']
        )
        
        title = QLabel("การแจ้งเตือน")
        title.setStyleSheet(f"""
            color: {Theme.COLORS['grey'][900]};
            font-size: {Theme.TYPOGRAPHY['fontSize']['lg']}px;
            font-weight: {Theme.TYPOGRAPHY['fontWeight']['medium']};
        """)
        header_layout.addWidget(title)
        
        mark_all = QPushButton("อ่านทั้งหมด")
        mark_all.setStyleSheet(f"""
            QPushButton {{
                color: {Theme.COLORS['primary']['main']};
                font-size: {Theme.TYPOGRAPHY['fontSize']['sm']}px;
                border: none;
                padding: {Theme.SPACING['xs']}px {Theme.SPACING['sm']}px;
                border-radius: {Theme.BORDER_RADIUS['sm']};
            }}
            QPushButton:hover {{
                background: {Theme.COLORS['primary'][50]};
            }}
        """)
        header_layout.addWidget(mark_all)
        
        layout.addWidget(header)
        
        # รายการแจ้งเตือน
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
        
        for notification in self.notifications:
            item = NotificationItem(notification)
            content_layout.addWidget(item)
        
        if not self.notifications:
            empty = QLabel("ไม่มีการแจ้งเตือน")
            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty.setStyleSheet(f"""
                color: {Theme.COLORS['grey'][500]};
                padding: {Theme.SPACING['xl']}px;
            """)
            content_layout.addWidget(empty)
        
        content_layout.addStretch()
        scroll.setWidget(content)
        layout.addWidget(scroll)
    
    def add_notification(self, notification):
        """เพิ่มการแจ้งเตือนใหม่"""
        item = NotificationItem(notification)
        self.layout().itemAt(1).widget().widget().layout().insertWidget(0, item)
    
    def clear_notifications(self):
        """ล้างการแจ้งเตือนทั้งหมด"""
        content = self.layout().itemAt(1).widget().widget()
        for i in reversed(range(content.layout().count() - 1)):
            content.layout().itemAt(i).widget().deleteLater()
        
        empty = QLabel("ไม่มีการแจ้งเตือน")
        empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        empty.setStyleSheet(f"""
            color: {Theme.COLORS['grey'][500]};
            padding: {Theme.SPACING['xl']}px;
        """)
        content.layout().insertWidget(0, empty) 