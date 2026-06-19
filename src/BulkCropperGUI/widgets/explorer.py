from pathlib import Path

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QComboBox,
    QScrollArea,
)

from .image_card import ImageCard
from .flow_layout import FlowLayout
from ..services.output_scanner import (
    list_folders,
    load_folder,
    index_json,
)


class Explorer(QWidget):

    image_selected = Signal(dict)

    def __init__(self, output_root: Path):
        super().__init__()

        self.output_root = output_root

        self._images = []
        self._indexed = {}
        self.current_folder = ""

        self.layout = QVBoxLayout(self)

        # -------------------
        # folder selector
        # -------------------

        self.folder_selector = QComboBox()
        self.folder_selector.currentTextChanged.connect(
            self.on_folder_changed
        )

        self.layout.addWidget(self.folder_selector)

        # -------------------
        # scroll area
        # -------------------

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.container = QWidget()

        self.flow = FlowLayout(
            self.container,
            margin=10,
            spacing=10,
        )

        self.container.setLayout(self.flow)

        self.scroll.setWidget(self.container)

        self.layout.addWidget(self.scroll)

        self.load_folders()

    # -------------------
    # folders
    # -------------------

    def load_folders(self):

        folders = list_folders(self.output_root)

        self.folder_selector.clear()

        for folder in folders:
            self.folder_selector.addItem(folder.name)

        if folders:
            self.load_folder(folders[0].name)

    def on_folder_changed(self, folder_name):

        self.load_folder(folder_name)

    # -------------------
    # data
    # -------------------

    def load_folder(self, folder_name):

        self.current_folder = folder_name

        folder_path = self.output_root / folder_name

        images, json_data = load_folder(folder_path)

        indexed = index_json(json_data)

        self._images = images
        self._indexed = indexed

        self.populate(images, indexed)

    def populate_current(self):

        self.populate(
            self._images,
            self._indexed,
        )

    # -------------------
    # populate
    # -------------------

    def populate(self, images, indexed):

        while self.flow.count():

            item = self.flow.takeAt(0)

            if item and item.widget():
                item.widget().deleteLater()

        for img in images:

            entry = indexed.get(img.name)

            if entry:

                data = {
                    "image_path": str(img),
                    "folder": self.current_folder,
                    "input_id": img.name,
                    "status": entry.get("status", "UNKNOWN"),
                    "items": entry.get("items", []),
                }

            else:

                data = {
                    "image_path": str(img),
                    "folder": self.current_folder,
                    "input_id": img.name,
                    "status": "NOT_PROCESSED",
                    "items": [],
                }

            card = ImageCard(data)

            card.clicked.connect(
                self.image_selected.emit
            )

            self.flow.addWidget(card)