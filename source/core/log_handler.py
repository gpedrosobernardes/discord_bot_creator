import logging
from typing import Optional

from PySide6.QtCore import QObject, Signal

from source.core.database import DatabaseController


class LogSignaler(QObject):
    """
    QObject dedicated solely to defining signals.
    Separating this avoids metaclass conflicts with logging.Handler.
    """

    # Signal: (Formatted Message, Log Level)
    log = Signal(str, int)


class LogHandler(logging.Handler):
    """
    Custom logging handler that delegates UI updates to a QObject bridge
    and persists logs to a database.
    """

    def __init__(self, database: Optional[DatabaseController] = None):
        """
        Initializes the LogHandler.

        Args:
            database (Optional[DatabaseController]): Controller for database operations.
        """
        super().__init__()
        self.database = database

        # Composition: The handler 'has a' signaler, it 'is not a' QObject.
        self.signaler = LogSignaler()

    def emit(self, record: logging.LogRecord) -> None:
        """
        Processes the log record. Overrides logging.Handler.emit.

        Args:
            record (logging.LogRecord): The log record to process.
        """
        # Formata a mensagem usando o Formatter configurado no Logger
        msg = self.format(record)

        # 1. Emite para a GUI (Thread-Safe via Qt Signal)
        # O .emit() aqui pertence ao objeto Signal, não ao QObject ou Handler
        self.signaler.log.emit(msg, record.levelno)

        # 2. Salva no Banco de Dados
        if self.database:
            try:
                self.database.new_log(record)
            except Exception:
                self.handleError(record)
