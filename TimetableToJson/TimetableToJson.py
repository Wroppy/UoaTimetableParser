from bs4 import BeautifulSoup


class TimetableToJson:
    parent_div_id = "win0divSSR_SBJCT_LVL1$0"

    def __init__(self):
        pass

    def timetable_html_to_json(self, filename: str):
        """
        Convert the timetable html to json format

        :param filename: path of the html file containing the timetable
        :return: json object
        """
        soup = self.parse_html(filename)
        filtered_soup = self.filter_timetable_html(soup)
        print(filtered_soup.prettify())

        self.write_html(filtered_soup, "data/timetable_filtered.html")

    def parse_html(self, filename: str) -> BeautifulSoup:
        """
        Parse the html file and return a BeautifulSoup object

        :param filename: path of the html file containing the timetable
        :return: BeautifulSoup object
        """
        with open(filename, 'r') as f:
            soup = BeautifulSoup(f, 'html.parser')

        return soup

    def filter_timetable_html(self, soup: BeautifulSoup) -> BeautifulSoup:
        """
        Filter the timetable html to remove unnecessary elements

        :param soup: BeautifulSoup object
        :return: BeautifulSoup object
        """

        # Finds the parent div element
        parent_div = soup.find('div', id=self.parent_div_id)

        return parent_div

    def write_html(self, soup: BeautifulSoup, filename: str):
        """
        Write the filtered timetable html to a new file

        :param soup: BeautifulSoup object
        :param filename: path of the new html file
        """
        with open(filename, 'w') as f:
            f.write(soup.prettify())
