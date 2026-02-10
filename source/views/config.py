import logging
from typing import Optional

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
    QWidget,
    QGroupBox,
)
from qextrawidgets.core.utils import QEmojiFonts


class ConfigView(QDialog):
    """
    Configuration dialog for the application.

    Allows the user to change language, theme, logging level, and other settings.
    """

    def __init__(self, parent: Optional[QWidget] = None):
        """
        Initialize the ConfigView.

        Args:
            parent: The parent widget.
        """
        super().__init__(parent)

        # Initialize UI components
        self._init_ui()
        self._init_layout()

        # Set initial texts
        self.translate_ui()

    def _init_ui(self) -> None:
        """Initialize all widgets and their properties."""
        self.setMinimumSize(450, 400)
        self.setWindowIcon(QIcon("assets/icons/window-icon.svg"))

        # --- General Settings ---
        self.language_label = QLabel()
        self.language_combo = QComboBox()
        for lang in ("en_us", "pt_br"):
            self.language_combo.addItem("", lang)

        self.auto_start_checkbox = QCheckBox()
        self.confirm_actions_checkbox = QCheckBox()

        # --- Appearance Settings ---
        self.theme_label = QLabel()
        self.theme_combo = QComboBox()
        self.theme_combo.addItem("", "Light")
        self.theme_combo.addItem("", "Dark")
        self.theme_combo.addItem("", "System")

        self.style_label = QLabel()
        self.style_combo = QComboBox()
        for style in QStyleFactory.keys():
            self.style_combo.addItem(style, style)

        self.emoji_font_label = QLabel()
        self.emoji_font_combo = QComboBox()
        # Load Twemoji font
        self.emoji_font_combo.addItem(QEmojiFonts.loadTwemojiFont(), "Twemoji")

        # --- Advanced Settings ---
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

        # --- Buttons ---
        self.save_button = QPushButton()
        self.cancel_button = QPushButton()

    def _init_layout(self) -> None:
        """Organize widgets into layouts."""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)

        # 1. General Group
        self.general_group = QGroupBox()
        general_layout = QFormLayout(self.general_group)
        general_layout.addRow(self.language_label, self.language_combo)
        general_layout.addRow(self.auto_start_checkbox)
        general_layout.addRow(self.confirm_actions_checkbox)
        main_layout.addWidget(self.general_group)

        # 2. Appearance Group
        self.appearance_group = QGroupBox()
        appearance_layout = QFormLayout(self.appearance_group)
        appearance_layout.addRow(self.theme_label, self.theme_combo)
        appearance_layout.addRow(self.style_label, self.style_combo)
        appearance_layout.addRow(self.emoji_font_label, self.emoji_font_combo)
        main_layout.addWidget(self.appearance_group)

        # 3. Advanced Group
        self.advanced_group = QGroupBox()
        advanced_layout = QFormLayout(self.advanced_group)
        advanced_layout.addRow(self.log_level_label, self.log_level_combo)
        main_layout.addWidget(self.advanced_group)

        # Spacer to push buttons to bottom
        main_layout.addStretch()

        # 4. Buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.cancel_button)
        main_layout.addLayout(buttons_layout)

    def translate_ui(self) -> None:
        """Translate UI elements to the current language."""
        self.setWindowTitle(self.tr("Configuration"))

        # Group Headers
        self.general_group.setTitle(self.tr("General"))
        self.appearance_group.setTitle(self.tr("Appearance"))
        self.advanced_group.setTitle(self.tr("Advanced"))

        # Labels
        self.language_label.setText(self.tr("Language"))
        self.theme_label.setText(self.tr("Theme"))
        self.style_label.setText(self.tr("Style"))
        self.emoji_font_label.setText(self.tr("Emoji Font"))
        self.log_level_label.setText(self.tr("Log level"))

        # Checkboxes
        self.auto_start_checkbox.setText(self.tr("Auto start bot"))
        self.confirm_actions_checkbox.setText(self.tr("Confirm actions"))

        # Combo Items
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

        # Buttons
        self.save_button.setText(self.tr("Save"))
        self.cancel_button.setText(self.tr("Cancel"))
