"""
Parses UOA's academic timetable to a JSON format to allow for easier manipulation of the data

UOA's current academic timetable in .ics format is 2 years behind the current year. This script parses the timetable
based on data from the website. Manual Manipulation of the data is required to get the correct timetable.
"""

from bs4 import BeautifulSoup
from datetime import date as Date


class TimetableToJson:
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

            # Begins parsing the rows

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
