import locale
import sys

from PySide6.QtCore import QTranslator
from PySide6.QtWidgets import QApplication

from source.core.settings import Settings


class BaseApplication(QApplication):
    def __init__(self):
        super().__init__(sys.argv)

        self.user_settings = Settings()

        self.translator = QTranslator()
        lang = self.user_settings.value("language")
        self.translator.load(f"translations/build/{lang}.qm")
        self.installTranslator(self.translator)

        locale.setlocale(locale.LC_ALL, lang)
