from typing import Generic, TypeVar, Optional, Callable

from PySide6.QtCore import QCoreApplication, QEvent, QObject
from PySide6.QtGui import QAction, QKeySequence, Qt
from PySide6.QtWidgets import QWidget
from qextrawidgets.gui.icons import QThemeResponsiveIcon

T = TypeVar("T", bound=QWidget)


class BaseController(QObject, Generic[T]):
    """
    Base class for all controllers.
    Ensures that every controller has a typed 'view' property.
    """

    def __init__(self, view: T):
        super().__init__()
        self._view = view
        QCoreApplication.instance().installEventFilter(self)

    @property
    def view(self) -> T:
        """Returns the view associated with this controller."""
        return self._view

    def eventFilter(self, watched, event):
        # Verifica se o evento é LanguageChange e se ocorreu no App
        if watched == QCoreApplication.instance() and event.type() == QEvent.Type.LanguageChange:
            self.translate_ui()
            # Não retorne True aqui, ou você impede que o evento chegue nas janelas!

        return super().eventFilter(watched, event)

    def translate_ui(self):
        pass

    # Helpers
    def _create_action(
        self,
        icon_name: Optional[str] = None,
        shortcut: Optional[str] = None,
        triggered: Optional[Callable] = None,
        shortcut_context: Qt.ShortcutContext = Qt.ShortcutContext.WidgetShortcut,
    ) -> QAction:
        """Helper to create a QAction."""
        action = QAction(self._view)
        if icon_name:
            action.setIcon(QThemeResponsiveIcon.fromAwesome(icon_name))
        if shortcut:
            action.setShortcut(QKeySequence(shortcut))
            action.setShortcutContext(shortcut_context)
        if triggered:
            action.triggered.connect(triggered)
        return action