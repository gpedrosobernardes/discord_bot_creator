from __future__ import annotations

import webbrowser

from PySide6.QtCore import (
    QCoreApplication,
    QSortFilterProxyModel,
    QSettings,
    QTranslator,
)
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QCompleter

from controllers.config import ConfigController
from controllers.message import MessageController
from core.database import DatabaseController
from utils.token_validator import TokenValidator
from views.config import ConfigView
from views.credits import CreditsView
from views.logs import LogsView
from views.main import MainView

translate = QCoreApplication.translate


class MainController:
    def __init__(
        self,
        database: DatabaseController,
        user_settings: QSettings,
        config_view: ConfigView,
        logs_view: LogsView,
        credits_view: CreditsView,
    ):
        self.database = database
        self.user_settings = user_settings
        self.view = MainView()

        self.messages_model = self.database.get_messages_model()
        self.messages_proxy_model = QSortFilterProxyModel()
        self.messages_proxy_model.setFilterCaseSensitivity(
            Qt.CaseSensitivity.CaseInsensitive
        )
        self.messages_proxy_model.setFilterKeyColumn(
            self.messages_model.fieldIndex("name")
        )
        self.message_windows = []
        self.messages_proxy_model.setSourceModel(self.messages_model)
        self.view.messages_list_view.setModel(self.messages_proxy_model)
        self.view.messages_list_view.setModelColumn(
            self.messages_model.fieldIndex("name")
        )

        self.setup_validators()
        self.setup_completers()
        self.setup_connections(self.view, logs_view, config_view, credits_view)
        self.load_settings()

    def load_settings(self):
        self.view.token_line_edit.setText(self.user_settings.value("token"))

    def setup_connections(
        self,
        view: MainView,
        logs_view: LogsView,
        config_view: ConfigView,
        credits_view: CreditsView,
    ):

        # line edits
        view.search_messages_line_edit.textChanged.connect(
            self.messages_proxy_model.setFilterFixedString
        )

        view.token_line_edit.editingFinished.connect(self.on_token_changed)

        # actions

        # file actions
        view.config_action.triggered.connect(config_view.window.show)

        # message actions
        view.new_message_action.triggered.connect(self.on_new_message_action)
        view.edit_message_action.triggered.connect(self.on_edit_message_action)
        view.remove_message_action.triggered.connect(self.on_remove_message_action)
        view.remove_all_message_action.triggered.connect(
            self.on_remove_all_message_action
        )

        # help actions
        view.discord_applications_action.triggered.connect(
            lambda: webbrowser.open("https://discord.com/developers/applications/")
        )
        view.report_bug_action.triggered.connect(
            lambda: webbrowser.open(
                "https://github.com/gustavopedrosob/discord_bot_creator/issues/new"
            )
        )
        view.project_action.triggered.connect(
            lambda: webbrowser.open(
                "https://github.com/gustavopedrosob/discord_bot_creator"
            )
        )
        view.logs_action.triggered.connect(logs_view.window.show)
        view.credits_action.triggered.connect(credits_view.window.show)

    def setup_validators(self):
        self.view.token_line_edit.setValidator(
            TokenValidator(self.view.token_line_edit)
        )

    def setup_completers(self):
        cmd_completer = QCompleter(["clear"])
        cmd_completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        cmd_completer.setFilterMode(Qt.MatchFlag.MatchContains)
        self.view.cmd_line_edit.setCompleter(cmd_completer)

    def on_token_changed(self):
        if self.view.token_line_edit.hasAcceptableInput():
            self.user_settings.setValue("token", self.view.token_line_edit.text())

    def on_new_message_action(self):
        self.new_message_controller()

    def on_edit_message_action(self):
        index = self.view.messages_list_view.currentIndex().row()
        self.new_message_controller(index)

    def on_remove_message_action(self):
        index = self.view.messages_list_view.currentIndex().row()
        self.messages_model.removeRow(index)

    def on_remove_all_message_action(self):
        self.messages_model.removeRows(0, self.messages_model.rowCount())

    def new_message_controller(self, index: int = None):
        message_controller = MessageController(
            self.messages_model, self.database, index
        )
        window = message_controller.view.window
        self.message_windows.append(message_controller)
        window.destroyed.connect(
            lambda: self.message_windows.remove(message_controller)
        )

    # def on_new_message(self, record: QSqlRecord):
    #     model = self.database.get_messages_model()
    #     model.insertRecord(-1, record)
    #     model.submit()
    #     self.messages_model.insertRow(self.messages_model.rowCount())
    #     index = self.messages_model.index(self.messages_model.rowCount())
    #     self.messages_model.setData(
    #         index, record.value("name"), role=Qt.ItemDataRole.DisplayRole
    #     )
