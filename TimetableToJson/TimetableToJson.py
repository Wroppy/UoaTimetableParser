from bs4 import BeautifulSoup


class TimetableToJson:
    parent_div_id = "win0divSSR_SBJCT_LVL1$0"
    days = {"Mo": "Monday", "Tu": "Tuesday", "We": "Wednesday", "Th": "Thursday", "Fr": "Friday", "Sa": "Saturday",
            "Su": "Sunday"}

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

        classes = self.get_course_classes(filtered_soup)

        courses_data = []

        for course_names, course_classes in zip(self.get_course_names(filtered_soup), classes):
            course_data = {"name": course_names["name"], "code": course_names["code"], "classes": course_classes}
            courses_data.append(course_data)

        return courses_data


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

    def get_course_names(self, soup: BeautifulSoup) -> list[dict]:
        """
        Get the course names from the timetable html

        :param soup: BeautifulSoup object
        :return: list of course names and codes in the form of [{name, code}]
        """

        selector = "h2.ps_header-group > a.ps-link"
        # Finds all the course names
        course_names = soup.select(selector)

        course_list = []
        for course in course_names:
            # text may contain newlines, and double spaces between words
            course_text = course.text.strip().replace("\n", "")
            course_text = " ".join(course_text.split())  # remove double spaces

            # get course code
            course_code = course_text.split(" ")[:2]
            course_code = " ".join(course_code)

            # Get course name
            course_name = course_text.split(" ")[2:]
            course_name = " ".join(course_name)

            course_list.append({"name": course_name, "code": course_code})

        return course_list

    def get_course_classes(self, soup: BeautifulSoup) -> list[dict]:
        """
        Get the classes from the timetable html with the course name, code and class type, days, times, and location

        :param soup: BeautifulSoup object
        :return: list of classes in the form of [{course, class}]
        """

        selector = "div.ps_box-grid-flex.psc_grid-nohbar.psc_grid-norowcount.psc_show-actionable.psc_grid-selectedhighlight.psa_border-bottom-none2.psc_grid-notitle table"
        # Finds all the classes
        courses = soup.select(selector)
        classes_list = []

        for courses in courses:
            course_data = []

            classes = courses.find_all("tr")

            # Classes elements are tables with class type, days, times, and location
            for class_ in classes:
                class_data = class_.find_all("td")

                # Checks for empty class data
                if not class_data:
                    continue

                class_data = [self.format_string(data.text) for data in class_data]

                class_type = class_data[1]

                times = self.format_time_string(class_data[3])

                locations = self.format_location_string(class_data[4])

                course_data.append({"type": class_type, "times": times, "locations": locations})

            classes_list.append(course_data)

        return classes_list

    def format_string(self, string: str) -> str:
        """
        Format the string by removing newlines and extra spaces

        :param string: string to format
        :return: formatted string
        """
        return " ".join(string.split())

    def format_time_string(self, string: str) -> list[str]:
        """
        Formats the time string to a list of start and end times

        :param string: time string of all class times in the form of "dd HH:MM - HH:MM"
        :return: list of start and end times
        """
        times = []

        # Remove the "More schedule details available" string
        string = string.replace("More schedule details available", "").replace("\n", "").strip()

        # Splits the time strings into its separate times every 16 characters
        n = 16
        unformatted_times = [(string[i:i + n]) for i in range(0, len(string), n)]

        for time in unformatted_times:
            day = self.days[time[:2]]
            time = time[3:]

            # Split the time string into start and end times
            time = time.split("-")
            start_time = time[0].strip()
            end_time = time[1].strip()

            times.append({"day": day, "start": start_time, "end": end_time})

        return times

    def format_location_string(self, string: str) -> list[str]:
        """
        Format the location string to remove extra spaces

        :param string: location string
        :return: formatted location strings in a list
        """

        locations = string.split(")")

        formatted_locations = []

        for location in locations:

            # Checks for empty location data
            if not location:
                continue

            location = location.strip()

            location = location.replace("(", "").strip()

            location_code = location.split(" ")[0]
            location_name = " ".join(location.split(" ")[1:])

            formatted_locations.append({"code": location_code, "name": location_name})

        return formatted_locations
