import logging
from datetime import datetime


class LogHandler(logging.Handler):
    def __init__(self, app):
        super().__init__()
        self.__app = app

    def emit(self, record: logging.LogRecord):
        self.__app.log(
            f"{datetime.fromtimestamp(record.created).strftime("%d/%m/%Y %H:%M:%S")} - {record.getMessage()}\n"
        )
