from enum import IntEnum, StrEnum, Enum

from PySide6.QtCore import QT_TRANSLATE_NOOP


class Actions(IntEnum):
    PIN = 0
    DELETE = 1
    NONE = 2


class Punishment(IntEnum):
    KICK = 0
    BAN = 1
    NONE = 2


class WhereReply(IntEnum):
    GROUP = 0
    PRIVATE = 1
    SAME_CHANNEL = 2
    BOTH = 3
    NONE = 4


class WhereReact(IntEnum):
    AUTHOR = 0
    BOT = 1
    NONE = 2


class Language(StrEnum):
    ENGLISH = "en_us"
    PORTUGUESE = "pt_br"


class StrField(Enum):
    MESSAGE = QT_TRANSLATE_NOOP("StrField", "Message")
    AUTHOR_NAME = QT_TRANSLATE_NOOP("StrField", "Author name")
    CHANNEL_NAME = QT_TRANSLATE_NOOP("StrField", "Channel name")
    GUILD_NAME = QT_TRANSLATE_NOOP("StrField", "Guild name")


class IntField(Enum):
    MENTIONS_TO_BOT = QT_TRANSLATE_NOOP("IntField", "Mentions to bot")
    MENTIONS = QT_TRANSLATE_NOOP("IntField", "Mentions")
    BOT_AUTHOR = QT_TRANSLATE_NOOP("IntField", "Bot author")
    EMOJIS = QT_TRANSLATE_NOOP("IntField", "Emojis")


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
