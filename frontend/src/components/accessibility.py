from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QCheckBox, QSlider, 
    QLabel, QComboBox, QPushButton
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from ..styles.theme import Theme

class AccessibilitySettings(QWidget):
    # สัญญาณสำหรับแจ้งเตือนการเปลี่ยนแปลงการตั้งค่า
    font_size_changed = pyqtSignal(int)
    contrast_changed = pyqtSignal(bool)
    dark_mode_changed = pyqtSignal(bool)
    screen_reader_changed = pyqtSignal(bool)
    keyboard_navigation_changed = pyqtSignal(bool)
    language_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(Theme.SPACING["base"])

        # ขนาดตัวอักษร
        font_label = QLabel("ขนาดตัวอักษร")
        self.font_slider = QSlider(Qt.Orientation.Horizontal)
        self.font_slider.setMinimum(8)
        self.font_slider.setMaximum(24)
        self.font_slider.setValue(14)
        self.font_slider.valueChanged.connect(self.font_size_changed.emit)
        
        layout.addWidget(font_label)
        layout.addWidget(self.font_slider)

        # High Contrast Mode
        self.high_contrast = QCheckBox("โหมดความคมชัดสูง")
        self.high_contrast.stateChanged.connect(
            lambda state: self.contrast_changed.emit(state == Qt.CheckState.Checked.value)
        )
        layout.addWidget(self.high_contrast)

        # Dark Mode
        self.dark_mode = QCheckBox("โหมดกลางคืน")
        self.dark_mode.stateChanged.connect(
            lambda state: self.dark_mode_changed.emit(state == Qt.CheckState.Checked.value)
        )
        layout.addWidget(self.dark_mode)

        # Screen Reader
        self.screen_reader = QCheckBox("เปิดใช้งานโปรแกรมอ่านหน้าจอ")
        self.screen_reader.stateChanged.connect(
            lambda state: self.screen_reader_changed.emit(state == Qt.CheckState.Checked.value)
        )
        layout.addWidget(self.screen_reader)

        # Keyboard Navigation
        self.keyboard_nav = QCheckBox("เปิดใช้งานการนำทางด้วยแป้นพิมพ์")
        self.keyboard_nav.stateChanged.connect(
            lambda state: self.keyboard_navigation_changed.emit(state == Qt.CheckState.Checked.value)
        )
        layout.addWidget(self.keyboard_nav)

        # Language Selection
        lang_label = QLabel("ภาษา")
        self.language = QComboBox()
        self.language.addItems(["ไทย", "English"])
        self.language.currentTextChanged.connect(self.language_changed.emit)
        
        layout.addWidget(lang_label)
        layout.addWidget(self.language)

class AccessibilityManager:
    def __init__(self, app):
        self.app = app
        self.settings = AccessibilitySettings()
        self.setup_connections()

    def setup_connections(self):
        # เชื่อมต่อสัญญาณกับฟังก์ชันจัดการ
        self.settings.font_size_changed.connect(self.update_font_size)
        self.settings.contrast_changed.connect(self.update_contrast)
        self.settings.dark_mode_changed.connect(self.update_dark_mode)
        self.settings.screen_reader_changed.connect(self.update_screen_reader)
        self.settings.keyboard_navigation_changed.connect(self.update_keyboard_navigation)
        self.settings.language_changed.connect(self.update_language)

    def update_font_size(self, size):
        # อัพเดทขนาดตัวอักษรทั้งแอพ
        font = self.app.font()
        font.setPointSize(size)
        self.app.setFont(font)

    def update_contrast(self, enabled):
        if enabled:
            # ใช้ธีมความคมชัดสูง
            self.app.setStyleSheet("""
                QWidget {
                    background-color: white;
                    color: black;
                }
                QPushButton {
                    background-color: black;
                    color: white;
                    border: 2px solid black;
                }
                QLineEdit {
                    background-color: white;
                    color: black;
                    border: 2px solid black;
                }
            """)
        else:
            # ใช้ธีมปกติ
            self.app.setStyleSheet(Theme.get_stylesheet())

    def update_dark_mode(self, enabled):
        # อัพเดทธีมสีทั้งแอพ
        self.app.setPalette(Theme.get_palette(dark_mode=enabled))
        self.app.setStyleSheet(Theme.get_stylesheet(dark_mode=enabled))

    def update_screen_reader(self, enabled):
        if enabled:
            # เพิ่ม accessibility descriptions
            for widget in self.app.allWidgets():
                if isinstance(widget, QLabel):
                    widget.setAccessibleName(widget.text())
                    widget.setAccessibleDescription(widget.text())
                elif isinstance(widget, QPushButton):
                    widget.setAccessibleName(widget.text())
                    widget.setAccessibleDescription(f"ปุ่ม {widget.text()}")

    def update_keyboard_navigation(self, enabled):
        if enabled:
            # เพิ่ม keyboard shortcuts
            for widget in self.app.allWidgets():
                widget.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        else:
            for widget in self.app.allWidgets():
                widget.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def update_language(self, language):
        # TODO: Implement language switching logic
        pass

class AccessibleWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_accessibility()

    def setup_accessibility(self):
        # ตั้งค่าการเข้าถึงพื้นฐาน
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setAccessibleName(self.__class__.__name__)
        
        # เพิ่ม keyboard shortcuts
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        
        # เพิ่ม screen reader support
        self.setAccessibleDescription(f"Widget {self.__class__.__name__}")

    def keyPressEvent(self, event):
        # จัดการ keyboard navigation
        if event.key() == Qt.Key.Key_Return:
            self.activate()
        super().keyPressEvent(event)

    def activate(self):
        # Override this method in subclasses
        pass 