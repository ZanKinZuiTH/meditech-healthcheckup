import sys
import pytest
from PyQt6.QtWidgets import QApplication
from PyQt6.QtTest import QTest
from PyQt6.QtCore import Qt

from app.main import MediTechApp
from app.ui.main_window import MainWindow
from app.ui.components.base import BaseButton, BaseInput
from app.ui.components.charts import LineChart, BarChart
from app.ui.components.reports import ReportGenerator

@pytest.fixture
def app():
    return MediTechApp(sys.argv)

@pytest.fixture
def main_window(app):
    return MainWindow()

class TestMainWindow:
    def test_window_title(self, main_window):
        assert main_window.windowTitle() == "MediTech HealthCheckup"

    def test_sidebar_exists(self, main_window):
        assert main_window.sidebar is not None
        assert len(main_window.sidebar.actions()) > 0

    def test_content_area_exists(self, main_window):
        assert main_window.content_area is not None

class TestBaseComponents:
    def test_base_button(self, app):
        button = BaseButton("Test Button")
        assert button.text() == "Test Button"
        assert button.isEnabled()

    def test_base_input(self, app):
        input_field = BaseInput()
        test_text = "Test Input"
        QTest.keyClicks(input_field, test_text)
        assert input_field.text() == test_text

class TestCharts:
    def test_line_chart(self, app):
        chart = LineChart()
        data = [(1, 10), (2, 20), (3, 30)]
        chart.add_line(data, "Test Line")
        assert len(chart.plot_items) == 1

    def test_bar_chart(self, app):
        chart = BarChart()
        data = {"A": 10, "B": 20, "C": 30}
        chart.set_data(data)
        assert len(chart.bars) == len(data)

class TestReports:
    def test_report_generator(self, app):
        generator = ReportGenerator()
        assert generator.report_types.count() > 0
        assert generator.date_range_start is not None
        assert generator.date_range_end is not None

    def test_generate_report(self, app, main_window):
        generator = ReportGenerator()
        generator.report_type.setCurrentText("สรุปผลตรวจสุขภาพ")
        success = generator.generate_report()
        assert success

class TestAccessibility:
    def test_font_size_change(self, main_window):
        original_size = main_window.font().pointSize()
        main_window.accessibility_manager.change_font_size(original_size + 2)
        assert main_window.font().pointSize() == original_size + 2

    def test_dark_mode_toggle(self, main_window):
        main_window.accessibility_manager.toggle_dark_mode(True)
        palette = main_window.palette()
        assert palette.color(palette.ColorRole.Window).name() in ["#2d2d2d", "#1e1e1e"]

    def test_high_contrast_toggle(self, main_window):
        main_window.accessibility_manager.toggle_high_contrast(True)
        palette = main_window.palette()
        assert palette.color(palette.ColorRole.WindowText).name() == "#ffffff"

class TestNavigation:
    def test_keyboard_navigation(self, main_window):
        main_window.show()
        QTest.keyClick(main_window, Qt.Key.Key_Tab)
        assert main_window.focusWidget() is not None

    def test_menu_navigation(self, main_window):
        menu_items = main_window.menuBar().actions()
        assert len(menu_items) > 0
        first_menu = menu_items[0]
        assert first_menu.menu() is not None 