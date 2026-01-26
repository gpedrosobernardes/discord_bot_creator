from typing import Any

from PySide6.QtCore import QLocale, QDateTime
from PySide6.QtWidgets import QStyledItemDelegate


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
