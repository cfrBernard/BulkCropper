from pathlib import Path

from PySide6.QtCore import Qt, Signal, QUrl
from PySide6.QtGui import QPixmap, QDesktopServices
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout


class ImageCard(QWidget):

    clicked = Signal(dict)

    WIDTH = 120
    HEIGHT = 140

    def __init__(self, data: dict):
        super().__init__()

        self.data = data or {}

        self.setFixedSize(self.WIDTH, self.HEIGHT)
        self.setCursor(Qt.PointingHandCursor)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(4)

        # -------------------
        # IMAGE
        # -------------------
        self.image = QLabel()
        self.image.setAlignment(Qt.AlignCenter)
        self.image.setFixedHeight(90)

        # -------------------
        # STATUS
        # -------------------
        self.status = QLabel()
        self.status.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.image)
        layout.addWidget(self.status)

        # init
        self._load_image()
        self._update_status()
        self._update_tooltip()

    # -------------------
    # IMAGE LOADING
    # -------------------
    def _load_image(self):
        path = Path(self.data.get("image_path", ""))

        if not path.exists():
            self.image.setText("No image")
            return

        pixmap = QPixmap(str(path))

        if pixmap.isNull():
            self.image.setText("Invalid")
            return

        pixmap = pixmap.scaled(
            160,
            140,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )

        self.image.setPixmap(pixmap)

    # -------------------
    # STATUS
    # -------------------
    def _update_status(self):
        status = self.data.get("status", "UNKNOWN")

        if status == "OK":
            items = self.data.get("items", [])
            if items:
                self.status.setText(f"🟢 {items[0].get('id', '')}")
            else:
                self.status.setText("🟢 OK")

        elif status == "NOT_FOUND":
            self.status.setText("🔴 Not found")

        elif status == "NOT_PROCESSED":
            self.status.setText("⚪ Not processed")

        else:
            self.status.setText("⚪ Unknown")

    # -------------------
    # TOOLTIP (SAFE)
    # -------------------
    def _update_tooltip(self):
        if self.data.get("status") != "OK":
            return

        items = self.data.get("items", [])
        if not items:
            return

        item = items[0]

        # SAFE ACCESS (dict only, normalisé par output_scanner)
        item_id = item.get("id", "")
        name = item.get("name", "")

        self.setToolTip(f"{item_id}\n\n{name}")

    # -------------------
    # CLICK
    # -------------------
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.data)

        super().mousePressEvent(event)

    # -------------------
    # DOUBLE CLICK
    # -------------------
    def mouseDoubleClickEvent(self, event):
        if event.button() != Qt.LeftButton:
            return

        items = self.data.get("items", [])
        if not items:
            return

        url = items[0].get("bricklink")
        if url:
            QDesktopServices.openUrl(QUrl(url))

        super().mouseDoubleClickEvent(event)