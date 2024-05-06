"""
Parses UOA's academic timetable to a JSON format to allow for easier manipulation of the data

UOA's current academic timetable in .ics format is 2 years behind the current year. This script parses the timetable
based on data from the website. Manual Manipulation of the data is required to get the correct timetable.
"""

from bs4 import BeautifulSoup
from datetime import date as Date


class TimetableToJson:
    months = {
        "january": 1,
        "february": 2,
        "march": 3,
        "april": 4,
        "may": 5,
        "june": 6,
        "july": 7,
        "august": 8,
        "september": 9,
        "october": 10,
        "november": 11,
        "december": 12
    }

    def __init__(self):
        pass

    def get_timetable(self, soup: BeautifulSoup) -> dict:
        """
        Extracts the timetable data from the html file

        :param soup: BeautifulSoup object of the html file
        :return: JSON object of the timetable
        """
        timetable = []

        # Gets all the rows in the table
        rows = soup.find_all("tr")

        started = False

        # Loops through each row
        for row in rows:
            # Cells in the row are in the format: [event name, date occurring]
            cells = row.find_all("td")
            if len(cells) != 2:
                continue

            [nameCell, dateCell] = cells

            # Only parses rows that are after the start date of the semester
            event_name = self.format_cell(nameCell)

            # If the semester hasn't started yet and the event is not the start date, skip the row
            if not (started or self.is_start_date(event_name)):
                continue

            # If the event date is TBC or TBA, skip the row
            event_date = dateCell.get_text().strip()
            if event_date.lower() in ["tbc", "tba"]:
                continue

            # If the event is the end of the semester, stop parsing the rows
            if self.is_semester_over(event_name):
                break

            # Begins parsing the rows
            started = True

            event = self.parse_row(event_name, event_date)
            timetable.append(event)

        return timetable

    def is_semester_over(self, event_name: str) -> bool:
        return event_name.lower().startswith("semester") and event_name.endswith("ends")

    def parse_row(self, event_name: str, event_date: str) -> dict:
        """
        Parses the row of the timetable

        :param event_name: The name of the event
        :param event_date: The date of the event
        :return: JSON object of the row
        """
        event_type = "single_day"

        ending_date = None

        # Checks if the event date spans multiple days
        #  – is a special character that is not a normal hyphen
        if " – " in event_date:
            event_type = "multi_day"

            # Gets the starting and ending date of the event
            [start_date, end_date] = event_date.split(" – ")

            ending_date = self.parse_general_date(end_date)

            # If the starting date doesn't have a month, it is assumed to be the same month as the ending date
            if len(start_date.split(" ")) == 2:
                start_date = f"{start_date} {end_date.split(" ")[2]}"


            # Start date does not have a year, so it is assumed to be the same year as the ending date
            starting_date = self.parse_general_date(f"{start_date} {str(ending_date.year)}")
        else:
            starting_date = self.parse_general_date(event_date)


        event = {
            "event_name": event_name,
            "event_date": {
                "starting_date": starting_date,
                "ending_date": ending_date
            },
            "event_type": event_type
        }

        return event

    def parse_general_date(self, str_date: str) -> Date:
        """
        Parses the date of the event to a Date object

        :param str_date: full_day DD full_month YYYY
        :return: Date object of the starting date
        """

        # Splits the date into its components
        # print(str_date)
        # [_, day_number, month, year] = str_date.split(" ")
        [_, day_number, month, year] = str_date.split(" ")

        # Converts the month to a number
        month = self.months[month.lower()]

        return Date(int(year), month, int(day_number))

    def is_start_date(self, event_name: str) -> bool:
        return event_name.lower().startswith("semester") and event_name.endswith("begins")

    def timetable_html_to_json(self, filename: str) -> dict:
        """
        Converts the html timetable to a json format

        :param filename: The filename of the html timetable
        :return: JSON object of the timetable
        """

        soup = self.parse_html(filename)
        timetable = self.get_timetable(soup)
        return timetable

    def parse_html(self, filename: str) -> BeautifulSoup:
        """
        Parses the html file and returns a BeautifulSoup object

        :param filename: The filename of the html file
        :return: A BeautifulSoup object
        """
        with open(filename, "r", encoding="utf-8") as f:
            html = f.read()
        soup = BeautifulSoup(html, "html.parser")
        return soup

    def format_cell(self, cell: BeautifulSoup) -> str:
        """
        Extracts the event name from the name cell

        :param cell: The name cell
        :return: The event name
        """
        # Removes any whitespace from the name
        return " ".join(cell.get_text().strip().split())

    def pretty_print(self, timetable: dict):
        """
        Pretty prints the timetable

        :param timetable: The timetable to print
        """
        for event in timetable:
            print(event)