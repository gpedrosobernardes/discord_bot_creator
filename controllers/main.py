import os
import typing
from pathlib import Path

from PySide6.QtCore import Qt, QCoreApplication, QStringListModel, QSortFilterProxyModel
from PySide6.QtGui import QCloseEvent, QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QListWidgetItem, QFileDialog
from qfluentwidgets import MessageBox

from core.bot_thread import QBotThread
from core.config import Config
from core.database import Database
from views.main import MainView
from widgets.confirm_message_box import QConfirmMessageBox

translate = QCoreApplication.translate


class MainController:
    def __init__(self, database: Database, bot_thread: QBotThread):
        self.view = MainView()
        self.messages_model = QStringListModel()
        self.messages_proxy_model = QSortFilterProxyModel()
        self.groups_model = QStandardItemModel()
        self.groups_proxy_model = QSortFilterProxyModel()
        self.view.messages_list_widget.setModel(self.messages_proxy_model)
        self.view.groups_list_widget.setModel(self.groups_proxy_model)
        self.database = database
        self.bot_thread = bot_thread
        self.setup_binds()
        self.setup_filter_proxys()
        self.update_bot_button()

    def setup_filter_proxys(self):
        self.messages_proxy_model.setSourceModel(self.messages_model)
        self.messages_proxy_model.setFilterCaseSensitivity(
            Qt.CaseSensitivity.CaseInsensitive
        )
        self.groups_proxy_model.setSourceModel(self.groups_model)
        self.groups_proxy_model.setFilterCaseSensitivity(
            Qt.CaseSensitivity.CaseInsensitive
        )

    def setup_binds(self):
        self.view.remove_message_button.clicked.connect(
            self.confirm_remove_selected_message
        )
        self.view.remove_all_message_button.clicked.connect(
            self.confirm_remove_messages
        )
        self.view.turn_on_bot_button.clicked.connect(self.start_turn_on_bot_thread)
        self.view.turn_off_bot_button.clicked.connect(self.turn_off_bot)
        self.__setup_message_list_binds(self.view.messages_list_widget)
        self.__setup_menu_bar_binds(self.view.menu_bar)
        self.__setup_bot_thread_binds(self.bot_thread)
        self.view.groups_list_widget.quit_action.triggered.connect(
            self.quit_selected_group
        )
        self.view.quit_group_button.clicked.connect(self.quit_selected_group)
        self.view.token_widget.textEdited.connect(self.update_token)
        self.view.search_messages.textEdited.connect(
            self.messages_proxy_model.setFilterFixedString
        )
        self.view.search_messages.clearSignal.connect(
            lambda: self.messages_proxy_model.setFilterFixedString("")
        )
        self.view.search_groups.textEdited.connect(
            self.groups_proxy_model.setFilterFixedString
        )
        self.view.search_groups.clearSignal.connect(
            lambda: self.groups_proxy_model.setFilterFixedString("")
        )
        # noinspection PyUnresolvedReferences
        self.view.cmd_combobox.lineEdit().returnPressed.connect(self.entry_command)
        self.view.window.close_event = self.close_event

    def __setup_menu_bar_binds(self, menu_bar):
        menu_bar.file.exit.triggered.connect(self.view.window.close)
        menu_bar.file.load.triggered.connect(self.on_load_action)

        menu_bar.config.language.english.triggered.connect(
            lambda: self.set_language("en_us")
        )
        menu_bar.config.language.portuguese.triggered.connect(
            lambda: self.set_language("pt_br")
        )

    def __setup_message_list_binds(self, message_list):
        message_list.remove_action.triggered.connect(
            self.confirm_remove_selected_message
        )
        message_list.remove_all_action.triggered.connect(self.confirm_remove_messages)

    def __setup_bot_thread_binds(self, bot_thread):
        bot_thread.finished.connect(self.on_bot_thread_finished)
        bot_thread.bot_ready.connect(self.on_bot_ready)
        bot_thread.login_failure.connect(self.on_login_failure)
        bot_thread.log.connect(self.view.logs_text_edit.add_log)
        bot_thread.guild_join.connect(self.update_groups)
        bot_thread.guild_remove.connect(self.update_groups)
        bot_thread.guild_update.connect(self.update_groups)

    def quit_selected_group(self):
        selection = self.view.groups_list_widget.selectedIndexes()
        if selection:
            selected = self.groups_proxy_model.mapToSource(selection[0])
            group_id = self.groups_model.data(selected, Qt.ItemDataRole.UserRole)
            self.groups_model.removeRow(selected.row())
            self.bot_thread.leave_group(group_id)

    def update_groups(self):
        self.groups_model.clear()
        for group_id, group in self.bot_thread.groups().items():
            item = QStandardItem(group.name)
            item.setData(group_id, Qt.ItemDataRole.UserRole)
            self.groups_model.appendRow(item)

    def on_login_failure(self):
        self.information_message_box(
            translate("MainWindow", "Login failure"),
            translate("MainWindow", "Improper token has been passed."),
        )
        self.view.turn_on_bot_button.setDisabled(False)

    def information_message_box(self, title: str, text: str):
        message_box = MessageBox(title, text, self.view.window)
        message_box.cancelButton.hide()
        message_box.exec()

    def update_window_title(self):
        title = "Discord Bot Creator"
        database_path = Path(Config.get("database"))
        if database_path and database_path.exists():
            title = f"Discord Bot Creator - {database_path.name}"
        if self.database.need_to_commit():
            title += " *"
        self.view.window.setWindowTitle(title)

    def on_load_action(self):
        database_path = self.select_file_dialog()
        if database_path:
            Config.set("database", str(database_path))
            Config.save()
            self.database.update_session()
            self.load_data()
            self.update_window_title()

    def select_file_dialog(self) -> typing.Optional[Path]:
        file_path, _ = QFileDialog.getOpenFileName(
            self.view.window,
            translate("MainWindow", "Open File"),
            os.getcwd(),
            "DB Files (*.db)",
        )
        if file_path:
            return Path(file_path)
        return None

    def saved_successfully_message_box(self):
        self.information_message_box(
            translate("MainWindow", "Saving"),
            translate(
                "MainWindow",
                "The file has been saved successfully.",
            ),
        )

    def set_language(self, language: str):
        self.information_message_box(
            translate("MainWindow", "Warning"),
            translate(
                "MainWindow",
                "You need to restart the application to apply the changes.",
            ),
        )
        Config.set("language", language)
        Config.save()

    def start_turn_on_bot_thread(self):
        if Config.get("token") == "":
            self.on_login_failure()
        else:
            self.bot_thread.start()
            self.view.turn_on_bot_button.setDisabled(True)

    def on_bot_ready(self):
        self.view.turn_on_bot_button.setDisabled(False)
        self.update_bot_button()
        self.update_groups()

    def entry_command(self):
        """Handles commands for the bot's log entry."""
        cmd = self.view.cmd_combobox.lineEdit().text()
        if cmd in ["cls", "clear"]:
            self.view.logs_text_edit.clear()
            self.view.cmd_combobox.clear()

    def update_token(self):
        """Updates the token in the "config.json" file and in the interface."""
        Config.set("token", self.view.token_widget.text())
        Config.save()

    def __get_list_item_message(self, message: str) -> typing.Optional[QListWidgetItem]:
        for i in self.view.messages_list_widget.selectedItems():
            if i.text() == message:
                return i
        return None

    def update_bot_button(self):
        on = self.bot_thread.isRunning()
        self.view.turn_on_bot_button.setHidden(on)
        self.view.turn_off_bot_button.setHidden(not on)

    def remove_selected_message(self):
        """Removes the selected message from the message list and deletes it from "message and reply.json"."""
        selected_messages = self.view.messages_list_widget.selectedIndexes()
        if selected_messages:
            selected_message = selected_messages[0]
            message_text = self.messages_model.data(selected_message)
            message = self.database.get_message(message_text)
            self.database.delete(message)
            data = self.messages_model.stringList()
            data.pop(selected_message.row())
            self.messages_model.setStringList(data)
            self.update_window_title()

    def confirm_remove_selected_message(self):
        """Asks the user if they want to remove the selected message."""
        if bool(self.view.messages_list_widget.selectedIndexes()):
            self.confirm_message_box(
                translate("MainWindow", "Remove message"),
                translate(
                    "MainWindow", "Are you sure you want to remove this message?"
                ),
                self.remove_selected_message,
            )

    def confirm_remove_messages(self):
        """Asks the user if they want to remove all messages."""
        self.confirm_message_box(
            translate("MainWindow", "Remove all messages"),
            translate("MainWindow", "Are you sure you want to remove all messages?"),
            self.remove_messages,
        )

    def confirm_message_box(self, title: str, text: str, callback):
        dialog = QConfirmMessageBox(title, text, self.view.window)
        dialog.accepted.connect(callback)
        dialog.exec()

    def remove_messages(self):
        """Removes all messages from the list."""
        self.messages_model.setStringList([])
        self.database.delete_messages()
        self.update_window_title()

    def load_data(self):
        """
        Loads all messages from the database and inserts them into the message list.
        """
        self.update_window_title()
        self.messages_model.setStringList(self.database.message_names())

    def file_dont_exists_message_box(self):
        self.information_message_box(
            translate("MainWindow", "Warning"),
            translate("MainWindow", "The file don't exists anymore."),
        )

    def accepted_edit_selected_message(
        self, old_message_name: str, new_message_name: str
    ):
        self.__get_list_item_message(old_message_name).setText(new_message_name)
        self.update_window_title()

    def accepted_new_message(self, message_name: str):
        data = self.messages_model.stringList()
        data.append(message_name)
        self.messages_model.setStringList(data)
        self.update_window_title()

    def turn_off_bot(self):
        self.bot_thread.close()
        self.view.turn_off_bot_button.setDisabled(True)

    def on_bot_thread_finished(self):
        self.view.turn_off_bot_button.setDisabled(False)
        self.update_bot_button()

    def close_event(self, event: QCloseEvent):
        if self.bot_thread.isRunning():
            self.turn_off_bot()
            self.view.window.setCursor(Qt.CursorShape.WaitCursor)
            self.bot_thread.quit()
            self.bot_thread.wait()
        event.accept()
