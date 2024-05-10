from dataclasses import dataclass


@dataclass
class Lecture:
    course_name: str
    course_code: str

    lecture_type: str

    location_code: str
    location_name: str

    day: str
    start_time: str
    end_time: str
