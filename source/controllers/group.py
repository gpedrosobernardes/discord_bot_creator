from PySide6.QtCore import Slot, Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QDataWidgetMapper, QMessageBox

from source.controllers.base import BaseController
from source.core.database import DatabaseController
from source.core.discord_api import DiscordAPIClient  # Importar cliente API
from source.qt.items.text_channel_item import TextChannelItem
from source.qt.items.voice_channel_item import VoiceChannelItem
from source.views.group import GroupView


# Remover imports do discord.py (Guild, TextChannel, etc)

class GroupController(BaseController[GroupView]):
    # ALTERADO: Assinatura do __init__ recebe ID, Nome e Token
    def __init__(self, database: DatabaseController, group_id: int, group_name: str, token: str):
        super().__init__(GroupView())
        self.database = database
        self.group_id = group_id
        self.group_name = group_name

        self.view.setWindowTitle(f"Configuring: {group_name}")

        # Configurar API Client localmente para este controller
        self.discord_api = DiscordAPIClient(self)
        self.discord_api.set_token(token)
        self.discord_api.channels_received.connect(self._on_channels_received)
        self.discord_api.request_failed.connect(self._on_api_error)

        self.model = self.database.get_groups_model()
        self.welcome_channels_model = QStandardItemModel()
        self.goodbye_channels_model = QStandardItemModel()

        self.view.welcome_message_channels.setModel(self.welcome_channels_model)
        self.view.goodbye_message_channels.setModel(self.goodbye_channels_model)

        self._init_mapper()
        self._init_connections()

        # Iniciar busca dos canais
        self.view.welcome_message_channels.setPlaceholderText("Loading channels...")
        self.discord_api.fetch_channels(str(self.group_id))

    def _init_mapper(self):
        # ... (código igual ao original) ...
        self.mapper = QDataWidgetMapper()
        self.mapper.setModel(self.model)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.SubmitPolicy.ManualSubmit)
        self.mapper.addMapping(self.view.welcome_message_textedit, self.model.fieldIndex("welcome_message"), b"plainText")
        self.mapper.addMapping(self.view.goodbye_message_textedit, self.model.fieldIndex("goodbye_message"), b"plainText")

    def _init_connections(self):
        self.view.confirm_button.clicked.connect(self.save)
        self.view.cancel_button.clicked.connect(self.view.close) # Botão cancelar funciona agora

    @Slot(str)
    def _on_api_error(self, error_msg: str):
        QMessageBox.warning(self.view, "Error fetching channels", error_msg)

    @Slot(list)
    def _on_channels_received(self, channels_data: list):
        """Processa o JSON de canais recebido da API."""
        # Tipos de canais (Discord API): 0 = Texto, 2 = Voz, 4 = Categoria, etc.
        text_channels = []
        voice_channels = []

        for ch in channels_data:
            ch_type = ch.get("type")
            ch_name = ch.get("name", "Unknown")
            ch_id = int(ch.get("id"))

            if ch_type == 0: # GUILD_TEXT
                text_channels.append((ch_name, ch_id))
            elif ch_type == 2: # GUILD_VOICE
                voice_channels.append((ch_name, ch_id))

        # Ordenar
        text_channels.sort(key=lambda x: x[0])
        voice_channels.sort(key=lambda x: x[0])

        self._populate_models(text_channels, voice_channels)

        # Após popular, inicializa os dados do banco
        self.set_group(self.group_id)

    def _populate_models(self, text_channels, voice_channels):
        self.welcome_channels_model.clear()
        self.goodbye_channels_model.clear()

        # Itens padrão
        for model in [self.welcome_channels_model, self.goodbye_channels_model]:
            empty = QStandardItem(self.tr("Select a channel"))
            empty.setData(None, Qt.ItemDataRole.UserRole)
            model.appendRow(empty)

        # Adicionar canais de texto
        for name, cid in text_channels:
            # Você pode criar um item simples ou reutilizar suas classes de Item se ajustar o __init__ delas
            item = TextChannelItem(name, cid)
            # item.setIcon(QIcon("assets/icons/hashtag.svg")) # Exemplo se tiver ícone
            self.welcome_channels_model.appendRow(item)

            item_copy = item.clone()
            self.goodbye_channels_model.appendRow(item_copy)

        # Adicionar canais de voz (se desejar permitir mensagens lá, o que é raro para texto, mas possível)
        for name, cid in voice_channels:
            item = VoiceChannelItem(name, cid)
            self.welcome_channels_model.appendRow(item)

            item_copy = item.clone()
            self.goodbye_channels_model.appendRow(item_copy)

    def set_group(self, group_id: int):
        # ... (código igual, apenas lógica de banco de dados) ...
        self.model.setFilter(f"id = {group_id}")
        self.model.select()

        if self.model.rowCount() == 0:
            record = self.model.record()
            record.setValue("id", group_id)
            self.model.insertRecord(-1, record)
            self.model.select()

        self.mapper.toFirst()
        self._load_channels_selection()

    def _load_channels_selection(self):
        # ... (código igual) ...
        record = self.model.record(self.mapper.currentIndex())

        # Lógica idêntica, apenas certifique-se que o findData funciona com Inteiros
        welcome_channel_id = record.value("welcome_message_channel")
        if welcome_channel_id:
            index = self.view.welcome_message_channels.findData(welcome_channel_id)
            if index >= 0:
                self.view.welcome_message_channels.setCurrentIndex(index)

        goodbye_channel_id = record.value("goodbye_message_channel")
        if goodbye_channel_id:
            index = self.view.goodbye_message_channels.findData(goodbye_channel_id)
            if index >= 0:
                self.view.goodbye_message_channels.setCurrentIndex(index)

    @Slot()
    def save(self):
        # ... (código igual) ...
        welcome_channel_id = self.view.welcome_message_channels.currentData()
        goodbye_channel_id = self.view.goodbye_message_channels.currentData()

        if self.model.rowCount() == 0:
            record = self.model.record()
            record.setValue("id", self.group_id)
            record.setValue("welcome_message_channel", welcome_channel_id)
            record.setValue("goodbye_message_channel", goodbye_channel_id)
            record.setValue("welcome_message", self.view.welcome_message_textedit.toPlainText())
            record.setValue("goodbye_message", self.view.goodbye_message_textedit.toPlainText())
            self.model.insertRecord(-1, record)
        else:
            record = self.model.record(0)
            record.setValue("welcome_message_channel", welcome_channel_id)
            record.setValue("goodbye_message_channel", goodbye_channel_id)
            self.model.setRecord(0, record)
            self.mapper.submit()

        self.model.submitAll()
        self.view.accept()