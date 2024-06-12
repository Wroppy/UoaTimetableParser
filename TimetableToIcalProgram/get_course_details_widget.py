from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from TimetableToIcalProgram.get_lecture_weeks_widget import GetLectureWeeksWidget
from TimetableToIcalProgram.select_lecture_room_widget import SelectLectureRoomWidget

from TimetableToIcalProgram.Lecture import Lecture


class GetCourseDetailsWidget(QWidget):

    def __init__(self, course: dict):
        super().__init__()

        self.course = course

        self.create_widgets()

    def create_widgets(self):
        layout = QVBoxLayout(self)

        name = self.course["name"]
        code = self.course["code"]

        heading = QLabel("Configure your lecture times and locations")
        self.name_label = QLabel(f"Course: {code}, {name}")

        layout.addWidget(heading)
        layout.addWidget(self.name_label)

        self.lectures_layout = QVBoxLayout()

        for lecture in self.course["classes"]:
            self.lectures_layout.addWidget(self.get_lecture_widget(lecture))

        layout.addLayout(self.lectures_layout)

    def get_lecture_widget(self, lecture: dict):
        lecture_widget = QWidget()
        layout = QVBoxLayout(lecture_widget)

        lecture_type = lecture["type"]

        layout.addWidget(QLabel(f"Class Type: {lecture_type}, {self.get_lecture_frequency_text(lecture)}"))

        # Gets the times the class is held
        times = lecture["times"]

        for time in times:
            select_lecture_room_widget = SelectLectureRoomWidget(lecture_type, time, lecture["locations"])
            layout.addWidget(select_lecture_room_widget)

        # Gets the weeks the class is held
        self.weeks_widget = GetLectureWeeksWidget(lecture)
        layout.addWidget(self.weeks_widget)

        return lecture_widget

    def get_lecture_frequency_text(self, class_: dict):
        frequency = len(class_['times'])
        if frequency == 1:
            return "1 lecture in a week"

        return f"{frequency} lectures in a week"

    def get_lectures(self) -> list[Lecture]:
        """
        Get the lectures from the widgets

        :return: list[Lecture]
        """
        lectures = []
        name = self.course["name"]
        code = self.course["code"]

        for lecture_widget in self.findChildren(QWidget):
            if isinstance(lecture_widget, SelectLectureRoomWidget):
                lecture_type, time, location = lecture_widget.get_lecture_times_and_location()

                for week in self.weeks_widget.get_weeks():
                    lecture = Lecture(name, code, lecture_type, location, self.find_location_name(location),
                                      time["day"],
                                      time["start"], time["end"], week)
                    lectures.append(lecture)

        return lectures

    def find_location_name(self, location_code: str) -> str:
        """
        Find the location name from the location code

        :param location_code:
        :return:
        """

        for lecture in self.course["classes"]:
            for location in lecture["locations"]:
                if location["code"] == location_code:
                    return location["name"]

        return "Unknown Location"
