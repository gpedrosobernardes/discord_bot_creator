from PySide6.QtCore import (
    Qt,
    QRegularExpression,
    QObject,
    QSize,
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
    QComboBox,
    QToolButton,
    QWidget,
)
from qextrawidgets import QAccordion
from qextrawidgets.icons import QThemeResponsiveIcon
from qextrawidgets.widgets.emoji_picker import QEmojiGrid

from core.constants import Actions, Punishment, WhereReply, WhereReact
from widgets.condition_form import QConditionForm
from widgets.reply_form import QReplyForm


class MessageView(QObject):
    def __init__(
        self,
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

        self.listbox_conditions = QConditionForm()

        # Reactions

        self.reactions_widget = QWidget()

        self.reactions_grid = QEmojiGrid(self.reactions_widget, 40, 0.2)
        self.reactions_grid.setSelectionMode(QEmojiGrid.SelectionMode.MultiSelection)

        self.add_reaction_button = QToolButton()
        self.add_reaction_button.setIcon(
            QThemeResponsiveIcon.fromAwesome("fa6s.face-smile")
        )
        self.add_reaction_button.setIconSize(QSize(20, 20))

        self.listbox_replies = QReplyForm()

        self.collapse_group = QAccordion()
        self.collapse_group.addSection("", self.listbox_conditions)
        self.collapse_group.addSection("", self.reactions_widget)
        self.collapse_group.addSection("", self.listbox_replies)
        self.collapse_group.expandAll(False)

        self.action_label = QLabel()
        self.action_combobox = QComboBox()
        self.action_combobox.insertItems(0, map(str, Actions))

        self.punishment_label = QLabel()
        self.punishment_combobox = QComboBox()
        self.punishment_combobox.insertItems(0, map(str, Punishment))

        self.where_reply_label = QLabel()
        self.where_reply_combobox = QComboBox()
        self.where_reply_combobox.insertItems(0, map(str, WhereReply))

        self.where_react_label = QLabel()
        self.where_react_combobox = QComboBox()
        self.where_react_combobox.insertItems(0, map(str, WhereReact))

        self.delay_label = QLabel()
        self.delay_spin_box = QSpinBox()
        self.confirm_button = QPushButton()
        self.setup_layout()

    def setup_layout(self):
        reactions_layout = QHBoxLayout()
        reactions_layout.addWidget(self.reactions_grid)
        reactions_layout.addWidget(self.add_reaction_button)
        self.reactions_widget.setLayout(reactions_layout)

        left_layout = QVBoxLayout()
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

        right_layout = QVBoxLayout()
        for widget in widgets:
            right_layout.addWidget(widget)
        right_layout.addStretch()
        right_layout.addWidget(self.confirm_button)

        horizontal_layout = QHBoxLayout()
        horizontal_layout.addLayout(left_layout)
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
            self.action_combobox.setItemText(i, text)

        self.punishment_label.setText(self.tr("Punishment"))

        for i, text in enumerate([self.tr("Kick"), self.tr("Ban"), self.tr("None")]):
            self.punishment_combobox.setItemText(i, text)

        self.where_reply_label.setText(self.tr("Where reply"))

        for i, text in enumerate(
            [
                self.tr("Group"),
                self.tr("Private"),
                self.tr("Same Channel"),
                self.tr("Both"),
                self.tr("None"),
            ]
        ):
            self.where_reply_combobox.setItemText(i, text)

        self.where_react_label.setText(self.tr("Where react"))

        for i, text in enumerate([self.tr("Author"), self.tr("Bot"), self.tr("None")]):
            self.where_react_combobox.setItemText(i, text)

        self.delay_label.setText(self.tr("Delay"))
        self.confirm_button.setText(self.tr("Confirm"))

        self.listbox_conditions.translate_ui()
