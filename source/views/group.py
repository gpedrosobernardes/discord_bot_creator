from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPalette
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QFormLayout,
    QSpacerItem,
    QSizePolicy,
    QComboBox,
    QPlainTextEdit,
    QCompleter,
    QVBoxLayout,
    QGroupBox,
    QPushButton,  # Importado QPushButton
)


class GroupView(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowMaximizeButtonHint)
        self.setWindowIcon(QIcon("assets/icons/window-icon.svg"))
        self.setMinimumSize(800, 600)
        self.resize(1000, 800)

        self._init_ui()
        self._init_layout()
        self.translate_ui()

    def _init_ui(self):
        # --- Welcome Section Widgets ---
        self.welcome_message_channel_label = QLabel()
        self.welcome_message_message_label = QLabel()

        self.welcome_info_label = QLabel()
        self._style_info_label(self.welcome_info_label)

        self.welcome_message_channels = QComboBox()
        self.welcome_message_channels.setEditable(True)
        self._setup_completer(self.welcome_message_channels)

        self.welcome_message_textedit = QPlainTextEdit()
        self.welcome_message_textedit.setMaximumHeight(200)

        # --- Goodbye Section Widgets ---
        self.goodbye_message_channel_label = QLabel()
        self.goodbye_message_message_label = QLabel()

        self.goodbye_info_label = QLabel()
        self._style_info_label(self.goodbye_info_label)

        self.goodbye_message_channels = QComboBox()
        self.goodbye_message_channels.setEditable(True)
        self._setup_completer(self.goodbye_message_channels)

        self.goodbye_message_textedit = QPlainTextEdit()
        self.goodbye_message_textedit.setMaximumHeight(200)

        # --- Footer Buttons (Alterado) ---
        # Botões simples sem ícones
        self.confirm_button = QPushButton()
        self.cancel_button = QPushButton()

    def _setup_completer(self, combobox: QComboBox):
        completer = combobox.completer()
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(Qt.MatchFlag.MatchContains)
        completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)

    def _style_info_label(self, label: QLabel):
        palette = label.palette()
        color = palette.color(QPalette.ColorRole.PlaceholderText)
        label.setStyleSheet(f"color: {color.name()}; font-size: 11px; margin-top: 2px;")

    def _init_layout(self):
        main_layout = QVBoxLayout()

        # --- Grupo 1: Boas-vindas ---
        self.welcome_group = QGroupBox()
        welcome_layout = QFormLayout()
        welcome_layout.addRow(self.welcome_message_channel_label, self.welcome_message_channels)
        welcome_layout.addRow(self.welcome_message_message_label, self.welcome_message_textedit)
        welcome_layout.addRow("", self.welcome_info_label)
        self.welcome_group.setLayout(welcome_layout)

        main_layout.addWidget(self.welcome_group)

        # --- Grupo 2: Despedida ---
        self.goodbye_group = QGroupBox()
        goodbye_layout = QFormLayout()
        goodbye_layout.addRow(self.goodbye_message_channel_label, self.goodbye_message_channels)
        goodbye_layout.addRow(self.goodbye_message_message_label, self.goodbye_message_textedit)
        goodbye_layout.addRow("", self.goodbye_info_label)
        self.goodbye_group.setLayout(goodbye_layout)

        main_layout.addWidget(self.goodbye_group)

        # Spacer
        main_layout.addItem(
            QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        )

        # --- Layout dos Botões ---
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch() # Empurra os botões para a direita
        buttons_layout.addWidget(self.cancel_button)  # Cancelar geralmente vem antes (ou à esquerda)
        buttons_layout.addWidget(self.confirm_button) # Confirmar como ação principal à direita

        main_layout.addLayout(buttons_layout)
        self.setLayout(main_layout)

    def translate_ui(self):
        self.setWindowTitle(self.tr("Group Configuration", "GroupView"))

        self.welcome_group.setTitle(self.tr("Welcome Settings", "GroupView"))
        self.welcome_message_channel_label.setText(self.tr("Channel:", "GroupView"))
        self.welcome_message_message_label.setText(self.tr("Message:", "GroupView"))
        self.welcome_info_label.setText(
            self.tr("Tip: You can use {member} to mention the user.", "GroupView")
        )

        self.goodbye_group.setTitle(self.tr("Goodbye Settings", "GroupView"))
        self.goodbye_message_channel_label.setText(self.tr("Channel:", "GroupView"))
        self.goodbye_message_message_label.setText(self.tr("Message:", "GroupView"))
        self.goodbye_info_label.setText(
            self.tr("Tip: You can use {member} to mention the user.", "GroupView")
        )

        # Texto dos novos botões
        self.confirm_button.setText(self.tr("Confirm", "GroupView"))
        self.cancel_button.setText(self.tr("Cancel", "GroupView"))