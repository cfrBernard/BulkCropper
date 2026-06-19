from BulkCropper.crop.config import Config

import os

from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
)


class Sidebar(QWidget):

    def __init__(self):
        super().__init__()

        self.setFixedWidth(220)

        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        # --- INPUT LABEL ---
        input_label = QLabel(
            "INPUT : Place your bulk images in this input folder. "
            "See the docs for more information on image requirements."
        )
        input_label.setWordWrap(True)
        input_label.setSizePolicy(
            QSizePolicy.Preferred,
            QSizePolicy.Maximum,
        )

        layout.addWidget(input_label)

        self.btn_open_input = QPushButton("Input folder")
        self.btn_open_input.clicked.connect(self.open_input_folder)
        layout.addWidget(self.btn_open_input)

        layout.addSpacing(15)

        # --- OUTPUT LABEL ---
        output_label = QLabel(
            "OUTPUT : The cropped images will appear here. "
            "You can also inject cropped .png files if you want to "
            "find their references via the 'find' process."
        )
        output_label.setWordWrap(True)
        output_label.setSizePolicy(
            QSizePolicy.Preferred,
            QSizePolicy.Maximum,
        )

        layout.addWidget(output_label)

        self.btn_open_output = QPushButton("Output folder")
        self.btn_open_output.clicked.connect(self.open_output_folder)
        layout.addWidget(self.btn_open_output)

        layout.addSpacing(30)

        # --- ACTION BUTTONS ---
        self.btn_crop = QPushButton("Run Crop")
        self.btn_find = QPushButton("Run Find")

        layout.addWidget(self.btn_crop)
        layout.addWidget(self.btn_find)

        layout.addStretch()

    def open_input_folder(self):
        self.open_folder(Config.input_path)

    def open_output_folder(self):
        self.open_folder(Config.output_path)

    def open_folder(self, path):
        os.makedirs(path, exist_ok=True)

        QDesktopServices.openUrl(
            QUrl.fromLocalFile(os.path.abspath(path))
        )