from json import JSONDecodeError
from threading import Thread

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QTextEdit,
    QListWidget,
    QLabel,
)

from bot import IntegratedBot
from core.config import instance as config
from functions import load_json, save_json
from interfaces import paths
from interfaces.classes.qpassword import QPassword
from interfaces.newmessage.main import EditMessageWindow, NewMessageWindow


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bot Discord Easy Creator")
        self.setMinimumSize(800, 600)
        self.setWindowIcon(QIcon("source/icons/window-icon.svg"))

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
        self.logs_text_edit = QTextEdit()
        self.logs_text_edit.setPlaceholderText("No momento não há logs.")
        self.logs_text_edit.setReadOnly(True)

        # Command Entry Frame
        self.cmd_line_edit = QLineEdit()
        self.cmd_line_edit.setPlaceholderText("Cmd")
        self.cmd_line_edit.returnPressed.connect(self.entry_command)

        # Token Entry Frame
        self.token_widget = QPassword()
        self.token_widget.line_edit.setText(config.get("token"))
        self.token_widget.line_edit.returnPressed.connect(self.update_token)

        # Execute Bot Button
        self.exec_bot_button = QPushButton("Executar o bot")
        self.exec_bot_button.clicked.connect(self.init_bot)

        # Adding Widgets to Right Frame
        right_frame.addWidget(self.logs_text_edit)
        right_frame.addWidget(self.cmd_line_edit)
        right_frame.addWidget(QLabel("Token:"))
        right_frame.addWidget(self.token_widget)
        right_frame.addWidget(self.exec_bot_button)

        # Left Frame for Messages
        left_frame = QVBoxLayout()

        edit_messages_button = QPushButton("Editar mensagem")
        edit_messages_button.clicked.connect(self.edit_message)

        self.messages_list_widget = QListWidget()

        add_message_button = QPushButton("Adicionar mensagem")
        add_message_button.clicked.connect(self.open_new_message_window)

        remove_message_button = QPushButton("Apagar mensagem")
        remove_message_button.clicked.connect(self.remove_message)

        remove_all_message_button = QPushButton("Apagar todas mensagens")
        remove_all_message_button.clicked.connect(self.remove_all_message)

        # Adding Widgets to Left Frame
        left_frame.addWidget(self.messages_list_widget)
        left_frame.addWidget(add_message_button)
        left_frame.addWidget(edit_messages_button)
        left_frame.addWidget(remove_message_button)
        left_frame.addWidget(remove_all_message_button)

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
        cmd = self.cmd_line_edit.text()
        if cmd in ["cls", "clear"]:
            self.logs_text_edit.clear()
            self.cmd_line_edit.clear()

    def update_token(self):
        """Updates the token in the "config.json" file and in the interface."""
        token = self.token_widget.line_edit.text()
        config.set("token", token)
        config.save()
        # Update label with new token (assuming you have a QLabel for it)

    def edit_message(self):
        """Opens the NewMessage interface and loads saved information."""
        names = [
            self.messages_list_widget.item(i).text()
            for i in range(self.messages_list_widget.count())
        ]
        try:
            selected_message = names[self.messages_list_widget.currentRow()]
            self.message_window = EditMessageWindow(self, selected_message)
            self.message_window.janela.exec()
        except IndexError:
            pass

    def remove_message(self):
        """Removes the selected message from the messages list and deletes it from "message and reply.json"."""
        selected_row = self.messages_list_widget.currentRow()
        if selected_row >= 0:
            selected_message = self.messages_list_widget.item(selected_row).text()
            self.messages_list_widget.takeItem(selected_row)
            message_and_reply_json = load_json(paths.message_and_reply)
            del message_and_reply_json[selected_message]
            save_json(paths.message_and_reply, message_and_reply_json)

    def remove_all_message(self):
        """Removes all messages from the list."""
        self.messages_list_widget.clear()
        save_json(paths.message_and_reply, {})

    def load_info_messages(self):
        """Loads all messages from "message and reply.json" and inserts them into the messages list."""
        try:
            all_messages = load_json(paths.message_and_reply)
            for message_name in all_messages.keys():
                self.messages_list_widget.addItem(message_name)
        except JSONDecodeError:
            pass

    def log(self, message):
        self.logs_text_edit.insertPlainText(message)

    def change_init_bot_button(self):
        self.exec_bot_button.setText("Desligar o bot")
        self.exec_bot_button.clicked.disconnect(self.init_bot)
        self.exec_bot_button.clicked.connect(self.turnoff_bot)

    def turnoff_bot(self):
        self.bot.client.loop.create_task(self.bot.client.close())
        self.bot_thread.join()
        self.exec_bot_button.setText("Executar o bot")
        self.exec_bot_button.clicked.disconnect(self.turnoff_bot)
        self.exec_bot_button.clicked.connect(self.init_bot)
        self.log("Bot desligado!")
