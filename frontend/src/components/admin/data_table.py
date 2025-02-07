from PyQt6.QtWidgets import (
    QTableWidget, QTableWidgetItem, QWidget, QVBoxLayout,
    QHBoxLayout, QLineEdit, QComboBox, QPushButton,
    QHeaderView, QMenu, QLabel
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QAction

from ...styles.theme import Theme
from ..base import BaseButton

class DataTable(QWidget):
    """ตารางข้อมูลขั้นสูงพร้อมฟีเจอร์การจัดการ"""
    
    item_selected = pyqtSignal(dict)
    item_deleted = pyqtSignal(str)
    item_edited = pyqtSignal(dict)
    
    def __init__(
        self,
        columns,
        actions=True,
        searchable=True,
        filterable=True,
        parent=None
    ):
        super().__init__(parent)
        self.columns = columns
        self.show_actions = actions
        self.show_search = searchable
        self.show_filter = filterable
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(Theme.SPACING['lg'])
        layout.setContentsMargins(0, 0, 0, 0)
        
        # แถบเครื่องมือด้านบน
        toolbar = QHBoxLayout()
        toolbar.setSpacing(Theme.SPACING['base'])
        
        # ช่องค้นหา
        if self.show_search:
            self.search_input = QLineEdit()
            self.search_input.setPlaceholderText("ค้นหา...")
            self.search_input.textChanged.connect(self.handle_search)
            self.search_input.setStyleSheet(f"""
                QLineEdit {{
                    padding: {Theme.SPACING['sm']}px;
                    border: 1px solid {Theme.COLORS['grey'][300]};
                    border-radius: {Theme.BORDER_RADIUS['base']};
                    background: {Theme.COLORS['grey'][100]};
                }}
                QLineEdit:focus {{
                    border-color: {Theme.COLORS['primary']['main']};
                }}
            """)
            toolbar.addWidget(self.search_input)
        
        # ตัวกรอง
        if self.show_filter:
            self.filter_combo = QComboBox()
            self.filter_combo.addItem("ทั้งหมด")
            self.filter_combo.currentTextChanged.connect(self.handle_filter)
            self.filter_combo.setStyleSheet(f"""
                QComboBox {{
                    padding: {Theme.SPACING['sm']}px;
                    border: 1px solid {Theme.COLORS['grey'][300]};
                    border-radius: {Theme.BORDER_RADIUS['base']};
                    background: {Theme.COLORS['grey'][100]};
                }}
                QComboBox:focus {{
                    border-color: {Theme.COLORS['primary']['main']};
                }}
            """)
            toolbar.addWidget(self.filter_combo)
        
        toolbar.addStretch()
        
        # ปุ่มเพิ่มข้อมูล
        if self.show_actions:
            add_button = BaseButton(
                text="เพิ่มข้อมูล",
                icon="icons/add.svg",
                variant="primary"
            )
            add_button.clicked.connect(self.handle_add)
            toolbar.addWidget(add_button)
        
        layout.addLayout(toolbar)
        
        # ตาราง
        self.table = QTableWidget()
        self.table.setColumnCount(len(self.columns))
        self.table.setHorizontalHeaderLabels([col['title'] for col in self.columns])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        
        # สไตล์ตาราง
        self.table.setStyleSheet(f"""
            QTableWidget {{
                border: 1px solid {Theme.COLORS['grey'][200]};
                border-radius: {Theme.BORDER_RADIUS['base']};
                background: white;
            }}
            QTableWidget::item {{
                padding: {Theme.SPACING['sm']}px;
            }}
            QTableWidget::item:selected {{
                background: {Theme.COLORS['primary']['light']};
                color: {Theme.COLORS['primary']['main']};
            }}
            QHeaderView::section {{
                background: {Theme.COLORS['grey'][100]};
                padding: {Theme.SPACING['sm']}px;
                border: none;
                font-weight: bold;
            }}
        """)
        
        layout.addWidget(self.table)
        
        # แถบสถานะด้านล่าง
        status_bar = QHBoxLayout()
        
        self.total_label = QLabel("รายการทั้งหมด: 0")
        status_bar.addWidget(self.total_label)
        
        status_bar.addStretch()
        
        self.selected_label = QLabel("เลือก: 0 รายการ")
        status_bar.addWidget(self.selected_label)
        
        layout.addLayout(status_bar)
    
    def set_data(self, data):
        """กำหนดข้อมูลในตาราง"""
        self.table.setRowCount(len(data))
        
        for row, item in enumerate(data):
            for col, column in enumerate(self.columns):
                cell_widget = self.create_cell_widget(item.get(column['key']), column.get('type', 'text'))
                self.table.setCellWidget(row, col, cell_widget)
            
            # เพิ่มปุ่มจัดการ
            if self.show_actions:
                actions_widget = self.create_actions_widget(item)
                self.table.setCellWidget(row, len(self.columns) - 1, actions_widget)
        
        self.total_label.setText(f"รายการทั้งหมด: {len(data)}")
    
    def create_cell_widget(self, value, type='text'):
        """สร้าง Widget สำหรับเซลล์ตามประเภทข้อมูล"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(Theme.SPACING['sm'], 0, Theme.SPACING['sm'], 0)
        
        if type == 'text':
            label = QLabel(str(value))
            layout.addWidget(label)
        elif type == 'status':
            label = QLabel(str(value))
            # TODO: เพิ่มสีตามสถานะ
            layout.addWidget(label)
        elif type == 'image':
            # TODO: แสดงรูปภาพขนาดเล็ก
            pass
        
        return widget
    
    def create_actions_widget(self, item):
        """สร้างปุ่มจัดการสำหรับแต่ละแถว"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(Theme.SPACING['sm'], 0, Theme.SPACING['sm'], 0)
        
        # ปุ่มแก้ไข
        edit_button = BaseButton(icon="icons/edit.svg", variant="secondary", size="sm")
        edit_button.clicked.connect(lambda: self.handle_edit(item))
        layout.addWidget(edit_button)
        
        # ปุ่มลบ
        delete_button = BaseButton(icon="icons/delete.svg", variant="danger", size="sm")
        delete_button.clicked.connect(lambda: self.handle_delete(item))
        layout.addWidget(delete_button)
        
        return widget
    
    def handle_search(self, text):
        """จัดการการค้นหา"""
        # TODO: กรองข้อมูลตามคำค้นหา
        pass
    
    def handle_filter(self, value):
        """จัดการการกรอง"""
        # TODO: กรองข้อมูลตามตัวกรอง
        pass
    
    def handle_add(self):
        """จัดการการเพิ่มข้อมูล"""
        # TODO: แสดงฟอร์มเพิ่มข้อมูล
        pass
    
    def handle_edit(self, item):
        """จัดการการแก้ไขข้อมูล"""
        self.item_edited.emit(item)
    
    def handle_delete(self, item):
        """จัดการการลบข้อมูล"""
        self.item_deleted.emit(item['id']) 