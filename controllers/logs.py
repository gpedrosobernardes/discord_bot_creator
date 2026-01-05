from PySide6.QtCore import QLocale, QSettings
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QHeaderView

from core.database import Database
from core.translator import Translator, LOGGING_TRANSLATIONS
from models.log import Log
from views.logs import LogsView


class LogsController:
    page_size = 100

    def __init__(self, settings: QSettings):
        self.settings = settings
        self.view = LogsView()
        self.logs_model = QStandardItemModel()
        self.logs_model.setHorizontalHeaderLabels(
            [
                Translator.translate("LogsWindow", "Date"),
                Translator.translate("LogsWindow", "Message"),
                Translator.translate("LogsWindow", "Level"),
            ]
        )

        self.view.logs_table.setModel(self.logs_model)
