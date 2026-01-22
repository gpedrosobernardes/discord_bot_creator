from PySide6.QtCore import Qt, QSize, QPoint
from PySide6.QtGui import QValidator, QAction
from PySide6.QtSql import QSqlTableModel
from PySide6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QToolButton,
    QListView,
)
from qextrawidgets import (
    QExtraTextEdit,
)
from qextrawidgets.icons import QThemeResponsiveIcon


class QReplyForm(QWidget):
    def __init__(self):
        super().__init__()

        self._list_view = QListView()
        self._list_view.setMinimumHeight(85)
        self._list_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

        self._add_button = QToolButton()
        self._add_button.setIcon(QThemeResponsiveIcon.fromAwesome("fa6s.arrow-right"))
        self._add_button.setIconSize(QSize(20, 20))

        self._emote_button = QToolButton()
        self._emote_button.setIcon(QThemeResponsiveIcon.fromAwesome("fa6s.face-smile"))
        self._emote_button.setIconSize(QSize(20, 20))

        self._text_edit = QExtraTextEdit()

        self.addButtonPressed = self._add_button.pressed
        self.emoteButtonPressed = self._emote_button.pressed

        self._setup_layout()
        self._setup_connections()

    def _setup_connections(self):
        self._list_view.customContextMenuRequested.connect(
            self.customContextMenuRequested.emit
        )

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

    def get_text(self) -> str:
        return self._text_edit.toPlainText()

    def insert_text(self, text: str):
        self._text_edit.insertPlainText(text)

    def clear_text(self):
        self._text_edit.clear()

    def set_model_column(self, index: int):
        self._list_view.setModelColumn(index)

    def set_model(self, model: QSqlTableModel):
        self._list_view.setModel(model)

    def set_text_validator(self, validator: QValidator):
        self._text_edit.setValidator(validator)

    def emoji_button_position(self):
        return self._emote_button.mapToGlobal(QPoint(0, 0))

    def add_list_view_action(self, action: QAction):
        self._list_view.addAction(action)

    def list_view_selected_indexes(self):
        return self._list_view.selectedIndexes()
