import logging

from PySide6.QtCore import QObject
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QComboBox,
    QCheckBox,
    QPushButton,
    QHBoxLayout,
    QFormLayout,
    QLabel,
    QStyleFactory,
)


class ConfigView(QObject):
    def __init__(self):
        super().__init__()
        self.window = QDialog()
        self.window.setMinimumSize(400, 250)
        self.window.setWindowIcon(QIcon("source/icons/window-icon.svg"))

        # Language
        self.language_label = QLabel()
        self.language_combo = QComboBox()
        for lang in ("en_us", "pt_br"):
            self.language_combo.addItem("", lang)

        # Auto start
        self.auto_start_checkbox = QCheckBox()

        # Log Level
        self.log_level_label = QLabel()
        self.log_level_combo = QComboBox()
        for level in (
            logging.CRITICAL,
            logging.ERROR,
            logging.WARNING,
            logging.INFO,
            logging.DEBUG,
        ):
            self.log_level_combo.addItem("", level)

        # Theme
        self.theme_label = QLabel()
        self.theme_combo = QComboBox()
        self.theme_combo.addItem("", "Light")
        self.theme_combo.addItem("", "Dark")
        self.theme_combo.addItem("", "System")

        # Style
        self.style_label = QLabel()
        self.style_combo = QComboBox()
        for style in QStyleFactory.keys():
            self.style_combo.addItem(style, style)

        # Buttons

        self.save_button = QPushButton()
        self.cancel_button = QPushButton()

        self.translate_ui()
        self.setup_layout()

    def translate_ui(self):
        self.window.setWindowTitle(self.tr("Configuration"))

        self.language_label.setText(self.tr("Language"))
        self.log_level_label.setText(self.tr("Log level"))
        self.theme_label.setText(self.tr("Theme"))
        self.style_label.setText(self.tr("Style"))
        self.auto_start_checkbox.setText(self.tr("Auto start bot"))

        self.language_combo.setItemText(0, self.tr("English"))
        self.language_combo.setItemText(1, self.tr("Portuguese"))

        self.theme_combo.setItemText(0, self.tr("Light"))
        self.theme_combo.setItemText(1, self.tr("Dark"))
        self.theme_combo.setItemText(2, self.tr("System"))

        self.log_level_combo.setItemText(0, self.tr("Critical"))
        self.log_level_combo.setItemText(1, self.tr("Error"))
        self.log_level_combo.setItemText(2, self.tr("Warning"))
        self.log_level_combo.setItemText(3, self.tr("Info"))
        self.log_level_combo.setItemText(4, self.tr("Debug"))

        self.save_button.setText(self.tr("Save"))
        self.cancel_button.setText(self.tr("Cancel"))

    def setup_layout(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        form_layout.addRow(self.language_label, self.language_combo)
        form_layout.addRow(self.log_level_label, self.log_level_combo)
        form_layout.addRow(self.theme_label, self.theme_combo)
        form_layout.addRow(self.style_label, self.style_combo)
        form_layout.addRow(self.auto_start_checkbox)

        layout.addLayout(form_layout)

        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.cancel_button)

        layout.addLayout(buttons_layout)

        self.window.setLayout(layout)
