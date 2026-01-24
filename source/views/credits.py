from PySide6.QtCore import QCoreApplication, QTranslator, QObject
from PySide6.QtGui import QIcon, QPixmap, Qt
from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout


class CreditsView(QObject):
    def __init__(self):
        super().__init__()
        self.window = QDialog()
        self.window.setFixedSize(400, 200)
        self.window.setWindowIcon(QIcon("assets/icons/window-icon.svg"))

        pixmap = QPixmap("assets/icons/icon.svg")
        self.logo_label = QLabel()
        self.logo_label.setPixmap(pixmap)

        self.credits_label = QLabel()

        self.setup_layout()
        self.translate_ui()

    def translate_ui(self):
        self.window.setWindowTitle(self.tr("Credits"))
        name = "Gustavo Pedroso Bernardes"
        self.credits_label.setText(self.tr("Developed by: {name}").format(name=name))

    def setup_layout(self):
        layout = QVBoxLayout()
        layout.addWidget(self.logo_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.credits_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.window.setLayout(layout)
