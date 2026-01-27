from PySide6.QtCore import QObject, Qt
from PySide6.QtGui import QIcon, QPixmap, QFont
from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout, QTabWidget, QWidget, QPlainTextEdit


class CreditsView(QObject):
    def __init__(self):
        super().__init__()
        self.window = QDialog()
        self.window.resize(600, 400)
        self.window.setWindowIcon(QIcon("assets/icons/window-icon.svg"))

        self._init_ui()
        self._init_layout()
        self.translate_ui()

    def _init_ui(self):
        # --- About Tab ---
        self.logo_label = QLabel()
        self.logo_label.setPixmap(QPixmap("assets/icons/icon.svg"))
        
        self.credits_label = QLabel()
        self.credits_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.about_tab = QWidget()

        # --- Licenses Tab ---
        self.licenses_text_edit = QPlainTextEdit()
        self.licenses_text_edit.setReadOnly(True)
        
        font = QFont("Courier New")
        font.setStyleHint(QFont.StyleHint.Monospace)
        self.licenses_text_edit.setFont(font)

        self.licenses_tab = QWidget()

        # --- Main Tabs ---
        self.tabs = QTabWidget()

    def _init_layout(self):
        # About Layout
        about_layout = QVBoxLayout()
        about_layout.addWidget(self.logo_label, alignment=Qt.AlignmentFlag.AlignCenter)
        about_layout.addWidget(self.credits_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.about_tab.setLayout(about_layout)

        # Licenses Layout
        licenses_layout = QVBoxLayout()
        licenses_layout.addWidget(self.licenses_text_edit)
        self.licenses_tab.setLayout(licenses_layout)

        # Main Layout
        self.tabs.addTab(self.about_tab, "")
        self.tabs.addTab(self.licenses_tab, "")

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        self.window.setLayout(main_layout)

    def translate_ui(self):
        self.window.setWindowTitle(self.tr("Credits"))
        
        name = "Gustavo Pedroso Bernardes"
        self.credits_label.setText(self.tr("Developed by: {name}").format(name=name))
        
        self.tabs.setTabText(0, self.tr("About"))
        self.tabs.setTabText(1, self.tr("Third Party Licenses"))

    def set_licenses(self, text: str):
        self.licenses_text_edit.setPlainText(text)
