from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from bs4 import BeautifulSoup


class GetUserTimetable(QWidget):
    """
    This widget handles

    """

    def __init__(self):
        super().__init__()

        self.create_widgets()

    def create_widgets(self):
        layout = QVBoxLayout(self)

        heading = QLabel("Import Timetable:")
        layout.addWidget(heading)

        self.file_path_widget = self.get_file_path_widget()
        layout.addWidget(self.file_path_widget)

        self.preview_html_text_edit = QTextEdit()
        self.preview_html_text_edit.setReadOnly(True)
        self.preview_html_text_edit.setPlaceholderText("Preview of timetable")
        self.preview_html_text_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(self.preview_html_text_edit)

    def get_file_path_widget(self) -> QWidget:
        """
        Returns a widget that allows the user to select a file path to their timetable.

        :return: QWidget
        """

        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        browse_button = QPushButton("Select Timetable File")

        browse_button.clicked.connect(self.browse_file)
        layout.addWidget(browse_button)

        return widget

    def browse_file(self):
        """
        Opens a file dialog to allow the user to select a file.
        """

        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilter("HTML files (*.html)")
        file_dialog.fileSelected.connect(self.file_selected)
        file_dialog.exec()

    def file_selected(self, file_path: str):
        """
        Called when the user has selected a file.

        :param file_path: str
        """

        print(file_path)
        self.set_timetable_preview(file_path)

    def set_timetable_preview(self, file_path: str):
        """
        Sets the preview text edit to display the timetable HTML.

        :param file_path: str
        :return: None
        """

        timetable = self.get_timetable_html(file_path)

        # Formats the HTML
        soup = BeautifulSoup(timetable, 'html.parser')
        timetable = soup.prettify()

        self.preview_html_text_edit.setText(timetable)



    def get_timetable_html(self, filename: str) -> str:
        """
        Returns the HTML of the timetable file.

        :return: str
        """

        with open(filename, 'r', encoding="utf-8") as file:
            return file.read()
