from math import ceil

from PySide6.QtCore import QDateTime, QLocale, Slot
from qextrawidgets.gui.proxys import QFormatProxyModel

from source.controllers.base import BaseController
from source.core.database import DatabaseController
from source.views.logs import LogsView


class LogsController(BaseController[LogsView]):
    def __init__(self, database: DatabaseController):
        super().__init__(LogsView())
        self.database = database
        self.format_proxy = self.create_format_proxy()
        self.logs_model = None
        self.items_per_page = 100

    @staticmethod
    def create_format_proxy() -> QFormatProxyModel:
        def _datetime_formatter(value):
            locale = QLocale()

            dt = QDateTime.fromSecsSinceEpoch(int(value))

            return dt.toString(
                locale.dateFormat(QLocale.FormatType.ShortFormat)
                + " "
                + locale.timeFormat(QLocale.FormatType.ShortFormat)
            )

        format_proxy = QFormatProxyModel()
        format_proxy.setColumnFormatter(1, _datetime_formatter)
        return format_proxy

    def load_logs_model(self):
        self.logs_model = self.database.get_logs_model()
        self.format_proxy.setSourceModel(self.logs_model)
        self.view.logs_table.setModel(self.format_proxy)

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
        self.view.rows_count.setText(
            self.tr("{} logs").format(self.logs_model.rowCount())
        )

    def translate_ui(self):
        self.logs_model.translate()
        self.view.translate_ui()
        self.translate_log_count()
