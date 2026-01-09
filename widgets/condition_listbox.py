from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QStandardItemModel
from PySide6.QtWidgets import (
    QTableWidget,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QToolButton,
    QComboBox,
)
from qextrawidgets.icons import QThemeResponsiveIcon

from core.constants import StrField, IntField


def translate(text):
    return text


class QConditionListbox(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._table_view = QTableWidget()
        self._table_view.verticalHeader().setVisible(False)
        self._table_view.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self._table_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

        self._field_combobox = QComboBox()
        self._operator_combobox = QComboBox()

        self._field_translations = {
            StrField.MESSAGE: translate("Message"),
            StrField.AUTHOR_NAME: translate("Author name"),
            StrField.CHANNEL_NAME: translate("Channel name"),
            StrField.GUILD_NAME: translate("Guild name"),
            IntField.MENTIONS_TO_BOT: translate("Mentions to bot"),
            IntField.MENTIONS: translate("Mentions"),
            IntField.BOT_AUTHOR: translate("Bot author"),
            IntField.EMOJIS: translate("Emojis"),
        }

        self._case_insensitive_tool_button = QToolButton()
        self._case_insensitive_tool_button.setIcon(
            QThemeResponsiveIcon.fromAwesome("fa6s.font")
        )
        self._case_insensitive_tool_button.setIconSize(QSize(20, 20))

        self._value_combo_box = QComboBox()
        self._value_combo_box.setEditable(True)

        self._add_button = QToolButton()
        self._add_button.setIcon(QThemeResponsiveIcon.fromAwesome("fa6s.arrow-right"))
        self._add_button.setIconSize(QSize(20, 20))

        self.addButtonPressed = self._add_button.pressed
        self.currentFieldIndexChanged = self._field_combobox.currentIndexChanged

        self._setup_layout()
        self.translate_ui()

    def _setup_layout(self):
        fields_layout = QHBoxLayout()
        fields_layout.addWidget(self._field_combobox, stretch=1)
        fields_layout.addWidget(self._operator_combobox, stretch=1)
        fields_layout.addWidget(self._case_insensitive_tool_button)
        fields_layout.addWidget(self._value_combo_box, stretch=1)
        fields_layout.addWidget(self._add_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self._table_view)
        main_layout.addLayout(fields_layout)

        self.setLayout(main_layout)

    def translate_ui(self):
        self._case_insensitive_tool_button.setToolTip(self.tr("Case insensitive"))

    def set_field_model(self, model: QStandardItemModel):
        self._field_combobox.setModel(model)

    def set_operator_model(self, model: QStandardItemModel):
        self._operator_combobox.setModel(model)

    def set_add_button_disabled(self, disabled: bool):
        self._add_button.setDisabled(disabled)

    def is_add_button_enabled(self) -> bool:
        return self._add_button.isEnabled()
