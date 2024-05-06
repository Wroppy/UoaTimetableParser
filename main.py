from TimetableToJson import TimetableToJson
import json

if __name__ == '__main__':
    timetable_parser = TimetableToJson()
    # print(timetable_parser.timetable_html_to_json("data/timetable.html"))
    print(json.dumps(timetable_parser.timetable_html_to_json("data/timetable.html"), indent=4))

