from PySide6.QtCore import QCoreApplication, Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QFormLayout,
    QSpacerItem,
    QSizePolicy,
    QToolButton,
    QComboBox,
    QPlainTextEdit,
)
from qextrawidgets import QColorButton
from qextrawidgets.icons import QThemeResponsiveIcon

from widgets.channel_dialog import ChannelDialog


class GroupView(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowMaximizeButtonHint)
        self.setWindowIcon(QIcon("source/icons/window-icon.svg"))
        self.setMinimumSize(800, 600)
        self.resize(1000, 800)

        self.channel_pick_dialog = ChannelDialog()

        self._init_ui()
        self._init_layout()
        self.translate_ui()

    def _init_ui(self):
        self.welcome_message_label = QLabel()
        self.welcome_message_channel_label = QLabel()
        self.welcome_message_message_label = QLabel()

        self.welcome_message_channels = QComboBox()
        self.welcome_message_textedit = QPlainTextEdit()
        self.welcome_message_textedit.setMaximumHeight(300)
        self.welcome_message_pick_button = QToolButton()
        self.welcome_message_pick_button.setIcon(
            QThemeResponsiveIcon.fromAwesome("fa6s.list")
        )
        self.welcome_message_pick_button.setIconSize(QSize(19, 19))

        self.goodbye_message_label = QLabel()
        self.goodbye_message_channel_label = QLabel()
        self.goodbye_message_message_label = QLabel()

        self.goodbye_message_channels = QComboBox()
        self.goodbye_message_textedit = QPlainTextEdit()
        self.goodbye_message_textedit.setMaximumHeight(300)

        self.goodbye_message_pick_button = QToolButton()
        self.goodbye_message_pick_button.setIcon(
            QThemeResponsiveIcon.fromAwesome("fa6s.list")
        )
        self.goodbye_message_pick_button.setIconSize(QSize(19, 19))

        self.save_button = QColorButton("#3DCC61")
        self.save_button.setIcon(QThemeResponsiveIcon.fromAwesome("fa6s.floppy-disk"))

    def _init_layout(self):
        main_layout = QFormLayout()
        main_layout.addRow(self.welcome_message_label)

        welcome_message_channel_layout = QHBoxLayout()
        welcome_message_channel_layout.addWidget(
            self.welcome_message_channels, stretch=1
        )
        welcome_message_channel_layout.addWidget(self.welcome_message_pick_button)
        main_layout.addRow(
            self.welcome_message_channel_label, welcome_message_channel_layout
        )
        main_layout.addRow(
            self.welcome_message_message_label, self.welcome_message_textedit
        )

        main_layout.addRow(self.goodbye_message_label)

        goodbye_message_channel_layout = QHBoxLayout()
        goodbye_message_channel_layout.addWidget(
            self.goodbye_message_channels, stretch=1
        )
        goodbye_message_channel_layout.addWidget(self.goodbye_message_pick_button)
        main_layout.addRow(
            self.goodbye_message_channel_label, goodbye_message_channel_layout
        )
        main_layout.addRow(
            self.goodbye_message_message_label, self.goodbye_message_textedit
        )

        main_layout.addItem(
            QSpacerItem(
                0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
            )
        )
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(
            self.save_button, alignment=Qt.AlignmentFlag.AlignRight
        )
        main_layout.addItem(buttons_layout)
        self.setLayout(main_layout)

    def translate_ui(self):
        self.setWindowTitle(self.tr("Group Configuration"))
        self.welcome_message_label.setText(self.tr("Welcome message:"))
        self.welcome_message_channel_label.setText(self.tr("Channel:"))
        self.welcome_message_message_label.setText(self.tr("Message:"))

        self.goodbye_message_label.setText(self.tr("Goodbye message:"))
        self.goodbye_message_channel_label.setText(self.tr("Channel:"))
        self.goodbye_message_message_label.setText(self.tr("Message:"))

        self.save_button.setText(self.tr("Confirm and save"))
