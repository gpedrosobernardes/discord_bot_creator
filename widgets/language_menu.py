from PySide6.QtGui import QActionGroup, QAction
from PySide6.QtWidgets import QMenu, QWidget


class QLanguageMenu(QMenu):
    def __init__(self, text: str, parent: QWidget):
        super().__init__(text, parent)

        self.action_group = QActionGroup(self)
        self.action_group.setExclusive(True)
        self.english = QAction("English", self, checkable=True)
        self.english.setObjectName("en_us")
        self.portuguese = QAction("Portuguese", self, checkable=True)
        self.portuguese.setObjectName("pt_br")
        self.setup_actions()

    def setup_actions(self):
        language_actions = (self.english, self.portuguese)
        for a in language_actions:
            self.action_group.addAction(a)
        self.addActions(language_actions)
