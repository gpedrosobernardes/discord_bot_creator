from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QMenu, QWidget, QVBoxLayout, QWidgetAction
from qextrawidgets import QEmojiPicker


class QEmojiPickerMenu(QMenu):
    emojiPicked = Signal(str)

    def __init__(self, parent=None, emoji_picker: QEmojiPicker = None):
        super().__init__(parent)
        self.emoji_picker = emoji_picker
        self._init_ui()

    def _init_ui(self):
        # Create a container widget
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        
        if self.emoji_picker:
            # Connect the signal
            self.emoji_picker.picked.connect(self._on_emoji_picked)
            layout.addWidget(self.emoji_picker)

        # Create the widget action
        widget_action = QWidgetAction(self)
        widget_action.setDefaultWidget(container)

        # Add to menu
        self.addAction(widget_action)

    def _on_emoji_picked(self, emoji: str):
        self.emojiPicked.emit(emoji)
        self.close()
