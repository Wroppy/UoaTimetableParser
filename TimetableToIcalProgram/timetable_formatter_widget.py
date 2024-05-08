from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from bs4 import BeautifulSoup

from TimetableToIcalProgram.get_user_timetable import GetUserTimetable


class TimetableFormatter(QWidget):
    def __init__(self):
        super().__init__(parent=None)
        self.set_widgets()

    def set_widgets(self):
        layout = QVBoxLayout(self)

        timetable_getter = GetUserTimetable()
        timetable_getter.parse_timetable.connect(self.parse_timetable)
        layout.addWidget(timetable_getter)

    def parse_timetable(self, timetable: BeautifulSoup):
        print("Timetable parsed!")
        print(timetable)
