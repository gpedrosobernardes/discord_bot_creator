import logging

from PySide6.QtCore import QSettings, Qt
from qextrawidgets.core.utils import QEmojiFonts

from source.core.constants import Language


class Settings(QSettings):
    def __init__(self):
        super().__init__("discord_bot_creator", "main")
        default_values = {
            "auto_start_bot": False,
            "confirm_actions": True,
            "language": Language.ENGLISH,
            "log_level": logging.INFO,
            "database": ":memory:",
            "style": "windows11",
            "theme": Qt.ColorScheme.Unknown,
            "emoji_font": QEmojiFonts.loadTwemojiFont(),
            "recent_emojis": [],
            "favorite_emojis": [],
        }
        for key, value in default_values.items():
            if not self.contains(key):
                self.setValue(key, value)
