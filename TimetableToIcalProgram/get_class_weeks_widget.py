from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class GetClassWeeksWidget(QWidget):

    def __init__(self, class_: dict):
        super().__init__()
        self.checkboxes = []

        self.class_ = class_

        self.create_widgets()

    def create_widgets(self):
        layout = QVBoxLayout(self)

        self.weeks_layout = QVBoxLayout()

        # Select all checkbox
        select_all_checkbox = QCheckBox("Select all")
        select_all_checkbox.setChecked(True)
        self.weeks_layout.addWidget(select_all_checkbox)

        select_all_checkbox.clicked.connect(lambda state: self.select_all_weeks(state))

        # Adds a checkbox for each week

        for week in range(1, 13):
            self.weeks_layout.addWidget(self.get_week_widget(week))

        layout.addLayout(self.weeks_layout)

    def select_all_weeks(self, state):
        for checkbox in self.checkboxes:
            checkbox.setChecked(state)

    def update_select_all_checkbox(self):
        all_checked = all(checkbox.isChecked() for checkbox in self.checkboxes)
        select_all_checkbox = self.weeks_layout.itemAt(0).widget()
        select_all_checkbox.setChecked(all_checked)

    def get_week_widget(self, week: int):
        week_widget = QWidget()
        layout = QHBoxLayout(week_widget)

        checkbox = QCheckBox(f"Week {week}")
        checkbox.stateChanged.connect(self.update_select_all_checkbox)
        checkbox.setChecked(True)

        layout.addWidget(checkbox)

        self.checkboxes.append(checkbox)

        return week_widget
