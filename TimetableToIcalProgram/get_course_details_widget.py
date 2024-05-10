from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from TimetableToIcalProgram.get_lecture_weeks_widget import GetLectureWeeksWidget


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

        # Gets the weeks the class is held
        weeks_widget = GetLectureWeeksWidget(lecture)
        layout.addWidget(weeks_widget)

        return lecture_widget

    def get_lecture_frequency_text(self, class_: dict):
        frequency = len(class_['times'])
        if frequency == 1:
            return "1 lecture in a week"

        return f"{frequency} lectures in a week"
