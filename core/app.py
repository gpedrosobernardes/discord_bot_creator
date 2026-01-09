import locale
import logging
import sys

from PySide6.QtCore import QSettings, QTranslator
from PySide6.QtWidgets import QApplication

from controllers.config import ConfigController
from controllers.credits import CreditsController
from controllers.group import GroupController
from controllers.logs import LogsController
from controllers.main import MainController
from core.constants import Language
from core.database import DatabaseController
from core.log_handler import LogHandler

logger = logging.getLogger(__name__)
logger.addHandler(LogHandler())


class Application:
    def __init__(self):
        self.application = QApplication(sys.argv)

        self.user_settings = self.create_user_settings()

        self.translator = QTranslator()
        lang = self.user_settings.value("language")
        self.translator.load(f"translations/build/{lang}.qm")
        self.application.installTranslator(self.translator)
        locale.setlocale(locale.LC_ALL, lang)

        logging.basicConfig(
            level=self.user_settings.value("log_level"),
            format="%(asctime)s - %(message)s",
            datefmt="%x %X",
        )

        self.database = DatabaseController(self.user_settings.value("database"))

        self.config_controller = ConfigController(self.translator, self.user_settings)
        self.logs_controller = LogsController()
        self.credits_controller = CreditsController()
        self.main_controller = MainController(
            self.database,
            self.user_settings,
            self.config_controller.view,
            self.logs_controller.view,
            self.credits_controller.view,
        )

        self.group_controller = GroupController()

        self.setup_connections()
        sys.exit(self.application.exec())

    def setup_connections(self):
        for view in (
            self.config_controller.view,
            self.main_controller.view,
            self.logs_controller.view,
        ):
            self.config_controller.language_changed.connect(view.translate_ui)

    @staticmethod
    def create_user_settings() -> QSettings:
        settings = QSettings("discord_bot_creator", "main")
        default_values = {
            "auto_start_bot": False,
            "language": Language.ENGLISH,
            "log_level": logging.INFO,
            "database": ":memory:",
            "style": "windows11",
        }
        for key, value in default_values.items():
            if not settings.contains(key):
                settings.setValue(key, value)
        return settings
