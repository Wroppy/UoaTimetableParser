from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from TimetableToIcalProgram.get_class_weeks_widget import GetClassWeeksWidget


class GetCourseDetailsWidget(QWidget):

    def __init__(self, course: dict):
        super().__init__()

        self.course = course

        self.create_widgets()

    def create_widgets(self):
        layout = QVBoxLayout(self)

        name = self.course["name"]
        code = self.course["code"]

        heading = QLabel("Configure your class times and locations")
        self.name_label = QLabel(f"Course: {code}, {name}")

        layout.addWidget(heading)
        layout.addWidget(self.name_label)

        self.classes_layout = QVBoxLayout()

        for class_ in self.course["classes"]:
            self.classes_layout.addWidget(self.get_class_widget(class_))

        layout.addLayout(self.classes_layout)

    def get_class_widget(self, class_: dict):
        class_widget = QWidget()
        layout = QVBoxLayout(class_widget)

        class_type = class_["type"]

        layout.addWidget(QLabel(f"Class Type: {class_type}, {self.get_class_frequency_text(class_)}"))

        # Gets the weeks the class is held
        weeks_widget = GetClassWeeksWidget(class_)
        layout.addWidget(weeks_widget)

        return class_widget

    def get_class_frequency_text(self, class_: dict):
        frequency = len(class_['times'])
        if frequency == 1:
            return "1 class in a week"

        return f"{frequency} classes in a week"

    def get_lecture_widget(self, class_: dict):
        pass
