from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtSql import QSqlTableModel
from PySide6.QtWidgets import (
    QTableWidget,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QToolButton,
    QComboBox,
    QLineEdit,
    QTableView,
    QHeaderView,
    QAbstractItemView,
)
from qextrawidgets.icons import QThemeResponsiveIcon

from source.core.constants import StrField, IntField, BoolField, StrComparator, IntComparator, BoolComparator
from source.qt.delegates.boolean import BooleanDelegate
from source.qt.delegates.translation import TranslationDelegate


class QConditionForm(QWidget):
    customContextMenuRequested = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._table_view = QTableView()

        self._table_view.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self._table_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self._table_view.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self._table_view.verticalHeader().hide()
        self._table_view.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        icon_size = QSize(20, 20)

        self._field_combobox = QComboBox()

        self._reverse_comparator_tool_button = QToolButton()
        self._reverse_comparator_tool_button.setIcon(
            QThemeResponsiveIcon.fromAwesome("fa6s.exclamation")
        )
        self._reverse_comparator_tool_button.setCheckable(True)
        self._reverse_comparator_tool_button.setIconSize(icon_size)

        self._comparator_combobox = QComboBox()

        self._case_insensitive_tool_button = QToolButton()
        self._case_insensitive_tool_button.setIcon(
            QThemeResponsiveIcon.fromAwesome("fa6s.font")
        )
        self._case_insensitive_tool_button.setCheckable(True)
        self._case_insensitive_tool_button.setIconSize(icon_size)

        self._value_line_edit = QLineEdit()
        self._value_combobox = QComboBox()
        self._value_combobox.setVisible(False)
        self._value_combobox.addItems(["True", "False"])

        self._add_button = QToolButton()
        self._add_button.setIcon(QThemeResponsiveIcon.fromAwesome("fa6s.arrow-right"))
        self._add_button.setIconSize(icon_size)

        self.add_button_pressed = self._add_button.clicked
        self.current_field_index_changed = self._field_combobox.currentIndexChanged

        self._boolean_delegate = None
        self._field_delegate = None
        self._comparator_delegate = None

        self._setup_layout()
        self._setup_connections()

    def _setup_layout(self):
        fields_layout = QHBoxLayout()
        fields_layout.addWidget(self._field_combobox, stretch=1)
        fields_layout.addWidget(self._reverse_comparator_tool_button)
        fields_layout.addWidget(self._comparator_combobox, stretch=1)
        fields_layout.addWidget(self._case_insensitive_tool_button)
        fields_layout.addWidget(self._value_line_edit, stretch=1)
        fields_layout.addWidget(self._value_combobox, stretch=1)
        fields_layout.addWidget(self._add_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self._table_view)
        main_layout.addLayout(fields_layout)

        self.setLayout(main_layout)

    def _setup_connections(self):
        self._table_view.customContextMenuRequested.connect(
            self.customContextMenuRequested.emit
        )

    def translate_ui(self):
        self._reverse_comparator_tool_button.setToolTip(self.tr("Reverse comparator"))
        self._case_insensitive_tool_button.setToolTip(self.tr("Case insensitive"))
        self._value_combobox.setItemText(0, self.tr("True"))
        self._value_combobox.setItemText(1, self.tr("False"))

    def set_field_model(self, model):
        self._field_combobox.setModel(model)

    def clear_fields(self):
        self._field_combobox.clear()

    def add_field_item(self, text, data):
        self._field_combobox.addItem(text, data)

    def set_comparator_model(self, model):
        self._comparator_combobox.setModel(model)

    def set_model(self, model: QSqlTableModel):
        self._table_view.setModel(model)
        if model:
            # Boolean delegates
            self._boolean_delegate = BooleanDelegate(self._table_view)
            self._table_view.setItemDelegateForColumn(
                model.fieldIndex("case_insensitive"), self._boolean_delegate
            )
            self._table_view.setItemDelegateForColumn(
                model.fieldIndex("reverse_comparator"), self._boolean_delegate
            )

            # Translation delegates
            self._field_delegate = TranslationDelegate(
                self._table_view, [StrField, IntField, BoolField]
            )
            self._table_view.setItemDelegateForColumn(
                model.fieldIndex("field"), self._field_delegate
            )

            self._comparator_delegate = TranslationDelegate(
                self._table_view, [StrComparator, IntComparator, BoolComparator]
            )
            self._table_view.setItemDelegateForColumn(
                model.fieldIndex("comparator"), self._comparator_delegate
            )

    def set_add_button_disabled(self, disabled: bool):
        self._add_button.setDisabled(disabled)

    def set_case_insensitive_disabled(self, disabled: bool):
        self._case_insensitive_tool_button.setDisabled(disabled)

    def is_add_button_enabled(self) -> bool:
        return self._add_button.isEnabled()

    def get_field_data(self):
        return self._field_combobox.currentData()

    def get_comparator_data(self):
        return self._comparator_combobox.currentData()

    def get_value_data(self):
        if self._value_combobox.isVisible():
            # Return "1" for True and "0" for False to be consistent with DB storage if needed,
            # or just the string "True"/"False" if the validator handles it.
            # The validator handles "True"/"False" strings.
            # But let's check what the combobox has.
            # It has "True" and "False" items.
            # Let's return "True" or "False" string.
            return "True" if self._value_combobox.currentIndex() == 0 else "False"
        return self._value_line_edit.text()

    def get_case_insensitive_data(self):
        return self._case_insensitive_tool_button.isChecked()

    def get_reverse_comparator_data(self):
        return self._reverse_comparator_tool_button.isChecked()

    def set_column_hidden(self, column: int, hidden: bool):
        self._table_view.setColumnHidden(column, hidden)

    def reset_fields(self):
        self._field_combobox.setCurrentIndex(0)
        self._comparator_combobox.setCurrentIndex(0)
        self._value_line_edit.clear()
        self._value_combobox.setCurrentIndex(0)
        self._case_insensitive_tool_button.setChecked(False)
        self._reverse_comparator_tool_button.setChecked(False)

    def add_action(self, action):
        self._table_view.addAction(action)

    def selected_indexes(self):
        return self._table_view.selectionModel().selectedRows()

    def map_to_global(self, pos):
        return self._table_view.mapToGlobal(pos)

    def table_view(self) -> QTableView:
        return self._table_view

    def select_all(self):
        self._table_view.selectAll()

    def set_value_input_mode(self, is_boolean: bool):
        if is_boolean:
            self._value_line_edit.setVisible(False)
            self._value_combobox.setVisible(True)
        else:
            self._value_line_edit.setVisible(True)
            self._value_combobox.setVisible(False)
