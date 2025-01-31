from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtCore import Qt

class Theme:
    # สีหลัก
    PRIMARY = "#2196F3"  # สีฟ้า Material Design
    SECONDARY = "#FF4081"  # สีชมพู Material Design
    BACKGROUND = "#FFFFFF"
    TEXT = "#212121"
    ERROR = "#F44336"
    SUCCESS = "#4CAF50"
    WARNING = "#FFC107"
    INFO = "#2196F3"

    # สีสำหรับ Dark Mode
    DARK_PRIMARY = "#1976D2"
    DARK_SECONDARY = "#C2185B"
    DARK_BACKGROUND = "#121212"
    DARK_SURFACE = "#1E1E1E"
    DARK_TEXT = "#FFFFFF"

    # ขนาดตัวอักษร
    FONT_SIZES = {
        "xs": 10,
        "sm": 12,
        "base": 14,
        "lg": 16,
        "xl": 18,
        "2xl": 20,
        "3xl": 24,
        "4xl": 30,
    }

    # ระยะห่าง
    SPACING = {
        "xs": 4,
        "sm": 8,
        "base": 16,
        "lg": 24,
        "xl": 32,
        "2xl": 48,
    }

    # รัศมีขอบ
    BORDER_RADIUS = {
        "sm": 4,
        "base": 8,
        "lg": 12,
        "xl": 16,
        "full": 9999,
    }

    # เงา
    SHADOWS = {
        "sm": "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
        "base": "0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)",
        "lg": "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
        "xl": "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)",
    }

    @staticmethod
    def get_palette(dark_mode=False):
        palette = QPalette()
        
        if dark_mode:
            # Dark Mode
            palette.setColor(QPalette.ColorRole.Window, QColor(Theme.DARK_BACKGROUND))
            palette.setColor(QPalette.ColorRole.WindowText, QColor(Theme.DARK_TEXT))
            palette.setColor(QPalette.ColorRole.Base, QColor(Theme.DARK_SURFACE))
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor(Theme.DARK_SURFACE))
            palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(Theme.DARK_SURFACE))
            palette.setColor(QPalette.ColorRole.ToolTipText, QColor(Theme.DARK_TEXT))
            palette.setColor(QPalette.ColorRole.Text, QColor(Theme.DARK_TEXT))
            palette.setColor(QPalette.ColorRole.Button, QColor(Theme.DARK_SURFACE))
            palette.setColor(QPalette.ColorRole.ButtonText, QColor(Theme.DARK_TEXT))
            palette.setColor(QPalette.ColorRole.Link, QColor(Theme.DARK_PRIMARY))
            palette.setColor(QPalette.ColorRole.Highlight, QColor(Theme.DARK_PRIMARY))
            palette.setColor(QPalette.ColorRole.HighlightedText, QColor(Theme.DARK_TEXT))
        else:
            # Light Mode
            palette.setColor(QPalette.ColorRole.Window, QColor(Theme.BACKGROUND))
            palette.setColor(QPalette.ColorRole.WindowText, QColor(Theme.TEXT))
            palette.setColor(QPalette.ColorRole.Base, QColor(Theme.BACKGROUND))
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor(Theme.BACKGROUND))
            palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(Theme.BACKGROUND))
            palette.setColor(QPalette.ColorRole.ToolTipText, QColor(Theme.TEXT))
            palette.setColor(QPalette.ColorRole.Text, QColor(Theme.TEXT))
            palette.setColor(QPalette.ColorRole.Button, QColor(Theme.BACKGROUND))
            palette.setColor(QPalette.ColorRole.ButtonText, QColor(Theme.TEXT))
            palette.setColor(QPalette.ColorRole.Link, QColor(Theme.PRIMARY))
            palette.setColor(QPalette.ColorRole.Highlight, QColor(Theme.PRIMARY))
            palette.setColor(QPalette.ColorRole.HighlightedText, QColor(Theme.BACKGROUND))

        return palette

    @staticmethod
    def get_stylesheet(dark_mode=False):
        primary = Theme.DARK_PRIMARY if dark_mode else Theme.PRIMARY
        background = Theme.DARK_BACKGROUND if dark_mode else Theme.BACKGROUND
        text = Theme.DARK_TEXT if dark_mode else Theme.TEXT
        surface = Theme.DARK_SURFACE if dark_mode else Theme.BACKGROUND

        return f"""
            /* Global */
            QWidget {{
                background-color: {background};
                color: {text};
                font-size: {Theme.FONT_SIZES["base"]}px;
            }}

            /* Buttons */
            QPushButton {{
                background-color: {primary};
                color: white;
                border: none;
                padding: {Theme.SPACING["sm"]}px {Theme.SPACING["base"]}px;
                border-radius: {Theme.BORDER_RADIUS["base"]}px;
            }}
            QPushButton:hover {{
                background-color: {Theme.DARK_PRIMARY if dark_mode else "#1E88E5"};
            }}
            QPushButton:pressed {{
                background-color: {Theme.DARK_PRIMARY if dark_mode else "#1976D2"};
            }}
            QPushButton:disabled {{
                background-color: #BDBDBD;
            }}

            /* Input Fields */
            QLineEdit, QTextEdit, QComboBox {{
                background-color: {surface};
                color: {text};
                border: 1px solid #BDBDBD;
                padding: {Theme.SPACING["sm"]}px;
                border-radius: {Theme.BORDER_RADIUS["base"]}px;
            }}
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus {{
                border: 2px solid {primary};
            }}

            /* Tables */
            QTableView {{
                background-color: {surface};
                alternate-background-color: {Theme.DARK_SURFACE if dark_mode else "#F5F5F5"};
                gridline-color: #E0E0E0;
            }}
            QHeaderView::section {{
                background-color: {surface};
                color: {text};
                padding: {Theme.SPACING["sm"]}px;
                border: none;
                border-right: 1px solid #E0E0E0;
                border-bottom: 1px solid #E0E0E0;
            }}

            /* Scrollbars */
            QScrollBar:vertical {{
                background-color: {surface};
                width: 12px;
                margin: 0;
            }}
            QScrollBar::handle:vertical {{
                background-color: #BDBDBD;
                min-height: 20px;
                border-radius: 6px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0;
            }}

            /* Tabs */
            QTabWidget::pane {{
                border: 1px solid #E0E0E0;
                border-radius: {Theme.BORDER_RADIUS["base"]}px;
            }}
            QTabBar::tab {{
                background-color: {surface};
                color: {text};
                padding: {Theme.SPACING["sm"]}px {Theme.SPACING["base"]}px;
                border: none;
                border-bottom: 2px solid transparent;
            }}
            QTabBar::tab:selected {{
                border-bottom: 2px solid {primary};
            }}
            QTabBar::tab:hover {{
                background-color: {Theme.DARK_SURFACE if dark_mode else "#F5F5F5"};
            }}

            /* Menus */
            QMenuBar {{
                background-color: {surface};
                color: {text};
            }}
            QMenuBar::item:selected {{
                background-color: {primary};
                color: white;
            }}
            QMenu {{
                background-color: {surface};
                color: {text};
                border: 1px solid #E0E0E0;
            }}
            QMenu::item:selected {{
                background-color: {primary};
                color: white;
            }}
        """ 