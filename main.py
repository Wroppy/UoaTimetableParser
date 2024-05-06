from UOA_academic_timetable import TimetableToJson
import json

if __name__ == '__main__':
    timetable_parser = TimetableToJson()
    timetable = timetable_parser.timetable_html_to_json("UOA_academic_timetable/2024_sem_1_dates.html")
    timetable_parser.pretty_print(timetable)