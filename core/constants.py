from enum import IntEnum, StrEnum, Enum

from PySide6.QtCore import QT_TRANSLATE_NOOP


class Actions(IntEnum):
    PIN = 1
    DELETE = 2
    NONE = 3


class Punishment(IntEnum):
    KICK = 1
    BAN = 2
    NONE = 3


class WhereReply(IntEnum):
    GROUP = 1
    PRIVATE = 2
    NONE = 3


class WhereReact(IntEnum):
    AUTHOR = 1
    BOT = 2
    NONE = 3


class Language(StrEnum):
    ENGLISH = "en_us"
    PORTUGUESE = "pt_br"


class StrField(StrEnum):
    MESSAGE = "message"
    AUTHOR_NAME = "author_name"
    CHANNEL_NAME = "channel_name"
    GUILD_NAME = "guild_name"


class IntField(StrEnum):
    MENTIONS_TO_BOT = "mentions_to_bot"
    MENTIONS = "mentions"
    BOT_AUTHOR = "bot_author"
    EMOJIS = "emojis"


class StrComparator(Enum):
    EQUAL_TO = QT_TRANSLATE_NOOP("StrComparator", "Equal to")
    CONTAINS = QT_TRANSLATE_NOOP("StrComparator", "Contains")
    STARTS_WITH = QT_TRANSLATE_NOOP("StrComparator", "Starts with")
    ENDS_WITH = QT_TRANSLATE_NOOP("StrComparator", "Ends with")
    REGEX = QT_TRANSLATE_NOOP("StrComparator", "Regex")


class IntComparator(StrEnum):
    EQUAL_TO = "equal_to"
    GREATER_THAN = "greater_than"
    LESS_THAN = "less_than"
    GREATER_OR_EQUAL_TO = "greater_or_equal_to"
    LESS_OR_EQUAL_TO = "less_or_equal_to"


print(StrComparator)
