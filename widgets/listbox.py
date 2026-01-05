import typing

from PySide6.QtCore import Qt, QCoreApplication, QSize, QPoint
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QScrollArea,
    QToolButton,
    QListWidget,
    QMenu,
)
from qextrawidgets import QExtraTextEdit, QEmojiPicker
from qextrawidgets.icons import QThemeResponsiveIcon

translate = QCoreApplication.translate


class QListBox(QScrollArea):
    def __init__(self):
        super().__init__()
        self.list = QListWidget()
        self.list.setMinimumHeight(85)
        self.add_button = QToolButton()
        self.add_button.setIcon(QThemeResponsiveIcon.fromAwesome("fa6s.arrow-right"))
        self.add_button.setIconSize(QSize(20, 20))
        self.emote_button = QToolButton()
        self.emote_button.setIcon(QThemeResponsiveIcon.fromAwesome("fa6s.face-smile"))
        self.emote_button.setIconSize(QSize(20, 20))
        self.text_edit = QExtraTextEdit()

        self.emoji_picker_popup = QEmojiPicker()
        self.emoji_picker_popup.setContentsMargins(10, 10, 10, 10)
        self.emoji_picker_popup.setWindowFlags(
            Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint
        )
        self.emoji_picker_popup.setFixedSize(500, 500)

        self.__context_menu = QMenu()
        delete_action = QAction(translate("QListBox", "Remove"), self)
        delete_action.triggered.connect(self.delete_selected_items)
        self.__context_menu.addAction(delete_action)

        self.setWidgetResizable(True)

        self.setup_layout()
        self.setup_connections()

    def setup_connections(self):
        self.emote_button.pressed.connect(self.raise_emoji_picker)
        self.emoji_picker_popup.picked.connect(
            lambda emoji: self.text_edit.insertPlainText(emoji[1])
        )
        self.add_button.clicked.connect(self.on_add_button)

    def setup_layout(self):
        horizontal_layout = QHBoxLayout()
        horizontal_layout.addWidget(self.text_edit)
        horizontal_layout.addWidget(
            self.add_button, alignment=Qt.AlignmentFlag.AlignTop
        )
        horizontal_layout.addWidget(
            self.emote_button, alignment=Qt.AlignmentFlag.AlignTop
        )
        horizontal_layout.setStretch(0, True)
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        layout.addWidget(self.list)
        layout.addLayout(horizontal_layout)
        self.setWidget(content_widget)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Delete:
            for item in self.list.selectedItems():
                self.list.takeItem(self.list.row(item))
        else:
            super().keyPressEvent(event)

    def on_add_button(self):
        self.list.addItem(self.text_edit.toPlainText())
        self.text_edit.clear()

    def raise_emoji_picker(self):
        absolute_pos = self.emote_button.mapToGlobal(QPoint(-500, -500))
        self.emoji_picker_popup.move(absolute_pos)
        self.emoji_picker_popup.show()

    def is_selecting(self) -> bool:
        return bool(self.list.selectedItems())

    def get_items_text(self) -> typing.List[str]:
        return [self.list.item(i).text() for i in range(self.list.count())]

    def add_item(self, *args):
        # noinspection PyArgumentList
        self.list.addItem(*args)

    def contextMenuEvent(self, event):
        if self.is_selecting():
            self.__context_menu.exec(event.globalPos())

    def delete_selected_items(self):
        for item in self.list.selectedItems():
            self.list.takeItem(self.list.row(item))
