from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator


class TokenValidator(QRegularExpressionValidator):
    def __init__(self, parent):
        regex_pattern = (
            r"^[A-Za-z0-9\-_]{24,26}\.[A-Za-z0-9\-_]{6}\.[A-Za-z0-9\-_]{27,45}$"
        )

        regex = QRegularExpression(regex_pattern)

        super().__init__(regex, parent)
