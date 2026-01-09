import logging
import os

from PySide6.QtCore import QStandardPaths
from PySide6.QtSql import (
    QSqlDatabase,
    QSqlQuery,
    QSqlTableModel,
    QSqlRelationalTableModel,
    QSqlRelation,
)


class DatabaseController:
    def __init__(self, name: str):
        path = self.get_database_path(name)

        self.database = QSqlDatabase.addDatabase("QSQLITE")
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
                operator TEXT NOT NULL,
                value TEXT NOT NULL,
                case_insensitive BOOLEAN DEFAULT 0,
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

    def get_groups_model(self):
        model = QSqlTableModel(db=self.database)
        model.setTable("groups")
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
        # model.select()
        return model

    def get_message_reactions_model(self) -> QSqlTableModel:
        # ALTERAÇÃO: Use QSqlTableModel em vez de QSqlRelationalTableModel
        model = QSqlTableModel(db=self.database)
        model.setTable("message_reactions")
        # REMOVIDO: model.setRelation(...) -> Não é necessário aqui e causa o erro
        # model.select()
        return model

    def get_message_conditions_model(self) -> QSqlTableModel:
        model = QSqlTableModel(db=self.database)
        model.setTable("message_conditions")

        return model

    def get_logs_model(self):
        model = QSqlTableModel(db=self.database)
        model.setTable("logs")
        return model

    def exec(self, sql: str):
        query = QSqlQuery(self.database)
        if not query.exec(sql):
            print(query.lastError().text())

    @staticmethod
    def get_database_path(file_name: str):
        if file_name == ":memory:":
            return file_name

        data_dir = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.AppDataLocation
        )

        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        full_path = os.path.join(data_dir, file_name)
        return os.path.normpath(full_path)
