from typing import Generic, TypeVar

from PySide6.QtCore import QCoreApplication, QEvent, QObject
from PySide6.QtWidgets import QWidget

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
