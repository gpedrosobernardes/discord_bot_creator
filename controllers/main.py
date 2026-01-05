from __future__ import annotations

import logging

from PySide6.QtCore import (
    QCoreApplication,
    QStringListModel,
    QSortFilterProxyModel,
    QSettings,
)
from PySide6.QtGui import QStandardItemModel, QAction

from utils.token_validator import TokenValidator
from views.main import MainView
from widgets.config_menu import QConfigMenu
from widgets.file_menu import QFileMenu
from widgets.menu_bar import MenuBar

translate = QCoreApplication.translate


class MenuController:
    def __init__(self, main_controller: MainController, menu: MenuBar):
        self.main_controller = main_controller
        self.menu = menu
        self.setup()

    def setup(self):
        self.setup_config_menu(self.menu.config)
        self.setup_file_menu(self.menu.file)

    def setup_file_menu(self, menu: QFileMenu):
        # connections
        menu.exit.triggered.connect(self.main_controller.view.window.close)
        # menu.load.triggered.connect(self.main_controller.on_load_action)

    def setup_config_menu(self, menu: QConfigMenu):
        # menu.language.english.triggered.connect(
        #     lambda: self.main_controller.set_language("en_us")
        # )
        # menu.language.portuguese.triggered.connect(
        #     lambda: self.main_controller.set_language("pt_br")
        # )
        menu.auto_start_bot.toggled.connect(
            lambda value: self.main_controller.settings.setValue(
                "auto_start_bot", value
            )
        )
        menu.auto_start_bot.setChecked(
            self.main_controller.settings.value("auto_start_bot") == "True"
        )
        language = self.main_controller.settings.value("language")
        language_action = menu.language.findChild(QAction, language)
        language_action.setChecked(True)

        log_level = self.main_controller.settings.value("log_level")
        log_level_name = logging.getLevelName(log_level)
        log_level_action = menu.log_level.findChild(QAction, log_level_name)
        log_level_action.setChecked(True)


class MainController:
    def __init__(self, settings: QSettings):
        self.settings = settings
        self.view = MainView()
        self.menu_controller = MenuController(self, self.view.menu_bar)
        self.messages_model = QStringListModel()
        self.messages_proxy_model = QSortFilterProxyModel()
        self.groups_model = QStandardItemModel()
        self.groups_proxy_model = QSortFilterProxyModel()
        self.view.messages_list_widget.setModel(self.messages_proxy_model)
        self.view.groups_list_widget.setModel(self.groups_proxy_model)
        self.setup_validators()
        self.setup_connections()
        self.load_settings()

    def load_settings(self):
        self.view.token_widget.setText(self.settings.value("token"))

    def setup_connections(self):
        self.view.token_widget.editingFinished.connect(self.on_token_changed)

    def setup_validators(self):
        self.view.token_widget.setValidator(TokenValidator(self.view.token_widget))

    def on_token_changed(self):
        if self.view.token_widget.hasAcceptableInput():
            self.settings.setValue("token", self.view.token_widget.text())
