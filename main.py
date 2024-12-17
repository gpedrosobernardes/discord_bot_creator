import sys
from PySide6.QtWidgets import QApplication
from interfaces.main.main import Main


app = QApplication(sys.argv)
window = Main()
window.show()
sys.exit(app.exec())