from typing import Dict, TypeVar, Generic, Optional, Any, List

from PySide6.QtWidgets import QWidget

from source.controllers.base import BaseController

T = TypeVar("T", bound=BaseController)


class ControllerManager(Generic[T]):
    """
    Manages multiple controller instances, ensuring uniqueness per key.
    """

    def __init__(self):
        self._controllers: Dict[Any, T] = {}

    def get(self, key: Any) -> Optional[T]:
        """Returns the controller for the given key if it exists."""
        return self._controllers.get(key)

    def get_all(self) -> List[T]:
        """Returns a list of all active controllers."""
        return list(self._controllers.values())

    def add(self, key: Any, controller: T, close_signal: Optional[Any] = None) -> bool:
        """
        Registers a controller.

        Args:
            key: Unique identifier for the controller context.
            controller: The controller instance.
            close_signal: Signal to connect to for automatic removal (e.g. window.destroyed).

        Returns:
            True if added, False if key already exists.
        """
        if key in self._controllers:
            return False

        self._controllers[key] = controller

        if close_signal:
            # Capture key in default argument to avoid closure issues
            close_signal.connect(lambda *args, k=key: self.remove(k))

        return True

    def remove(self, key: Any):
        """Removes the controller associated with the key."""
        if key in self._controllers:
            del self._controllers[key]

    def activate(self, key: Any):
        """Attempts to bring the controller's view to the front."""
        controller = self.get(key)
        if not controller:
            return

        # Since T is bound to BaseController, we know it has a 'view' property
        view = controller.view

        if isinstance(view, QWidget):
            view.show()
            view.activateWindow()
            view.raise_()
