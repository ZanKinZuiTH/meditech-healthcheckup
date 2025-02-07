from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QScrollArea, QSizePolicy, QSpacerItem
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor

from ..components.charts import LineChart, BarChart, PieChart
from ..components.base import Card, BaseButton
from ..styles.theme import Theme

class StatCard(Card):
    """การ์ดแสดงสถิติ"""
    
    def __init__(self, title, value, icon_path, color, parent=None):
        super().__init__(parent)
        self.setup_stat_ui(title, value, icon_path, color)
    
    def setup_stat_ui(self, title, value, icon_path, color):
        layout = QVBoxLayout(self)
        layout.setSpacing(Theme.SPACING['sm'])
        
        # หัวข้อ
        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            color: {Theme.COLORS['grey'][600]};
            font-size: {Theme.TYPOGRAPHY['fontSize']['sm']}px;
        """)
        
        # ค่า
        value_label = QLabel(value)
        value_label.setStyleSheet(f"""
            color: {color};
            font-size: {Theme.TYPOGRAPHY['fontSize']['3xl']}px;
            font-weight: {Theme.TYPOGRAPHY['fontWeight']['bold']};
        """)
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)

class AdminDashboard(QWidget):
    """หน้า Dashboard สำหรับผู้ดูแลระบบ"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(Theme.SPACING['xl'])
        main_layout.setContentsMargins(
            Theme.SPACING['xl'],
            Theme.SPACING['xl'],
            Theme.SPACING['xl'],
            Theme.SPACING['xl']
        )
        
        # ส่วนบนแสดงสถิติ
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(Theme.SPACING['lg'])
        
        # สร้างการ์ดสถิติ
        stats = [
            ("ผู้ป่วยทั้งหมด", "1,234", "icons/patients.svg", Theme.COLORS['primary']['main']),
            ("นัดหมายวันนี้", "45", "icons/calendar.svg", Theme.COLORS['success']['main']),
            ("รอดำเนินการ", "12", "icons/pending.svg", Theme.COLORS['warning']['main']),
            ("รายได้เดือนนี้", "฿123,456", "icons/revenue.svg", Theme.COLORS['info']['main'])
        ]
        
        for title, value, icon, color in stats:
            card = StatCard(title, value, icon, color)
            stats_layout.addWidget(card)
        
        main_layout.addLayout(stats_layout)
        
        # ส่วนกลางแสดงกราฟ
        charts_layout = QHBoxLayout()
        charts_layout.setSpacing(Theme.SPACING['lg'])
        
        # กราฟแสดงจำนวนผู้ป่วยรายเดือน
        patients_chart = Card("จำนวนผู้ป่วยรายเดือน")
        line_chart = LineChart()
        patients_chart.add_widget(line_chart)
        charts_layout.addWidget(patients_chart, stretch=2)
        
        charts_right_layout = QVBoxLayout()
        charts_right_layout.setSpacing(Theme.SPACING['lg'])
        
        # กราฟวงกลมแสดงประเภทการตรวจ
        exam_types_chart = Card("ประเภทการตรวจ")
        pie_chart = PieChart()
        exam_types_chart.add_widget(pie_chart)
        charts_right_layout.addWidget(exam_types_chart)
        
        # กราฟแท่งแสดงรายได้
        revenue_chart = Card("รายได้รายวัน")
        bar_chart = BarChart()
        revenue_chart.add_widget(bar_chart)
        charts_right_layout.addWidget(revenue_chart)
        
        charts_layout.addLayout(charts_right_layout, stretch=1)
        main_layout.addLayout(charts_layout)
        
        # ส่วนล่างแสดงตารางและการแจ้งเตือน
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(Theme.SPACING['lg'])
        
        # ตารางนัดหมายวันนี้
        appointments_card = Card("นัดหมายวันนี้")
        appointments_table = self.create_appointments_table()
        appointments_card.add_widget(appointments_table)
        bottom_layout.addWidget(appointments_card)
        
        # การแจ้งเตือนและกิจกรรม
        notifications_card = Card("การแจ้งเตือนและกิจกรรม")
        notifications_list = self.create_notifications_list()
        notifications_card.add_widget(notifications_list)
        bottom_layout.addWidget(notifications_card)
        
        main_layout.addLayout(bottom_layout)
    
    def create_appointments_table(self):
        # TODO: สร้างตารางนัดหมาย
        return QWidget()
    
    def create_notifications_list(self):
        # TODO: สร้างรายการแจ้งเตือน
        return QWidget()
    
    def load_data(self):
        # TODO: โหลดข้อมูลจริงจาก API
        pass 