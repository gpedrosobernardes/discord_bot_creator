import typing

from PySide6.QtCore import QCoreApplication, Slot, Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QDataWidgetMapper
from discord import Guild, TextChannel, VoiceChannel

from source.controllers.base import BaseController
from source.core.database import DatabaseController
from source.views.group import GroupView
from source.qt.items.text_channel_item import TextChannelItem
from source.qt.items.voice_channel_item import VoiceChannelItem

translate = QCoreApplication.translate


class GroupController(BaseController[GroupView]):
    def __init__(self, database: DatabaseController, discord_group: Guild):
        super().__init__(GroupView())
        self.database = database
        self.group_id: typing.Optional[int] = None
        self.discord_group: Guild = discord_group

        self.model = self.database.get_groups_model()
        self.welcome_channels_model = QStandardItemModel()
        self.goodbye_channels_model = QStandardItemModel()

        self.view.welcome_message_channels.setModel(self.welcome_channels_model)
        self.view.goodbye_message_channels.setModel(self.goodbye_channels_model)

        self._init_mapper()
        self._init_connections()
        self._populate_channels()

    def _init_mapper(self):
        self.mapper = QDataWidgetMapper()
        self.mapper.setModel(self.model)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.SubmitPolicy.ManualSubmit)

        self.mapper.addMapping(
            self.view.welcome_message_textedit,
            self.model.fieldIndex("welcome_message"),
            b"plainText",
        )
        self.mapper.addMapping(
            self.view.goodbye_message_textedit,
            self.model.fieldIndex("goodbye_message"),
            b"plainText",
        )

    def _init_connections(self):
        self.view.save_button.clicked.connect(self.save)

    def _populate_channels(self):
        """Popula os comboboxes com os canais de texto e voz do grupo."""
        if not self.discord_group:
            return

        channels = []
        for channel in self.discord_group.channels:
            if isinstance(channel, (TextChannel, VoiceChannel)):
                channels.append(channel)

        # Ordenar por nome
        channels.sort(key=lambda x: x.name)

        self.welcome_channels_model.clear()
        self.goodbye_channels_model.clear()

        # Adicionar opção padrão/vazia
        empty_item_welcome = QStandardItem(self.tr("Select a channel"))
        empty_item_welcome.setData(None, Qt.ItemDataRole.UserRole)
        self.welcome_channels_model.appendRow(empty_item_welcome)

        empty_item_goodbye = QStandardItem(self.tr("Select a channel"))
        empty_item_goodbye.setData(None, Qt.ItemDataRole.UserRole)
        self.goodbye_channels_model.appendRow(empty_item_goodbye)

        for channel in channels:
            if isinstance(channel, TextChannel):
                self.welcome_channels_model.appendRow(TextChannelItem(channel))
                self.goodbye_channels_model.appendRow(TextChannelItem(channel))
            elif isinstance(channel, VoiceChannel):
                self.welcome_channels_model.appendRow(VoiceChannelItem(channel))
                self.goodbye_channels_model.appendRow(VoiceChannelItem(channel))

    def set_group(self, group_id: int):
        self.group_id = group_id
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
        """Carrega a seleção correta nos comboboxes baseado nos dados do modelo."""
        record = self.model.record(self.mapper.currentIndex())

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
        # Salvar manualmente os IDs dos canais no modelo antes de submeter
        welcome_channel_id = self.view.welcome_message_channels.currentData()
        goodbye_channel_id = self.view.goodbye_message_channels.currentData()

        # Atualizar o registro atual no modelo
        # Como o mapper está no índice 0 (pois filtramos por ID), pegamos o record 0
        if self.model.rowCount() > 0:
            record = self.model.record(0)
            record.setValue("welcome_message_channel", welcome_channel_id)
            record.setValue("goodbye_message_channel", goodbye_channel_id)
            self.model.setRecord(0, record)

        self.mapper.submit()
        self.model.submitAll()
        self.view.accept()
