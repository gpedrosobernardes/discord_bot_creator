import locale
import sys

from PySide6.QtCore import QTranslator
from PySide6.QtNetwork import QLocalServer, QLocalSocket
from PySide6.QtWidgets import QApplication, QMessageBox

from source.core.settings import Settings


class BaseApplication(QApplication):
    def __init__(self):
        super().__init__(sys.argv)

        # Verificar instância única
        self._server_name = "DiscordBotCreatorSingleInstance"
        self._local_server = None

        if not self._check_single_instance():
            # Se já existe uma instância, mostrar mensagem e sair
            QMessageBox.warning(
                None,
                "Discord Bot Creator",
                "A aplicação já está em execução.",
            )
            sys.exit(0)

        self.setQuitOnLastWindowClosed(False)

        self.user_settings = Settings()

        self.translator = QTranslator()
        lang = self.user_settings.value("language")
        self.translator.load(f"translations/build/{lang}.qm")
        self.installTranslator(self.translator)

        locale.setlocale(locale.LC_ALL, lang)

    def _check_single_instance(self) -> bool:
        """
        Verifica se já existe uma instância da aplicação em execução.
        Retorna True se esta é a primeira instância, False caso contrário.
        """
        # Tentar conectar a um servidor existente
        socket = QLocalSocket()
        socket.connectToServer(self._server_name)

        # Se conseguiu conectar, significa que já existe uma instância
        if socket.waitForConnected(500):
            # Enviar sinal para a instância existente mostrar a janela
            socket.write(b"show")
            socket.waitForBytesWritten(1000)
            socket.disconnectFromServer()
            return False

        # Criar servidor local para esta instância
        self._local_server = QLocalServer()
        # Remover servidor anterior se existir (cleanup de crashes)
        QLocalServer.removeServer(self._server_name)

        if not self._local_server.listen(self._server_name):
            return False

        # Conectar sinal para receber conexões
        self._local_server.newConnection.connect(self._on_new_connection)
        return True

    def _on_new_connection(self):
        """
        Chamado quando outra instância tenta se conectar.
        """
        client_socket = self._local_server.nextPendingConnection()
        if client_socket:
            client_socket.waitForReadyRead(1000)
            data = client_socket.readAll().data()

            if data == b"show":
                # Mostrar e ativar a janela principal
                self._show_main_window()

            client_socket.disconnectFromServer()

    def _show_main_window(self):
        """
        Método para ser sobrescrito pela classe filha para mostrar a janela principal.
        """
        pass
