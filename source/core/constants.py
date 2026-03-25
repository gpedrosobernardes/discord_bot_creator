from enum import Enum, IntEnum, StrEnum

from PySide6.QtCore import QT_TRANSLATE_NOOP


class Actions(IntEnum):
    NONE = 0
    PIN = 1
    DELETE = 2


class Punishment(IntEnum):
    NONE = 0
    KICK = 1
    BAN = 2


class WhereReply(IntEnum):
    SAME_CHANNEL = 0
    GROUP = 1
    PRIVATE = 2
    BOTH = 3
    NONE = 4


class WhereReact(IntEnum):
    AUTHOR = 0
    BOT = 1
    NONE = 2


class Language(StrEnum):
    ENGLISH = "en_US"
    PORTUGUESE = "pt_BR"


class StrField(Enum):
    MESSAGE = QT_TRANSLATE_NOOP("StrField", "Message")
    AUTHOR_NAME = QT_TRANSLATE_NOOP("StrField", "Author name")
    CHANNEL_NAME = QT_TRANSLATE_NOOP("StrField", "Channel name")
    GUILD_NAME = QT_TRANSLATE_NOOP("StrField", "Guild name")


class IntField(Enum):
    BOT_MENTIONS = QT_TRANSLATE_NOOP("IntField", "Bot Mentions")
    MENTIONS = QT_TRANSLATE_NOOP("IntField", "Mentions")
    EMOJIS = QT_TRANSLATE_NOOP("IntField", "Emojis")


class BoolField(Enum):
    BOT_AUTHOR = QT_TRANSLATE_NOOP("BoolField", "Bot author")
    MENTIONS_THE_BOT = QT_TRANSLATE_NOOP("BoolField", "Mentions the bot")


class StrComparator(Enum):
    EQUAL_TO = QT_TRANSLATE_NOOP("StrComparator", "Equal to")
    CONTAINS = QT_TRANSLATE_NOOP("StrComparator", "Contains")
    STARTS_WITH = QT_TRANSLATE_NOOP("StrComparator", "Starts with")
    ENDS_WITH = QT_TRANSLATE_NOOP("StrComparator", "Ends with")
    REGEX = QT_TRANSLATE_NOOP("StrComparator", "Regex")


class IntComparator(Enum):
    EQUAL_TO = QT_TRANSLATE_NOOP("IntComparator", "Equal to")
    GREATER_THAN = QT_TRANSLATE_NOOP("IntComparator", "Greater than")
    LESS_THAN = QT_TRANSLATE_NOOP("IntComparator", "Less than")
    GREATER_OR_EQUAL_TO = QT_TRANSLATE_NOOP("IntComparator", "Greater or equal to")
    LESS_OR_EQUAL_TO = QT_TRANSLATE_NOOP("IntComparator", "Less or equal to")


class BoolComparator(Enum):
    EQUAL_TO = QT_TRANSLATE_NOOP("BoolComparator", "Equal to")
