from typing import Any

from PySide6.QtCore import QLocale, QDateTime, QObject
from PySide6.QtWidgets import QStyledItemDelegate

from source.core.database import DatabaseController
from source.views.logs import LogsView


class TimestampDelegate(QStyledItemDelegate):
    def displayText(self, value: Any, locale: QLocale) -> str:
        """
        Converte o timestamp unix (float ou str) para data legível.
        """
        try:
            # 1. Tratamento de entrada (pode vir como float, int ou string com vírgula)
            if isinstance(value, str):
                # Troca vírgula por ponto se for string locale pt-BR
                value = float(value.replace(",", "."))

            if not isinstance(value, (int, float)):
                return super().displayText(value, locale)

            # 2. Converte para QDateTime
            # fromSecsSinceEpoch aceita int, então convertemos o float
            dt = QDateTime.fromSecsSinceEpoch(int(value))

            # 3. Retorna formatado (Ex: 22/01/2026 15:30)
            # Você pode usar "dd/MM/yyyy HH:mm:ss" ou usar o formato padrão do sistema:
            return dt.toString(
                locale.dateFormat(QLocale.FormatType.ShortFormat)
                + " "
                + locale.timeFormat(QLocale.FormatType.ShortFormat)
            )

        except ValueError:
            # Se falhar a conversão, retorna o valor original
            return super().displayText(value, locale)


class LogsController(QObject):
    def __init__(self, database: DatabaseController):
        super().__init__()
        self.view = LogsView()
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
