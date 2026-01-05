from PySide6.QtCore import (
    Qt,
    QCoreApplication,
    QRegularExpression,
)
from PySide6.QtGui import (
    QIcon,
    QRegularExpressionValidator,
)
from PySide6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QDialog,
    QLabel,
    QPushButton,
    QLineEdit,
    QSpinBox,
    QButtonGroup,
    QGroupBox,
)
from qextrawidgets import QColorButton, QAccordion, QEmojiPicker
from qextrawidgets.icons import QThemeResponsiveIcon

from widgets.condition_listbox import QConditionListbox
from widgets.custom_checkbox import QCustomRadioButton

from widgets.listbox import QListBox

translate = QCoreApplication.translate


class MessageView:
    def __init__(self):
        self.window = QDialog()
        self.window.setWindowFlags(
            self.window.windowFlags() | Qt.WindowType.WindowMaximizeButtonHint
        )
        self.window.setWindowIcon(QIcon("source/icons/window-icon.svg"))
        self.window.setMinimumSize(800, 600)
        self.window.resize(1000, 800)
        self.window.setWindowTitle(translate("MessageWindow", "Message"))

        self.name_text = QLabel()
        self.name_text.setText(translate("MessageWindow", "Name"))
        self.name_entry = QLineEdit()
        self.name_entry.setToolTip(
            translate(
                "MessageWindow",
                "The name can include letters (with accents), numbers, and spaces. Example: 'John123'.",
            )
        )
        name_entry_validator = QRegularExpressionValidator(
            QRegularExpression(r"[A-zÀ-ú0-9 ]*")
        )
        self.name_entry.setMaxLength(40)
        self.name_entry.setValidator(name_entry_validator)
        self.listbox_conditions = QConditionListbox()
        self.listbox_reactions = QListBox()
        self.listbox_replies = QListBox()
        self.collapse_group = QAccordion()
        self.collapse_group.addSection(
            translate("MessageWindow", "Conditions"), self.listbox_conditions
        )
        self.collapse_group.addSection(
            translate("MessageWindow", "Reactions"),
            self.listbox_reactions,
        )
        self.collapse_group.addSection(
            translate("MessageWindow", "Replies"), self.listbox_replies
        )

        self.group_pin_or_del = QGroupBox(translate("MessageWindow", "Action"))
        self.group_pin_or_del_layout = QVBoxLayout()
        self.group_pin_or_del.setLayout(self.group_pin_or_del_layout)
        self.pin_or_del_button_group = QButtonGroup(self.window)
        self.pin_or_del_button_group.setExclusive(True)
        self.pin_checkbox = QCustomRadioButton("pin", translate("MessageWindow", "Pin"))
        self.del_checkbox = QCustomRadioButton(
            "delete", translate("MessageWindow", "Delete")
        )
        self.none_action_checkbox = QCustomRadioButton(
            "none", translate("MessageWindow", "None")
        )
        self.none_action_checkbox.setChecked(True)
        self.pin_or_del_button_group.addButton(self.pin_checkbox)
        self.pin_or_del_button_group.addButton(self.del_checkbox)
        self.pin_or_del_button_group.addButton(self.none_action_checkbox)
        self.group_pin_or_del_layout.addWidget(self.pin_checkbox)
        self.group_pin_or_del_layout.addWidget(self.del_checkbox)
        self.group_pin_or_del_layout.addWidget(self.none_action_checkbox)

        self.group_kick_or_ban = QGroupBox(translate("MessageWindow", "Penalty"))
        self.group_kick_or_ban_layout = QVBoxLayout()
        self.group_kick_or_ban.setLayout(self.group_kick_or_ban_layout)
        self.kick_or_ban_button_group = QButtonGroup(self.window)
        self.kick_or_ban_button_group.setExclusive(True)
        self.kick_checkbox = QCustomRadioButton(
            "kick", translate("MessageWindow", "Kick")
        )
        self.ban_checkbox = QCustomRadioButton("ban", translate("MessageWindow", "Ban"))
        self.none_penalty_checkbox = QCustomRadioButton(
            "none", translate("MessageWindow", "None")
        )
        self.none_penalty_checkbox.setChecked(True)
        self.kick_or_ban_button_group.addButton(self.kick_checkbox)
        self.kick_or_ban_button_group.addButton(self.ban_checkbox)
        self.kick_or_ban_button_group.addButton(self.none_penalty_checkbox)
        self.group_kick_or_ban_layout.addWidget(self.kick_checkbox)
        self.group_kick_or_ban_layout.addWidget(self.ban_checkbox)
        self.group_kick_or_ban_layout.addWidget(self.none_penalty_checkbox)

        self.group_where_reply = QGroupBox(translate("MessageWindow", "Where reply"))
        self.group_where_reply_layout = QVBoxLayout()
        self.group_where_reply.setLayout(self.group_where_reply_layout)
        self.where_reply_button_group = QButtonGroup(self.window)
        self.where_reply_button_group.setExclusive(True)
        self.group_reply_checkbox = QCustomRadioButton(
            "group", translate("MessageWindow", "Group")
        )
        self.private_reply_checkbox = QCustomRadioButton(
            "private", translate("MessageWindow", "Private")
        )
        self.none_reply_checkbox = QCustomRadioButton(
            "none", translate("MessageWindow", "None")
        )
        self.none_reply_checkbox.setChecked(True)
        self.where_reply_button_group.addButton(self.group_reply_checkbox)
        self.where_reply_button_group.addButton(self.private_reply_checkbox)
        self.where_reply_button_group.addButton(self.none_reply_checkbox)
        self.group_where_reply_layout.addWidget(self.group_reply_checkbox)
        self.group_where_reply_layout.addWidget(self.private_reply_checkbox)
        self.group_where_reply_layout.addWidget(self.none_reply_checkbox)

        self.group_where_react = QGroupBox(translate("MessageWindow", "Where react"))
        self.group_where_react_layout = QVBoxLayout()
        self.group_where_react.setLayout(self.group_where_react_layout)
        self.where_react_button_group = QButtonGroup(self.window)
        self.where_react_button_group.setExclusive(True)
        self.author_checkbox = QCustomRadioButton(
            "author", translate("MessageWindow", "Author")
        )
        self.bot_checkbox = QCustomRadioButton("bot", translate("MessageWindow", "Bot"))
        self.none_react_checkbox = QCustomRadioButton(
            "none", translate("MessageWindow", "None")
        )
        self.none_react_checkbox.setChecked(True)
        self.where_react_button_group.addButton(self.author_checkbox)
        self.where_react_button_group.addButton(self.bot_checkbox)
        self.where_react_button_group.addButton(self.none_react_checkbox)
        self.group_where_react_layout.addWidget(self.author_checkbox)
        self.group_where_react_layout.addWidget(self.bot_checkbox)
        self.group_where_react_layout.addWidget(self.none_react_checkbox)

        self.delay_label = QLabel(translate("MessageWindow", "Delay"))
        self.delay = QSpinBox()
        self.confirm = QPushButton()
        self.confirm.setText(translate("MessageWindow", "Confirm"))
        self.confirm_and_save = QColorButton(
            translate("MessageWindow", "Confirm and save"),
            "#3DCC61",
            parent=self.window,
        )
        self.confirm_and_save.setAutoDefault(False)
        self.confirm_and_save.setDefault(False)
        self.confirm_and_save.setIcon(
            QThemeResponsiveIcon.fromAwesome("fa6s.floppy-disk")
        )
        self.setup_layout()

    def setup_layout(self):
        left_layout = QVBoxLayout()
        mid_layout = QVBoxLayout()
        right_layout = QVBoxLayout()
        left_layout.addWidget(self.collapse_group)
        left_layout.setSpacing(0)
        left_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.addWidget(self.group_pin_or_del)
        right_layout.addWidget(self.group_kick_or_ban)
        right_layout.addWidget(self.group_where_reply)
        right_layout.addWidget(self.group_where_react)
        for widget in (
            self.delay_label,
            self.delay,
        ):
            right_layout.addWidget(widget)
        right_layout.addStretch()
        right_layout.addWidget(self.confirm)
        right_layout.addWidget(self.confirm_and_save)
        horizontal_layout = QHBoxLayout()
        horizontal_layout.addLayout(left_layout)
        horizontal_layout.addLayout(mid_layout)
        horizontal_layout.addLayout(right_layout)
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.name_text)
        vertical_layout.addWidget(self.name_entry)
        vertical_layout.addLayout(horizontal_layout)
        self.window.setLayout(vertical_layout)
