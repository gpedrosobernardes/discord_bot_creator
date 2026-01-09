from PySide6.QtCore import QObject
from PySide6.QtGui import QIcon, Qt
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QSizePolicy,
    QLineEdit,
    QComboBox,
    QDateEdit,
    QPushButton,
    QTableView,
    QLabel,
)
from qextrawidgets import QPager


class LogsView(QObject):
    def __init__(self, model):
        super().__init__()
        self.window = QDialog()
        self.window.setMinimumSize(800, 600)
        self.window.resize(1000, 800)
        self.window.setWindowIcon(QIcon("source/icons/window-icon.svg"))
        self.message_filter = QLineEdit()
        self.level_filter = QComboBox()
        self.date_filter = QDateEdit()
        self.date_filter.setDisplayFormat(Qt.DateFormat.TextDate.name)
        self.filter_button = QPushButton()
        self.reset_filter_button = QPushButton()
        self.update_button = QPushButton()
        self.logs_table = QTableView()
        self.logs_table.setModel(model)
        self.logs_table.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )
        self.pager = QPager()
        self.rows_count = QLabel()
        self._setup_layout()
        self.translate_ui()

    def translate_ui(self):
        self.window.setWindowTitle(self.tr("Logs"))
        self.message_filter.setPlaceholderText(self.tr("Message Filter"))
        self.filter_button.setText(self.tr("Filter"))
        self.reset_filter_button.setText(self.tr("Reset"))
        self.update_button.setText(self.tr("Update"))
        self.logs_table.model().setHorizontalHeaderLabels(
            [
                self.tr("Date"),
                self.tr("Message"),
                self.tr("Level"),
            ]
        )

    def _setup_layout(self):
        filters_layout = QHBoxLayout()
        filters_layout.addWidget(self.message_filter)
        filters_layout.addWidget(self.level_filter)
        filters_layout.addWidget(self.date_filter)
        filters_layout.addWidget(self.filter_button)
        filters_layout.addWidget(self.reset_filter_button)
        filters_layout.addWidget(self.update_button)

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.rows_count)
        bottom_layout.addStretch(1)
        bottom_layout.addWidget(self.pager)

        layout = QVBoxLayout()
        layout.addLayout(filters_layout)
        layout.addWidget(self.logs_table, 1)
        layout.addLayout(bottom_layout)
        self.window.setLayout(layout)
