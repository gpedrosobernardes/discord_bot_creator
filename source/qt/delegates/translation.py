from PySide6.QtCore import Qt, QCoreApplication
from PySide6.QtWidgets import QStyledItemDelegate


class TranslationDelegate(QStyledItemDelegate):
    def __init__(self, parent=None, enums=None):
        super().__init__(parent)
        self.enums = enums or []

    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        value = index.data(Qt.ItemDataRole.DisplayRole)

        if not value:
            return

        for enum_cls in self.enums:
            for member in enum_cls:
                if member.value == value:
                    option.text = QCoreApplication.translate(enum_cls.__name__, value)
                    return
