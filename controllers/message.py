from enum import IntEnum

from PySide6.QtCore import Qt, QSettings, QStringListModel
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtSql import QSqlTableModel
from PySide6.QtWidgets import (
    QMessageBox,
    QDataWidgetMapper,
)
from qextrawidgets import QEmojiPicker, QEmojiValidator

from core.constants import StrField, IntField, StrComparator
from core.database import DatabaseController
from views.messages import MessageView


class MessageWindowContext(IntEnum):
    NEW = 1
    EDIT = 2


class MessageController:
    def __init__(
        self,
        message_model: QSqlTableModel,
        database: DatabaseController,
        settings: QSettings,
        index: int = None,
    ):
        self.model = message_model
        self.reactions_model = database.get_message_reactions_model()
        self.reply_model = database.get_message_replies_model()
        self.index = index
        self.context = MessageWindowContext.EDIT

        self.emoji_picker = QEmojiPicker()
        self.emoji_picker.setContentsMargins(10, 10, 10, 10)
        self.emoji_picker.setWindowFlags(
            Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint
        )
        self.emoji_picker.setFixedSize(500, 500)

        self.view = MessageView(
            self.reactions_model,
            self.reply_model,
            self.emoji_picker,
        )

        # self.view.listbox_conditions.set_field_model(self.str_fields_model)

        if index is None:
            self.index = self.model.rowCount()
            self.model.insertRow(self.index)
            id_field = self.model.fieldIndex("id")
            self.model.setData(self.model.index(self.index, id_field), self.index)
            self.context = MessageWindowContext.NEW
        self.data_mapper = self.create_data_mapper()
        if self.context == MessageWindowContext.NEW:
            self.view.name_line_edit.setText(self.view.tr("New message"))
            self.data_mapper.submit()

        self.setup_binds()
        self.setup_validators()
        self.setup_reactions_model()
        self.setup_replies_model()

    def setup_validators(self):
        self.view.listbox_reactions.set_text_validator(QEmojiValidator())
        self.view.listbox_reactions.set_line_limit(1)

    def setup_binds(self):
        self.view.confirm_button.clicked.connect(self.validate)
        self.view.window.accepted.connect(self.on_accepted)
        self.view.window.rejected.connect(self.on_rejected)

        self.view.listbox_reactions.addButtonPressed.connect(self.add_reaction)
        self.view.listbox_replies.addButtonPressed.connect(self.add_reply)

    def setup_reactions_model(self):
        self.reactions_model.setFilter(f"message_id = {self.index}")
        self.reactions_model.select()

        self.view.listbox_reactions.set_model_column(
            self.reactions_model.fieldIndex("reaction")
        )

    def setup_replies_model(self):
        self.reply_model.setFilter(f"message_id = {self.index}")
        self.reply_model.select()

        self.view.listbox_replies.set_model_column(self.reply_model.fieldIndex("text"))

    def add_reaction(self):
        text = self.view.listbox_reactions.get_text()
        if not text:
            return

        record = self.reactions_model.record()
        record.setValue("reaction", text)
        record.setValue("message_id", self.index)

        if self.reactions_model.insertRecord(-1, record):
            self.view.listbox_reactions.clear_text()
            self.reactions_model.setFilter(f"message_id = {self.index}")

    def add_reply(self):
        text = self.view.listbox_replies.get_text()
        if not text:
            return

        record = self.reply_model.record()
        record.setValue("text", text)
        record.setValue("message_id", self.index)

        if self.reply_model.insertRecord(-1, record):
            self.view.listbox_replies.clear_text()
            self.reply_model.setFilter(f"message_id = {self.index}")

    def create_data_mapper(self) -> QDataWidgetMapper:
        mapper = QDataWidgetMapper()
        mapper.setModel(self.model)
        mapper.setSubmitPolicy(QDataWidgetMapper.SubmitPolicy.ManualSubmit)
        mapper.addMapping(self.view.name_line_edit, self.model.fieldIndex("name"))
        mapper.addMapping(self.view.action_combobox, self.model.fieldIndex("action"))
        mapper.addMapping(
            self.view.punishment_combobox, self.model.fieldIndex("punishment")
        )
        mapper.addMapping(
            self.view.where_reply_combobox, self.model.fieldIndex("where_reply")
        )
        mapper.addMapping(
            self.view.where_react_combobox, self.model.fieldIndex("where_reaction")
        )
        mapper.addMapping(self.view.delay_spin_box, self.model.fieldIndex("delay"))
        mapper.setCurrentIndex(self.index)
        return mapper

    def validate(self):
        if not self.view.name_line_edit.text():
            window = self.view.window
            QMessageBox.warning(window, window.tr("Error"), window.tr("Empty name"))
            self.view.name_line_edit.setFocus()
        elif not self.view.name_line_edit.hasAcceptableInput():
            window = self.view.window
            QMessageBox.warning(window, window.tr("Error"), window.tr("Invalid name"))
            self.view.name_line_edit.setFocus()
        else:
            self.view.window.accept()

    def on_accepted(self):
        self.data_mapper.submit()

    def on_rejected(self):
        self.data_mapper.revert()
        if self.context == MessageWindowContext.NEW:
            self.model.removeRow(self.index)
