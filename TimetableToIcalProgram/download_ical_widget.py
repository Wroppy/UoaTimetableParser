from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *


class DownloadIcalWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.create_widgets()

    def create_widgets(self):
        layout = QVBoxLayout(self)

        self.download_button = QPushButton("Download Ical File")
        self.download_button.clicked.connect(self.download_button_clicked)

        layout.addWidget(self.download_button)

    def download_button_clicked(self):
        file_dialog = QFileDialog()
        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        file_dialog.setNameFilter("Ical Files (*.ics)")
        file_dialog.setDefaultSuffix("ics")
        file_dialog.setFileMode(QFileDialog.FileMode.AnyFile)
        file_dialog.setDirectory(QDir.currentPath())

        if file_dialog.exec() == QDialog.DialogCode.Accepted:
            file_path = file_dialog.selectedFiles()[0]
            print(file_path)
