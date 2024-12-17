from json import JSONDecodeError
from threading import Thread
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QTextEdit, QListWidget
)
from core.config import instance as config
from bot import IntegratedBot
from interfaces.fonts import *
from interfaces import paths
from functions import load_json, save_json
from interfaces.newmessage.main import EditMessageWindow, NewMessageWindow


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Bot Discord Easy Creator')
        self.setMinimumSize(800, 600)

        self.message_window = None
        self.bot = IntegratedBot(self)
        self.bot_thread = Thread(target=self.bot.run)

        # Central Widget and Layouts
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        # Right Frame for Bot Controls
        right_frame = QVBoxLayout()
        self.log_do_bot = QTextEdit()
        self.log_do_bot.setFont(arial)
        self.log_do_bot.setReadOnly(True)

        # Command Entry Frame
        command_frame = QHBoxLayout()
        self.entrada_comandos = QLineEdit()
        self.entrada_comandos.setFont(arial)
        command_button = QPushButton('>')
        command_button.clicked.connect(self.entry_command)

        command_frame.addWidget(self.entrada_comandos)
        command_frame.addWidget(command_button)

        # Token Entry Frame
        token_frame = QHBoxLayout()
        self.inserir_token = QLineEdit()
        token_button = QPushButton('>')
        token_button.clicked.connect(self.update_token)

        token_frame.addWidget(self.inserir_token)
        token_frame.addWidget(token_button)

        # Execute Bot Button
        self.executar_o_bot = QPushButton('Executar o bot')
        self.executar_o_bot.clicked.connect(self.init_bot)

        # Adding Widgets to Right Frame
        right_frame.addWidget(self.log_do_bot)
        right_frame.addLayout(command_frame)
        right_frame.addLayout(token_frame)

        self.token_label = QLabel(f'Token:\n{self.get_token()}')

        right_frame.addWidget(self.token_label)
        right_frame.addWidget(self.executar_o_bot)

        # Left Frame for Messages
        left_frame = QVBoxLayout()

        editar_mensagem_button = QPushButton('Editar mensagem')
        editar_mensagem_button.clicked.connect(self.edit_message)

        self.todas_mensagens = QListWidget()

        adicionar_mensagem_button = QPushButton('Adicionar mensagem')
        adicionar_mensagem_button.clicked.connect(self.open_new_message_window)

        remover_mensagem_button = QPushButton('Apagar mensagem')
        remover_mensagem_button.clicked.connect(self.remove_message)

        remover_todas_mensagens_button = QPushButton('Apagar todas mensagens')
        remover_todas_mensagens_button.clicked.connect(self.remove_all_message)

        # Adding Widgets to Left Frame
        left_frame.addWidget(self.todas_mensagens)
        left_frame.addWidget(adicionar_mensagem_button)
        left_frame.addWidget(editar_mensagem_button)
        left_frame.addWidget(remover_mensagem_button)
        left_frame.addWidget(remover_todas_mensagens_button)

        main_layout.addLayout(left_frame)
        main_layout.addLayout(right_frame)

        self.load_info_messages()

    def open_new_message_window(self):
        if self.message_window:
            self.message_window.janela.reject()
        self.message_window = NewMessageWindow(self)
        self.message_window.janela.exec()

    @staticmethod
    def get_token():
        """Returns the current token saved in the "config.json" file."""
        return config.get("token")

    def init_bot(self):
        self.bot_thread.start()

    def entry_command(self):
        """Handles commands for the bot's log entry."""
        entrada = self.entrada_comandos.text()
        if entrada in ['/clear', '/limpar']:
            self.log_do_bot.clear()
            self.entrada_comandos.clear()

    def update_token(self):
        """Updates the token in the "config.json" file and in the interface."""
        token = self.inserir_token.text()
        self.token_label.setText(f'Token:\n{token}')
        config.set("token", token)
        config.save()
        # Update label with new token (assuming you have a QLabel for it)

    def edit_message(self):
        """Opens the NewMessage interface and loads saved information."""
        lista_nomes = [self.todas_mensagens.item(i).text() for i in range(self.todas_mensagens.count())]
        try:
            selecionado = lista_nomes[self.todas_mensagens.currentRow()]
            self.message_window = EditMessageWindow(self, selecionado)
            self.message_window.janela.exec()
        except IndexError:
            pass

    def remove_message(self):
        """Removes the selected message from the messages list and deletes it from "message and reply.json"."""
        selecionado = self.todas_mensagens.currentRow()
        if selecionado >= 0:
            nome_selecionado = self.todas_mensagens.item(selecionado).text()
            self.todas_mensagens.takeItem(selecionado)
            message_and_reply_json = load_json(paths.message_and_reply)
            del message_and_reply_json[nome_selecionado]
            save_json(paths.message_and_reply, message_and_reply_json)

    def remove_all_message(self):
        """Removes all messages from the list."""
        self.todas_mensagens.clear()
        save_json(paths.message_and_reply, {})

    def load_info_messages(self):
        """Loads all messages from "message and reply.json" and inserts them into the messages list."""
        try:
            all_messages = load_json(paths.message_and_reply)
            for x in all_messages.keys():
                self.todas_mensagens.addItem(x)
        except JSONDecodeError:
            pass

    def log(self, message):
        self.log_do_bot.insertPlainText(message)

    def change_init_bot_button(self):
        self.executar_o_bot.setText("Desligar o bot")
        self.executar_o_bot.clicked.disconnect(self.init_bot)
        self.executar_o_bot.clicked.connect(self.turnoff_bot)

    def turnoff_bot(self):
        self.bot.client.loop.create_task(self.bot.client.close())
        self.bot_thread.join()
        self.executar_o_bot.setText("Executar o bot")
        self.executar_o_bot.clicked.disconnect(self.turnoff_bot)
        self.executar_o_bot.clicked.connect(self.init_bot)
        self.log("Bot desligado!")