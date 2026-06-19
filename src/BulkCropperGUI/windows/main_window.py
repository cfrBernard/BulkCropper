from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QSplitter,
)

from ..widgets.sidebar import Sidebar
from ..widgets.explorer import Explorer
from ..widgets.details_panel import DetailsPanel


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("BulkCropper")
        self.resize(940, 690)

        # ⚠️ TEMP FIX (plus tard: config file)
        output_root = Path("data/output")

        central = QWidget()
        self.setCentralWidget(central)

        layout = QHBoxLayout(central)

        splitter = QSplitter(Qt.Horizontal)

        # sidebar
        self.sidebar = Sidebar()

        # right side
        right = QWidget()
        right_layout = QVBoxLayout(right)

        self.explorer = Explorer(output_root)
        self.details = DetailsPanel()

        self.explorer.image_selected.connect(
            self.details.set_data
        )

        right_layout.addWidget(self.explorer, 3)
        right_layout.addWidget(self.details, 1)

        splitter.addWidget(self.sidebar)
        splitter.addWidget(right)

        layout.addWidget(splitter)