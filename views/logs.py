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

from core.translator import Translator


class LogsView:
    def __init__(self):
        self.window = QDialog()
        self.window.setWindowTitle(Translator.translate("LogsWindow", "Logs"))
        self.window.setMinimumSize(800, 600)
        self.window.resize(1000, 800)
        self.window.setWindowIcon(QIcon("source/icons/window-icon.svg"))
        self.message_filter = QLineEdit()
        self.message_filter.setPlaceholderText(
            Translator.translate("LogsWindow", "Message")
        )
        self.level_filter = QComboBox()
        self.date_filter = QDateEdit()
        self.date_filter.setDisplayFormat(Qt.DateFormat.TextDate.name) # Or a specific format string
        self.filter_button = QPushButton()
        self.filter_button.setText(Translator.translate("LogsWindow", "Filter"))
        self.reset_filter_button = QPushButton()
        self.reset_filter_button.setText(Translator.translate("LogsWindow", "Reset"))
        self.update_button = QPushButton()
        self.update_button.setText(Translator.translate("LogsWindow", "Update"))
        self.logs_table = QTableView()
        self.logs_table.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )
        self.pager = QPager()
        self.rows_count = QLabel()
        self._setup_layout()

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
