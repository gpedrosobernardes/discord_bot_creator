from PySide6.QtCore import Qt, QSize, QPoint
from PySide6.QtGui import QAction, QValidator
from PySide6.QtSql import QSqlTableModel
from PySide6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QToolButton,
    QMenu,
    QListView,
)
from qextrawidgets import (
    QExtraTextEdit,
    QEmojiPicker,
    QStandardTwemojiDelegate,
    QTwemojiTextDocument,
)
from qextrawidgets.icons import QThemeResponsiveIcon


class QListBox(QWidget):
    def __init__(self, model: QSqlTableModel, emoji_picker: QEmojiPicker):
        super().__init__()

        self._list_view = QListView()
        self._list_view.setItemDelegate(QStandardTwemojiDelegate())
        self._list_view.setMinimumHeight(85)
        self._list_view.setModel(model)
        self._list_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

        self._add_button = QToolButton()
        self._add_button.setIcon(QThemeResponsiveIcon.fromAwesome("fa6s.arrow-right"))
        self._add_button.setIconSize(QSize(20, 20))

        self._emote_button = QToolButton()
        self._emote_button.setIcon(QThemeResponsiveIcon.fromAwesome("fa6s.face-smile"))
        self._emote_button.setIconSize(QSize(20, 20))

        self._text_edit = QExtraTextEdit()
        self._document: QTwemojiTextDocument = self._text_edit.document()
        self._document.setDevicePixelRatio(self.devicePixelRatio())

        self._emoji_picker = emoji_picker

        self._delete_action = QAction()
        self._delete_action.setShortcut("Delete")

        self.addButtonPressed = self._add_button.pressed

        self._setup_layout()
        self._setup_connections()
        self.translate_ui()

    def _setup_connections(self):
        self._emote_button.pressed.connect(self._show_emoji_picker)
        self._list_view.customContextMenuRequested.connect(self._on_context_menu)
        self._delete_action.triggered.connect(self._delete_selected_indexes)

    def _setup_layout(self):
        horizontal_layout = QHBoxLayout()
        horizontal_layout.addWidget(self._text_edit)
        horizontal_layout.addWidget(self._add_button, 0, Qt.AlignmentFlag.AlignTop)
        horizontal_layout.addWidget(self._emote_button, 0, Qt.AlignmentFlag.AlignTop)
        horizontal_layout.setStretch(0, True)

        layout = QVBoxLayout()
        layout.addWidget(self._list_view)
        layout.addLayout(horizontal_layout)

        self.setLayout(layout)

    def translate_ui(self):
        self._delete_action.setText(self.tr("Remove"))

    def _show_emoji_picker(self):
        absolute_pos = self._emote_button.mapToGlobal(QPoint(-500, -500))
        self._emoji_picker.move(absolute_pos)
        self._emoji_picker.picked.disconnect()
        self._emoji_picker.picked.connect(
            lambda emoji: self._text_edit.insertPlainText(emoji[1])
        )
        self._emoji_picker.show()

    def _delete_selected_indexes(self):
        indexes = self._list_view.selectedIndexes()
        rows = sorted(set(index.row() for index in indexes), reverse=True)
        model = self._list_view.model()
        for row in rows:
            model.removeRow(row)

    def _on_context_menu(self, position: QPoint):
        global_position = self._list_view.mapToGlobal(position)
        if self._list_view.selectedIndexes():
            context_menu = QMenu()
            context_menu.addAction(self._delete_action)
            context_menu.exec(global_position)

    def get_text(self) -> str:
        return self._document.toPlainText()

    def clear_text(self):
        self._document.clear()

    def set_model_column(self, index: int):
        self._list_view.setModelColumn(index)

    def set_text_validator(self, validator: QValidator):
        self._text_edit.setValidator(validator)

    def set_line_limit(self, line_limit: int):
        self._document.setLineLimit(line_limit)
