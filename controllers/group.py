import typing

from PySide6.QtCore import QCoreApplication
from discord import Guild

from core.database import Database
from models.group import Group
from views.group import GroupView

translate = QCoreApplication.translate


class GroupController:
    def __init__(self):
        self.view = GroupView()
        self.group: typing.Optional[Group] = None
        self.discord_group: typing.Optional[Guild] = None
