from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from TimetableToJson import TimetableToJson


class SetTimeTableDetailsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.classes = 0

        self.create_widgets()

    def create_widgets(self):
        layout = QVBoxLayout(self)

        self.classStack = QStackedWidget()

        loading_widget = QWidget()
        loading_layout = QVBoxLayout(loading_widget)
        loading_label = QLabel("Loading your timetable...")
        loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        loading_layout.addWidget(loading_label)

        self.classStack.addWidget(loading_widget)

        layout.addWidget(self.classStack)

        self.next_button = QPushButton("Loading...")
        self.next_button.setDisabled(True)
        self.next_button.clicked.connect(self.go_to_next_class)

        layout.addWidget(self.next_button)

    def update_widget(self):
        pass

    def parse_timetable(self, file_path: str):
        """
        Parse the timetable html file and display the classes in the stack

        :param file_path:
        :return:
        """
        parser = TimetableToJson()

        timetable = parser.timetable_html_to_json(file_path)
        self.enable_button()

        for course in timetable:
            name = course["name"]
            self.classStack.addWidget(QLabel(name))

    def go_to_next_class(self):
        """
        Go to the next class in the stack

        :return:
        """
        self.classes += 1
        self.classStack.setCurrentIndex(self.classes)

        if self.classes == self.classStack.count() - 1:
            self.disable_button()

    def clear_stack(self):
        """
        Deletes all the widgets in the stack except the loading widget

        :return: None
        """

        self.classes = 0
        self.classStack.setCurrentIndex(0)

        for i in range(1, self.classStack.count()):
            self.classStack.removeWidget(self.classStack.widget(i))

    def enable_button(self):
        self.next_button.setDisabled(False)
        self.next_button.setText("Next")

    def disable_button(self):
        self.next_button.setDisabled(True)
        self.next_button.setText("Loading...")
