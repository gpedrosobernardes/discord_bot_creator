from PySide6.QtCore import Slot
from source.controllers.base import BaseController
from source.core.database import DatabaseController
from source.qt.delegates.timestamp import TimestampDelegate
from source.views.logs import LogsView
from math import ceil


class LogsController(BaseController[LogsView]):
    def __init__(self, database: DatabaseController):
        super().__init__(LogsView())
        self.database = database
        self.logs_model = None
        self.items_per_page = 100
        self._init_delegates()

    def _init_delegates(self):
        self.logs_model = self.database.get_logs_model()
        self.view.logs_table.setItemDelegateForColumn(
            self.logs_model.fieldIndex("datetime"), TimestampDelegate()
        )

    def load_logs_model(self):
        self.logs_model = self.database.get_logs_model()
        self.view.logs_table.setModel(self.logs_model)
        
        # Configurar paginação
        total_logs = self.database.get_logs_count()
        total_pages = ceil(total_logs / self.items_per_page)
        self.view.pager.setTotalPages(total_pages)
        
        # Conectar sinais
        self.view.pager.currentPageChanged.connect(self.on_page_changed)
        
        # Carregar primeira página
        self.on_page_changed(self.view.pager.currentPage())

    @Slot(int)
    def on_page_changed(self, page: int):
        offset = (page - 1) * self.items_per_page
        
        self.logs_model.select_page(self.items_per_page, offset)

        self.translate_log_count()

    def translate_log_count(self):
        self.view.rows_count.setText(self.tr("{} logs").format(self.logs_model.rowCount()))

    def translate_ui(self):
        self.logs_model.translate()
        self.view.translate_ui()
        self.translate_log_count()
