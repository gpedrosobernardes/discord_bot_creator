import logging

from PySide6.QtCore import QCoreApplication
from PySide6.QtGui import QAction, QActionGroup
from PySide6.QtWidgets import QWidget, QMenu

translate = QCoreApplication.translate


class QLogLevelMenu(QMenu):
    def __init__(self, text: str, parent: QWidget):
        super().__init__(text, parent)

        self.action_group = QActionGroup(self)
        self.action_group.setExclusive(True)

        self.debug_level_action = QAction(
            translate("MainWindow", "Debug"),
            self,
            checkable=True,
        )
        self.debug_level_action.setObjectName(logging.getLevelName(logging.DEBUG))
        self.info_level_action = QAction(
            translate("MainWindow", "Info"),
            self,
            checkable=True,
        )
        self.info_level_action.setObjectName(logging.getLevelName(logging.INFO))
        self.warning_level_action = QAction(
            translate("MainWindow", "Warning"),
            self,
            checkable=True,
        )
        self.warning_level_action.setObjectName(logging.getLevelName(logging.WARNING))
        self.error_level_action = QAction(
            translate("MainWindow", "Error"),
            self,
            checkable=True,
        )
        self.error_level_action.setObjectName(logging.getLevelName(logging.ERROR))

        self.setup_actions()

    def setup_actions(self):
        log_level_actions = (
            self.debug_level_action,
            self.info_level_action,
            self.warning_level_action,
            self.error_level_action,
        )
        self.addActions(log_level_actions)
        for a in log_level_actions:
            self.action_group.addAction(a)
