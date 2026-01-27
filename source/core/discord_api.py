import json
from typing import Optional

from PySide6.QtCore import QObject, Signal, QUrl, QByteArray
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply


class DiscordAPIClient(QObject):
    """
    Cliente para interagir com a API REST do Discord.
    """
    # Sinais
    bot_identity_received = Signal(str, str, QByteArray)  # username, id, avatar_bytes
    guilds_received = Signal(list)  # lista de dicts
    channels_received = Signal(list)  # lista de dicts
    guild_icon_received = Signal(str, QByteArray) # guild_id, icon_bytes (NOVO)

    request_failed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._manager = QNetworkAccessManager(self)
        self._token: Optional[str] = None

    def set_token(self, token: str):
        self._token = token

    def _create_request(self, endpoint: str) -> QNetworkRequest:
        request = QNetworkRequest(QUrl(f"https://discord.com/api/v10{endpoint}"))

        # OBRIGATÓRIO: User-Agent para evitar erro 403
        user_agent = b"DiscordBot (https://github.com/gustavopedrosob/discord_bot_creator, 1.0)"
        request.setRawHeader(b"User-Agent", user_agent)

        if self._token:
            request.setRawHeader(b"Authorization", f"Bot {self._token}".encode())
        request.setRawHeader(b"Content-Type", b"application/json")
        return request

    # --- Buscas ---

    def fetch_bot_identity(self):
        if not self._token: return
        reply = self._manager.get(self._create_request("/users/@me"))
        reply.finished.connect(lambda: self._on_identity_response(reply))

    def fetch_guilds(self):
        if not self._token: return
        reply = self._manager.get(self._create_request("/users/@me/guilds"))
        reply.finished.connect(lambda: self._on_guilds_response(reply))

    def fetch_channels(self, guild_id: str):
        if not self._token: return
        reply = self._manager.get(self._create_request(f"/guilds/{guild_id}/channels"))
        reply.finished.connect(lambda: self._on_channels_response(reply))

    def fetch_guild_icon(self, guild_id: str, icon_hash: str):
        """Busca o ícone do servidor."""
        # URL da CDN do Discord para ícones
        url = QUrl(f"https://cdn.discordapp.com/icons/{guild_id}/{icon_hash}.png")

        # Requisição simples (CDN geralmente não precisa de Auth header, mas User-Agent é bom)
        request = QNetworkRequest(url)
        request.setRawHeader(b"User-Agent", b"DiscordBot (https://github.com/gustavopedrosob/discord_bot_creator, 1.0)")

        reply = self._manager.get(request)
        reply.finished.connect(lambda: self._on_guild_icon_response(reply, guild_id))

    # --- Respostas ---

    def _on_identity_response(self, reply: QNetworkReply):
        # ... (mesmo código da resposta anterior) ...
        reply.deleteLater()
        data = self._parse_reply(reply)
        if data:
            self._fetch_avatar(data.get("id"), data.get("avatar"), data.get("username"))

    def _on_guilds_received_internal(self, reply):
        # ... lógica interna se precisar ...
        pass

    def _on_guilds_response(self, reply: QNetworkReply):
        reply.deleteLater()
        data = self._parse_reply(reply)
        if isinstance(data, list):
            self.guilds_received.emit(data)

    def _on_channels_response(self, reply: QNetworkReply):
        reply.deleteLater()
        data = self._parse_reply(reply)
        if isinstance(data, list):
            self.channels_received.emit(data)

    def _on_guild_icon_response(self, reply: QNetworkReply, guild_id: str):
        reply.deleteLater()
        if reply.error() != QNetworkReply.NetworkError.NoError:
            # Falha silenciosa ou log
            return
        self.guild_icon_received.emit(guild_id, reply.readAll())

    # ... (métodos _parse_reply, _fetch_avatar e _on_avatar_received iguais ao anterior) ...
    def _parse_reply(self, reply: QNetworkReply):
        status_code = reply.attribute(QNetworkRequest.Attribute.HttpStatusCodeAttribute)
        if reply.error() != QNetworkReply.NetworkError.NoError:
            err_msg = f"Erro API ({status_code}): {reply.errorString()}"
            self.request_failed.emit(err_msg)
            return None
        try:
            return json.loads(reply.readAll().data().decode())
        except:
            return None

    def _fetch_avatar(self, user_id: str, avatar_hash: str, username: str):
        url = QUrl(f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_hash}.png")
        reply = self._manager.get(QNetworkRequest(url))
        reply.finished.connect(lambda: self._on_avatar_received(reply, username, user_id))

    def _on_avatar_received(self, reply: QNetworkReply, username: str, user_id: str):
        reply.deleteLater()
        data = reply.readAll() if reply.error() == QNetworkReply.NetworkError.NoError else QByteArray()
        self.bot_identity_received.emit(username, user_id, data)