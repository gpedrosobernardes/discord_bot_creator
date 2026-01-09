import typing

from PySide6.QtCore import QCoreApplication
from discord import Guild


from views.group import GroupView

translate = QCoreApplication.translate


class GroupController:
    def __init__(self):
        self.view = GroupView()
        self.group: typing.Optional = None
        self.discord_group: typing.Optional[Guild] = None
