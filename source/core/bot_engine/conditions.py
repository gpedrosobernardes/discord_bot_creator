import logging
import re
import operator
from typing import List, Dict, Callable, Union

import discord
import emoji_data_python
from PySide6.QtCore import QCoreApplication
from PySide6.QtSql import QSqlRecord

from source.core.constants import StrField, IntField, StrComparator, IntComparator

logger = logging.getLogger(__name__)


class MessageConditionValidator:
    """
    Validates a Discord message against a list of conditions defined in QSqlRecords.

    This class extracts specific fields from a Discord message and compares them
    against target values using specified operators (e.g., equals, contains, regex).
    """

    emoji_regex = emoji_data_python.get_emoji_regex()

    def __init__(
        self,
        conditions: List[QSqlRecord],
        message: discord.Message,
    ):
        """
        Initialize the validator with conditions and the message to check.

        Args:
            conditions: A list of QSqlRecord objects containing condition details.
            message: The discord.Message object to validate.
        """
        self.conditions = conditions
        self.message = message
        self.conditions_count = len(conditions)
        self.conditions_validated = 0

        # 1. Data Extraction Strategies
        self._field_extractors: Dict[
            str, Callable[[discord.Message], Union[str, int]]
        ] = {
            StrField.MESSAGE.value: lambda m: str(m.clean_content),
            StrField.AUTHOR_NAME.value: lambda m: m.author.name,
            StrField.CHANNEL_NAME.value: lambda m: m.channel.name,
            StrField.GUILD_NAME.value: lambda m: m.guild.name,
            IntField.MENTIONS_TO_BOT.value: lambda m: len(
                [u for u in m.mentions if u.bot]
            ),
            IntField.MENTIONS.value: lambda m: len(m.mentions),
            IntField.BOT_AUTHOR.value: lambda m: int(m.author.bot),
            IntField.EMOJIS.value: lambda m: len(self.emoji_regex.findall(m.content)),
        }

        # 2. Integer Operators
        self._int_operators: Dict[str, Callable[[int, int], bool]] = {
            IntComparator.EQUAL_TO.value: operator.eq,
            IntComparator.GREATER_THAN.value: operator.gt,
            IntComparator.LESS_THAN.value: operator.lt,
            IntComparator.GREATER_OR_EQUAL_TO.value: operator.ge,
            IntComparator.LESS_OR_EQUAL_TO.value: operator.le,
        }

        # 3. String Operators (Except Regex)
        # operator.contains(a, b) is equivalent to "b in a"
        self._str_operators: Dict[str, Callable[[str, str], bool]] = {
            StrComparator.EQUAL_TO.value: operator.eq,
            StrComparator.CONTAINS.value: operator.contains,
            StrComparator.STARTS_WITH.value: str.startswith,
            StrComparator.ENDS_WITH.value: str.endswith,
        }

    def is_valid_all(self) -> bool:
        """
        Check if the message satisfies all conditions.

        Returns:
            True if all conditions are met, False otherwise.
        """
        return all(self.check_condition(condition) for condition in self.conditions)

    def check_condition(self, condition: QSqlRecord) -> bool:
        """
        Evaluate a single condition against the message.

        Args:
            condition: The QSqlRecord containing the condition logic.

        Returns:
            True if the condition is met, False otherwise.

        Raises:
            ValueError: If the field specified in the condition is unknown.
        """
        field_enum = condition.value("field")

        extractor = self._field_extractors.get(field_enum)
        if not extractor:
            raise ValueError(f"Unknown field: {field_enum}")

        # Extract value from message (e.g., channel name, emoji count)
        message_value = extractor(self.message)

        if isinstance(message_value, int):
            result = self._validate_int(condition, message_value)
        else:
            result = self._validate_str(condition, str(message_value))

        if condition.value("reverse_comparator"):
            result = not result

        return result

    def _validate_int(self, condition: QSqlRecord, msg_value: int) -> bool:
        """
        Validate an integer field.

        Args:
            condition: The condition record.
            msg_value: The integer value extracted from the message.

        Returns:
            True if valid, False otherwise.

        Raises:
            ValueError: If the integer comparator is invalid.
        """
        target_value = int(condition.value("value"))
        comparator = condition.value("comparator")

        op_func = self._int_operators.get(comparator)
        if not op_func:
            raise ValueError(f"Invalid integer comparator: {comparator}")

        result = op_func(msg_value, target_value)
        self._log_validation(condition, msg_value, target_value, result)
        return result

    def _validate_str(self, condition: QSqlRecord, msg_value: str) -> bool:
        """
        Validate a string field.

        Args:
            condition: The condition record.
            msg_value: The string value extracted from the message.

        Returns:
            True if valid, False otherwise.

        Raises:
            ValueError: If the string comparator is invalid.
        """
        target_value = condition.value("value")
        comparator = condition.value("comparator")
        case_insensitive = bool(condition.value("case_insensitive"))

        # Special Case: REGEX
        # Regex has its own case insensitive handling (flags) and doesn't use simple operators
        if comparator == StrComparator.REGEX.value:
            flags = re.IGNORECASE if case_insensitive else 0
            # Using search to find pattern anywhere in the string
            result = bool(re.search(target_value, msg_value, flags))
            self._log_validation(
                condition, msg_value, target_value, result, case_insensitive
            )
            return result

        # Standard Case: String Operators
        op_func = self._str_operators.get(comparator)
        if not op_func:
            raise ValueError(f"Invalid string comparator: {comparator}")

        # Prepare data for normal comparison
        check_val, check_target = msg_value, target_value
        if case_insensitive:
            check_val = msg_value.lower()
            check_target = target_value.lower()

        result = op_func(check_val, check_target)
        self._log_validation(
            condition, msg_value, target_value, result, case_insensitive
        )
        return result

    def _log_validation(
        self,
        condition: QSqlRecord,
        msg_value: Union[str, int],
        target_value: Union[str, int],
        result: bool,
        case_insensitive: bool = False,
    ) -> None:
        """
        Log the validation result for debugging purposes.

        Args:
            condition: The condition record.
            msg_value: The value extracted from the message.
            target_value: The target value to compare against.
            result: The result of the validation.
            case_insensitive: Whether the comparison was case-insensitive.
        """
        self.conditions_validated += 1

        field = condition.value("field")
        comparator = condition.value("comparator")

        # 1. Translate dynamic components individually
        # This ensures "Author Name" becomes "Nome do Autor", etc.
        field_trans = QCoreApplication.translate("StrField", field)

        comp_trans = QCoreApplication.translate("StrComparator", comparator)
        # Fallback to IntComparator if translation doesn't change (means not found in StrComparator)
        if comp_trans == comparator:
            comp_trans = QCoreApplication.translate("IntComparator", comparator)

        # 2. Prepare Case Insensitive tag
        # It also needs to be translatable in isolation
        case_tag = ""
        if case_insensitive:
            # The space at the end is intentional to avoid sticking to the operator
            case_tag = QCoreApplication.translate("ConditionValidator", "[NoCase] ")

        # 3. Define STATIC template (Translation Key)
        # This string is fixed and never changes, regardless of values.
        # The translator will see: "Validating ({current}/{total}): field {field}..."
        log_template = "Validating condition ({current}/{total}): field {field} {value} {case_tag}{operator} {target} ({result})"

        # 4. Translate the template
        translated_template = QCoreApplication.translate(
            "ConditionValidator", log_template
        )

        # 5. Inject variables into the ALREADY translated string
        final_log_msg = translated_template.format(
            current=self.conditions_validated,
            total=self.conditions_count,
            field=field_trans,
            value=repr(msg_value),
            case_tag=case_tag,
            operator=comp_trans.lower(),
            target=repr(target_value),
            result=result,
        )

        logger.debug(final_log_msg)
