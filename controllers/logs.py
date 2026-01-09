from PySide6.QtCore import QTranslator
from PySide6.QtGui import QStandardItemModel

from views.logs import LogsView


class LogsController:
    page_size = 100

    def __init__(self):
        self.logs_model = QStandardItemModel()
        self.view = LogsView(self.logs_model)
