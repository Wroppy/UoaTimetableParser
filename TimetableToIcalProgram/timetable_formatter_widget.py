from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from bs4 import BeautifulSoup

from TimetableToIcalProgram.Lecture import Lecture
from TimetableToIcalProgram.download_ical_widget import DownloadIcalWidget
from TimetableToIcalProgram.get_user_timetable import GetUserTimetable
from TimetableToIcalProgram.set_timetable_details_widget import SetTimeTableDetailsWidget
from icalendar import Calendar, Event, vCalAddress, vText


class TimetableFormatter(QStackedWidget):
    def __init__(self):
        super().__init__(parent=None)
        self.set_widgets()

    def set_widgets(self):
        timetable_getter = GetUserTimetable()
        timetable_getter.parse_timetable.connect(self.parse_timetable)
        self.addWidget(timetable_getter)

        self.timetable_parser_widget = SetTimeTableDetailsWidget()
        self.timetable_parser_widget.timetable_configured.connect(self.timetable_configured)

        self.addWidget(self.timetable_parser_widget)

        download_ical_widget = DownloadIcalWidget()
        self.addWidget(download_ical_widget)

    def timetable_configured(self, lectures: list[Lecture]):
        self.setCurrentIndex(2)
        print(lectures)

    def parse_timetable(self, timetable: str):
        self.timetable_parser_widget.parse_timetable(timetable)
        self.setCurrentIndex(1)
