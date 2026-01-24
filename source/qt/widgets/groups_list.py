from PySide6.QtCore import Qt
from PySide6.QtWidgets import QAbstractItemView, QListView


class QGroupsList(QListView):
    def __init__(self):
        super().__init__()

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
