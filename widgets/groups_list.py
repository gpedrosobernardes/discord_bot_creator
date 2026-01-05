from PySide6.QtCore import QPoint, Qt, QCoreApplication
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QAbstractItemView, QListView, QMenu

translate = QCoreApplication.translate


class QGroupsList(QListView):
    def __init__(self):
        super().__init__()

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.group_context_menu_event)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.config_action = QAction(translate("MainWindow", "Config group"), self)
        self.quit_action = QAction(translate("MainWindow", "Quit group"), self)

    def group_context_menu_event(self, position: QPoint):
        if bool(self.selectedIndexes()):
            context_menu = QMenu()
            context_menu.addAction(self.config_action)
            context_menu.addAction(self.quit_action)
            context_menu.exec(self.mapToGlobal(position))
