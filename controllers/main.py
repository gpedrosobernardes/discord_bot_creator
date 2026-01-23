from __future__ import annotations

import sys
import webbrowser
from typing import Optional

from PySide6.QtCore import (
    QSortFilterProxyModel,
    QSettings,
    Qt,
    Slot,
    QObject,
    Signal,
    QPoint,
)
from PySide6.QtGui import QAction, QKeySequence, QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QCompleter, QInputDialog, QMessageBox, QMenu
from qextrawidgets.icons import QThemeResponsiveIcon

from controllers.config import ConfigController
from controllers.message import MessageController
from core.bot_thread import QBotThread
from core.database import DatabaseController
from core.log_handler import LogHandler
from utils.token_validator import TokenValidator
from views.credits import CreditsView
from views.logs import LogsView
from views.main import MainView


class MainController(QObject):
    """
    Controller for the Main Window.

    Orchestrates the interaction between the MainView, DatabaseController,
    and other sub-controllers/views.
    """

    switch_project = Signal()

    def __init__(
        self,
        database: DatabaseController,
        user_settings: QSettings,
        config_controller: ConfigController,
        logs_view: LogsView,
        credits_view: CreditsView,
        log_handler: LogHandler,
    ):
        """
        Initializes the MainController.

        Args:
            database: The database controller instance.
            user_settings: The user settings instance.
            config_controller: The configuration controller instance.
            logs_view: The logs view instance.
            credits_view: The credits view instance.
        """
        super().__init__()
        # 1. Dependency Injection
        self.database = database
        self.user_settings = user_settings
        self.config_view = config_controller.view
        self.config_controller = config_controller
        self.logs_view = logs_view
        self.credits_view = credits_view
        self.log_handler = log_handler

        # 2. State & Context
        self.message_windows = []
        self.messages_model = self.database.get_messages_model()
        self.messages_proxy_model = QSortFilterProxyModel()
        self.groups_model = QStandardItemModel()
        self.bot_thread = QBotThread()

        # 3. View Initialization
        self.view = MainView()

        # 4. Init Sequence
        self._init_models()
        self._init_actions()
        self._init_validators()
        self._init_completers()
        self._init_connections()

        # 5. Initial State
        self.translate_ui()
        self.view.show()

    # --- Initialization ---

    def _init_models(self):
        """Initialize and configure data models."""
        self.messages_proxy_model.setSourceModel(self.messages_model)
        self.messages_proxy_model.setFilterCaseSensitivity(
            Qt.CaseSensitivity.CaseInsensitive
        )
        self.messages_proxy_model.setFilterKeyColumn(
            self.messages_model.fieldIndex("name")
        )

        self.view.messages_list_view.setModel(self.messages_proxy_model)
        self.view.messages_list_view.setModelColumn(
            self.messages_model.fieldIndex("name")
        )

        self.view.groups_list_widget.setModel(self.groups_model)

    def _init_actions(self):
        """Initialize all QActions and assign them to menus/buttons."""
        self._setup_project_actions()
        self._setup_edit_actions()
        self._setup_group_actions()
        self._setup_help_actions()

    def _init_validators(self):
        """Initialize input validators."""
        self.view.token_line_edit.setValidator(
            TokenValidator(self.view.token_line_edit)
        )

    def _init_completers(self):
        """Initialize input completers."""
        cmd_completer = QCompleter(["clear"])
        cmd_completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        cmd_completer.setFilterMode(Qt.MatchFlag.MatchContains)
        self.view.cmd_line_edit.setCompleter(cmd_completer)

    def _init_connections(self):
        """Connect signals to slots."""
        self.view.search_messages_line_edit.textChanged.connect(
            self.messages_proxy_model.setFilterFixedString
        )
        self.view.token_line_edit.editingFinished.connect(self.on_token_changed)
        self.view.switch_bot_button.clicked.connect(self.on_switch_bot_clicked)

        # Groups List Context Menu
        self.view.groups_list_widget.customContextMenuRequested.connect(
            self.on_groups_list_context_menu
        )

        # Bot Thread Connections
        self.bot_thread.signals.login_failure.connect(self.on_bot_login_failure)
        self.bot_thread.finished.connect(self.on_bot_finished)
        self.bot_thread.signals.bot_ready.connect(self.on_bot_ready)
        self.bot_thread.signals.guild_join.connect(self.on_guild_join)
        self.bot_thread.signals.guild_remove.connect(self.on_guild_remove)
        self.bot_thread.signals.guild_update.connect(self.on_guild_update)

        # Log Handler Connections
        self.log_handler.signaler.log.connect(self.view.logs_text_edit.add_log)

    def load_initial_state(self):
        """Load initial state from settings."""
        self.view.token_line_edit.setText(self.user_settings.value("token"))

        current_project = self.user_settings.value("current_project")
        projects = DatabaseController.list_projects()

        if current_project and current_project in projects:
            self._switch_project(current_project)
            return

        while True:
            projects = DatabaseController.list_projects()

            if not projects:
                name = self._prompt_new_project_name(strict=True)
                if name:
                    self._switch_project(name)
                    return
            else:
                new_project_str = self.tr("<Create New Project>")
                items = [new_project_str] + projects

                item, ok = QInputDialog.getItem(
                    self.view,
                    self.tr("Load Project"),
                    self.tr("Select a project or create a new one:"),
                    items,
                    0,
                    False,
                )

                if not ok:
                    sys.exit(0)

                if item == new_project_str:
                    name = self._prompt_new_project_name(strict=False)
                    if name:
                        self._switch_project(name)
                        return
                else:
                    self._switch_project(item)
                    return

    # --- Action Setup Helpers ---

    def _create_action(
        self,
        icon_name: Optional[str] = None,
        shortcut: Optional[str] = None,
        triggered=None,
    ) -> QAction:
        """Helper to create a QAction."""
        action = QAction(self.view)
        if icon_name:
            action.setIcon(QThemeResponsiveIcon.fromAwesome(icon_name))
        if shortcut:
            action.setShortcut(QKeySequence(shortcut))
        if triggered:
            action.triggered.connect(triggered)
        return action

    def _setup_project_actions(self):
        self.new_project_action = self._create_action(
            triggered=self.on_new_project_action
        )
        self.load_project_action = self._create_action(
            triggered=self.on_load_project_action
        )
        self.save_as_project_action = self._create_action(
            triggered=self.on_save_as_project_action
        )
        self.rename_project_action = self._create_action(
            triggered=self.on_rename_project_action
        )
        self.config_action = self._create_action(triggered=self.config_view.show)
        self.exit_action = self._create_action(triggered=self.view.close)

        self.view.project_menu.addActions(
            [
                self.new_project_action,
                self.load_project_action,
                self.save_as_project_action,
                self.rename_project_action,
                self.config_action,
                self.exit_action,
            ]
        )

    def _setup_edit_actions(self):
        self.new_message_action = self._create_action(
            "fa6s.plus", "Ctrl+N", self.on_new_message_action
        )
        self.edit_message_action = self._create_action(
            "fa6s.pencil", "Ctrl+E", self.on_edit_message_action
        )
        self.remove_message_action = self._create_action(
            "fa6s.minus", "Delete", self.on_remove_message_action
        )
        self.remove_all_message_action = self._create_action(
            "fa6s.trash", "Ctrl+Delete", self.on_remove_all_message_action
        )

        self.view.edit_menu.addActions(
            [self.new_message_action, self.remove_all_message_action]
        )

        # Bind to buttons
        self.view.new_message_tool_button.setDefaultAction(self.new_message_action)
        self.view.edit_message_tool_button.setDefaultAction(self.edit_message_action)
        self.view.remove_message_tool_button.setDefaultAction(
            self.remove_message_action
        )
        self.view.remove_all_message_tool_button.setDefaultAction(
            self.remove_all_message_action
        )

    def _setup_group_actions(self):
        self.config_group_action = self._create_action("fa6s.gear")
        self.quit_group_action = self._create_action("fa6s.arrow-right-from-bracket")

        self.view.config_group_button.setDefaultAction(self.config_group_action)
        self.view.quit_group_button.setDefaultAction(self.quit_group_action)

    def _setup_help_actions(self):
        self.discord_applications_action = self._create_action(
            triggered=lambda: webbrowser.open(
                "https://discord.com/developers/applications/"
            )
        )
        self.report_bug_action = self._create_action(
            triggered=lambda: webbrowser.open(
                "https://github.com/gustavopedrosob/discord_bot_creator/issues/new"
            )
        )
        self.project_action = self._create_action(
            triggered=lambda: webbrowser.open(
                "https://github.com/gustavopedrosob/discord_bot_creator"
            )
        )
        self.logs_action = self._create_action(triggered=self.logs_view.window.show)
        self.credits_action = self._create_action(
            triggered=self.credits_view.window.show
        )

        self.view.help_menu.addActions(
            [
                self.discord_applications_action,
                self.logs_action,
                self.credits_action,
                self.project_action,
                self.report_bug_action,
            ]
        )

    def translate_ui(self):
        """Translate UI texts for actions."""
        self.view.translate_ui()

        # Project
        self.new_project_action.setText(self.tr("New"))
        self.load_project_action.setText(self.tr("Load"))
        self.save_as_project_action.setText(self.tr("Save as"))
        self.rename_project_action.setText(self.tr("Rename"))
        self.config_action.setText(self.tr("Configuration"))
        self.exit_action.setText(self.tr("Exit"))

        # Edit / Messages
        self.new_message_action.setText(self.tr("New message"))
        self.edit_message_action.setText(self.tr("Edit message"))
        self.remove_message_action.setText(self.tr("Remove message"))
        self.remove_all_message_action.setText(self.tr("Remove all messages"))

        # Groups
        self.config_group_action.setText(self.tr("Config group"))
        self.quit_group_action.setText(self.tr("Quit group"))

        # Help
        self.credits_action.setText(self.tr("Credits"))
        self.logs_action.setText(self.tr("Logs"))
        self.project_action.setText(self.tr("Project"))
        self.report_bug_action.setText(self.tr("Report bug"))
        self.discord_applications_action.setText(self.tr("Discord applications"))

    # --- Project Management Logic ---

    def _switch_project(self, project_name: str):
        if not project_name:
            return

        self.database.switch_database(project_name)
        self.user_settings.setValue("current_project", project_name)
        self._refresh_models()
        self.view.setWindowTitle(f"Discord Bot Creator - {project_name}")
        self.bot_thread.set_database_name(project_name)
        self.switch_project.emit()

    def _refresh_models(self):
        self.messages_model = self.database.get_messages_model()
        self.messages_proxy_model.setSourceModel(self.messages_model)
        self.messages_proxy_model.setFilterKeyColumn(
            self.messages_model.fieldIndex("name")
        )
        self.view.messages_list_view.setModel(self.messages_proxy_model)
        self.view.messages_list_view.setModelColumn(
            self.messages_model.fieldIndex("name")
        )

    def _prompt_new_project_name(self, strict: bool = False) -> Optional[str]:
        default_name = self.tr("New Project")
        while True:
            dialog = QInputDialog(self.view)
            dialog.setWindowTitle(self.tr("New Project"))
            dialog.setLabelText(self.tr("Project Name:"))
            dialog.setTextValue(default_name)

            if strict:
                dialog.setWindowFlags(
                    Qt.WindowType.Dialog
                    | Qt.WindowType.WindowTitleHint
                    | Qt.WindowType.CustomizeWindowHint
                )

            ret = dialog.exec()

            if ret == QInputDialog.DialogCode.Accepted:
                name = dialog.textValue().strip()
                if not name:
                    QMessageBox.warning(
                        self.view,
                        self.tr("Error"),
                        self.tr("Project name cannot be empty."),
                    )
                    continue
                if name in DatabaseController.list_projects():
                    QMessageBox.warning(
                        self.view,
                        self.tr("Error"),
                        self.tr("A project with this name already exists."),
                    )
                    continue
                return name
            else:
                if strict:
                    continue
                return None

    @Slot()
    def on_new_project_action(self):
        name = self._prompt_new_project_name()
        if name:
            self._switch_project(name)

    @Slot()
    def on_load_project_action(self):
        projects = DatabaseController.list_projects()
        if not projects:
            QMessageBox.information(
                self.view,
                self.tr("Load Project"),
                self.tr("No projects found."),
            )
            return

        current = self.database.name
        current_index = projects.index(current) if current in projects else 0

        name, ok = QInputDialog.getItem(
            self.view,
            self.tr("Load Project"),
            self.tr("Select Project:"),
            projects,
            current_index,
            False,
        )
        if ok and name:
            self._switch_project(name)

    @Slot()
    def on_save_as_project_action(self):
        name, ok = QInputDialog.getText(
            self.view,
            self.tr("Save Project As"),
            self.tr("New Project Name:"),
        )
        if ok and name:
            if self.database.copy_database(name):
                self._switch_project(name)
                QMessageBox.information(
                    self.view,
                    self.tr("Project Saved"),
                    self.tr(f"Project '{name}' saved successfully."),
                )
            else:
                QMessageBox.critical(
                    self.view,
                    self.tr("Error"),
                    self.tr(
                        "Failed to save project. The name might already exist or be invalid."
                    ),
                )

    @Slot()
    def on_rename_project_action(self):
        name = self._prompt_new_project_name()
        if name:
            if self.database.rename_database(name):
                self.user_settings.setValue("current_project", name)
                self.view.setWindowTitle(f"Discord Bot Creator - {name}")
                QMessageBox.information(
                    self.view,
                    self.tr("Project Renamed"),
                    self.tr(f"Project renamed to '{name}' successfully."),
                )
            else:
                QMessageBox.critical(
                    self.view,
                    self.tr("Error"),
                    self.tr(
                        "Failed to rename project. The name might already exist or be invalid."
                    ),
                )

    # --- Message Management Logic ---

    def _new_message_controller(self, index: Optional[int] = None):
        message_controller = MessageController(
            self.messages_model, self.database, self.user_settings, index
        )
        window = message_controller.view.window
        self.message_windows.append(message_controller)
        window.destroyed.connect(
            lambda: self.message_windows.remove(message_controller)
        )
        self.config_controller.language_changed.connect(message_controller.translate_ui)

    @Slot()
    def on_new_message_action(self):
        self._new_message_controller()

    @Slot()
    def on_edit_message_action(self):
        index = self.view.messages_list_view.currentIndex()
        id_index = index.siblingAtColumn(self.messages_model.fieldIndex("id"))
        data = self.messages_model.data(id_index)
        self._new_message_controller(data)

    @Slot()
    def on_remove_message_action(self):
        index = self.view.messages_list_view.currentIndex()
        id_index = index.siblingAtColumn(self.messages_model.fieldIndex("id"))
        data = self.messages_model.data(id_index)
        self.database.delete_message_by_id(data)
        self.messages_model.select()

    @Slot()
    def on_remove_all_message_action(self):
        if self.user_settings.value("confirm_actions", type=bool):
            ret = QMessageBox.question(
                self.view,
                self.tr("Confirm Deletion"),
                self.tr("Are you sure you want to delete all messages?"),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )

            if ret == QMessageBox.StandardButton.No:
                return

        self.database.delete_all_messages()
        self.messages_model.select()

    # --- App Logic ---

    @Slot()
    def on_token_changed(self):
        if self.view.token_line_edit.hasAcceptableInput():
            self.user_settings.setValue("token", self.view.token_line_edit.text())

    # --- Bot Logic ---

    @Slot()
    def on_switch_bot_clicked(self):
        """Handle bot start/stop."""
        if self.view.switch_bot_button.isChecked():
            token = self.view.token_line_edit.text()
            if not token:
                QMessageBox.warning(
                    self.view,
                    self.tr("Error"),
                    self.tr("Please enter a valid token."),
                )
                self.view.switch_bot_button.setChecked(False)
                return

            self.bot_thread.set_token(token)
            self.bot_thread.start()
            self.view.token_line_edit.setReadOnly(True)
        else:
            self.bot_thread.close()
            self.view.token_line_edit.setReadOnly(False)

    @Slot()
    def on_bot_login_failure(self):
        """Called when login fails."""
        QMessageBox.critical(
            self.view,
            self.tr("Login Failed"),
            self.tr("Invalid token. Please check your token and try again."),
        )
        self.view.switch_bot_button.setChecked(False)
        self.view.token_line_edit.setReadOnly(False)

    @Slot()
    def on_bot_finished(self):
        """Called when the bot thread finishes."""
        if self.view.switch_bot_button.isChecked():
            self.view.switch_bot_button.setChecked(False)
        self.view.token_line_edit.setReadOnly(False)
        self.groups_model.clear()

    @Slot()
    def on_bot_ready(self):
        """Called when the bot is ready."""
        self.groups_model.clear()
        for guild_id, guild in self.bot_thread.groups().items():
            item = QStandardItem(guild.name)
            item.setData(guild_id, Qt.ItemDataRole.UserRole)
            self.groups_model.appendRow(item)

    @Slot(QPoint)
    def on_groups_list_context_menu(self, position: QPoint):
        """Handles the context menu request for the groups list."""
        menu = QMenu(self.view)
        menu.addAction(self.config_group_action)
        menu.addAction(self.quit_group_action)
        global_position = self.view.groups_list_widget.mapToGlobal(position)
        menu.exec(global_position)

    @Slot(str)
    def on_guild_join(self, guild_id_str: str):
        guild_id = int(guild_id_str)
        guilds = self.bot_thread.groups()
        guild = guilds.get(guild_id)

        if guild:
            item = QStandardItem(guild.name)
            item.setData(guild_id, Qt.ItemDataRole.UserRole)
            self.groups_model.appendRow(item)

    @Slot(str)
    def on_guild_remove(self, guild_id_str: str):
        guild_id = int(guild_id_str)
        matches = self.groups_model.match(
            self.groups_model.index(0, 0),
            Qt.ItemDataRole.UserRole,
            guild_id,
            1,
            Qt.MatchFlag.MatchExactly,
        )
        if matches:
            self.groups_model.removeRow(matches[0].row())

    @Slot(str)
    def on_guild_update(self, guild_id_str: str):
        guild_id = int(guild_id_str)
        guilds = self.bot_thread.groups()
        guild = guilds.get(guild_id)

        if not guild:
            return

        matches = self.groups_model.match(
            self.groups_model.index(0, 0),
            Qt.ItemDataRole.UserRole,
            guild_id,
            1,
            Qt.MatchFlag.MatchExactly,
        )
        if matches:
            item = self.groups_model.itemFromIndex(matches[0])
            item.setText(guild.name)
