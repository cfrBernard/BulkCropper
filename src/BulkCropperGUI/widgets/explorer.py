from pathlib import Path

from PySide6.QtCore import Signal, QFileSystemWatcher, QTimer
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

        # -------------------
        # filesystem watcher
        # -------------------

        self.watcher = QFileSystemWatcher(self)

        self.watcher.directoryChanged.connect(
            self._on_directory_changed
        )

        self.watcher.addPath(str(self.output_root))

        # debounce
        self.refresh_timer = QTimer(self)
        self.refresh_timer.setSingleShot(True)
        self.refresh_timer.setInterval(200)
        self.refresh_timer.timeout.connect(
            self._perform_refresh
        )

        self._refresh_folders = False

        self.load_folders()

    # -------------------
    # watcher
    # -------------------

    def _on_directory_changed(self, path):

        path = Path(path)

        if path == self.output_root:
            self._refresh_folders = True

        self.refresh_timer.start()

    def _perform_refresh(self):

        if self._refresh_folders:

            current = self.current_folder

            self.load_folders()

            if current:
                index = self.folder_selector.findText(current)

                if index >= 0:
                    self.folder_selector.setCurrentIndex(index)

            self._refresh_folders = False

        elif self.current_folder:

            self.load_folder(self.current_folder)

    # -------------------
    # folders
    # -------------------

    def load_folders(self):

        folders = list_folders(self.output_root)

        current = self.folder_selector.currentText()

        self.folder_selector.blockSignals(True)
        self.folder_selector.clear()

        for folder in folders:
            self.folder_selector.addItem(folder.name)

        self.folder_selector.blockSignals(False)

        if current:
            index = self.folder_selector.findText(current)
            if index >= 0:
                self.folder_selector.setCurrentIndex(index)
                return

        if folders:
            self.folder_selector.setCurrentIndex(0)
            self.load_folder(folders[0].name)

    def on_folder_changed(self, folder_name):

        self.load_folder(folder_name)

    # -------------------
    # data
    # -------------------

    def load_folder(self, folder_name):

        self.current_folder = folder_name

        folder_path = self.output_root / folder_name

        # retire les anciens watchers (sauf la racine)
        for watched in self.watcher.directories():

            if watched != str(self.output_root):

                self.watcher.removePath(watched)

        # surveille le dossier courant
        if folder_path.exists():

            self.watcher.addPath(str(folder_path))

        images, json_data = load_folder(folder_path)

        self._images = images
        self._indexed = index_json(json_data)

        self.populate(
            self._images,
            self._indexed,
        )

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