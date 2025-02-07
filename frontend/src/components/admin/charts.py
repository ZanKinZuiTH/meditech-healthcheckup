from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtChart import (
    QChart, QChartView, QLineSeries, QPieSeries,
    QBarSeries, QBarSet, QValueAxis, QBarCategoryAxis
)
from PyQt6.QtGui import QPainter, QColor

from ...styles.theme import Theme

class BaseChart(QFrame):
    """คลาสพื้นฐานสำหรับกราฟ"""
    
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.title = title
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(Theme.SPACING['sm'])
        
        # หัวข้อ
        title = QLabel(self.title)
        title.setStyleSheet(f"""
            color: {Theme.COLORS['grey'][900]};
            font-size: {Theme.TYPOGRAPHY['fontSize']['lg']}px;
            font-weight: {Theme.TYPOGRAPHY['fontWeight']['medium']};
        """)
        layout.addWidget(title)
        
        # กราฟ
        self.chart = QChart()
        self.chart.setBackgroundVisible(False)
        self.chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        
        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.chart_view.setStyleSheet(f"""
            background: white;
            border: 1px solid {Theme.COLORS['grey'][200]};
            border-radius: {Theme.BORDER_RADIUS['lg']};
        """)
        
        layout.addWidget(self.chart_view)

class LineChart(BaseChart):
    """กราฟเส้น"""
    
    def __init__(self, title, data, parent=None):
        super().__init__(title, parent)
        self.data = data
        self.plot_data()
    
    def plot_data(self):
        series = QLineSeries()
        series.setColor(QColor(Theme.COLORS['primary']['main']))
        
        for x, y in self.data:
            series.append(x, y)
        
        self.chart.addSeries(series)
        
        # แกน X
        axis_x = QValueAxis()
        axis_x.setRange(min(x for x, _ in self.data), max(x for x, _ in self.data))
        self.chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axis_x)
        
        # แกน Y
        axis_y = QValueAxis()
        axis_y.setRange(min(y for _, y in self.data), max(y for _, y in self.data))
        self.chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_y)

class PieChart(BaseChart):
    """กราฟวงกลม"""
    
    def __init__(self, title, data, parent=None):
        super().__init__(title, parent)
        self.data = data
        self.plot_data()
    
    def plot_data(self):
        series = QPieSeries()
        
        colors = [
            Theme.COLORS['primary']['main'],
            Theme.COLORS['secondary']['main'],
            Theme.COLORS['success']['main'],
            Theme.COLORS['warning']['main'],
            Theme.COLORS['error']['main']
        ]
        
        for i, (label, value) in enumerate(self.data):
            slice = series.append(label, value)
            slice.setBrush(QColor(colors[i % len(colors)]))
        
        self.chart.addSeries(series)
        series.setLabelsVisible(True)

class BarChart(BaseChart):
    """กราฟแท่ง"""
    
    def __init__(self, title, data, parent=None):
        super().__init__(title, parent)
        self.data = data
        self.plot_data()
    
    def plot_data(self):
        series = QBarSeries()
        
        # สร้างชุดข้อมูล
        bar_set = QBarSet("")
        bar_set.setColor(QColor(Theme.COLORS['primary']['main']))
        categories = []
        
        for label, value in self.data:
            bar_set.append(value)
            categories.append(label)
        
        series.append(bar_set)
        self.chart.addSeries(series)
        
        # แกน X (หมวดหมู่)
        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        self.chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axis_x)
        
        # แกน Y (ค่า)
        axis_y = QValueAxis()
        axis_y.setRange(0, max(value for _, value in self.data))
        self.chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_y)

class StatsCard(QFrame):
    """การ์ดแสดงสถิติ"""
    
    def __init__(self, title, value, icon=None, color=None, parent=None):
        super().__init__(parent)
        self.title = title
        self.value = value
        self.icon = icon
        self.color = color or Theme.COLORS['primary']['main']
        self.setup_ui()
    
    def setup_ui(self):
        self.setStyleSheet(f"""
            QFrame {{
                background: white;
                border: 1px solid {Theme.COLORS['grey'][200]};
                border-radius: {Theme.BORDER_RADIUS['lg']};
                padding: {Theme.SPACING['lg']}px;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(Theme.SPACING['xs'])
        
        # หัวข้อ
        title = QLabel(self.title)
        title.setStyleSheet(f"""
            color: {Theme.COLORS['grey'][600]};
            font-size: {Theme.TYPOGRAPHY['fontSize']['sm']}px;
        """)
        layout.addWidget(title)
        
        # ค่า
        value = QLabel(str(self.value))
        value.setStyleSheet(f"""
            color: {self.color};
            font-size: {Theme.TYPOGRAPHY['fontSize']['xl']}px;
            font-weight: {Theme.TYPOGRAPHY['fontWeight']['bold']};
        """)
        layout.addWidget(value)
        
        # ไอคอน (ถ้ามี)
        if self.icon:
            icon = QLabel()
            icon.setPixmap(self.icon.pixmap(24, 24))
            layout.addWidget(icon, alignment=Qt.AlignmentFlag.AlignRight) 