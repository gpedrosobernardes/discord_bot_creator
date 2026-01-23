from typing import Any

from PySide6.QtCore import QLocale, QDateTime, QObject, Qt
from PySide6.QtSql import QSqlTableModel
from PySide6.QtWidgets import QStyledItemDelegate

from core.database import DatabaseController
from views.logs import LogsView


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
        self._init_delegates()

    def _init_delegates(self):
        logs_model = self.database.get_logs_model()
        self.view.logs_table.setItemDelegateForColumn(
            logs_model.fieldIndex("datetime"), TimestampDelegate()
        )

    def load_logs_model(self):
        logs_model = self.database.get_logs_model()
        logs_model.select()

        self.view.logs_table.setModel(logs_model)
        self.translate_model(logs_model)

    def translate_model(self, logs_model: QSqlTableModel):
        logs_model.setHeaderData(
            logs_model.fieldIndex("id"), Qt.Orientation.Horizontal, self.tr("ID")
        )
        logs_model.setHeaderData(
            logs_model.fieldIndex("datetime"),
            Qt.Orientation.Horizontal,
            self.tr("Datetime"),
        )
        logs_model.setHeaderData(
            logs_model.fieldIndex("level_number"),
            Qt.Orientation.Horizontal,
            self.tr("Level Number"),
        )
        logs_model.setHeaderData(
            logs_model.fieldIndex("message"),
            Qt.Orientation.Horizontal,
            self.tr("Message"),
        )
