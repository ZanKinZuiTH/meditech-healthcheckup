from PyQt6.QtWidgets import (
    QPushButton, QLineEdit, QLabel, QWidget, QVBoxLayout,
    QHBoxLayout, QTableWidget, QHeaderView, QComboBox,
    QScrollArea, QSizePolicy, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QIcon, QColor, QPalette, QGraphicsDropShadowEffect
from ..styles.theme import Theme

class BaseButton(QPushButton):
    """ปุ่มพื้นฐานที่มีการออกแบบตามธีม"""
    
    def __init__(self, text="", icon=None, variant="primary", size="base", parent=None):
        super().__init__(text, parent)
        self.variant = variant
        self.size = size
        if icon:
            self.setIcon(icon)
        self.setup_style()
        
    def setup_style(self):
        # กำหนดสไตล์ตามประเภทปุ่ม
        colors = {
            'primary': Theme.COLORS['primary'],
            'secondary': Theme.COLORS['secondary'],
            'success': Theme.COLORS['success'],
            'warning': Theme.COLORS['warning'],
            'error': Theme.COLORS['error']
        }
        
        # กำหนดขนาดปุ่ม
        sizes = {
            'sm': (Theme.SPACING['sm'], Theme.SPACING['base'], Theme.TYPOGRAPHY['fontSize']['sm']),
            'base': (Theme.SPACING['base'], Theme.SPACING['lg'], Theme.TYPOGRAPHY['fontSize']['base']),
            'lg': (Theme.SPACING['lg'], Theme.SPACING['xl'], Theme.TYPOGRAPHY['fontSize']['lg'])
        }
        
        color = colors.get(self.variant, colors['primary'])
        padding_v, padding_h, font_size = sizes.get(self.size, sizes['base'])
        
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color['main']};
                color: {color['contrast']};
                padding: {padding_v}px {padding_h}px;
                border-radius: {Theme.BORDER_RADIUS['base']};
                border: none;
                font-weight: {Theme.TYPOGRAPHY['fontWeight']['medium']};
                font-size: {font_size}px;
            }}
            QPushButton:hover {{
                background-color: {color['dark']};
            }}
            QPushButton:pressed {{
                background-color: {color['light']};
            }}
            QPushButton:disabled {{
                background-color: {Theme.COLORS['grey'][400]};
                color: {Theme.COLORS['grey'][600]};
            }}
        """)

class BaseInput(QLineEdit):
    """ช่องกรอกข้อมูลพื้นฐานที่มีการออกแบบตามธีม"""
    
    def __init__(self, placeholder="", label="", required=False, parent=None):
        super().__init__(parent)
        self.label = label
        self.required = required
        self.setPlaceholderText(placeholder)
        self.setup_ui()
        
    def setup_ui(self):
        container = QWidget(self.parent())
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(Theme.SPACING['xs'])
        
        if self.label:
            label_text = f"{self.label}{'*' if self.required else ''}"
            label = QLabel(label_text, container)
            label.setStyleSheet(f"""
                QLabel {{
                    color: {Theme.COLORS['grey'][900]};
                    font-size: {Theme.TYPOGRAPHY['fontSize']['sm']}px;
                    font-weight: {Theme.TYPOGRAPHY['fontWeight']['medium']};
                }}
            """)
            layout.addWidget(label)
        
        layout.addWidget(self)
        
        self.setStyleSheet(f"""
            QLineEdit {{
                background-color: {Theme.COLORS['grey'][100]};
                color: {Theme.COLORS['grey'][900]};
                padding: {Theme.SPACING['sm']}px;
                border-radius: {Theme.BORDER_RADIUS['base']};
                border: 1px solid {Theme.COLORS['grey'][300]};
                font-size: {Theme.TYPOGRAPHY['fontSize']['base']}px;
            }}
            QLineEdit:focus {{
                border: 2px solid {Theme.COLORS['primary']['main']};
            }}
            QLineEdit:disabled {{
                background-color: {Theme.COLORS['grey'][200]};
                color: {Theme.COLORS['grey'][600]};
            }}
        """)

class BaseTable(QTableWidget):
    """ตารางพื้นฐานที่มีการออกแบบตามธีม"""
    
    def __init__(self, headers=None, parent=None):
        super().__init__(parent)
        self.headers = headers or []
        self.setup_ui()
        
    def setup_ui(self):
        # ตั้งค่าหัวตาราง
        self.setColumnCount(len(self.headers))
        self.setHorizontalHeaderLabels(self.headers)
        
        # ตั้งค่าการแสดงผล
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setStretchLastSection(True)
        
        self.setStyleSheet(f"""
            QTableWidget {{
                background-color: {Theme.COLORS['grey'][100]};
                color: {Theme.COLORS['grey'][900]};
                border: none;
                gridline-color: {Theme.COLORS['grey'][300]};
            }}
            QTableWidget::item {{
                padding: {Theme.SPACING['sm']}px;
            }}
            QTableWidget::item:selected {{
                background-color: {Theme.COLORS['primary']['light']};
                color: {Theme.COLORS['primary']['contrast']};
            }}
            QHeaderView::section {{
                background-color: {Theme.COLORS['grey'][200]};
                color: {Theme.COLORS['grey'][900]};
                padding: {Theme.SPACING['sm']}px;
                border: none;
                font-weight: {Theme.TYPOGRAPHY['fontWeight']['medium']};
            }}
        """)

class BaseComboBox(QComboBox):
    """คอมโบบ็อกซ์พื้นฐานที่มีการออกแบบตามธีม"""
    
    def __init__(self, items=None, label="", parent=None):
        super().__init__(parent)
        self.label = label
        if items:
            self.addItems(items)
        self.setup_ui()
        
    def setup_ui(self):
        container = QWidget(self.parent())
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(Theme.SPACING['xs'])
        
        if self.label:
            label = QLabel(self.label, container)
            label.setStyleSheet(f"""
                QLabel {{
                    color: {Theme.COLORS['grey'][900]};
                    font-size: {Theme.TYPOGRAPHY['fontSize']['sm']}px;
                    font-weight: {Theme.TYPOGRAPHY['fontWeight']['medium']};
                }}
            """)
            layout.addWidget(label)
        
        layout.addWidget(self)
        
        self.setStyleSheet(f"""
            QComboBox {{
                background-color: {Theme.COLORS['grey'][100]};
                color: {Theme.COLORS['grey'][900]};
                padding: {Theme.SPACING['sm']}px;
                border-radius: {Theme.BORDER_RADIUS['base']};
                border: 1px solid {Theme.COLORS['grey'][300]};
                font-size: {Theme.TYPOGRAPHY['fontSize']['base']}px;
            }}
            QComboBox:focus {{
                border: 2px solid {Theme.COLORS['primary']['main']};
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QComboBox::down-arrow {{
                image: url(resources/icons/chevron-down.svg);
                width: 12px;
                height: 12px;
            }}
        """)

class ResponsiveWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Scroll Area for responsiveness
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        # Content Widget
        self.content = QWidget()
        self.content_layout = QVBoxLayout(self.content)
        self.scroll.setWidget(self.content)
        self.layout.addWidget(self.scroll)

    def add_widget(self, widget):
        self.content_layout.addWidget(widget)

    def add_layout(self, layout):
        self.content_layout.addLayout(layout)

class Card(QFrame):
    """การ์ดที่มีการออกแบบตามธีม"""
    
    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self.title = title
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            Theme.SPACING['lg'],
            Theme.SPACING['lg'],
            Theme.SPACING['lg'],
            Theme.SPACING['lg']
        )
        layout.setSpacing(Theme.SPACING['base'])
        
        if self.title:
            title_label = QLabel(self.title, self)
            title_label.setStyleSheet(f"""
                QLabel {{
                    color: {Theme.COLORS['grey'][900]};
                    font-size: {Theme.TYPOGRAPHY['fontSize']['lg']}px;
                    font-weight: {Theme.TYPOGRAPHY['fontWeight']['bold']};
                }}
            """)
            layout.addWidget(title_label)
        
        self.content_widget = QWidget(self)
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.content_widget)
        
        self.setStyleSheet(f"""
            Card {{
                background-color: {Theme.COLORS['grey'][100]};
                border-radius: {Theme.BORDER_RADIUS['lg']};
                border: 1px solid {Theme.COLORS['grey'][200]};
            }}
        """)
        
        # เพิ่มเงา
        self.setGraphicsEffect(self.create_shadow())
    
    def add_widget(self, widget):
        """เพิ่ม widget ลงในการ์ด"""
        self.content_layout.addWidget(widget)
    
    def add_layout(self, layout):
        """เพิ่ม layout ลงในการ์ด"""
        self.content_layout.addLayout(layout)
    
    def create_shadow(self):
        """สร้างเงาให้การ์ด"""
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 30))
        return shadow 