from PySide6.QtCore import (
    Qt,
    QRegularExpression,
    QObject,
)
from PySide6.QtGui import (
    QIcon,
    QRegularExpressionValidator,
)
from PySide6.QtSql import QSqlTableModel
from PySide6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QDialog,
    QLabel,
    QPushButton,
    QLineEdit,
    QSpinBox,
    QComboBox,
)
from qextrawidgets import QAccordion, QEmojiPicker

from widgets.condition_listbox import QConditionListbox
from widgets.listbox import QListBox


class MessageView(QObject):
    def __init__(
        self,
        reaction_model: QSqlTableModel,
        reply_model: QSqlTableModel,
        emoji_picker: QEmojiPicker,
    ):
        super().__init__()

        self.window = QDialog()
        self.window.setWindowFlags(
            self.window.windowFlags() | Qt.WindowType.WindowMaximizeButtonHint
        )
        self.window.setWindowIcon(QIcon("source/icons/window-icon.svg"))
        self.window.setMinimumSize(800, 600)
        self.window.resize(1000, 800)

        # models

        # widgets

        self.name_text = QLabel()
        self.name_line_edit = QLineEdit()
        name_entry_validator = QRegularExpressionValidator(
            QRegularExpression(r"[A-zÀ-ú0-9 ]+")
        )
        self.name_line_edit.setMaxLength(40)
        self.name_line_edit.setValidator(name_entry_validator)
        self.listbox_conditions = QConditionListbox()
        self.listbox_reactions = QListBox(reaction_model, emoji_picker)
        self.listbox_replies = QListBox(reply_model, emoji_picker)
        self.collapse_group = QAccordion()
        self.collapse_group.addSection("", self.listbox_conditions)
        self.collapse_group.addSection(
            "",
            self.listbox_reactions,
        )
        self.collapse_group.addSection("", self.listbox_replies)
        self.collapse_group.expandAll(False)

        self.action_label = QLabel()
        self.action_combobox = QComboBox()

        self.punishment_label = QLabel()
        self.punishment_combobox = QComboBox()

        self.where_reply_label = QLabel()
        self.where_reply_combobox = QComboBox()

        self.where_react_label = QLabel()
        self.where_react_combobox = QComboBox()

        self.delay_label = QLabel()
        self.delay_spin_box = QSpinBox()
        self.confirm_button = QPushButton()
        self.setup_layout()
        self.translate_ui()

    def setup_layout(self):
        left_layout = QVBoxLayout()
        mid_layout = QVBoxLayout()
        right_layout = QVBoxLayout()
        left_layout.addWidget(self.collapse_group)
        left_layout.setSpacing(0)
        left_layout.setContentsMargins(0, 0, 0, 0)

        widgets = (
            self.action_label,
            self.action_combobox,
            self.punishment_label,
            self.punishment_combobox,
            self.where_reply_label,
            self.where_reply_combobox,
            self.where_react_label,
            self.where_react_combobox,
            self.delay_label,
            self.delay_spin_box,
        )

        for widget in widgets:
            right_layout.addWidget(widget)
        right_layout.addStretch()
        right_layout.addWidget(self.confirm_button)
        horizontal_layout = QHBoxLayout()
        horizontal_layout.addLayout(left_layout)
        horizontal_layout.addLayout(mid_layout)
        horizontal_layout.addLayout(right_layout)
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.name_text)
        vertical_layout.addWidget(self.name_line_edit)
        vertical_layout.addLayout(horizontal_layout)
        self.window.setLayout(vertical_layout)
        self.window.show()

    def translate_ui(self):
        self.window.setWindowTitle(self.tr("Message"))
        self.name_text.setText(self.tr("Name"))
        self.name_line_edit.setToolTip(
            self.tr("The name can include letters (with accents), numbers, and spaces.")
        )

        for i, text in enumerate(
            [self.tr("Conditions"), self.tr("Reactions"), self.tr("Replies")]
        ):
            self.collapse_group.setSectionTitle(i, text)

        self.action_label.setText(self.tr("Action"))

        for i, text in enumerate([self.tr("Pin"), self.tr("Delete"), self.tr("None")]):
            self.action_combobox.insertItem(i, text)

        self.punishment_label.setText(self.tr("Punishment"))

        for i, text in enumerate([self.tr("Kick"), self.tr("Ban"), self.tr("None")]):
            self.punishment_combobox.insertItem(i, text)

        self.where_reply_label.setText(self.tr("Where reply"))

        for i, text in enumerate(
            [self.tr("Group"), self.tr("Private"), self.tr("None")]
        ):
            self.where_reply_combobox.insertItem(i, text)

        self.where_react_label.setText(self.tr("Where react"))

        for i, text in enumerate([self.tr("Author"), self.tr("Bot"), self.tr("None")]):
            self.where_react_combobox.insertItem(i, text)

        self.delay_label.setText(self.tr("Delay"))
        self.confirm_button.setText(self.tr("Confirm"))

        # models
        # str_fields = (
        #     self.tr("Message"),
        #     self.tr("Author name"),
        #     self.tr("Channel name"),
        #     self.tr("Guild name"),
        # )
        # for row, field in enumerate(str_fields):
        #     index = self.str_fields.index(row, 0)
        #     self.str_fields.setData(index, field)

        # int_fields = (self.tr("Mentions to bot"), self.tr("Mentions"), self.tr("Bot author"), self.tr("Emojis"))
        #
