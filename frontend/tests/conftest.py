import sys
import pytest
from PyQt6.QtWidgets import QApplication

from app.main import MediTechApp
from app.ui.main_window import MainWindow
from app.ui.components.base import BaseButton, BaseInput
from app.ui.components.charts import LineChart, BarChart
from app.ui.components.reports import ReportGenerator

@pytest.fixture(scope="session")
def qapp():
    app = QApplication(sys.argv)
    yield app
    app.quit()

@pytest.fixture
def app(qapp):
    return MediTechApp(sys.argv)

@pytest.fixture
def main_window(app):
    window = MainWindow()
    window.show()
    return window

@pytest.fixture
def base_button():
    return BaseButton("Test Button")

@pytest.fixture
def base_input():
    return BaseInput()

@pytest.fixture
def line_chart():
    return LineChart()

@pytest.fixture
def bar_chart():
    return BarChart()

@pytest.fixture
def report_generator():
    return ReportGenerator()

@pytest.fixture
def test_data():
    return {
        "line_data": [(1, 10), (2, 20), (3, 30)],
        "bar_data": {"A": 10, "B": 20, "C": 30},
        "report_data": {
            "patient_id": "test_patient",
            "type": "health_summary",
            "date_range": {
                "start": "2024-01-01",
                "end": "2024-01-31"
            }
        }
    } 