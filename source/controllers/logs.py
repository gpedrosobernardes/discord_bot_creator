from source.controllers.base import BaseController
from source.core.database import DatabaseController
from source.qt.delegates.timestamp import TimestampDelegate
from source.views.logs import LogsView


class LogsController(BaseController[LogsView]):
    def __init__(self, database: DatabaseController):
        super().__init__(LogsView())
        self.database = database
        self.logs_model = None
        self._init_delegates()

    def _init_delegates(self):
        self.logs_model = self.database.get_logs_model()
        self.view.logs_table.setItemDelegateForColumn(
            self.logs_model.fieldIndex("datetime"), TimestampDelegate()
        )

    def load_logs_model(self):
        self.logs_model = self.database.get_logs_model()
        self.logs_model.select()
        self.view.logs_table.setModel(self.logs_model)

    def translate_ui(self):
        self.logs_model.translate()
