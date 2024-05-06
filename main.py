from UOA_academic_timetable import TimetableToJson

if __name__ == '__main__':
    timetable_parser = TimetableToJson()
    timetable_parser.timetable_html_to_json("UOA_academic_timetable/2024_sem_1_dates.html")