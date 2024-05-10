from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from TimetableToIcalProgram.get_course_details_widget import GetCourseDetailsWidget
from TimetableToJson import TimetableToJson


class SetTimeTableDetailsWidget(QWidget):
    timetable_configured = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.lectures = 0
        self.course_widgets: list[GetCourseDetailsWidget] = []

        self.create_widgets()

    def create_widgets(self):
        layout = QVBoxLayout(self)

        self.lecture_stacked_widget = QStackedWidget()

        loading_widget = QWidget()
        loading_layout = QVBoxLayout(loading_widget)
        loading_label = QLabel("Loading your timetable...")
        loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        loading_layout.addWidget(loading_label)

        self.lecture_stacked_widget.addWidget(loading_widget)

        layout.addWidget(self.lecture_stacked_widget)

        self.next_button = QPushButton("Loading...")
        self.next_button.setDisabled(True)
        self.next_button.clicked.connect(self.button_clicked)

        layout.addWidget(self.next_button)

    def update_widget(self, timetable: dict):
        self.course_widgets = []
        for course in timetable:
            course_widget = GetCourseDetailsWidget(course)
            self.course_widgets.append(course_widget)

            # Scroll area so the checkboxes don't take up the whole screen
            scroll_area = QScrollArea()
            scroll_area.setWidget(course_widget)
            scroll_area.setWidgetResizable(True)
            scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

            self.lecture_stacked_widget.addWidget(scroll_area)

    def parse_timetable(self, file_path: str):
        """
        Parse the timetable html file and display the lectures in the stack

        :param file_path:
        :return:
        """
        parser = TimetableToJson()

        timetable = parser.timetable_html_to_json(file_path)
        self.enable_button()

        self.update_widget(timetable)

    def go_to_next_lecture(self):
        """
        Go to the next lecture in the stack

        :return:
        """

        self.lectures += 1
        self.lecture_stacked_widget.setCurrentIndex(self.lectures)

    def button_clicked(self):
        """
        Called when the next button is clicked, will either go to the next lecture or emit the signal that the user has
        finished setting the timetable details
        :return:
        """

        if self.lectures < self.lecture_stacked_widget.count() - 1:
            self.go_to_next_lecture()
        else:
            self.timetable_configured.emit(self.get_timetable_details())

    def get_timetable_details(self) -> list:
        """
        Get the timetable details from the widgets

        :return: list of lectures
        """
        lectures = []
        for course_widget in self.course_widgets:
            course_lectures = course_widget.get_lectures()
            lectures.extend(course_lectures)

        return lectures

    def clear_stack(self):
        """
        Deletes all the widgets in the stack except the loading widget

        :return: None
        """

        self.lectures = 0
        self.lecture_stacked_widget.setCurrentIndex(0)

        for i in range(1, self.lecture_stacked_widget.count()):
            self.lecture_stacked_widget.removeWidget(self.lecture_stacked_widget.widget(i))

    def enable_button(self):
        self.next_button.setDisabled(False)
        self.next_button.setText("Next")

    def disable_button(self):
        self.next_button.setDisabled(True)
        self.next_button.setText("Loading...")
