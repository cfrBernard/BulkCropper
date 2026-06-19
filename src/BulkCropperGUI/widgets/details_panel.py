from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
)


class DetailsPanel(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        self.image_name = QLabel("No selection")
        self.status = QLabel("")
        self.part_id = QLabel("")
        self.part_name = QLabel("")

        layout.addWidget(self.image_name)
        layout.addWidget(self.status)
        layout.addWidget(self.part_id)
        layout.addWidget(self.part_name)

        layout.addStretch()