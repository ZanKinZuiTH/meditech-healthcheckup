from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
import pyqtgraph as pg
import numpy as np
from ..styles.theme import Theme

class BaseChart(QWidget):
    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self.title = title
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # สร้าง PlotWidget
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('w')
        self.plot_widget.showGrid(x=True, y=True)
        
        if self.title:
            self.plot_widget.setTitle(self.title, size=Theme.FONT_SIZES["lg"])
        
        layout.addWidget(self.plot_widget)

        # ตั้งค่าสไตล์
        self.setup_style()

    def setup_style(self):
        # ตั้งค่าสีและสไตล์
        self.plot_widget.getAxis('bottom').setPen(pg.mkPen(color='#212121'))
        self.plot_widget.getAxis('left').setPen(pg.mkPen(color='#212121'))
        self.plot_widget.getAxis('bottom').setTextPen(pg.mkPen(color='#212121'))
        self.plot_widget.getAxis('left').setTextPen(pg.mkPen(color='#212121'))

class LineChart(BaseChart):
    def __init__(self, title="", parent=None):
        super().__init__(title, parent)
        self.lines = []

    def add_line(self, x_data, y_data, name="", color=None):
        pen = pg.mkPen(color=color or Theme.PRIMARY, width=2)
        line = self.plot_widget.plot(x_data, y_data, name=name, pen=pen)
        self.lines.append(line)
        
        if name:
            self.plot_widget.addLegend()

    def clear(self):
        self.plot_widget.clear()
        self.lines = []

class BarChart(BaseChart):
    def __init__(self, title="", parent=None):
        super().__init__(title, parent)
        self.bars = []

    def add_bars(self, x_data, y_data, names=None, colors=None):
        self.plot_widget.clear()
        
        if colors is None:
            colors = [Theme.PRIMARY] * len(x_data)
        
        # สร้าง bar graph
        bargraph = pg.BarGraphItem(
            x=range(len(x_data)),
            height=y_data,
            width=0.6,
            brush=colors
        )
        self.plot_widget.addItem(bargraph)
        
        # ตั้งค่าแกน x
        if names:
            ax = self.plot_widget.getAxis('bottom')
            ax.setTicks([[(i, name) for i, name in enumerate(names)]])

class PieChart(BaseChart):
    def __init__(self, title="", parent=None):
        super().__init__(title, parent)

    def set_data(self, values, labels=None, colors=None):
        self.plot_widget.clear()
        
        if colors is None:
            colors = [Theme.PRIMARY, Theme.SECONDARY, Theme.SUCCESS, Theme.WARNING, Theme.ERROR]
            colors = colors * (len(values) // len(colors) + 1)
            colors = colors[:len(values)]
        
        total = sum(values)
        start_angle = 0
        
        for i, value in enumerate(values):
            angle = value * 360 / total
            
            # สร้าง pie segment
            path = pg.arrayToQPath([0, 0], [0, 0], closed=True)
            item = pg.QtGui.QGraphicsPathItem(path)
            item.setPen(pg.mkPen(colors[i]))
            item.setBrush(pg.mkBrush(colors[i]))
            
            # หมุน segment
            transform = pg.QtGui.QTransform()
            transform.rotate(start_angle)
            item.setTransform(transform)
            
            self.plot_widget.addItem(item)
            
            # เพิ่ม label
            if labels:
                label = pg.TextItem(text=f"{labels[i]}\n{value:.1f}%")
                angle_rad = np.radians(start_angle + angle/2)
                x = np.cos(angle_rad) * 0.8
                y = np.sin(angle_rad) * 0.8
                label.setPos(x, y)
                self.plot_widget.addItem(label)
            
            start_angle += angle

class ScatterPlot(BaseChart):
    def __init__(self, title="", parent=None):
        super().__init__(title, parent)

    def add_points(self, x_data, y_data, name="", color=None, size=10, symbol='o'):
        pen = pg.mkPen(None)
        brush = pg.mkBrush(color or Theme.PRIMARY)
        
        scatter = pg.ScatterPlotItem(
            x=x_data,
            y=y_data,
            pen=pen,
            brush=brush,
            size=size,
            symbol=symbol,
            name=name
        )
        
        self.plot_widget.addItem(scatter)
        
        if name:
            self.plot_widget.addLegend()

class HeatMap(BaseChart):
    def __init__(self, title="", parent=None):
        super().__init__(title, parent)

    def set_data(self, data, x_labels=None, y_labels=None):
        self.plot_widget.clear()
        
        # สร้าง color map
        colormap = pg.ColorMap(
            pos=np.linspace(0.0, 1.0, 6),
            color=[(25,25,112), (0,0,255), (0,255,255), (0,255,0), (255,255,0), (255,0,0)]
        )
        
        # สร้าง heat map
        heatmap = pg.ImageItem()
        heatmap.setImage(data)
        heatmap.setLookupTable(colormap.getLookupTable())
        
        self.plot_widget.addItem(heatmap)
        
        # เพิ่ม labels
        if x_labels:
            ax = self.plot_widget.getAxis('bottom')
            ax.setTicks([[(i, label) for i, label in enumerate(x_labels)]])
        
        if y_labels:
            ay = self.plot_widget.getAxis('left')
            ay.setTicks([[(i, label) for i, label in enumerate(y_labels)]]) 