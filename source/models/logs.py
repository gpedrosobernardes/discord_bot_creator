from PySide6.QtCore import Qt
from PySide6.QtSql import QSqlQueryModel, QSqlDatabase


class LogsTableModel(QSqlQueryModel):
    def __init__(self, db: QSqlDatabase):
        super().__init__()
        self._db = db
        # Inicializa com uma query vazia ou a primeira página
        self.select_page(0, 0)

    def select_page(self, limit: int, offset: int):
        # Se limit for 0, não traz nada (estado inicial)
        if limit == 0:
            self.setQuery("SELECT id, datetime, level_number, message FROM logs WHERE 1=0", self._db)
        else:
            query = f"SELECT id, datetime, level_number, message FROM logs LIMIT {limit} OFFSET {offset}"
            self.setQuery(query, self._db)
        
        self.translate()

    def fieldIndex(self, field_name: str) -> int:
        return self.record().indexOf(field_name)

    def translate(self):
        # Os índices dependem da ordem do SELECT
        self.setHeaderData(0, Qt.Orientation.Horizontal, self.tr("ID"))
        self.setHeaderData(1, Qt.Orientation.Horizontal, self.tr("Datetime"))
        self.setHeaderData(2, Qt.Orientation.Horizontal, self.tr("Level Number"))
        self.setHeaderData(3, Qt.Orientation.Horizontal, self.tr("Message"))
