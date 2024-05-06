"""
Parses UOA's academic timetable to a JSON format to allow for easier manipulation of the data

UOA's current academic timetable in .ics format is 2 years behind the current year. This script parses the timetable
based on data from the website. Manual Manipulation of the data is required to get the correct timetable.
"""

from bs4 import BeautifulSoup


class TimetableToJson:
    def __init__(self):
        print("TimetableToJson object created")
