from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QWidget, QMessageBox

translate = QCoreApplication.translate


class QConfirmMessageBox(QMessageBox):
    def __init__(self, title: str, text: str, parent: QWidget):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setText(text)
        self.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        self.button(QMessageBox.StandardButton.Yes).setText(translate("MainWindow", "Yes"))
        self.button(QMessageBox.StandardButton.No).setText(translate("MainWindow", "No"))
