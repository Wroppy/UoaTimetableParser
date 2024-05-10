from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from TimetableToIcalProgram.Lecture import Lecture


class SelectLectureRoomWidget(QWidget):
    def __init__(self, lecture_type: str, time: dict[str, str], lecture_rooms: list[dict]):
        super().__init__()
        self.time = time
        self.lecture_type = lecture_type
        self.create_widgets(time, lecture_rooms)

    def create_widgets(self, time: dict[str, str], lecture_rooms: list[dict]):
        layout = QVBoxLayout(self)

        self.time_label = QLabel(f"{time['day']}: {time['start']} - {time['end']}")
        layout.addWidget(self.time_label)

        formatted_lecture_rooms = [self.format_location(location) for location in lecture_rooms]

        self.lecture_room_combobox = QComboBox()
        self.lecture_room_combobox.addItems(formatted_lecture_rooms)
        self.lecture_room_combobox.setCurrentIndex(0)

        layout.addWidget(self.lecture_room_combobox)

    def get_selected_lecture_room(self):
        return self.lecture_room_combobox.currentText()

    def format_location(self, location: dict[str, str]):
        return f"{location['code']} - ({location['name']})"

    def unformat_location(self, location: str):
        return location.split(" - ")[0]

    def get_lecture_times_and_location(self):
        return self.lecture_type, self.time, self.unformat_location(self.get_selected_lecture_room())
