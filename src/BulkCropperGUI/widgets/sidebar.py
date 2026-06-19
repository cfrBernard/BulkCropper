from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
)


class Sidebar(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Input"))

        self.btn_open_input = QPushButton("Open")

        layout.addWidget(self.btn_open_input)

        layout.addSpacing(15)

        layout.addWidget(QLabel("Output"))

        self.btn_open_output = QPushButton("Open")

        layout.addWidget(self.btn_open_output)

        layout.addSpacing(30)

        self.btn_crop = QPushButton("Run Crop")
        self.btn_find = QPushButton("Run Find")
        self.btn_full = QPushButton("Full Pipeline")

        layout.addWidget(self.btn_crop)
        layout.addWidget(self.btn_find)
        layout.addWidget(self.btn_full)

        layout.addStretch()