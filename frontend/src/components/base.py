from PyQt6.QtWidgets import (
    QPushButton, QLineEdit, QLabel, QWidget, QVBoxLayout,
    QHBoxLayout, QTableWidget, QHeaderView, QComboBox,
    QScrollArea, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QIcon
from ..styles.theme import Theme

class BaseButton(QPushButton):
    def __init__(self, text="", icon=None, variant="primary", size="base", parent=None):
        super().__init__(text, parent)
        self.variant = variant
        self.size = size
        if icon:
            self.setIcon(QIcon(icon))
        self.setup_style()

    def setup_style(self):
        # ขนาดปุ่ม
        padding = {
            "sm": (Theme.SPACING["xs"], Theme.SPACING["sm"]),
            "base": (Theme.SPACING["sm"], Theme.SPACING["base"]),
            "lg": (Theme.SPACING["base"], Theme.SPACING["lg"]),
        }
        font_size = {
            "sm": Theme.FONT_SIZES["sm"],
            "base": Theme.FONT_SIZES["base"],
            "lg": Theme.FONT_SIZES["lg"],
        }
        
        # สีตามประเภท
        colors = {
            "primary": (Theme.PRIMARY, "#FFFFFF"),
            "secondary": (Theme.SECONDARY, "#FFFFFF"),
            "success": (Theme.SUCCESS, "#FFFFFF"),
            "error": (Theme.ERROR, "#FFFFFF"),
            "warning": (Theme.WARNING, "#212121"),
            "info": (Theme.INFO, "#FFFFFF"),
        }

        bg_color, text_color = colors.get(self.variant, colors["primary"])
        p_v, p_h = padding.get(self.size, padding["base"])
        f_size = font_size.get(self.size, font_size["base"])

        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg_color};
                color: {text_color};
                border: none;
                padding: {p_v}px {p_h}px;
                border-radius: {Theme.BORDER_RADIUS["base"]}px;
                font-size: {f_size}px;
            }}
            QPushButton:hover {{
                background-color: {self.adjust_color(bg_color, -10)};
            }}
            QPushButton:pressed {{
                background-color: {self.adjust_color(bg_color, -20)};
            }}
            QPushButton:disabled {{
                background-color: #BDBDBD;
                color: #757575;
            }}
        """)

    @staticmethod
    def adjust_color(hex_color, factor):
        # ปรับความสว่างของสี
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        
        r = max(0, min(255, r + factor))
        g = max(0, min(255, g + factor))
        b = max(0, min(255, b + factor))
        
        return f"#{r:02x}{g:02x}{b:02x}"

class BaseInput(QLineEdit):
    def __init__(self, placeholder="", label="", required=False, parent=None):
        super().__init__(parent)
        self.placeholder = placeholder
        self.label_text = label
        self.required = required
        self.setup_ui()

    def setup_ui(self):
        self.setPlaceholderText(self.placeholder)
        if self.required:
            self.setStyleSheet(f"""
                QLineEdit {{
                    border: 1px solid #BDBDBD;
                    padding: {Theme.SPACING["sm"]}px;
                    border-radius: {Theme.BORDER_RADIUS["base"]}px;
                    font-size: {Theme.FONT_SIZES["base"]}px;
                }}
                QLineEdit:focus {{
                    border: 2px solid {Theme.PRIMARY};
                }}
                QLineEdit[required="true"] {{
                    border-left: 3px solid {Theme.ERROR};
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QLineEdit {{
                    border: 1px solid #BDBDBD;
                    padding: {Theme.SPACING["sm"]}px;
                    border-radius: {Theme.BORDER_RADIUS["base"]}px;
                    font-size: {Theme.FONT_SIZES["base"]}px;
                }}
                QLineEdit:focus {{
                    border: 2px solid {Theme.PRIMARY};
                }}
            """)

class BaseTable(QTableWidget):
    def __init__(self, headers=None, parent=None):
        super().__init__(parent)
        self.headers = headers or []
        self.setup_ui()

    def setup_ui(self):
        # ตั้งค่าหัวตาราง
        self.setColumnCount(len(self.headers))
        self.setHorizontalHeaderLabels(self.headers)
        
        # จัดการขนาดคอลัมน์
        header = self.horizontalHeader()
        for i in range(len(self.headers)):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
        
        # ตั้งค่าการแสดงผล
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        self.setStyleSheet(f"""
            QTableWidget {{
                border: 1px solid #E0E0E0;
                gridline-color: #E0E0E0;
                background-color: white;
                alternate-background-color: #F5F5F5;
            }}
            QHeaderView::section {{
                background-color: white;
                padding: {Theme.SPACING["sm"]}px;
                border: none;
                border-right: 1px solid #E0E0E0;
                border-bottom: 1px solid #E0E0E0;
                font-weight: bold;
            }}
            QTableWidget::item {{
                padding: {Theme.SPACING["sm"]}px;
            }}
            QTableWidget::item:selected {{
                background-color: {Theme.PRIMARY};
                color: white;
            }}
        """)

class BaseComboBox(QComboBox):
    def __init__(self, items=None, label="", parent=None):
        super().__init__(parent)
        self.label_text = label
        if items:
            self.addItems(items)
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet(f"""
            QComboBox {{
                border: 1px solid #BDBDBD;
                padding: {Theme.SPACING["sm"]}px;
                border-radius: {Theme.BORDER_RADIUS["base"]}px;
                background-color: white;
            }}
            QComboBox:focus {{
                border: 2px solid {Theme.PRIMARY};
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QComboBox::down-arrow {{
                image: url(resources/icons/arrow_down.png);
                width: 12px;
                height: 12px;
            }}
            QComboBox QAbstractItemView {{
                border: 1px solid #BDBDBD;
                selection-background-color: {Theme.PRIMARY};
                selection-color: white;
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

class Card(QWidget):
    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self.title = title
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Title
        if self.title:
            title_label = QLabel(self.title)
            title_label.setFont(QFont("", Theme.FONT_SIZES["lg"], QFont.Weight.Bold))
            layout.addWidget(title_label)

        # Content Widget
        self.content = QWidget()
        self.content_layout = QVBoxLayout(self.content)
        layout.addWidget(self.content)

        # Style
        self.setStyleSheet(f"""
            Card {{
                background-color: white;
                border-radius: {Theme.BORDER_RADIUS["lg"]}px;
                padding: {Theme.SPACING["lg"]}px;
            }}
        """)
        self.setGraphicsEffect(self.create_shadow())

    def add_widget(self, widget):
        self.content_layout.addWidget(widget)

    def add_layout(self, layout):
        self.content_layout.addLayout(layout)

    def create_shadow(self):
        from PyQt6.QtWidgets import QGraphicsDropShadowEffect
        from PyQt6.QtGui import QColor
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 30))
        return shadow 