from PySide6.QtCore import Qt, QEvent
from PySide6.QtWidgets import QStyledItemDelegate, QStyleOptionViewItem


class BooleanDelegate(QStyledItemDelegate):
    # noinspection PyUnresolvedReferences
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)

        # Get value
        value = index.data(Qt.ItemDataRole.EditRole)
        checked = False
        try:
            checked = bool(int(value))
        except (ValueError, TypeError):
            pass

        # Configure option to show checkbox
        option.features |= QStyleOptionViewItem.ViewItemFeature.HasCheckIndicator
        option.checkState = (
            Qt.CheckState.Checked if checked else Qt.CheckState.Unchecked
        )
        option.features &= ~QStyleOptionViewItem.ViewItemFeature.HasDisplay  # Hide text
        option.text = ""
        option.displayAlignment = Qt.AlignmentFlag.AlignCenter

    def createEditor(self, parent, option, index):
        return None

    def editorEvent(self, event, model, option, index):
        if event.type() == QEvent.Type.MouseButtonRelease:
            # Toggle value
            value = index.data(Qt.ItemDataRole.EditRole)
            try:
                current_val = int(value)
            except (ValueError, TypeError):
                current_val = 0

            new_val = 1 if current_val == 0 else 0
            model.setData(index, new_val, Qt.ItemDataRole.EditRole)
            return True
        return False
