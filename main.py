from TimetableToIcalProgram.timetable_formatter_window import TimetableFormatterWindow
from PyQt6.QtWidgets import QApplication
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    timetable_parser = TimetableFormatterWindow()
    timetable_parser.show()
    app.exec()