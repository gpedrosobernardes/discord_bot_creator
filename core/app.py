import locale
import logging
import sys

from PySide6.QtCore import QSettings, QTranslator
from PySide6.QtWidgets import QApplication
from qextrawidgets.utils import QEmojiFonts

from controllers.config import ConfigController
from controllers.credits import CreditsController
from controllers.group import GroupController
from controllers.logs import LogsController
from controllers.main import MainController
from core.constants import Language
from core.database import DatabaseController
from core.log_handler import LogHandler


class Application:
    def __init__(self):
        self.application = QApplication(sys.argv)

        self.user_settings = self.create_user_settings()

        self.translator = QTranslator()
        lang = self.user_settings.value("language")
        self.translator.load(f"translations/build/{lang}.qm")
        self.application.installTranslator(self.translator)
        locale.setlocale(locale.LC_ALL, lang)

        self.database = DatabaseController(self.user_settings.value("database"), "main")

        self.log_handler = LogHandler(self.database)
        logging.getLogger("core").addHandler(self.log_handler)

        self.config_controller = ConfigController(self.translator, self.user_settings)
        self.logs_controller = LogsController(self.database)
        self.credits_controller = CreditsController()
        self.main_controller = MainController(
            self.database,
            self.user_settings,
            self.config_controller.view,
            self.logs_controller.view,
            self.credits_controller.view,
            self.log_handler,
        )

        self.group_controller = GroupController()

        self.setup_connections()
        self.main_controller.load_initial_state()
        sys.exit(self.application.exec())

    def setup_connections(self):
        for controller in (
            self.config_controller,
            self.main_controller,
            self.logs_controller,
        ):
            self.config_controller.language_changed.connect(controller.translate_ui)

        self.main_controller.switch_project.connect(
            self.logs_controller.load_logs_model
        )

    @staticmethod
    def create_user_settings() -> QSettings:
        settings = QSettings("discord_bot_creator", "main")
        default_values = {
            "auto_start_bot": False,
            "confirm_actions": True,
            "language": Language.ENGLISH,
            "log_level": logging.INFO,
            "database": ":memory:",
            "style": "windows11",
            "emoji_font": QEmojiFonts.loadTwemojiFont(),
        }
        for key, value in default_values.items():
            if not settings.contains(key):
                settings.setValue(key, value)
        return settings
