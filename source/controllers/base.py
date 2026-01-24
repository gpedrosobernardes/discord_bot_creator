from typing import Generic, TypeVar

from PySide6.QtCore import QObject
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

    @property
    def view(self) -> T:
        """Returns the view associated with this controller."""
        return self._view
