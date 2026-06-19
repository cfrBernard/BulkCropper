from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
)


class ClickableLabel(QLabel):

    def __init__(self):
        super().__init__()

        self._url = None

        self.setCursor(Qt.PointingHandCursor)

        self.setStyleSheet("""
        QLabel{
            color:#4da3ff;
            text-decoration: underline;
        }
        """)

    def set_url(self, text, url):

        self._url = url
        self.setText(text)

    def mousePressEvent(self, event):

        if self._url:
            QDesktopServices.openUrl(QUrl(self._url))

        super().mousePressEvent(event)


class DetailsPanel(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        self.image_name = QLabel("No selection")
        self.folder = QLabel("")
        self.status = QLabel("")
        self.part_id = QLabel("")
        self.part_name = QLabel("")
        self.bricklink = ClickableLabel()

        layout.addWidget(self.image_name)
        layout.addWidget(self.folder)
        layout.addWidget(self.status)
        layout.addWidget(self.part_id)
        layout.addWidget(self.part_name)
        layout.addWidget(self.bricklink)

        layout.addStretch()

    def set_data(self, data):

        self.image_name.setText(
            f"Image : {data.get('input_id', '')}"
        )

        self.folder.setText(
            f"Folder : {data.get('folder', '')}"
        )

        self.status.setText(
            f"Status : {data.get('status', '')}"
        )

        items = data.get("items", [])

        if not items:

            self.part_id.setText("")
            self.part_name.setText("")
            self.bricklink.setText("")

            return

        item = items[0]

        self.part_id.setText(
            f"Bricklink ID : {item.get('id', '')}"
        )

        self.part_name.setText(
            item.get("name", "")
        )

        self.bricklink.set_url(
            "🔗 Open Bricklink",
            item.get("bricklink", "")
        )