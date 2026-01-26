import json

from PySide6.QtCore import QObject, Signal, QUrl, QByteArray
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply


class BotIdentityFetcher(QObject):
    """
    Helper class to fetch bot identity using QNetworkAccessManager.
    """
    info_received = Signal(str, QByteArray)
    failed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._manager = QNetworkAccessManager(self)

    def fetch(self, token: str):
        """
        Starts the fetch process for the given token.
        """
        request = QNetworkRequest(QUrl("https://discord.com/api/v10/users/@me"))
        request.setRawHeader(b"Authorization", f"Bot {token}".encode())
        reply = self._manager.get(request)
        reply.finished.connect(lambda: self._on_user_info_received(reply))

    def _on_user_info_received(self, reply: QNetworkReply):
        reply.deleteLater()
        if reply.error() != QNetworkReply.NetworkError.NoError:
            self.failed.emit()
            return

        try:
            data = json.loads(reply.readAll().data().decode())
            username = data.get("username")
            user_id = data.get("id")
            avatar_hash = data.get("avatar")

            if user_id and avatar_hash:
                self._fetch_avatar(user_id, avatar_hash, username)
            else:
                self.info_received.emit(username, QByteArray())
        except Exception as e:
            print(f"Error parsing bot info: {e}")
            self.failed.emit()

    def _fetch_avatar(self, user_id: str, avatar_hash: str, username: str):
        url = QUrl(f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_hash}.png")
        reply = self._manager.get(QNetworkRequest(url))
        reply.finished.connect(lambda: self._on_avatar_received(reply, username))

    def _on_avatar_received(self, reply: QNetworkReply, username: str):
        reply.deleteLater()
        if reply.error() != QNetworkReply.NetworkError.NoError:
            # Return username even if avatar fails
            self.info_received.emit(username, QByteArray())
            return

        self.info_received.emit(username, reply.readAll())
