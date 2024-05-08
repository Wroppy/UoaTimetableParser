from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from TimetableToIcalProgram.timetable_formatter_widget import TimetableFormatter


class TimetableFormatterWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Timetable Formatter")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = TimetableFormatter()
        self.setCentralWidget(self.central_widget)
