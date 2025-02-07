from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QTextEdit, QPushButton, QFrame,
    QScrollArea, QMessageBox, QSpinBox, QComboBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from ..components.base import Card, BaseButton
from ..styles.theme import Theme

class SymptomInput(QFrame):
    """ส่วนกรอกอาการ"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # ช่องกรอกอาการ
        self.symptom_input = QTextEdit()
        self.symptom_input.setPlaceholderText("กรอกอาการที่พบ (แยกแต่ละอาการด้วยเครื่องหมาย ,)")
        layout.addWidget(self.symptom_input)
        
        # ข้อมูลเพิ่มเติม
        details_layout = QHBoxLayout()
        
        # อายุ
        age_layout = QVBoxLayout()
        age_label = QLabel("อายุ")
        self.age_input = QSpinBox()
        self.age_input.setRange(0, 150)
        age_layout.addWidget(age_label)
        age_layout.addWidget(self.age_input)
        details_layout.addLayout(age_layout)
        
        # เพศ
        gender_layout = QVBoxLayout()
        gender_label = QLabel("เพศ")
        self.gender_input = QComboBox()
        self.gender_input.addItems(["ชาย", "หญิง", "อื่นๆ"])
        gender_layout.addWidget(gender_label)
        gender_layout.addWidget(self.gender_input)
        details_layout.addLayout(gender_layout)
        
        # ระยะเวลาที่มีอาการ
        duration_layout = QVBoxLayout()
        duration_label = QLabel("ระยะเวลาที่มีอาการ (วัน)")
        self.duration_input = QSpinBox()
        self.duration_input.setRange(0, 365)
        duration_layout.addWidget(duration_label)
        duration_layout.addWidget(self.duration_input)
        details_layout.addLayout(duration_layout)
        
        layout.addLayout(details_layout)
        
        # ประวัติการรักษา
        history_label = QLabel("ประวัติการรักษาที่เกี่ยวข้อง (ถ้ามี)")
        self.history_input = QTextEdit()
        self.history_input.setMaximumHeight(100)
        layout.addWidget(history_label)
        layout.addWidget(self.history_input)
        
        self.setStyleSheet(f"""
            QLabel {{
                color: {Theme.COLORS['grey'][700]};
                font-size: {Theme.TYPOGRAPHY['fontSize']['sm']}px;
            }}
            QTextEdit, QSpinBox, QComboBox {{
                padding: {Theme.SPACING['sm']}px;
                border: 1px solid {Theme.COLORS['grey'][300]};
                border-radius: {Theme.BORDER_RADIUS['base']};
                background: white;
            }}
            QTextEdit:focus, QSpinBox:focus, QComboBox:focus {{
                border-color: {Theme.COLORS['primary']['main']};
            }}
        """)
    
    def get_input_data(self):
        """รวบรวมข้อมูลที่กรอก"""
        symptoms = [s.strip() for s in self.symptom_input.toPlainText().split(",") if s.strip()]
        return {
            "symptoms": symptoms,
            "age": self.age_input.value() or None,
            "gender": self.gender_input.currentText().lower(),
            "duration_days": self.duration_input.value() or None,
            "medical_history": self.history_input.toPlainText().split("\n") if self.history_input.toPlainText() else None
        }

class DiagnosisResult(Card):
    """แสดงผลการวินิจฉัย"""
    
    def __init__(self, parent=None):
        super().__init__("ผลการวินิจฉัยเบื้องต้น", parent)
        self.setup_result_ui()
    
    def setup_result_ui(self):
        content_layout = QVBoxLayout()
        
        # โรคที่เป็นไปได้
        conditions_label = QLabel("โรคที่เป็นไปได้:")
        conditions_label.setStyleSheet(f"""
            font-weight: {Theme.TYPOGRAPHY['fontWeight']['bold']};
            color: {Theme.COLORS['grey'][900]};
        """)
        self.conditions_list = QLabel()
        content_layout.addWidget(conditions_label)
        content_layout.addWidget(self.conditions_list)
        
        # ระดับความเชื่อมั่น
        confidence_label = QLabel("ระดับความเชื่อมั่น:")
        self.confidence_value = QLabel()
        content_layout.addWidget(confidence_label)
        content_layout.addWidget(self.confidence_value)
        
        # คำแนะนำ
        recommendation_label = QLabel("คำแนะนำ:")
        self.recommendation_text = QLabel()
        self.recommendation_text.setWordWrap(True)
        content_layout.addWidget(recommendation_label)
        content_layout.addWidget(self.recommendation_text)
        
        # สัญญาณอันตราย
        self.warning_frame = QFrame()
        self.warning_frame.setVisible(False)
        warning_layout = QVBoxLayout(self.warning_frame)
        warning_label = QLabel("⚠️ สัญญาณอันตราย:")
        warning_label.setStyleSheet(f"""
            color: {Theme.COLORS['error']['main']};
            font-weight: {Theme.TYPOGRAPHY['fontWeight']['bold']};
        """)
        self.warning_text = QLabel()
        self.warning_text.setWordWrap(True)
        self.warning_text.setStyleSheet(f"color: {Theme.COLORS['error']['main']};")
        warning_layout.addWidget(warning_label)
        warning_layout.addWidget(self.warning_text)
        content_layout.addWidget(self.warning_frame)
        
        self.add_layout(content_layout)
    
    def update_result(self, result_data):
        """อัพเดทผลการวินิจฉัย"""
        self.conditions_list.setText("\n".join(f"- {c}" for c in result_data["possible_conditions"]))
        self.confidence_value.setText(f"{result_data['confidence_score']*100:.1f}%")
        self.recommendation_text.setText(result_data["recommendation"])
        
        if result_data["warning_signs"]:
            self.warning_frame.setVisible(True)
            self.warning_text.setText("\n".join(result_data["warning_signs"]))
        else:
            self.warning_frame.setVisible(False)

class DiagnosisView(QWidget):
    """หน้าวินิจฉัยโรคเบื้องต้น"""
    
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(Theme.SPACING['xl'])
        
        # ส่วนกรอกข้อมูล
        input_card = Card("กรอกข้อมูลอาการ")
        self.symptom_input = SymptomInput()
        input_card.add_widget(self.symptom_input)
        
        # ปุ่มวินิจฉัย
        diagnose_btn = BaseButton(
            "วินิจฉัย",
            variant="primary",
            size="lg"
        )
        diagnose_btn.clicked.connect(self.handle_diagnose)
        input_card.add_widget(diagnose_btn)
        
        layout.addWidget(input_card)
        
        # ส่วนแสดงผล
        self.result_widget = DiagnosisResult()
        self.result_widget.setVisible(False)
        layout.addWidget(self.result_widget)
        
        # คำเตือน
        disclaimer = QLabel(
            "⚠️ ระบบนี้ให้การวินิจฉัยเบื้องต้นเท่านั้น "
            "ไม่สามารถใช้แทนการตรวจวินิจฉัยโดยแพทย์ได้"
        )
        disclaimer.setStyleSheet(f"""
            color: {Theme.COLORS['warning']['dark']};
            padding: {Theme.SPACING['base']}px;
            background: {Theme.COLORS['warning']['light']};
            border-radius: {Theme.BORDER_RADIUS['base']};
        """)
        disclaimer.setWordWrap(True)
        layout.addWidget(disclaimer)
    
    async def handle_diagnose(self):
        """จัดการการกดปุ่มวินิจฉัย"""
        try:
            input_data = self.symptom_input.get_input_data()
            
            if not input_data["symptoms"]:
                QMessageBox.warning(
                    self,
                    "ข้อมูลไม่ครบถ้วน",
                    "กรุณากรอกอาการที่พบอย่างน้อย 1 อาการ"
                )
                return
            
            # เรียก API
            result = await self.api_client.get_diagnosis(input_data)
            
            # แสดงผล
            self.result_widget.setVisible(True)
            self.result_widget.update_result(result)
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "เกิดข้อผิดพลาด",
                f"ไม่สามารถวินิจฉัยได้: {str(e)}"
            ) 