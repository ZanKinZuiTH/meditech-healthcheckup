import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from .views.main_window import MainWindow
from .styles.theme import Theme
from .components.accessibility import AccessibilityManager

class MediTechApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        
        # ตั้งค่าธีม
        self.theme = Theme()
        self.setPalette(self.theme.get_palette())
        self.setStyleSheet(self.theme.get_stylesheet())
        
        # ตั้งค่า Accessibility
        self.accessibility = AccessibilityManager(self)
        
        # สร้างหน้าต่างหลัก
        self.main_window = MainWindow()
        self.main_window.show()

def main():
    # สร้าง Application
    app = MediTechApp(sys.argv)
    
    # รัน Event Loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 