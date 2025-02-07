from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QComboBox, QDateEdit, QTimeEdit,
    QSpinBox, QTextEdit, QDialogButtonBox, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon

from ...styles.theme import Theme
from ..base import BaseButton

class FormField(QFrame):
    """ฟิลด์ในฟอร์มพร้อมป้ายกำกับ"""
    
    def __init__(self, label, field_type="text", required=False, parent=None):
        super().__init__(parent)
        self.label = label
        self.field_type = field_type
        self.required = required
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(Theme.SPACING['xs'])
        layout.setContentsMargins(0, 0, 0, Theme.SPACING['base'])
        
        # ป้ายกำกับ
        label_text = self.label
        if self.required:
            label_text += " *"
        
        label = QLabel(label_text)
        label.setStyleSheet(f"""
            color: {Theme.COLORS['grey'][700]};
            font-size: {Theme.TYPOGRAPHY['fontSize']['sm']}px;
            font-weight: {Theme.TYPOGRAPHY['fontWeight']['medium']};
        """)
        layout.addWidget(label)
        
        # สร้าง input ตามประเภท
        if self.field_type == "text":
            self.input = QLineEdit()
            self.input.setStyleSheet(self.get_input_style())
        elif self.field_type == "select":
            self.input = QComboBox()
            self.input.setStyleSheet(self.get_input_style())
        elif self.field_type == "date":
            self.input = QDateEdit()
            self.input.setCalendarPopup(True)
            self.input.setStyleSheet(self.get_input_style())
        elif self.field_type == "time":
            self.input = QTimeEdit()
            self.input.setStyleSheet(self.get_input_style())
        elif self.field_type == "number":
            self.input = QSpinBox()
            self.input.setStyleSheet(self.get_input_style())
        elif self.field_type == "textarea":
            self.input = QTextEdit()
            self.input.setStyleSheet(self.get_input_style())
        
        layout.addWidget(self.input)
    
    def get_input_style(self):
        """สไตล์สำหรับ input"""
        return f"""
            padding: {Theme.SPACING['sm']}px;
            border: 1px solid {Theme.COLORS['grey'][300]};
            border-radius: {Theme.BORDER_RADIUS['base']};
            background: white;
            font-size: {Theme.TYPOGRAPHY['fontSize']['base']}px;
        """
    
    def get_value(self):
        """ดึงค่าจาก input"""
        if self.field_type == "text":
            return self.input.text()
        elif self.field_type == "select":
            return self.input.currentText()
        elif self.field_type == "date":
            return self.input.date().toPyDate()
        elif self.field_type == "time":
            return self.input.time().toPyTime()
        elif self.field_type == "number":
            return self.input.value()
        elif self.field_type == "textarea":
            return self.input.toPlainText()
    
    def set_value(self, value):
        """กำหนดค่าให้ input"""
        if self.field_type == "text":
            self.input.setText(str(value))
        elif self.field_type == "select":
            index = self.input.findText(str(value))
            if index >= 0:
                self.input.setCurrentIndex(index)
        elif self.field_type == "date":
            self.input.setDate(value)
        elif self.field_type == "time":
            self.input.setTime(value)
        elif self.field_type == "number":
            self.input.setValue(value)
        elif self.field_type == "textarea":
            self.input.setPlainText(str(value))

class FormDialog(QDialog):
    """Dialog สำหรับแสดงฟอร์มเพิ่ม/แก้ไขข้อมูล"""
    
    submitted = pyqtSignal(dict)
    
    def __init__(self, title, fields, data=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.fields = fields
        self.data = data
        self.setup_ui()
        
        if data:
            self.load_data()
    
    def setup_ui(self):
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(Theme.SPACING['lg'])
        layout.setContentsMargins(
            Theme.SPACING['xl'],
            Theme.SPACING['xl'],
            Theme.SPACING['xl'],
            Theme.SPACING['xl']
        )
        
        # สร้างฟิลด์
        self.form_fields = {}
        for field in self.fields:
            form_field = FormField(
                label=field['label'],
                field_type=field.get('type', 'text'),
                required=field.get('required', False)
            )
            self.form_fields[field['key']] = form_field
            layout.addWidget(form_field)
        
        # ปุ่มดำเนินการ
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        
        # สไตล์ปุ่ม
        for button in buttons.buttons():
            if buttons.buttonRole(button) == QDialogButtonBox.ButtonRole.AcceptRole:
                button.setText("บันทึก")
                button.setStyleSheet(f"""
                    QPushButton {{
                        padding: {Theme.SPACING['sm']}px {Theme.SPACING['lg']}px;
                        border: none;
                        border-radius: {Theme.BORDER_RADIUS['base']};
                        background: {Theme.COLORS['primary']['main']};
                        color: white;
                        font-weight: {Theme.TYPOGRAPHY['fontWeight']['medium']};
                    }}
                    QPushButton:hover {{
                        background: {Theme.COLORS['primary']['dark']};
                    }}
                """)
            else:
                button.setText("ยกเลิก")
                button.setStyleSheet(f"""
                    QPushButton {{
                        padding: {Theme.SPACING['sm']}px {Theme.SPACING['lg']}px;
                        border: 1px solid {Theme.COLORS['grey'][300]};
                        border-radius: {Theme.BORDER_RADIUS['base']};
                        background: white;
                        color: {Theme.COLORS['grey'][700]};
                    }}
                    QPushButton:hover {{
                        background: {Theme.COLORS['grey'][100]};
                    }}
                """)
        
        layout.addWidget(buttons)
    
    def load_data(self):
        """โหลดข้อมูลเดิมเข้าฟอร์ม"""
        for key, field in self.form_fields.items():
            if key in self.data:
                field.set_value(self.data[key])
    
    def get_data(self):
        """รวบรวมข้อมูลจากฟอร์ม"""
        data = {}
        for key, field in self.form_fields.items():
            data[key] = field.get_value()
        return data
    
    def accept(self):
        """จัดการเมื่อกดปุ่มบันทึก"""
        data = self.get_data()
        self.submitted.emit(data)
        super().accept()
    
    def validate(self):
        """ตรวจสอบความถูกต้องของข้อมูล"""
        for key, field in self.form_fields.items():
            if field.required and not field.get_value():
                return False
        return True 