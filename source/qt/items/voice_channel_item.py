from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItem
from discord import VoiceChannel
from qextrawidgets.icons import QThemeResponsiveIcon


class VoiceChannelItem(QStandardItem):
    def __init__(self, name: str, channel_id: int):
        super().__init__(name)
        self.setIcon(QThemeResponsiveIcon.fromAwesome("fa6s.volume-high"))
        self.setData(channel_id, Qt.ItemDataRole.UserRole)
        self.setEditable(False)
