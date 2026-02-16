import typing
from enum import IntEnum

from PySide6.QtCore import (
    QCoreApplication,
    QModelIndex,
    QPersistentModelIndex,
    QPoint,
    QSettings,
    Qt,
    Slot,
)
from PySide6.QtGui import QAction, QKeySequence, QStandardItem, QStandardItemModel
from PySide6.QtSql import QSqlTableModel
from PySide6.QtWidgets import (
    QDataWidgetMapper,
    QListView,
    QMenu,
    QMessageBox,
    QTableView,
    QToolButton,
)
from qextrawidgets.core.utils import QTwemojiImageProvider
from qextrawidgets.gui.models import QEmojiPickerModel
from qextrawidgets.gui.proxys.decoration_role_proxy import QDecorationRoleProxyModel
from qextrawidgets.widgets.menus.emoji_picker_menu import QEmojiPickerMenu

from source.controllers.base import BaseController
from source.core.constants import (
    BoolComparator,
    BoolField,
    IntComparator,
    IntField,
    StrComparator,
    StrField,
)
from source.core.database import DatabaseController
from source.views.message import MessageView


class MessageWindowContext(IntEnum):
    NEW = 1
    EDIT = 2


class MessageController(BaseController[MessageView]):
    def __init__(
        self,
        message_model: QSqlTableModel,
        database: DatabaseController,
        user_settings: QSettings,
        emoji_picker_model: QEmojiPickerModel,
        message_id: int = None,
    ):
        super().__init__(MessageView())
        self.database = database
        self.model = message_model
        self.user_settings = user_settings
        self.message_id = message_id

        # Determine Context
        self.context = MessageWindowContext.EDIT
        if self.message_id is None:
            self.context = MessageWindowContext.NEW
            self.message_id = self._create_new_message_row()

        # Proxys
        self.reactions_proxy = QDecorationRoleProxyModel()

        # Models
        self.reactions_model = database.get_message_reactions_model()
        self.reply_model = database.get_message_replies_model()
        self.conditions_model = database.get_message_conditions_model()

        # Helper Models
        self._str_comparator_model = QStandardItemModel()
        self._int_comparator_model = QStandardItemModel()
        self._bool_comparator_model = QStandardItemModel()

        # View

        self.emoji_picker_model = emoji_picker_model

        # Initial State
        self._setup_actions()
        self._setup_models()
        self._setup_emoji_picker_menu()
        self._setup_connections()
        self._setup_data_mapper()

        self.translate_ui()
        self.on_condition_field_changed()

        if self.context == MessageWindowContext.NEW:
            self.view.name_line_edit.setText(self.tr("New message"))
            # Do not submit immediately for new messages
            # self.data_mapper.submit()

    def _create_new_message_row(self) -> int:
        row = self.model.rowCount()
        self.model.insertRow(row)
        id_field = self.model.fieldIndex("id")
        self.model.setData(self.model.index(row, id_field), row)
        return row

    def _setup_models(self):
        # Reactions
        self.reactions_model.setFilter(f"message_id = {self.message_id}")
        self.reactions_model.select()
        self.reactions_proxy.setSourceModel(self.reactions_model)
        self.view.reactions_grid.setModel(self.reactions_proxy)

        # Replies
        self.reply_model.setFilter(f"message_id = {self.message_id}")
        self.reply_model.select()
        self.view.listbox_replies.set_model(self.reply_model)
        self.view.listbox_replies.set_model_column(self.reply_model.fieldIndex("text"))

        # Conditions
        self.conditions_model.setFilter(f"message_id = {self.message_id}")
        self.conditions_model.select()
        self.view.listbox_conditions.set_model(self.conditions_model)
        self.view.listbox_conditions.set_column_hidden(
            self.conditions_model.fieldIndex("id"), True
        )
        self.view.listbox_conditions.set_column_hidden(
            self.conditions_model.fieldIndex("message_id"), True
        )

    def _setup_actions(self):
        # Replies Actions
        self.delete_replies_action = self._create_action(
            QKeySequence.StandardKey.Delete, self.on_delete_replies
        )
        self.clear_replies_action = self._create_action(
            Qt.KeyboardModifier.ControlModifier | Qt.Key.Key_Delete,
            self.on_clear_replies,
        )
        self.view.listbox_replies.add_list_view_action(self.delete_replies_action)
        self.view.listbox_replies.add_list_view_action(self.clear_replies_action)

        # Reactions Actions
        self.delete_reactions_action = self._create_action(
            QKeySequence.StandardKey.Delete, self.on_delete_reactions
        )
        self.clear_reactions_action = self._create_action(
            Qt.KeyboardModifier.ControlModifier | Qt.Key.Key_Delete,
            self.on_clear_reactions,
        )
        self.view.reactions_grid.addAction(self.delete_reactions_action)
        self.view.reactions_grid.addAction(self.clear_reactions_action)

        # Conditions Actions
        self.delete_conditions_action = self._create_action(
            QKeySequence.StandardKey.Delete, self.on_delete_conditions
        )
        self.clear_conditions_action = self._create_action(
            Qt.KeyboardModifier.ControlModifier | Qt.Key.Key_Delete,
            self.on_clear_conditions,
        )
        self.view.listbox_conditions.add_action(self.delete_conditions_action)
        self.view.listbox_conditions.add_action(self.clear_conditions_action)

    @staticmethod
    def _create_action(shortcut, slot):
        action = QAction(
            shortcut=shortcut, shortcutContext=Qt.ShortcutContext.WidgetShortcut
        )
        action.triggered.connect(slot)
        return action

    def _setup_connections(self):
        # Main Window
        self.view.confirm_button.clicked.connect(self.validate)
        self.view.accepted.connect(self.on_accepted)
        self.view.cancel_button.clicked.connect(self.view.reject)
        self.view.rejected.connect(self.on_rejected)

        # Replies
        self.view.listbox_replies.add_button_pressed.connect(self.add_reply)
        self.view.listbox_replies.customContextMenuRequested.connect(
            self._show_replies_menu
        )

        # Reactions
        self.view.reactions_grid.customContextMenuRequested.connect(
            self._show_reactions_menu
        )

        # Conditions
        self.view.listbox_conditions.add_button_pressed.connect(self.add_condition)
        self.view.listbox_conditions.current_field_index_changed.connect(
            self.on_condition_field_changed
        )
        self.view.listbox_conditions.customContextMenuRequested.connect(
            self._show_conditions_menu
        )

        # Emoji Picker Menus
        self.reply_emoji_picker_menu.picked.connect(
            lambda emoji_item: self.view.listbox_replies.insert_text(
                emoji_item.coloredEmojiChar().char
            )
        )
        self.reaction_emoji_picker_menu.picked.connect(
            lambda emoji_item: self.add_reaction(emoji_item.coloredEmojiChar().char)
        )

        # Request Image
        reactions_grid_delegate = self.view.reactions_grid.itemDelegate()
        reactions_grid_delegate.requestImage.connect(self._on_request_reaction_image)

    def _setup_data_mapper(self):
        self.data_mapper = QDataWidgetMapper()
        self.data_mapper.setModel(self.model)
        self.data_mapper.setSubmitPolicy(QDataWidgetMapper.SubmitPolicy.ManualSubmit)
        self.data_mapper.addMapping(
            self.view.name_line_edit, self.model.fieldIndex("name")
        )
        self.data_mapper.addMapping(
            self.view.action_combobox, self.model.fieldIndex("action"), b"currentIndex"
        )
        self.data_mapper.addMapping(
            self.view.punishment_combobox,
            self.model.fieldIndex("punishment"),
            b"currentIndex",
        )
        self.data_mapper.addMapping(
            self.view.where_reply_combobox,
            self.model.fieldIndex("where_reply"),
            b"currentIndex",
        )
        self.data_mapper.addMapping(
            self.view.where_react_combobox,
            self.model.fieldIndex("where_reaction"),
            b"currentIndex",
        )
        self.data_mapper.addMapping(
            self.view.delay_spin_box, self.model.fieldIndex("delay")
        )
        self.data_mapper.setCurrentIndex(self.message_id)

    def _setup_emoji_picker_menu(self):
        self.reply_emoji_picker_menu = QEmojiPickerMenu(
            self.view, self.emoji_picker_model
        )
        self.view.listbox_replies.set_emoji_button_menu(self.reply_emoji_picker_menu)

        self.reaction_emoji_picker_menu = QEmojiPickerMenu(
            self.view, self.emoji_picker_model
        )
        self.view.add_reaction_button.setMenu(self.reaction_emoji_picker_menu)
        self.view.add_reaction_button.setPopupMode(
            QToolButton.ToolButtonPopupMode.InstantPopup
        )

    def translate_ui(self):
        self.view.translate_ui()
        self.conditions_model.translate()

        # Actions Text
        self.delete_replies_action.setText(self.tr("Delete selected replie(s)"))
        self.clear_replies_action.setText(self.tr("Clear all replies"))
        self.delete_reactions_action.setText(self.tr("Delete selected reaction(s)"))
        self.clear_reactions_action.setText(self.tr("Clear all reactions"))
        self.delete_conditions_action.setText(self.tr("Delete selected condition(s)"))
        self.clear_conditions_action.setText(self.tr("Clear all conditions"))

        # Populate Condition Fields
        self._populate_condition_fields()
        self._populate_comparator_models()

    def _populate_condition_fields(self):
        self.view.listbox_conditions.clear_fields()
        for field in StrField:
            self.view.listbox_conditions.add_field_item(
                QCoreApplication.translate("StrField", field.value), field.value
            )
        for field in IntField:
            self.view.listbox_conditions.add_field_item(
                QCoreApplication.translate("IntField", field.value), field.value
            )
        for field in BoolField:
            self.view.listbox_conditions.add_field_item(
                QCoreApplication.translate("BoolField", field.value), field.value
            )

    def _populate_comparator_models(self):
        self._str_comparator_model.clear()
        for comparator in StrComparator:
            item = QStandardItem(
                QCoreApplication.translate("StrComparator", comparator.value)
            )
            item.setData(comparator.value, Qt.ItemDataRole.UserRole)
            self._str_comparator_model.appendRow(item)

        self._int_comparator_model.clear()
        for comparator in IntComparator:
            item = QStandardItem(
                QCoreApplication.translate("IntComparator", comparator.value)
            )
            item.setData(comparator.value, Qt.ItemDataRole.UserRole)
            self._int_comparator_model.appendRow(item)

        self._bool_comparator_model.clear()
        for comparator in BoolComparator:
            item = QStandardItem(
                QCoreApplication.translate("BoolComparator", comparator.value)
            )
            item.setData(comparator.value, Qt.ItemDataRole.UserRole)
            self._bool_comparator_model.appendRow(item)

    # --- Generic Helpers ---

    @staticmethod
    def _delete_selected_rows(
        model: QSqlTableModel,
        selected_indexes: typing.List[QModelIndex],
        view_widget: typing.Union[QListView, QTableView],
    ):
        rows = sorted(set(index.row() for index in selected_indexes), reverse=True)
        for row in rows:
            result = model.removeRow(row)
            if result:
                view_widget.setRowHidden(row, True)
            else:
                print(f"Erro do modelo: {model.lastError().text()}")

    @staticmethod
    def _has_visible_rows(view: typing.Union[QListView, QTableView]) -> bool:
        model = view.model()
        if not model:
            return False
        for row in range(model.rowCount()):
            if not view.isRowHidden(row):
                return True
        return False

    def _confirm_deletion(self, title: str, text: str) -> bool:
        if not self.user_settings.value("confirm_actions", type=bool):
            return True

        reply = QMessageBox.question(
            self.view,
            title,
            text,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        return reply == QMessageBox.StandardButton.Yes

    # --- Replies Logic ---

    def add_reply(self):
        text = self.view.listbox_replies.get_text()
        if not text:
            return
        record = self.reply_model.record()
        record.setValue("text", text)
        record.setValue("message_id", self.message_id)
        if self.reply_model.insertRecord(-1, record):
            self.view.listbox_replies.clear_text()

    def on_delete_replies(self):
        self._delete_selected_rows(
            self.reply_model,
            self.view.listbox_replies.list_view_selected_indexes(),
            self.view.listbox_replies.list_view(),
        )

    def on_clear_replies(self):
        if self._confirm_deletion(
            self.tr("Clear replies"),
            self.tr("Are you sure you want to delete all replies?"),
        ):
            self.view.listbox_replies.select_all()
            self.on_delete_replies()

    def _show_replies_menu(self, position: QPoint):
        list_view = self.view.listbox_replies.list_view()
        index = list_view.indexAt(position)

        menu = QMenu(self.view)
        if index.isValid() and list_view.selectionModel().isSelected(index):
            menu.addAction(self.delete_replies_action)

        if self._has_visible_rows(list_view):
            menu.addAction(self.clear_replies_action)

        menu.exec(list_view.mapToGlobal(position))

    # --- Reactions Logic ---

    def add_reaction(self, emoji: str):
        reaction_idx = self.reactions_model.fieldIndex("reaction")
        start_index = self.reactions_model.index(0, reaction_idx)
        match_list = self.reactions_model.match(
            start_index,
            Qt.ItemDataRole.EditRole,
            emoji,
            1,
            Qt.MatchFlag.MatchExactly,
        )

        if match_list:
            source_index = match_list[0]
            sibling_index = self.reactions_model.index(source_index.row(), 0)
            if sibling_index.isValid():
                self.view.reactions_grid.setCurrentIndex(sibling_index)
            return

        if self.reactions_model.rowCount() >= 20:
            self._show_error(self.tr("The maximum number of reactions is 20."))
            return

        record = self.reactions_model.record()
        record.setValue("reaction", emoji)
        record.setValue("message_id", self.message_id)
        if self.reactions_model.insertRecord(-1, record):
            pass
            # self.reactions_model.select() # Removed auto-select

    def on_delete_reactions(self):
        self._delete_selected_rows(
            self.reactions_model,
            self.view.reactions_grid.selectedIndexes(),
            self.view.reactions_grid,
        )

    def on_clear_reactions(self):
        if self._confirm_deletion(
            self.tr("Clear reactions"),
            self.tr("Are you sure you want to delete all reactions?"),
        ):
            self.view.reactions_grid.selectAll()
            self.on_delete_reactions()

    def _show_reactions_menu(self, position: QPoint):
        index = self.view.reactions_grid.indexAt(position)

        menu = QMenu(self.view)
        if index.isValid() and self.view.reactions_grid.selectionModel().isSelected(
            index
        ):
            menu.addAction(self.delete_reactions_action)

        if self._has_visible_rows(self.view.reactions_grid):
            menu.addAction(self.clear_reactions_action)

        menu.exec(self.view.reactions_grid.mapToGlobal(position))

    @Slot(QPersistentModelIndex)
    def _on_request_reaction_image(self, persistent_index: QPersistentModelIndex):
        index = self.reactions_proxy.mapToSource(persistent_index)
        if not index.isValid():
            return

        emoji_index = self.reactions_model.fieldIndex("reaction")
        sibling_index = self.reactions_model.index(index.row(), emoji_index)

        emoji = self.reactions_model.data(sibling_index, Qt.ItemDataRole.EditRole)
        emoji_pixmap = QTwemojiImageProvider.getPixmap(emoji, 0, 100)
        self.reactions_proxy.setData(
            persistent_index, emoji_pixmap, Qt.ItemDataRole.DecorationRole
        )

    # --- Conditions Logic ---

    def add_condition(self):
        value = self.view.listbox_conditions.get_value_data()
        if not value:
            return

        record = self.conditions_model.record()
        record.setValue("field", self.view.listbox_conditions.get_field_data())
        record.setValue(
            "comparator", self.view.listbox_conditions.get_comparator_data()
        )
        record.setValue("value", value)
        record.setValue(
            "case_insensitive", self.view.listbox_conditions.get_case_insensitive_data()
        )
        record.setValue(
            "reverse_comparator",
            self.view.listbox_conditions.get_reverse_comparator_data(),
        )
        record.setValue("message_id", self.message_id)

        if self.conditions_model.insertRecord(-1, record):
            self.view.listbox_conditions.reset_fields()
            # self.conditions_model.select() # Removed auto-select

    def on_delete_conditions(self):
        self._delete_selected_rows(
            self.conditions_model,
            self.view.listbox_conditions.selected_indexes(),
            self.view.listbox_conditions.table_view(),
        )

    def on_clear_conditions(self):
        if self._confirm_deletion(
            self.tr("Clear conditions"),
            self.tr("Are you sure you want to delete all conditions?"),
        ):
            self.view.listbox_conditions.select_all()
            self.on_delete_conditions()

    def on_condition_field_changed(self):
        field = self.view.listbox_conditions.get_field_data()
        if field in [f.value for f in StrField]:
            self.view.listbox_conditions.set_comparator_model(
                self._str_comparator_model
            )
            self.view.listbox_conditions.set_case_insensitive_disabled(False)
            self.view.listbox_conditions.set_value_input_mode(is_boolean=False)
        elif field in [f.value for f in IntField]:
            self.view.listbox_conditions.set_comparator_model(
                self._int_comparator_model
            )
            self.view.listbox_conditions.set_case_insensitive_disabled(True)
            self.view.listbox_conditions.set_value_input_mode(is_boolean=False)
        elif field in [f.value for f in BoolField]:
            self.view.listbox_conditions.set_comparator_model(
                self._bool_comparator_model
            )
            self.view.listbox_conditions.set_case_insensitive_disabled(True)
            self.view.listbox_conditions.set_value_input_mode(is_boolean=True)

    def _show_conditions_menu(self, position: QPoint):
        table_view = self.view.listbox_conditions.table_view()
        index = table_view.indexAt(position)

        menu = QMenu(self.view)
        if index.isValid() and table_view.selectionModel().isSelected(index):
            menu.addAction(self.delete_conditions_action)

        if self._has_visible_rows(table_view):
            menu.addAction(self.clear_conditions_action)

        menu.exec(self.view.listbox_conditions.map_to_global(position))

    # --- Validation & Form ---

    def validate(self):
        name_edit = self.view.name_line_edit
        if not name_edit.text():
            self._show_error(self.tr("Empty name"))
            name_edit.setFocus()
        elif not name_edit.hasAcceptableInput():
            self._show_error(self.tr("Invalid name"))
            name_edit.setFocus()
        elif not self._has_visible_rows(self.view.listbox_conditions.table_view()):
            self._show_error(self.tr("You must add at least one condition."))
        else:
            self.view.accept()

    def _show_error(self, message: str):
        QMessageBox.warning(self.view, self.tr("Error"), message)

    def on_accepted(self):
        # Submit all changes manually
        self.data_mapper.submit()
        self.model.submitAll()
        self.reactions_model.submitAll()
        self.reply_model.submitAll()
        self.conditions_model.submitAll()

    def on_rejected(self):
        self.data_mapper.revert()
        self.model.revertAll()
        self.reactions_model.revertAll()
        self.reply_model.revertAll()
        self.conditions_model.revertAll()

        if self.context == MessageWindowContext.NEW:
            # For new messages, we might need to remove the row if it was inserted but not committed
            # However, since we are using OnManualSubmit, revertAll should handle it if it wasn't submitted.
            # But if we inserted it into the model, we might need to remove it explicitly if revertAll doesn't catch it.
            # Given the previous logic, let's keep the explicit removal just in case,
            # but usually revertAll is enough for OnManualSubmit.
            # Actually, if we inserted a row and didn't submit, it's just in the cache.
            pass
