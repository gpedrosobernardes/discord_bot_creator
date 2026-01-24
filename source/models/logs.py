from PySide6.QtCore import Qt
from PySide6.QtSql import QSqlTableModel, QSqlDatabase


class LogsTableModel(QSqlTableModel):
    def __init__(self, db: QSqlDatabase):
        super().__init__(db=db)
        self.setTable("logs")
        self.translate()

    def translate(self):
        self.setHeaderData(
            self.fieldIndex("id"), Qt.Orientation.Horizontal, self.tr("ID")
        )
        self.setHeaderData(
            self.fieldIndex("datetime"),
            Qt.Orientation.Horizontal,
            self.tr("Datetime"),
        )
        self.setHeaderData(
            self.fieldIndex("level_number"),
            Qt.Orientation.Horizontal,
            self.tr("Level Number"),
        )
        self.setHeaderData(
            self.fieldIndex("message"),
            Qt.Orientation.Horizontal,
            self.tr("Message"),
        )
