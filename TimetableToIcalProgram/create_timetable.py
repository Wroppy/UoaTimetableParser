from datetime import date as Date, datetime as DateTime, timedelta
import icalendar

from TimetableToIcalProgram.Lecture import Lecture

START = Date(2024, 2, 26)
END = Date(2024, 5, 31)

# Sem break at Friday 29 March – Friday 12 April 2024
BREAK_START = Date(2024, 3, 29)
BREAK_END = Date(2024, 4, 12)

HOLIDAYS = [
    Date(2024, 3, 29),  # Good Friday
    Date(2024, 4, 25),  # ANZAC Day
]

DAY = {
    "Monday": 0,
    "Tuesday": 1,
    "Wednesday": 2,
    "Thursday": 3,
    "Friday": 4,
}


def create_timetable(lectures: list[Lecture]) -> icalendar.Calendar:
    lectures = format_lectures(lectures)

    cal = icalendar.Calendar()
    cal.add('prodid', '-//TimetableToIcal//')
    cal.add('version', '2.0')

    day = START
    week = 0
    # Loop through each week and add the lectures to the calendar
    while day <= END:

        day_int = day.weekday()

        # If the day is monday, increment the week number
        if day_int == 0 and not is_break(day):
            week += 1

        if is_holiday(day) or is_weekend(day) or is_break(day):
            day += timedelta(days=1)
            continue

        if week <= 0:
            day += timedelta(days=1)
            continue

        # Loop through each lecture for the day and add it to the calendar
        for lecture in lectures[week][day_int]:
            event = create_lecture_event(lecture, day)
            cal.add_component(event)

        day += timedelta(days=1)

    return cal


def create_lecture_event(lecture: Lecture, date: Date) -> icalendar.Event:
    """
    Create an icalendar event for a lecture

    :param lecture: the lecture
    :param date: the date of the lecture
    :return: an icalendar event
    """

    start_time = lecture.start_time.split(":")
    start_date_time = DateTime(date.year, date.month, date.day, int(start_time[0]), int(start_time[1]))

    end_time = lecture.end_time.split(":")
    end_date_time = DateTime(date.year, date.month, date.day, int(end_time[0]), int(end_time[1]))

    event = icalendar.Event()
    event.add('summary', f"{get_summary(lecture)}")
    event.add('dtstart', start_date_time)
    event.add('dtend', end_date_time)

    event.add('location', lecture.location_code)
    event.add('description', f"{lecture.course_name}")

    return event


def get_summary(lecture: Lecture) -> str:
    summary = f"{lecture.course_code}"

    if lecture.lecture_type != "Lecture":
        summary += f" - {lecture.lecture_type.lower()[:3]}"

    return summary


def format_lectures(lectures: list[Lecture]) -> dict[int, list[list[Lecture]]]:
    """
    Formats the lectures into a dictionary with the key being the week number and the value being a list of lectures
    for that week

    :param lectures: a list of lectures
    :return: a formatted dictionary
    """

    formatted = {
        1: [[], [], [], [], []],
        2: [[], [], [], [], []],
        3: [[], [], [], [], []],
        4: [[], [], [], [], []],
        5: [[], [], [], [], []],
        6: [[], [], [], [], []],
        7: [[], [], [], [], []],
        8: [[], [], [], [], []],
        9: [[], [], [], [], []],
        10: [[], [], [], [], []],
        11: [[], [], [], [], []],
        12: [[], [], [], [], []],
    }

    for lecture in lectures:
        formatted[lecture.week][DAY[lecture.day]].append(lecture)
    return formatted


def is_holiday(date: Date) -> bool:
    return date in HOLIDAYS


def is_break(date: Date) -> bool:
    return BREAK_START <= date <= BREAK_END


def is_weekend(date: Date) -> bool:
    return date.weekday() >= 5
