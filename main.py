from TimetableToIcalProgram import TimetableFormatterWindow
from PySide6.QtWidgets import QApplication


if __name__ == '__main__':
    app = QApplication([])
    timetable_parser = TimetableFormatterWindow()
    timetable_parser.show()
    app.exec()