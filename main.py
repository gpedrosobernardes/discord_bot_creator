import logging
import sys

from PySide6.QtWidgets import QApplication

from interfaces.main.main import Main

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
        datefmt="%d/%m/%Y %H:%M:%S",
    )
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec())
