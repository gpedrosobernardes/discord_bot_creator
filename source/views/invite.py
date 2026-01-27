from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QCheckBox,
    QLineEdit,
    QLabel,
    QDialogButtonBox,
    QGridLayout,
    QScrollArea,
    QWidget,
    QHBoxLayout,
    QPushButton,
)

import discord


class InviteDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("Generate Invite Link"))
        self.resize(500, 600)

        self._copy_clipboard = False

        self.client_id_edit = QLineEdit()
        self.client_id_edit.setPlaceholderText(self.tr("Client ID (Application ID)"))

        self.copy_btn = QPushButton(self.tr("Copy Link"))

        self.select_all_btn = QPushButton(self.tr("Select All"))
        self.deselect_all_btn = QPushButton(self.tr("Deselect All"))

        self.permissions_checks = {}
        self.permissions_layout = QGridLayout()

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        self.button_box.button(QDialogButtonBox.StandardButton.Ok).setText(self.tr("Open in Browser"))

        self._init_permissions()
        self._init_layout()
        self._init_connections()

    def _init_permissions(self):
        # List of permissions
        perms = [
            ("administrator", self.tr("Administrator")),
            ("manage_guild", self.tr("Manage Server")),
            ("manage_roles", self.tr("Manage Roles")),
            ("manage_channels", self.tr("Manage Channels")),
            ("kick_members", self.tr("Kick Members")),
            ("ban_members", self.tr("Ban Members")),
            ("create_instant_invite", self.tr("Create Invite")),
            ("change_nickname", self.tr("Change Nickname")),
            ("manage_nicknames", self.tr("Manage Nicknames")),
            ("manage_emojis", self.tr("Manage Emojis")),
            ("manage_webhooks", self.tr("Manage Webhooks")),
            ("view_audit_log", self.tr("View Audit Log")),
            ("view_channel", self.tr("View Channels (Read Messages)")),
            ("send_messages", self.tr("Send Messages")),
            ("send_tts_messages", self.tr("Send TTS Messages")),
            ("manage_messages", self.tr("Manage Messages")),
            ("embed_links", self.tr("Embed Links")),
            ("attach_files", self.tr("Attach Files")),
            ("read_message_history", self.tr("Read Message History")),
            ("mention_everyone", self.tr("Mention Everyone")),
            ("use_external_emojis", self.tr("Use External Emojis")),
            ("add_reactions", self.tr("Add Reactions")),
            ("connect", self.tr("Connect")),
            ("speak", self.tr("Speak")),
            ("mute_members", self.tr("Mute Members")),
            ("deafen_members", self.tr("Deafen Members")),
            ("move_members", self.tr("Move Members")),
            ("use_voice_activation", self.tr("Use Voice Activity")),
            ("priority_speaker", self.tr("Priority Speaker")),
            ("stream", self.tr("Video")),
            ("request_to_speak", self.tr("Request to Speak")),
            ("manage_threads", self.tr("Manage Threads")),
            ("create_public_threads", self.tr("Create Public Threads")),
            ("create_private_threads", self.tr("Create Private Threads")),
            ("send_messages_in_threads", self.tr("Send Messages in Threads")),
            ("moderate_members", self.tr("Moderate Members")),
        ]

        for perm_attr, perm_name in perms:
            cb = QCheckBox(perm_name)
            cb.setProperty("perm_attr", perm_attr)
            cb.setChecked(True)  # Selected by default
            self.permissions_checks[perm_attr] = cb

    def _init_layout(self):
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel(self.tr("Client ID:")))
        layout.addWidget(self.client_id_edit)

        layout.addWidget(QLabel(self.tr("Permissions:")))

        # Selection buttons
        selection_layout = QHBoxLayout()
        selection_layout.addWidget(self.select_all_btn)
        selection_layout.addWidget(self.deselect_all_btn)
        selection_layout.addStretch()
        layout.addLayout(selection_layout)

        # Add checkboxes to layout
        for i, cb in enumerate(self.permissions_checks.values()):
            self.permissions_layout.addWidget(cb, i // 2, i % 2)

        # Scroll Area for permissions
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_content.setLayout(self.permissions_layout)
        scroll.setWidget(scroll_content)

        layout.addWidget(scroll)
        
        # Buttons layout
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.copy_btn)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.button_box)
        
        layout.addLayout(buttons_layout)

    def _init_connections(self):
        self.select_all_btn.clicked.connect(self.select_all)
        self.deselect_all_btn.clicked.connect(self.deselect_all)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.copy_btn.clicked.connect(self.on_copy_clicked)

    def on_copy_clicked(self):
        self._copy_clipboard = True
        self.accept()

    def select_all(self):
        for cb in self.permissions_checks.values():
            cb.setChecked(True)

    def deselect_all(self):
        for cb in self.permissions_checks.values():
            cb.setChecked(False)

    def get_permissions(self) -> discord.Permissions:
        p = discord.Permissions.none()
        for attr, cb in self.permissions_checks.items():
            if cb.isChecked():
                setattr(p, attr, True)
        return p

    def get_client_id(self) -> str:
        return self.client_id_edit.text().strip()

    def set_client_id(self, client_id: str):
        self.client_id_edit.setText(client_id)

    def should_copy_clipboard(self) -> bool:
        return self._copy_clipboard
