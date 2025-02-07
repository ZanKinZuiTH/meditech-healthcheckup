from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel,
    QScrollArea, QWidget, QPushButton, QComboBox,
    QDateEdit, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QIcon
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog

from ...styles.theme import Theme

class ReportFilter(QFrame):
    """ตัวกรองรายงาน"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
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
        
        layout = QHBoxLayout(self)
        layout.setSpacing(Theme.SPACING['lg'])
        
        # ประเภทรายงาน
        report_type = QComboBox()
        report_type.addItems([
            "รายงานการนัดหมาย",
            "รายงานผลการตรวจ",
            "รายงานรายได้",
            "รายงานสถิติผู้ป่วย"
        ])
        report_type.setStyleSheet(self.get_input_style())
        layout.addWidget(report_type)
        
        # วันที่เริ่มต้น
        start_date = QDateEdit()
        start_date.setCalendarPopup(True)
        start_date.setDate(QDate.currentDate().addMonths(-1))
        start_date.setStyleSheet(self.get_input_style())
        layout.addWidget(start_date)
        
        # วันที่สิ้นสุด
        end_date = QDateEdit()
        end_date.setCalendarPopup(True)
        end_date.setDate(QDate.currentDate())
        end_date.setStyleSheet(self.get_input_style())
        layout.addWidget(end_date)
        
        # ปุ่มค้นหา
        search = QPushButton("ค้นหา")
        search.setStyleSheet(f"""
            QPushButton {{
                background: {Theme.COLORS['primary']['main']};
                color: white;
                border: none;
                padding: {Theme.SPACING['sm']}px {Theme.SPACING['lg']}px;
                border-radius: {Theme.BORDER_RADIUS['md']};
                font-weight: {Theme.TYPOGRAPHY['fontWeight']['medium']};
            }}
            QPushButton:hover {{
                background: {Theme.COLORS['primary']['dark']};
            }}
        """)
        layout.addWidget(search)
    
    def get_input_style(self):
        """สไตล์สำหรับ input"""
        return f"""
            padding: {Theme.SPACING['sm']}px;
            border: 1px solid {Theme.COLORS['grey'][300]};
            border-radius: {Theme.BORDER_RADIUS['md']};
            background: white;
            min-width: 200px;
        """

class ReportTable(QFrame):
    """ตารางแสดงรายงาน"""
    
    def __init__(self, headers, data=None, parent=None):
        super().__init__(parent)
        self.headers = headers
        self.data = data or []
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
        layout.setSpacing(Theme.SPACING['lg'])
        
        # ส่วนหัว
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        title = QLabel("รายงาน")
        title.setStyleSheet(f"""
            color: {Theme.COLORS['grey'][900]};
            font-size: {Theme.TYPOGRAPHY['fontSize']['lg']}px;
            font-weight: {Theme.TYPOGRAPHY['fontWeight']['medium']};
        """)
        header_layout.addWidget(title)
        
        export = QPushButton("ส่งออก PDF")
        export.setStyleSheet(f"""
            QPushButton {{
                color: {Theme.COLORS['primary']['main']};
                border: 1px solid {Theme.COLORS['primary']['main']};
                padding: {Theme.SPACING['sm']}px {Theme.SPACING['lg']}px;
                border-radius: {Theme.BORDER_RADIUS['md']};
            }}
            QPushButton:hover {{
                background: {Theme.COLORS['primary'][50]};
            }}
        """)
        export.clicked.connect(self.export_pdf)
        header_layout.addWidget(export)
        
        layout.addWidget(header)
        
        # ตาราง
        table = QTableWidget()
        table.setColumnCount(len(self.headers))
        table.setHorizontalHeaderLabels(self.headers)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setStyleSheet(f"""
            QTableWidget {{
                border: none;
                gridline-color: {Theme.COLORS['grey'][200]};
            }}
            QHeaderView::section {{
                background: {Theme.COLORS['grey'][50]};
                color: {Theme.COLORS['grey'][700]};
                font-weight: {Theme.TYPOGRAPHY['fontWeight']['medium']};
                padding: {Theme.SPACING['sm']}px;
                border: none;
                border-bottom: 1px solid {Theme.COLORS['grey'][200]};
            }}
        """)
        
        # เพิ่มข้อมูล
        table.setRowCount(len(self.data))
        for i, row in enumerate(self.data):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                table.setItem(i, j, item)
        
        layout.addWidget(table)
    
    def export_pdf(self):
        """ส่งออกรายงานเป็น PDF"""
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
        
        dialog = QPrintDialog(printer)
        if dialog.exec() == QPrintDialog.DialogCode.Accepted:
            # TODO: สร้าง PDF จากข้อมูลในตาราง
            pass

class ReportDashboard(QFrame):
    """หน้าแสดงรายงานและสถิติ"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(Theme.SPACING['xl'])
        layout.setContentsMargins(
            Theme.SPACING['xl'],
            Theme.SPACING['xl'],
            Theme.SPACING['xl'],
            Theme.SPACING['xl']
        )
        
        # ตัวกรอง
        filter = ReportFilter()
        layout.addWidget(filter)
        
        # ตารางรายงาน
        headers = ["วันที่", "รหัสผู้ป่วย", "ชื่อ-นามสกุล", "รายการตรวจ", "ค่าใช้จ่าย", "สถานะ"]
        data = [
            ["2024-01-18", "P001", "สมชาย ใจดี", "ตรวจสุขภาพประจำปี", "2,500", "เสร็จสิ้น"],
            ["2024-01-18", "P002", "สมหญิง รักดี", "ตรวจเลือด", "1,500", "รอผล"],
            ["2024-01-18", "P003", "มานี มีสุข", "X-Ray", "3,000", "เสร็จสิ้น"]
        ]
        table = ReportTable(headers, data)
        layout.addWidget(table) 