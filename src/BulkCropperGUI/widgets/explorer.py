from pathlib import Path

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QComboBox,
    QScrollArea,
    QWidget,
    QGridLayout,
)

from .image_card import ImageCard
from ..services.output_scanner import (
    list_folders,
    load_folder,
    index_json,
)


class Explorer(QWidget):

    def __init__(self, output_root: Path):
        super().__init__()

        self.output_root = output_root

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
        # scroll grid
        # -------------------
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.container = QWidget()
        self.grid = QGridLayout(self.container)

        self.scroll.setWidget(self.container)

        self.layout.addWidget(self.scroll)

        # init
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

    # -------------------
    # CHANGE FOLDER
    # -------------------
    def on_folder_changed(self, folder_name):

        self.load_folder(folder_name)

    # -------------------
    # LOAD CONTENT
    # -------------------
    def load_folder(self, folder_name):

        folder_path = self.output_root / folder_name

        images, json_data = load_folder(folder_path)

        indexed = index_json(json_data)

        self.populate(images, indexed)

    # -------------------
    # BUILD GRID
    # -------------------
    def populate(self, images, indexed):

        # clear grid
        while self.grid.count():
            item = self.grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        cols = 5

        for i, img in enumerate(images):

            entry = indexed.get(img.name)

            if entry:
                data = {
                    "image_path": str(img),
                    "input_id": img.name,
                    "status": entry["status"],
                    "items": entry["items"],
                }
            else:
                data = {
                    "image_path": str(img),
                    "input_id": img.name,
                    "status": "NOT_PROCESSED",
                    "items": [],
                }

            card = ImageCard(data)

            row = i // cols
            col = i % cols

            self.grid.addWidget(card, row, col)