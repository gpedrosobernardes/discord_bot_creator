import typing

from core.database import Database
from models.message import Message
from views.messages import MessageView


class MessageController:
    def __init__(self):
        self.view = MessageView()
        self.current_message: typing.Optional[Message] = None
