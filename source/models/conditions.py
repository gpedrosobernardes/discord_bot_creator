from PySide6.QtCore import Qt
from PySide6.QtSql import QSqlTableModel, QSqlDatabase


class ConditionsTableModel(QSqlTableModel):
    def __init__(self, db: QSqlDatabase):
        super().__init__(db=db)
        self.setTable("message_conditions")
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnManualSubmit)
        self.translate()

    def translate(self):
        self.setHeaderData(
            self.fieldIndex("field"), Qt.Orientation.Horizontal, self.tr("Field")
        )
        self.setHeaderData(
            self.fieldIndex("comparator"),
            Qt.Orientation.Horizontal,
            self.tr("Comparator"),
        )
        self.setHeaderData(
            self.fieldIndex("value"), Qt.Orientation.Horizontal, self.tr("Value")
        )
        self.setHeaderData(
            self.fieldIndex("case_insensitive"),
            Qt.Orientation.Horizontal,
            self.tr("Case insensitive"),
        )
        self.setHeaderData(
            self.fieldIndex("reverse_comparator"),
            Qt.Orientation.Horizontal,
            self.tr("Reverse comparator"),
        )
