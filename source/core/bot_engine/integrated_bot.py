import discord
from PySide6.QtCore import QObject, Signal

from source.core.bot_engine.bot import Bot


class BotSignals(QObject):
    """
    Classe dedicada apenas para definição dos sinais.
    Serve como ponte entre o Bot (asyncio) e a GUI (Qt).
    """

    bot_ready = Signal()
    login_failure = Signal()
    privileged_intents_error = Signal()
    guild_join = Signal(str)
    guild_remove = Signal(str)
    guild_update = Signal(str)


class IntegratedBot(Bot):
    def __init__(self, signals: BotSignals, database_name: str):
        # Não passamos mais o thread_executor, apenas os sinais
        self.signals = signals
        super().__init__(database_name)

    async def on_ready(self):
        await super().on_ready()
        # Emite diretamente do objeto de sinais
        self.signals.bot_ready.emit()

    async def on_guild_join(self, guild: discord.Guild):
        self.signals.guild_join.emit(str(guild.id))

    async def on_guild_remove(self, guild: discord.Guild):
        self.signals.guild_remove.emit(str(guild.id))

    async def on_guild_update(self, _: discord.Guild, after: discord.Guild):
        self.signals.guild_update.emit(str(after.id))
