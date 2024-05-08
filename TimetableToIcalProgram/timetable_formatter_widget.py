from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from TimetableToIcalProgram.get_user_timetable import GetUserTimetable


class TimetableFormatter(QWidget):
    def __init__(self):
        super().__init__(parent=None)
        self.set_widgets()

    def set_widgets(self):
        layout = QVBoxLayout(self)

        timetable_getter = GetUserTimetable()
        layout.addWidget(timetable_getter)
