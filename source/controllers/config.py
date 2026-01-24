from __future__ import annotations

import locale
import logging

from PySide6.QtCore import QTranslator, QSettings, Signal, QObject
from PySide6.QtGui import QGuiApplication, Qt, QFontDatabase
from PySide6.QtWidgets import QApplication

from source.views.config import ConfigView


class ConfigController(QObject):
    language_changed = Signal()

    def __init__(self, translator: QTranslator, user_settings: QSettings):
        super().__init__()
        self.view = ConfigView()
        self.load_settings(user_settings)
        self.apply_theme(user_settings)
        self.apply_style(user_settings)
        self.apply_emoji_font(user_settings)
        self.apply_logging_config(user_settings)
        self.setup_connections(user_settings, translator)

    def translate_ui(self):
        self.view.translate_ui()

    def load_settings(self, user_settings: QSettings):
        # Language
        current_lang = user_settings.value("language")
        index = self.view.language_combo.findData(current_lang)
        if index >= 0:
            self.view.language_combo.setCurrentIndex(index)

        # Auto start
        auto_start = user_settings.value("auto_start_bot", type=bool)
        self.view.auto_start_checkbox.setChecked(auto_start)

        # Confirm actions
        confirm_actions = user_settings.value("confirm_actions", type=bool)
        self.view.confirm_actions_checkbox.setChecked(confirm_actions)

        # Log Level
        current_log_level = user_settings.value("log_level", type=int)
        index = self.view.log_level_combo.findData(current_log_level)
        if index >= 0:
            self.view.log_level_combo.setCurrentIndex(index)

        # Theme
        current_theme = user_settings.value("theme")
        index = self.view.theme_combo.findData(current_theme)
        if index >= 0:
            self.view.theme_combo.setCurrentIndex(index)

        # Style
        current_style = user_settings.value("style")
        index = self.view.style_combo.findData(current_style)
        if index >= 0:
            self.view.style_combo.setCurrentIndex(index)

        # Emoji Font
        current_emoji_font = user_settings.value("emoji_font")
        index = self.view.emoji_font_combo.findData(current_emoji_font)
        if index >= 0:
            self.view.emoji_font_combo.setCurrentIndex(index)

    @staticmethod
    def apply_theme(user_settings: QSettings):
        selected_theme = user_settings.value("theme")
        style_hints = QGuiApplication.styleHints()
        if selected_theme == "Dark":
            style_hints.setColorScheme(Qt.ColorScheme.Dark)
        elif selected_theme == "Light":
            style_hints.setColorScheme(Qt.ColorScheme.Light)
        else:
            style_hints.setColorScheme(Qt.ColorScheme.Unknown)

    @staticmethod
    def apply_style(user_settings: QSettings):
        selected_style = user_settings.value("style")
        QApplication.setStyle(selected_style)

    @staticmethod
    def apply_emoji_font(user_settings: QSettings):
        selected_font = user_settings.value("emoji_font")
        QFontDatabase.addApplicationEmojiFontFamily(selected_font)

    @staticmethod
    def apply_logging_config(user_settings: QSettings):
        selected_log_level = user_settings.value("log_level", type=int)
        logger = logging.getLogger("source.core")
        logger.setLevel(selected_log_level)

    def setup_connections(self, user_settings: QSettings, translator: QTranslator):
        self.view.save_button.clicked.connect(
            lambda: self.save_settings(user_settings, translator)
        )
        self.view.cancel_button.clicked.connect(self.view.close)

    def save_settings(self, user_settings: QSettings, translator: QTranslator):
        # Language
        selected_lang = self.view.language_combo.currentData()
        user_settings.setValue("language", selected_lang)
        locale.setlocale(locale.LC_ALL, selected_lang)
        translator.load(f"translations/build/{selected_lang}.qm")
        self.language_changed.emit()

        # Auto start
        user_settings.setValue(
            "auto_start_bot", self.view.auto_start_checkbox.isChecked()
        )

        # Confirm actions
        user_settings.setValue(
            "confirm_actions", self.view.confirm_actions_checkbox.isChecked()
        )

        # Log Level
        selected_log_level = self.view.log_level_combo.currentData()
        user_settings.setValue("log_level", selected_log_level)
        self.apply_logging_config(user_settings)

        # Theme
        selected_theme = self.view.theme_combo.currentData()
        user_settings.setValue("theme", selected_theme)
        self.apply_theme(user_settings)

        # Style
        selected_style = self.view.style_combo.currentData()
        user_settings.setValue("style", selected_style)
        self.apply_style(user_settings)

        # Emoji Font
        selected_emoji_font = self.view.emoji_font_combo.currentData()
        user_settings.setValue("emoji_font", selected_emoji_font)
        self.apply_emoji_font(user_settings)

        self.view.accept()
