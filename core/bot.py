import asyncio
import logging
import random
import typing

import discord
from PySide6.QtCore import QCoreApplication
from PySide6.QtSql import QSqlTableModel, QSqlRecord
from discord import MessageType

from core.constants import Actions, Punishment, WhereReply, WhereReact
from core.database import DatabaseController
from core.log_handler import LogHandler
from interpreter.conditions import MessageConditionValidator
from interpreter.variable import Variable

logger = logging.getLogger(__name__)
logger.addHandler(LogHandler())


class Bot(discord.Client):
    def __init__(self, database_name: str):
        super().__init__(intents=discord.Intents.all())
        self.database = DatabaseController(database_name, "bot")

    # --- Lifecycle Events ---

    async def on_ready(self):
        logger.info(QCoreApplication.translate("Bot", "Bot started!"))

    async def close(self):
        await super().close()
        logger.info(QCoreApplication.translate("Bot", "Bot finished!"))

    # --- Member Events ---

    async def on_member_join(self, member: discord.Member):
        await self._handle_member_event(
            member,
            "welcome_message",
            "welcome_message_channel",
            "Sending welcome message",
        )

    async def on_member_remove(self, member: discord.Member):
        await self._handle_member_event(
            member,
            "goodbye_message",
            "goodbye_message_channel",
            "Sending goodbye message",
        )

    async def _handle_member_event(
        self,
        member: discord.Member,
        msg_field: str,
        channel_field: str,
        log_action: str,
    ):
        record = self._get_group_record(member.guild.id)
        if not record:
            return

        message_template = record.value(msg_field)
        channel_id = record.value(channel_field)

        if message_template and channel_id:
            channel = member.guild.get_channel(channel_id)
            if channel:
                formatted_message = message_template.format(member=member.name)
                await channel.send(formatted_message)

                # Construct log message based on action to preserve translation keys if possible,
                # or use a generic one.
                # To strictly preserve the original keys:
                if "welcome" in msg_field:
                    log_msg = QCoreApplication.translate(
                        "Bot",
                        'Sending welcome message "{}" on channel "{}" at "{}" group.',
                    )
                else:
                    log_msg = QCoreApplication.translate(
                        "Bot",
                        'Sending goodbye message "{}" on channel "{}" at "{}" group.',
                    )

                logger.info(
                    log_msg.format(formatted_message, channel.name, member.guild.name)
                )

    def _get_group_record(self, guild_id: int) -> typing.Optional[QSqlRecord]:
        groups_model = self.database.get_groups_model()
        groups_model.setFilter(f"id = {guild_id}")
        groups_model.select()
        if groups_model.rowCount() > 0:
            return groups_model.record(0)
        return None

    # --- Message Events ---

    async def on_message(self, discord_message: discord.Message):
        if (
            discord_message.author == self.user
            or discord_message.type != MessageType.default
        ):
            return

        logger.info(
            QCoreApplication.translate("Bot", 'Identified message "{}".').format(
                discord_message.clean_content
            )
        )

        await self._process_message_rules(discord_message)

    async def _process_message_rules(self, discord_message: discord.Message):
        messages_model = self.database.get_messages_model()
        # Iterate manually as we need to process each rule
        for i in range(messages_model.rowCount()):
            message_record = messages_model.record(i)
            await self._execute_rule_if_valid(message_record, discord_message)

    async def _execute_rule_if_valid(
        self, message_record: QSqlRecord, discord_message: discord.Message
    ):
        if not self._check_conditions(message_record, discord_message):
            return

        # Delay
        delay = message_record.value("delay")
        if delay:
            await self.apply_delay(delay)

        # Execute Actions
        await self._handle_replies(message_record, discord_message)
        await self._handle_reactions(message_record, discord_message)
        await self._handle_action(message_record, discord_message)
        await self._handle_punishment(message_record, discord_message)

    def _check_conditions(
        self, message_record: QSqlRecord, discord_message: discord.Message
    ) -> bool:
        message_id = message_record.value("id")
        conditions_model = self.database.get_message_conditions_model()
        conditions_model.setFilter(f"message_id = {message_id}")
        conditions_model.select()

        conditions = [
            conditions_model.record(j) for j in range(conditions_model.rowCount())
        ]
        validator = MessageConditionValidator(conditions, discord_message)
        return validator.is_valid_all()

    async def _handle_replies(
        self, message_record: QSqlRecord, discord_message: discord.Message
    ):
        message_id = message_record.value("id")
        replies_model = self.database.get_message_replies_model()
        replies_model.setFilter(f"message_id = {message_id}")
        replies_model.select()

        if replies_model.rowCount() > 0:
            await self.send_replies(replies_model, message_record, discord_message)

    async def _handle_reactions(
        self, message_record: QSqlRecord, discord_message: discord.Message
    ):
        where_reaction = message_record.value("where_reaction")
        if where_reaction != WhereReact.AUTHOR:
            return

        message_id = message_record.value("id")
        reactions_model = self.database.get_message_reactions_model()
        reactions_model.setFilter(f"message_id = {message_id}")
        reactions_model.select()

        if reactions_model.rowCount() > 0:
            await self.send_reactions(reactions_model, discord_message)

    async def _handle_action(
        self, message_record: QSqlRecord, discord_message: discord.Message
    ):
        action = message_record.value("action")
        if action == Actions.DELETE:
            await self.remove_message(discord_message)
        elif action == Actions.PIN:
            await self.pin_message(discord_message)

    async def _handle_punishment(
        self, message_record: QSqlRecord, discord_message: discord.Message
    ):
        punishment = message_record.value("punishment")
        if punishment == Punishment.BAN:
            await self.ban_member(discord_message.author)
        elif punishment == Punishment.KICK:
            await self.kick_member(discord_message.author)

    # --- Helper Methods / Actions ---

    @staticmethod
    async def apply_delay(delay: int):
        logger.info(
            QCoreApplication.translate(
                "Bot", "Waiting {} seconds delay to next execution!"
            ).format(delay)
        )
        await asyncio.sleep(delay)

    @staticmethod
    async def send_reactions(
        reactions_model: QSqlTableModel, discord_message: discord.Message
    ):
        reactions = [
            reactions_model.record(i).value("reaction")
            for i in range(reactions_model.rowCount())
        ]

        for reaction_text in reactions:
            try:
                await discord_message.add_reaction(reaction_text)
                logger.info(
                    QCoreApplication.translate(
                        "Bot",
                        'Adding reaction "{}" to the message "{}" by the author {}.',
                    ).format(
                        reaction_text,
                        discord_message.clean_content,
                        discord_message.author,
                    )
                )
            except discord.HTTPException as e:
                # Log error or ignore as per original code (original printed to stdout)
                logger.warning(f"Failed to add reaction {reaction_text}: {e}")

    async def send_replies(
        self,
        replies_model: QSqlTableModel,
        message_record: QSqlRecord,
        discord_message: discord.Message,
    ):
        replies = [
            replies_model.record(i).value("text")
            for i in range(replies_model.rowCount())
        ]

        for reply_text_raw in replies:
            reply_text = Variable(discord_message).apply_variable(reply_text_raw)

            where_reply = message_record.value("where_reply")

            if (
                where_reply == WhereReply.GROUP
                and discord_message.channel.guild is not None
            ):
                await self.send_reply(
                    reply_text,
                    discord_message,
                    discord_message.channel,
                    message_record,
                )
            elif where_reply == WhereReply.PRIVATE:
                dm_channel = await discord_message.author.create_dm()
                await self.send_reply(
                    reply_text, discord_message, dm_channel, message_record
                )

    async def send_reply(
        self,
        reply: str,
        discord_message: discord.Message,
        channel: discord.abc.Messageable,
        message_record: QSqlRecord,
    ):
        where_reply = message_record.value("where_reply")
        if where_reply == WhereReply.GROUP:
            log_msg = QCoreApplication.translate(
                "Bot", 'Replying on group "{}" to the message "{}" by the author {}.'
            )
        else:
            log_msg = QCoreApplication.translate(
                "Bot", 'Replying on private "{}" to the message "{}" by the author {}.'
            )

        logger.info(
            log_msg.format(reply, discord_message.clean_content, discord_message.author)
        )

        reply_message = await self.send_message(channel, reply)

        # Handle reactions on the bot's reply
        where_reaction = message_record.value("where_reaction")
        if where_reaction == WhereReact.BOT and reply_message:
            message_id = message_record.value("id")
            reactions_model = self.database.get_message_reactions_model()
            reactions_model.setFilter(f"message_id = {message_id}")
            reactions_model.select()
            if reactions_model.rowCount() > 0:
                await self.send_reactions(reactions_model, reply_message)

    @staticmethod
    async def send_message(
        channel: discord.abc.Messageable, message: str
    ) -> typing.Optional[discord.Message]:
        try:
            return await channel.send(message)
        except discord.errors.HTTPException as exception:
            if exception.code == 50035 and exception.status == 400:
                logger.error(
                    QCoreApplication.translate(
                        "Bot",
                        "Content must be 2000 or fewer in length.",
                    ).format(message, channel)
                )
            return None

    @staticmethod
    async def remove_message(message: discord.Message):
        try:
            await message.delete()
            logger.info(
                QCoreApplication.translate(
                    "Bot", 'Removing message "{}" by the author {}.'
                ).format(message.clean_content, message.author)
            )
        except discord.Forbidden:
            logger.error(
                QCoreApplication.translate(
                    "Bot",
                    'Don\'t have permission to remove message "{}" by the author {}.',
                ).format(message.clean_content, message.author)
            )

    @staticmethod
    async def pin_message(message: discord.Message):
        try:
            await message.pin()
            logger.info(
                QCoreApplication.translate(
                    "Bot", 'Pinning message "{}" by the author {}.'
                ).format(message.clean_content, message.author)
            )
        except discord.Forbidden:
            logger.error(
                QCoreApplication.translate(
                    "Bot",
                    'Don\'t have permission to pin message "{}" by the author {}.',
                ).format(message.clean_content, message.author)
            )

    @staticmethod
    async def kick_member(member: discord.Member):
        try:
            await member.kick()
            logger.info(
                QCoreApplication.translate("Bot", 'Kicking member "{}".').format(
                    member.name
                )
            )
        except discord.Forbidden:
            logger.error(
                QCoreApplication.translate(
                    "Bot", 'Don\'t have permission to kick "{}".'
                ).format(member.name)
            )

    @staticmethod
    async def ban_member(member: discord.Member):
        try:
            if isinstance(member, discord.Member):
                await member.ban()
                logger.info(
                    QCoreApplication.translate("Bot", 'Banning member "{}".').format(
                        member.name
                    )
                )
            elif isinstance(member, discord.User):
                logger.warning(
                    QCoreApplication.translate(
                        "Bot",
                        'Cannot ban member "{}": message is not associated with any group.',
                    ).format(member.name)
                )
        except discord.Forbidden:
            logger.error(
                QCoreApplication.translate(
                    "Bot", 'Don\'t have permission to ban "{}".'
                ).format(member.name)
            )

    @staticmethod
    async def leave_guild(guild: discord.Guild):
        await guild.leave()
        logger.info(
            QCoreApplication.translate("Bot", 'Leaving guild "{}"').format(guild.name)
        )

    def get_guild(self, guild_id: int) -> typing.Optional[discord.Guild]:
        return next(filter(lambda g: g.id == guild_id, self.guilds), None)
