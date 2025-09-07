import logging
import re
import typing
from abc import ABC, abstractmethod

import discord
import emojis

from core.translator import (
    Translator,
    FIELDS_TRANSLATIONS,
    OPERATORS_TRANSLATIONS,
    BOOL_TRANSLATIONS,
)
from models.condition import MessageCondition
from core.log_handler import LogHandler


logger = logging.getLogger(__name__)
logger.addHandler(LogHandler())
translate = Translator.translate


class MessageConditionValidator:
    STR_FIELDS = (
        "message",
        "author name",
        "channel name",
        "guild name",
    )
    INT_FIELDS = (
        "mentions to bot",
        "mentions",
        "bot author",
        "emojis",
    )
    ENUM_FIELDS = ("channel type",)
    STR_OPERATORS = (
        "equal to",
        "not equal to",
        "contains",
        "not contains",
        "starts with",
        "ends with",
        "regex",
    )
    INT_OPERATORS = (
        "equal to",
        "not equal to",
        "is greater than",
        "is less than",
        "is greater or equal to",
        "is less or equal to",
    )
    ENUM_OPERATORS = ("equal to",)

    def __init__(
        self,
        conditions: list[MessageCondition],
        message: discord.Message,
    ):
        self.conditions = conditions
        self.message = message
        self.conditions_count = len(conditions)
        self.conditions_validated = 0

    def is_valid(self, condition: MessageCondition) -> bool:
        if condition.field == "message":
            return StringConditionValidator(
                condition, str(self.message.clean_content)
            ).is_valid()
        elif condition.field == "author name":
            return StringConditionValidator(
                condition, self.message.author.name
            ).is_valid()
        elif condition.field == "channel name":
            return StringConditionValidator(
                condition, self.message.channel.name
            ).is_valid()
        elif condition.field == "guild name":
            return StringConditionValidator(
                condition, self.message.guild.name
            ).is_valid()
        elif condition.field == "mentions to bot":
            return IntegerConditionValidator(
                condition, len(list(user.bot for user in self.message.mentions))
            ).is_valid()
        elif condition.field == "mentions":
            return IntegerConditionValidator(
                condition, len(self.message.mentions)
            ).is_valid()
        elif condition.field == "bot author":
            return IntegerConditionValidator(
                condition, int(self.message.author.bot)
            ).is_valid()
        elif condition.field == "emojis":
            return IntegerConditionValidator(
                condition, emojis.count(self.message.clean_content)
            ).is_valid()
        elif condition.field == "channel type":
            channel_type = type(self.message.channel.type).__name__
            return EnumConditionValidator(
                condition,
                channel_type,
            ).is_valid()
        else:
            raise ValueError(f"Invalid field: {condition.field}")

    def is_valid_all(self) -> bool:
        return all(self.is_valid(condition) for condition in self.conditions)

    def log(
        self,
        condition: MessageCondition,
        condition_value: typing.Union[str, int],
        result: bool,
        value: typing.Union[str, int],
    ) -> None:
        format_kwargs = dict(
            conditions_validated=self.conditions_validated,
            conditions_count=self.conditions_count,
            field=FIELDS_TRANSLATIONS[condition.field],
            value=value,
            operator=OPERATORS_TRANSLATIONS[condition.operator].lower(),
            condition_value=repr(condition_value),
            result=BOOL_TRANSLATIONS[result],
        )
        if condition.case_insensitive:
            format_kwargs["case_insensitive"] = Translator.translate(
                "ConditionValidator", "Case insensitive"
            ).lower()
            log = Translator.translate(
                "ConditionValidator",
                "Validating condition ({conditions_validated}/{conditions_count}): field {field} {value} {case_insensitive} {operator} {condition_value} ({result})",
            ).format(**format_kwargs)
        else:
            log = Translator.translate(
                "ConditionValidator",
                "Validating condition ({conditions_validated}/{conditions_count}): field {field} {value} {operator} {condition_value} ({result})",
            ).format(**format_kwargs)
        logger.debug(log)


class ConditionValidator(ABC):
    def __init__(
        self, condition: MessageCondition, value: typing.Union[str, int]
    ) -> None:
        self.condition = condition
        self.value = value

    @abstractmethod
    def is_valid(self) -> bool:
        pass


class StringConditionValidator(ConditionValidator):
    def is_valid(self) -> bool:
        new_value = self.value
        condition_value = self.condition.value
        if self.condition.case_insensitive:
            new_value = self.value.lower()
            condition_value = condition_value.lower()
        if self.condition.operator == "equal to":
            return new_value == condition_value
        elif self.condition.operator == "not equal to":
            return new_value != condition_value
        elif self.condition.operator == "contains":
            return condition_value in new_value
        elif self.condition.operator == "not contains":
            return condition_value not in new_value
        elif self.condition.operator == "starts with":
            return new_value.startswith(condition_value)
        elif self.condition.operator == "ends with":
            return new_value.endswith(condition_value)
        elif self.condition.operator == "regex":
            flag = re.IGNORECASE if self.condition.case_insensitive else 0
            return re.match(self.condition.value, self.value, flag) is not None
        else:
            raise ValueError(f"Invalid operator: {self.condition.operator}")


class IntegerConditionValidator(ConditionValidator):
    def is_valid(self) -> bool:
        condition_value = int(self.condition.value)
        if self.condition.operator == "equal to":
            return condition_value == self.value
        elif self.condition.operator == "not equal to":
            return condition_value != self.value
        elif self.condition.operator == "is greater than":
            return condition_value > self.value
        elif self.condition.operator == "is less than":
            return condition_value < self.value
        elif self.condition.operator == "is greater or equal to":
            return condition_value >= self.value
        elif self.condition.operator == "is less or equal to":
            return condition_value <= self.value
        else:
            raise ValueError(f"Invalid operator: {self.condition.operator}")


class EnumConditionValidator(ConditionValidator):
    def is_valid(self) -> bool:
        return self.condition.value == self.value
