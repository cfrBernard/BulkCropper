from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QComboBox,
    QScrollArea,
    QWidget,
)

from .image_card import ImageCard
from .flow_layout import FlowLayout
from ..services.output_scanner import (
    list_folders,
    load_folder,
    index_json,
)


class Explorer(QWidget):

    def __init__(self, output_root: Path):
        super().__init__()

        self.output_root = output_root

        self._images = []
        self._indexed = {}

        self.layout = QVBoxLayout(self)

        # -------------------
        # folder selector
        # -------------------
        self.folder_selector = QComboBox()
        self.folder_selector.currentTextChanged.connect(self.on_folder_changed)
        self.layout.addWidget(self.folder_selector)

        # -------------------
        # scroll area
        # -------------------
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.container = QWidget()
        self.flow = FlowLayout(self.container, margin=10, spacing=10)

        self.container.setLayout(self.flow)

        self.scroll.setWidget(self.container)
        self.layout.addWidget(self.scroll)

        self.load_folders()

    # -------------------
    # FOLDERS
    # -------------------
    def load_folders(self):
        folders = list_folders(self.output_root)

        self.folder_selector.clear()
        for f in folders:
            self.folder_selector.addItem(f.name)

        if folders:
            self.load_folder(folders[0].name)

    def on_folder_changed(self, folder_name):
        self.load_folder(folder_name)

    # -------------------
    # DATA
    # -------------------
    def load_folder(self, folder_name):
        folder_path = self.output_root / folder_name

        images, json_data = load_folder(folder_path)
        indexed = index_json(json_data)

        self._images = images
        self._indexed = indexed

        self.populate(images, indexed)

    def populate_current(self):
        self.populate(self._images, self._indexed)

    # -------------------
    # POPULATE FLOW
    # -------------------
    def populate(self, images, indexed):

        # clear layout
        while self.flow.count():
            item = self.flow.takeAt(0)
            if item and item.widget():
                item.widget().deleteLater()

        for img in images:

            entry = indexed.get(img.name)

            if entry:
                data = {
                    "image_path": str(img),
                    "input_id": img.name,
                    "status": entry.get("status", "UNKNOWN"),
                    "items": entry.get("items", []),
                }
            else:
                data = {
                    "image_path": str(img),
                    "input_id": img.name,
                    "status": "NOT_PROCESSED",
                    "items": [],
                }

            card = ImageCard(data)
            self.flow.addWidget(card)