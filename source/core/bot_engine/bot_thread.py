import asyncio
import logging
from typing import Dict, Optional

import discord
from PySide6.QtCore import QThread
from discord import LoginFailure

from source.core.bot_engine.integrated_bot import IntegratedBot, BotSignals

# Logger setup para capturar erros internos da thread
logger = logging.getLogger(__name__)


class QBotThread(QThread):
    """
    Thread dedicada para executar o loop de eventos asyncio do Discord Bot.
    Gerencia a comunicação thread-safe entre a GUI (Qt) e o Bot (Asyncio).
    """

    def __init__(self) -> None:
        """Initializes the QBotThread."""
        super().__init__()
        self._token: str = ""
        self.signals = BotSignals()
        self._bot: Optional[IntegratedBot] = None
        self._database_name: str = None

    def set_token(self, token: str) -> None:
        """Sets the bot token before starting."""
        self._token = token

    def set_database_name(self, database_name: str):
        self._database_name = database_name
        if self._bot:
            self._bot.database.switch_database(database_name)

    def run(self) -> None:
        """
        Main entry point for the thread.
        Initializes the IntegratedBot and starts the asyncio loop.
        """
        # Sempre recria o bot ao iniciar a thread para garantir um loop limpo
        self._bot = IntegratedBot(self.signals, self._database_name)

        try:
            if not self._token:
                logging.error("Token not provided.")
                return

            # run() do discord.py é bloqueante, o que é perfeito para QThread.run()
            self._bot.run(self._token)

        except LoginFailure:
            self.signals.login_failure.emit()
            logging.error("Login failed: Invalid Token.")
        except Exception as e:
            logging.critical(f"Critical Bot Error: {e}")
        finally:
            # Limpeza ao encerrar
            self._bot = None

    def groups(self) -> Dict[int, discord.Guild]:
        """
        Retrieves the current guilds safely.

        Returns:
            Dict[int, discord.Guild]: Dictionary of guilds or empty dict if bot not ready.
        """
        if self._bot and self._bot.is_ready():
            # Nota: Acessar .guilds de outra thread é tecnicamente arriscado,
            # mas para leitura simples geralmente funciona em Python (GIL).
            # O ideal seria emitir isso via sinal, mas para getters síncronos, mantemos assim.
            return {guild.id: guild for guild in self._bot.guilds}
        return {}

    def get_bot_id(self) -> Optional[int]:
        """
        Retrieves the bot's user ID safely.

        Returns:
            Optional[int]: The bot's ID or None if not ready.
        """
        if self._bot and self._bot.is_ready() and self._bot.user:
            return self._bot.user.id
        return None

    def leave_group(self, group_id: int) -> None:
        """
        Schedules a task to leave a guild in the bot's async loop safely.

        Args:
            group_id (int): The ID of the guild to leave.
        """
        if not self._bot or not self._bot.loop.is_running():
            return

        guild = self._bot.get_guild(group_id)
        if guild:
            # THREAD SAFETY: Usa run_coroutine_threadsafe para injetar no loop
            asyncio.run_coroutine_threadsafe(
                self._bot.leave_guild(guild), self._bot.loop
            )

    def close(self) -> None:
        """
        Schedules the bot closure safely from the main thread.
        """
        if self._bot and not self._bot.is_closed() and self._bot.loop.is_running():
            # THREAD SAFETY: Injeta o comando de fechar no loop do bot
            future = asyncio.run_coroutine_threadsafe(self._bot.close(), self._bot.loop)
            # Opcional: aguardar o futuro se quiser travar a GUI até fechar,
            # mas geralmente deixamos fechar em background.
