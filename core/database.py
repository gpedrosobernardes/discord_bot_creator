import logging
import os
import shutil

from PySide6.QtCore import QStandardPaths, Qt
from PySide6.QtSql import (
    QSqlDatabase,
    QSqlQuery,
    QSqlTableModel,
)


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


class DatabaseController:
    def __init__(self, name: str, connection_name: str):
        self.name = name

        if QSqlDatabase.contains(connection_name):
            self.database = QSqlDatabase.database(connection_name)
        else:
            self.database = QSqlDatabase.addDatabase("QSQLITE", connection_name)
            path = self.get_database_path(name)
            self.database.setDatabaseName(path)

        if self.database.open():
            self.create_tables()
        else:
            print(f"Failed to open database: {self.database.lastError().text()}")

    def create_tables(self):
        # Tabela groups
        self.exec(
            """
            CREATE TABLE IF NOT EXISTS groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                welcome_message TEXT,
                welcome_message_channel INTEGER,
                goodbye_message TEXT,
                goodbye_message_channel INTEGER
            )
            """
        )

        # Tabela messages
        self.exec(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                action INTEGER,
                punishment INTEGER,
                where_reply INTEGER,
                where_reaction INTEGER,
                delay INTEGER DEFAULT 0
            )
            """
        )

        # Tabela message_replies
        self.exec(
            """
            CREATE TABLE IF NOT EXISTS message_replies (
                id INTEGER PRIMARY KEY,
                message_id INTEGER NOT NULL,
                text TEXT NOT NULL,
                FOREIGN KEY (message_id) REFERENCES messages(id) ON DELETE CASCADE
            )
            """
        )

        # Tabela message_reactions
        self.exec(
            """
            CREATE TABLE IF NOT EXISTS message_reactions (
                id INTEGER PRIMARY KEY,
                message_id INTEGER NOT NULL,
                reaction TEXT NOT NULL,
                FOREIGN KEY (message_id) REFERENCES messages(id) ON DELETE CASCADE
            )
            """
        )

        # Tabela message_conditions
        self.exec(
            """
            CREATE TABLE IF NOT EXISTS message_conditions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message_id INTEGER NOT NULL,
                field TEXT NOT NULL,
                comparator TEXT NOT NULL,
                value TEXT NOT NULL,
                case_insensitive BOOLEAN DEFAULT 0,
                reverse_comparator BOOLEAN DEFAULT 0,
                FOREIGN KEY (message_id) REFERENCES messages(id) ON DELETE CASCADE
            )
            """
        )

        # Tabela logs
        self.exec(
            """
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                datetime DATETIME,
                message TEXT,
                level_number INTEGER
            )
            """
        )

    def switch_database(self, new_name: str):
        if self.database.isOpen():
            self.database.close()

        self.name = new_name
        path = self.get_database_path(new_name)
        self.database.setDatabaseName(path)

        if self.database.open():
            self.create_tables()
        else:
            print(f"Failed to switch database: {self.database.lastError().text()}")

    def copy_database(self, new_name: str) -> bool:
        current_path = self.get_database_path(self.name)
        new_path = self.get_database_path(new_name)

        if os.path.exists(new_path):
            return False

        # Flush changes before copying
        self.database.commit()

        try:
            shutil.copy2(current_path, new_path)
            return True
        except IOError as e:
            print(f"Failed to copy database: {e}")
            return False

    def rename_database(self, new_name: str) -> bool:
        current_path = self.get_database_path(self.name)
        new_path = self.get_database_path(new_name)

        if os.path.exists(new_path):
            return False

        # Close database before renaming
        if self.database.isOpen():
            self.database.close()

        try:
            os.rename(current_path, new_path)
            self.name = new_name
            # Reopen database with new name
            self.database.setDatabaseName(new_path)
            if not self.database.open():
                print(
                    f"Failed to reopen database after rename: {self.database.lastError().text()}"
                )
                return False
            return True
        except OSError as e:
            print(f"Failed to rename database: {e}")
            # Try to reopen old database
            self.database.setDatabaseName(current_path)
            self.database.open()
            return False

    def get_groups_model(self):
        model = QSqlTableModel(db=self.database)
        model.setTable("groups")
        model.setEditStrategy(QSqlTableModel.EditStrategy.OnManualSubmit)
        return model

    def get_messages_model(self) -> QSqlTableModel:
        model = QSqlTableModel(db=self.database)
        model.setTable("messages")
        model.setEditStrategy(QSqlTableModel.EditStrategy.OnManualSubmit)
        model.select()
        return model

    def get_message_replies_model(self) -> QSqlTableModel:
        model = QSqlTableModel(db=self.database)
        model.setTable("message_replies")
        model.setEditStrategy(QSqlTableModel.EditStrategy.OnManualSubmit)
        return model

    def get_message_reactions_model(self) -> QSqlTableModel:
        model = QSqlTableModel(db=self.database)
        model.setTable("message_reactions")
        model.setEditStrategy(QSqlTableModel.EditStrategy.OnManualSubmit)
        return model

    def get_message_conditions_model(self) -> ConditionsTableModel:
        return ConditionsTableModel(db=self.database)

    def get_logs_model(self) -> LogsTableModel:
        return LogsTableModel(db=self.database)

    def exec(self, sql: str):
        query = QSqlQuery(self.database)
        if not query.exec(sql):
            print(query.lastError().text())

    def new_log(self, record: logging.LogRecord):
        query = QSqlQuery(self.database)
        query.prepare(
            "INSERT INTO logs (datetime, message, level_number) VALUES (?, ?, ?)"
        )
        query.addBindValue(record.created)
        query.addBindValue(record.getMessage())
        query.addBindValue(record.levelno)
        if not query.exec():
            print(query.lastError().text())

    def delete_reactions_by_message_id(self, message_id: int):
        query = QSqlQuery(self.database)
        query.prepare("DELETE FROM message_reactions WHERE message_id = ?")
        query.addBindValue(message_id)
        if not query.exec():
            print(query.lastError().text())

    def delete_all_reactions(self):
        query = QSqlQuery(self.database)
        query.prepare("DELETE FROM message_reactions")
        if not query.exec():
            print(query.lastError().text())

    def delete_replies_by_message_id(self, message_id: int):
        query = QSqlQuery(self.database)
        query.prepare("DELETE FROM message_replies WHERE message_id = ?")
        query.addBindValue(message_id)
        if not query.exec():
            print(query.lastError().text())

    def delete_all_replies(self):
        query = QSqlQuery(self.database)
        query.prepare("DELETE FROM message_replies")
        if not query.exec():
            print(query.lastError().text())

    def delete_conditions_by_message_id(self, message_id: int):
        query = QSqlQuery(self.database)
        query.prepare("DELETE FROM message_conditions WHERE message_id = ?")
        query.addBindValue(message_id)
        if not query.exec():
            print(query.lastError().text())

    def delete_all_conditions(self):
        query = QSqlQuery(self.database)
        query.prepare("DELETE FROM message_conditions")
        if not query.exec():
            print(query.lastError().text())

    def delete_message_by_id(self, message_id: int):
        query = QSqlQuery(self.database)
        query.prepare("DELETE FROM messages WHERE id = ?")
        query.addBindValue(message_id)
        if not query.exec():
            print(query.lastError().text())
        self.delete_conditions_by_message_id(message_id)
        self.delete_reactions_by_message_id(message_id)
        self.delete_replies_by_message_id(message_id)

    def delete_all_messages(self):
        query = QSqlQuery(self.database)
        query.prepare("DELETE FROM messages")
        if not query.exec():
            print(query.lastError().text())
        self.delete_all_conditions()
        self.delete_all_reactions()
        self.delete_all_replies()

    @staticmethod
    def get_database_path(file_name: str):
        if file_name == ":memory:":
            return file_name

        data_dir = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.AppDataLocation
        )
        data_dir = os.path.join(data_dir, "projects")

        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        full_path = os.path.join(data_dir, f"{file_name}.db")
        return os.path.normpath(full_path)

    @staticmethod
    def list_projects():
        data_dir = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.AppDataLocation
        )
        data_dir = os.path.join(data_dir, "projects")
        if not os.path.exists(data_dir):
            return []
        return [f.replace(".db", "") for f in os.listdir(data_dir) if f.endswith(".db")]
