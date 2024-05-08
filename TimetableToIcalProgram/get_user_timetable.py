from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class GetUserTimetable(QWidget):
    def __init__(self):
        super().__init__()

        self.create_widgets()


    def create_widgets(self):
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Get user timetable here"))
