from PySide6.QtCore import QObject
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QHeaderView,
)
from qextrawidgets import QPager, QFilterableTable


class LogsView(QDialog):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(800, 600)
        self.resize(1000, 800)
        self.setWindowIcon(QIcon("assets/icons/window-icon.svg"))

        self.logs_table = QFilterableTable()
        self.logs_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.logs_table.verticalHeader().hide()

        self.pager = QPager()
        self.rows_count = QLabel()
        self._setup_layout()
        self.translate_ui()

    def translate_ui(self):
        self.setWindowTitle(self.tr("Logs"))

    def _setup_layout(self):
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.rows_count)
        bottom_layout.addStretch(1)
        bottom_layout.addWidget(self.pager)

        layout = QVBoxLayout()
        layout.addWidget(self.logs_table, 1)
        layout.addLayout(bottom_layout)
        self.window.setLayout(layout)
