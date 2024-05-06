from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *


class TimetableFormatter(QWidget):
    def __init__(self):
        super().__init__()
        self.set_widgets()

    def set_widgets(self):
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Timetable Formatter"))


class TimetableFormatterWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Timetable Formatter")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = TimetableFormatter()
        self.setCentralWidget(self.central_widget)
