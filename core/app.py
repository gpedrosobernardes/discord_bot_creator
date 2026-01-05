import locale
import logging
import sys

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QApplication

from controllers.credits import CreditsController
from controllers.group import GroupController
from controllers.logs import LogsController
from controllers.main import MainController
from controllers.message import MessageController
from core.log_handler import LogHandler
from core.translator import Translator

logger = logging.getLogger(__name__)
logger.addHandler(LogHandler())


class Application(QApplication):
    def __init__(self):
        super().__init__(sys.argv)
        self.settings = self.create_settings()

        logging.basicConfig(
            level=self.settings.value("log_level", logging.INFO),
            format="%(asctime)s - %(message)s",
            datefmt="%x %X",
        )
        lang = self.settings.value("language", "en_us")
        locale.setlocale(locale.LC_ALL, lang)
        self.installTranslator(Translator().get_instance())
        # LogHandler().set_signal(self.bot_thread.log)
        self.main_controller = MainController(self.settings)
        self.logs_controller = LogsController(self.settings)
        self.message_controller = MessageController()
        self.group_controller = GroupController()
        self.credits_controller = CreditsController()

    @staticmethod
    def create_settings() -> QSettings:
        settings = QSettings("discord_bot_creator", "main")
        if not settings.contains("auto_start_bot"):
            settings.setValue("auto_start_bot", False)
        if not settings.contains("language"):
            settings.setValue("language", "en_us")
        if not settings.contains("log_level"):
            settings.setValue("log_level", logging.INFO)
        return settings
