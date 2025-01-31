from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QComboBox, QDateEdit, QTableWidget,
    QTableWidgetItem, QFileDialog, QPrintDialog
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtPrintSupport import QPrinter
from PyQt6.QtGui import QPainter, QFont, QRect, QImage
from PyQt6.QtCore import QFile
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from .base import BaseButton, Card
from .charts import LineChart, BarChart, PieChart
from ..styles.theme import Theme

class ReportGenerator(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Controls
        controls_layout = QHBoxLayout()
        
        # Report Type
        self.report_type = QComboBox()
        self.report_type.addItems([
            "รายงานผลตรวจสุขภาพ",
            "รายงานสถิติผู้ป่วย",
            "รายงานการนัดหมาย",
            "รายงานการเงิน"
        ])
        controls_layout.addWidget(QLabel("ประเภทรายงาน:"))
        controls_layout.addWidget(self.report_type)

        # Date Range
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate().addMonths(-1))
        self.end_date = QDateEdit()
        self.end_date.setDate(QDate.currentDate())
        
        controls_layout.addWidget(QLabel("วันที่เริ่มต้น:"))
        controls_layout.addWidget(self.start_date)
        controls_layout.addWidget(QLabel("วันที่สิ้นสุด:"))
        controls_layout.addWidget(self.end_date)

        # Buttons
        self.generate_btn = BaseButton("สร้างรายงาน", variant="primary")
        self.generate_btn.clicked.connect(self.generate_report)
        self.export_btn = BaseButton("ส่งออก", variant="secondary")
        self.export_btn.clicked.connect(self.export_report)
        self.print_btn = BaseButton("พิมพ์", variant="info")
        self.print_btn.clicked.connect(self.print_report)
        
        controls_layout.addWidget(self.generate_btn)
        controls_layout.addWidget(self.export_btn)
        controls_layout.addWidget(self.print_btn)
        
        layout.addLayout(controls_layout)

        # Report Content
        self.content_card = Card("เนื้อหารายงาน")
        self.content_layout = QVBoxLayout()
        
        # Table
        self.table = QTableWidget()
        self.content_layout.addWidget(self.table)
        
        # Charts
        charts_layout = QHBoxLayout()
        
        # Line Chart
        self.line_chart = LineChart("แนวโน้มตามเวลา")
        charts_layout.addWidget(self.line_chart)
        
        # Bar Chart
        self.bar_chart = BarChart("การเปรียบเทียบ")
        charts_layout.addWidget(self.bar_chart)
        
        # Pie Chart
        self.pie_chart = PieChart("สัดส่วน")
        charts_layout.addWidget(self.pie_chart)
        
        self.content_layout.addLayout(charts_layout)
        self.content_card.add_layout(self.content_layout)
        layout.addWidget(self.content_card)

    def generate_report(self):
        # ตัวอย่างข้อมูล
        data = {
            'วันที่': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05'],
            'จำนวนผู้ป่วย': [10, 15, 12, 18, 20],
            'รายได้': [5000, 7500, 6000, 9000, 10000]
        }
        df = pd.DataFrame(data)

        # แสดงตาราง
        self.display_table(df)

        # แสดงกราฟ
        self.display_charts(df)

    def display_table(self, df):
        self.table.setRowCount(len(df))
        self.table.setColumnCount(len(df.columns))
        self.table.setHorizontalHeaderLabels(df.columns)

        for i in range(len(df)):
            for j in range(len(df.columns)):
                item = QTableWidgetItem(str(df.iloc[i, j]))
                self.table.setItem(i, j, item)

        self.table.resizeColumnsToContents()

    def display_charts(self, df):
        # Line Chart
        self.line_chart.clear()
        self.line_chart.add_line(
            range(len(df)),
            df['จำนวนผู้ป่วย'].values,
            name='จำนวนผู้ป่วย'
        )

        # Bar Chart
        self.bar_chart.add_bars(
            df['วันที่'].values,
            df['รายได้'].values,
            names=df['วันที่'].values
        )

        # Pie Chart
        total_patients = df['จำนวนผู้ป่วย'].sum()
        values = [x/total_patients*100 for x in df['จำนวนผู้ป่วย']]
        self.pie_chart.set_data(values, labels=df['วันที่'].values)

    def export_report(self):
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "บันทึกรายงาน",
            "",
            "PDF Files (*.pdf);;Excel Files (*.xlsx)"
        )
        
        if filename:
            if filename.endswith('.pdf'):
                self.export_to_pdf(filename)
            elif filename.endswith('.xlsx'):
                self.export_to_excel(filename)

    def export_to_pdf(self, filename):
        doc = SimpleDocTemplate(filename, pagesize=A4)
        elements = []
        
        # Title
        styles = getSampleStyleSheet()
        elements.append(Paragraph(f"รายงาน{self.report_type.currentText()}", styles['Title']))
        
        # Table Data
        table_data = []
        headers = []
        for j in range(self.table.columnCount()):
            headers.append(self.table.horizontalHeaderItem(j).text())
        table_data.append(headers)
        
        for i in range(self.table.rowCount()):
            row = []
            for j in range(self.table.columnCount()):
                item = self.table.item(i, j)
                row.append(item.text() if item else "")
            table_data.append(row)
        
        # Create Table
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        doc.build(elements)

    def export_to_excel(self, filename):
        data = []
        headers = []
        
        for j in range(self.table.columnCount()):
            headers.append(self.table.horizontalHeaderItem(j).text())
        
        for i in range(self.table.rowCount()):
            row = []
            for j in range(self.table.columnCount()):
                item = self.table.item(i, j)
                row.append(item.text() if item else "")
            data.append(row)
        
        df = pd.DataFrame(data, columns=headers)
        df.to_excel(filename, index=False)

    def print_report(self):
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        dialog = QPrintDialog(printer, self)
        
        if dialog.exec() == QPrintDialog.DialogCode.Accepted:
            # ตั้งค่าการพิมพ์
            painter = QPainter()
            painter.begin(printer)

            # พิมพ์หัวข้อ
            font = QFont()
            font.setPointSize(16)
            font.setBold(True)
            painter.setFont(font)
            painter.drawText(
                QRect(0, 0, printer.width(), 50),
                Qt.AlignmentFlag.AlignCenter,
                f"รายงาน{self.report_type.currentText()}"
            )

            # พิมพ์ตาราง
            table_rect = QRect(50, 100, printer.width() - 100, printer.height() - 200)
            self.print_table(painter, table_rect)

            # พิมพ์กราฟ
            charts_rect = QRect(50, table_rect.bottom() + 50, printer.width() - 100, 300)
            self.print_charts(painter, charts_rect)

            painter.end()

    def print_table(self, painter, rect):
        # คำนวณขนาดของแต่ละเซลล์
        row_height = 30
        col_width = rect.width() / self.table.columnCount()
        
        # วาดหัวตาราง
        font = QFont()
        font.setBold(True)
        painter.setFont(font)
        
        for col in range(self.table.columnCount()):
            header_rect = QRect(
                rect.left() + col * col_width,
                rect.top(),
                col_width,
                row_height
            )
            painter.drawRect(header_rect)
            painter.drawText(
                header_rect,
                Qt.AlignmentFlag.AlignCenter,
                self.table.horizontalHeaderItem(col).text()
            )

        # วาดข้อมูล
        font.setBold(False)
        painter.setFont(font)
        
        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                cell_rect = QRect(
                    rect.left() + col * col_width,
                    rect.top() + (row + 1) * row_height,
                    col_width,
                    row_height
                )
                painter.drawRect(cell_rect)
                
                item = self.table.item(row, col)
                if item:
                    painter.drawText(
                        cell_rect,
                        Qt.AlignmentFlag.AlignCenter,
                        item.text()
                    )

    def print_charts(self, painter, rect):
        # แบ่งพื้นที่สำหรับกราฟแต่ละอัน
        chart_width = rect.width() / 3
        
        # พิมพ์กราฟเส้น
        line_rect = QRect(rect.left(), rect.top(), chart_width, rect.height())
        self.line_chart.grab().save("temp_line.png")
        painter.drawImage(line_rect, QImage("temp_line.png"))
        
        # พิมพ์กราฟแท่ง
        bar_rect = QRect(rect.left() + chart_width, rect.top(), chart_width, rect.height())
        self.bar_chart.grab().save("temp_bar.png")
        painter.drawImage(bar_rect, QImage("temp_bar.png"))
        
        # พิมพ์กราฟวงกลม
        pie_rect = QRect(rect.left() + 2 * chart_width, rect.top(), chart_width, rect.height())
        self.pie_chart.grab().save("temp_pie.png")
        painter.drawImage(pie_rect, QImage("temp_pie.png"))
        
        # ลบไฟล์ชั่วคราว
        QFile.remove("temp_line.png")
        QFile.remove("temp_bar.png")
        QFile.remove("temp_pie.png") 