from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtCore import Qt

class Theme:
    # Color Palette - สีหลักของระบบ
    COLORS = {
        'primary': {
            'main': '#2196F3',      # สีหลัก
            'light': '#64B5F6',     # สีอ่อน
            'dark': '#1976D2',      # สีเข้ม
            'contrast': '#FFFFFF'    # สีตัดกัน
        },
        'secondary': {
            'main': '#FF4081',
            'light': '#FF80AB',
            'dark': '#C51162',
            'contrast': '#FFFFFF'
        },
        'success': {
            'main': '#4CAF50',
            'light': '#81C784',
            'dark': '#388E3C',
            'contrast': '#FFFFFF'
        },
        'warning': {
            'main': '#FFC107',
            'light': '#FFD54F',
            'dark': '#FFA000',
            'contrast': '#000000'
        },
        'error': {
            'main': '#F44336',
            'light': '#E57373',
            'dark': '#D32F2F',
            'contrast': '#FFFFFF'
        },
        'info': {
            'main': '#2196F3',
            'light': '#64B5F6',
            'dark': '#1976D2',
            'contrast': '#FFFFFF'
        },
        'grey': {
            100: '#F5F5F5',
            200: '#EEEEEE',
            300: '#E0E0E0',
            400: '#BDBDBD',
            500: '#9E9E9E',
            600: '#757575',
            700: '#616161',
            800: '#424242',
            900: '#212121'
        }
    }

    # Typography - การจัดการตัวอักษร
    TYPOGRAPHY = {
        'fontFamily': {
            'thai': 'Sarabun',
            'english': 'Roboto'
        },
        'fontSize': {
            'xs': 10,
            'sm': 12,
            'base': 14,
            'lg': 16,
            'xl': 18,
            '2xl': 20,
            '3xl': 24,
            '4xl': 30,
            '5xl': 36,
            'display': 48
        },
        'fontWeight': {
            'light': 300,
            'regular': 400,
            'medium': 500,
            'bold': 700
        },
        'lineHeight': {
            'tight': 1.25,
            'normal': 1.5,
            'relaxed': 1.75
        }
    }

    # Spacing - ระยะห่าง
    SPACING = {
        'xs': 4,
        'sm': 8,
        'base': 16,
        'lg': 24,
        'xl': 32,
        '2xl': 48,
        '3xl': 64,
        '4xl': 80
    }

    # Shadows - เงา
    SHADOWS = {
        'none': 'none',
        'sm': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
        'base': '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
        'md': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        'lg': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
        'xl': '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
        '2xl': '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
        'inner': 'inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)'
    }

    # Border Radius - มุมโค้ง
    BORDER_RADIUS = {
        'none': '0',
        'sm': '0.125rem',
        'base': '0.25rem',
        'md': '0.375rem',
        'lg': '0.5rem',
        'xl': '0.75rem',
        '2xl': '1rem',
        'full': '9999px'
    }

    # Transitions - การเคลื่อนไหว
    TRANSITIONS = {
        'duration': {
            'fast': 150,
            'normal': 250,
            'slow': 350
        },
        'timing': {
            'ease-in': 'cubic-bezier(0.4, 0, 1, 1)',
            'ease-out': 'cubic-bezier(0, 0, 0.2, 1)',
            'ease-in-out': 'cubic-bezier(0.4, 0, 0.2, 1)'
        }
    }

    # Z-Index - ลำดับชั้น
    Z_INDEX = {
        'behind': -1,
        'base': 0,
        'above': 1,
        'dropdown': 1000,
        'sticky': 1100,
        'modal': 1300,
        'popover': 1400,
        'tooltip': 1500
    }

    # Breakpoints - จุดเปลี่ยนขนาดหน้าจอ
    BREAKPOINTS = {
        'sm': 640,
        'md': 768,
        'lg': 1024,
        'xl': 1280,
        '2xl': 1536
    }

    @staticmethod
    def get_color(color_path):
        """ดึงค่าสีจาก path เช่น 'primary.main'"""
        parts = color_path.split('.')
        value = Theme.COLORS
        for part in parts:
            value = value[part]
        return value

    @staticmethod
    def get_style_sheet(dark_mode=False):
        """สร้าง stylesheet สำหรับ Qt widgets"""
        primary = Theme.get_color('primary.main')
        background = Theme.COLORS['grey'][900 if dark_mode else 100]
        text = Theme.COLORS['grey'][100 if dark_mode else 900]

        return f"""
            /* Global Styles */
            QWidget {{
                background-color: {background};
                color: {text};
                font-family: {Theme.TYPOGRAPHY['fontFamily']['thai']};
                font-size: {Theme.TYPOGRAPHY['fontSize']['base']}px;
            }}

            /* Buttons */
            QPushButton {{
                background-color: {primary};
                color: {Theme.get_color('primary.contrast')};
                padding: {Theme.SPACING['sm']}px {Theme.SPACING['base']}px;
                border-radius: {Theme.BORDER_RADIUS['base']};
                border: none;
                font-weight: {Theme.TYPOGRAPHY['fontWeight']['medium']};
            }}

            QPushButton:hover {{
                background-color: {Theme.get_color('primary.dark')};
            }}

            QPushButton:pressed {{
                background-color: {Theme.get_color('primary.light')};
            }}

            QPushButton:disabled {{
                background-color: {Theme.COLORS['grey'][400]};
                color: {Theme.COLORS['grey'][600]};
            }}

            /* Input Fields */
            QLineEdit, QTextEdit, QComboBox {{
                background-color: {Theme.COLORS['grey'][200 if dark_mode else 100]};
                color: {text};
                padding: {Theme.SPACING['sm']}px;
                border-radius: {Theme.BORDER_RADIUS['base']};
                border: 1px solid {Theme.COLORS['grey'][400]};
            }}

            QLineEdit:focus, QTextEdit:focus, QComboBox:focus {{
                border: 2px solid {primary};
            }}

            /* Tables */
            QTableView {{
                background-color: {background};
                alternate-background-color: {Theme.COLORS['grey'][800 if dark_mode else 200]};
                gridline-color: {Theme.COLORS['grey'][700 if dark_mode else 300]};
            }}

            QHeaderView::section {{
                background-color: {Theme.COLORS['grey'][800 if dark_mode else 200]};
                color: {text};
                padding: {Theme.SPACING['sm']}px;
                border: none;
            }}

            /* Scrollbars */
            QScrollBar:vertical {{
                background-color: {Theme.COLORS['grey'][800 if dark_mode else 200]};
                width: 12px;
                margin: 0;
            }}

            QScrollBar::handle:vertical {{
                background-color: {Theme.COLORS['grey'][600]};
                min-height: 20px;
                border-radius: 6px;
            }}

            /* Tabs */
            QTabWidget::pane {{
                border: 1px solid {Theme.COLORS['grey'][700 if dark_mode else 300]};
                border-radius: {Theme.BORDER_RADIUS['base']};
            }}

            QTabBar::tab {{
                background-color: {background};
                color: {text};
                padding: {Theme.SPACING['sm']}px {Theme.SPACING['base']}px;
                border-bottom: 2px solid transparent;
            }}

            QTabBar::tab:selected {{
                border-bottom: 2px solid {primary};
            }}
        """

    @staticmethod
    def get_palette(dark_mode=False):
        palette = QPalette()
        
        if dark_mode:
            # Dark Mode
            palette.setColor(QPalette.ColorRole.Window, QColor(Theme.COLORS['grey'][900]))
            palette.setColor(QPalette.ColorRole.WindowText, QColor(Theme.COLORS['grey'][100]))
            palette.setColor(QPalette.ColorRole.Base, QColor(Theme.COLORS['grey'][800]))
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor(Theme.COLORS['grey'][800]))
            palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(Theme.COLORS['grey'][800]))
            palette.setColor(QPalette.ColorRole.ToolTipText, QColor(Theme.COLORS['grey'][100]))
            palette.setColor(QPalette.ColorRole.Text, QColor(Theme.COLORS['grey'][100]))
            palette.setColor(QPalette.ColorRole.Button, QColor(Theme.COLORS['grey'][800]))
            palette.setColor(QPalette.ColorRole.ButtonText, QColor(Theme.COLORS['grey'][100]))
            palette.setColor(QPalette.ColorRole.Link, QColor(Theme.COLORS['primary']['dark']))
            palette.setColor(QPalette.ColorRole.Highlight, QColor(Theme.COLORS['primary']['dark']))
            palette.setColor(QPalette.ColorRole.HighlightedText, QColor(Theme.COLORS['grey'][100]))
        else:
            # Light Mode
            palette.setColor(QPalette.ColorRole.Window, QColor(Theme.COLORS['grey'][100]))
            palette.setColor(QPalette.ColorRole.WindowText, QColor(Theme.COLORS['grey'][900]))
            palette.setColor(QPalette.ColorRole.Base, QColor(Theme.COLORS['grey'][100]))
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor(Theme.COLORS['grey'][100]))
            palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(Theme.COLORS['grey'][100]))
            palette.setColor(QPalette.ColorRole.ToolTipText, QColor(Theme.COLORS['grey'][900]))
            palette.setColor(QPalette.ColorRole.Text, QColor(Theme.COLORS['grey'][900]))
            palette.setColor(QPalette.ColorRole.Button, QColor(Theme.COLORS['grey'][100]))
            palette.setColor(QPalette.ColorRole.ButtonText, QColor(Theme.COLORS['grey'][900]))
            palette.setColor(QPalette.ColorRole.Link, QColor(Theme.COLORS['primary']['main']))
            palette.setColor(QPalette.ColorRole.Highlight, QColor(Theme.COLORS['primary']['main']))
            palette.setColor(QPalette.ColorRole.HighlightedText, QColor(Theme.COLORS['grey'][100]))

        return palette

    @staticmethod
    def get_stylesheet(dark_mode=False):
        primary = Theme.get_color('primary.main')
        background = Theme.COLORS['grey'][900 if dark_mode else 100]
        text = Theme.COLORS['grey'][100 if dark_mode else 900]
        surface = Theme.COLORS['grey'][800 if dark_mode else 200]

        return f"""
            /* Global */
            QWidget {{
                background-color: {background};
                color: {text};
                font-size: {Theme.TYPOGRAPHY['fontSize']['base']}px;
            }}

            /* Buttons */
            QPushButton {{
                background-color: {primary};
                color: {Theme.get_color('primary.contrast')};
                border: none;
                padding: {Theme.SPACING['sm']}px {Theme.SPACING['base']}px;
                border-radius: {Theme.BORDER_RADIUS['base']};
            }}
            QPushButton:hover {{
                background-color: {Theme.get_color('primary.dark')};
            }}
            QPushButton:pressed {{
                background-color: {Theme.get_color('primary.light')};
            }}
            QPushButton:disabled {{
                background-color: {Theme.COLORS['grey'][400]};
                color: {Theme.COLORS['grey'][600]};
            }}

            /* Input Fields */
            QLineEdit, QTextEdit, QComboBox {{
                background-color: {surface};
                color: {text};
                border: 1px solid {Theme.COLORS['grey'][400]};
                padding: {Theme.SPACING['sm']}px;
                border-radius: {Theme.BORDER_RADIUS['base']};
            }}
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus {{
                border: 2px solid {primary};
            }}

            /* Tables */
            QTableView {{
                background-color: {surface};
                alternate-background-color: {Theme.COLORS['grey'][800 if dark_mode else 200]};
                gridline-color: {Theme.COLORS['grey'][700 if dark_mode else 300]};
            }}
            QHeaderView::section {{
                background-color: {surface};
                color: {text};
                padding: {Theme.SPACING['sm']}px;
                border: none;
                border-right: 1px solid {Theme.COLORS['grey'][700 if dark_mode else 300]};
                border-bottom: 1px solid {Theme.COLORS['grey'][700 if dark_mode else 300]};
            }}

            /* Scrollbars */
            QScrollBar:vertical {{
                background-color: {surface};
                width: 12px;
                margin: 0;
            }}
            QScrollBar::handle:vertical {{
                background-color: {Theme.COLORS['grey'][600]};
                min-height: 20px;
                border-radius: 6px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0;
            }}

            /* Tabs */
            QTabWidget::pane {{
                border: 1px solid {Theme.COLORS['grey'][700 if dark_mode else 300]};
                border-radius: {Theme.BORDER_RADIUS['base']};
            }}
            QTabBar::tab {{
                background-color: {surface};
                color: {text};
                padding: {Theme.SPACING['sm']}px {Theme.SPACING['base']}px;
                border: none;
                border-bottom: 2px solid transparent;
            }}
            QTabBar::tab:selected {{
                border-bottom: 2px solid {primary};
            }}
            QTabBar::tab:hover {{
                background-color: {Theme.COLORS['grey'][800 if dark_mode else 200]};
            }}

            /* Menus */
            QMenuBar {{
                background-color: {surface};
                color: {text};
            }}
            QMenuBar::item:selected {{
                background-color: {primary};
                color: {Theme.get_color('primary.contrast')};
            }}
            QMenu {{
                background-color: {surface};
                color: {text};
                border: 1px solid {Theme.COLORS['grey'][700 if dark_mode else 300]};
            }}
            QMenu::item:selected {{
                background-color: {primary};
                color: {Theme.get_color('primary.contrast')};
            }}
        """ 