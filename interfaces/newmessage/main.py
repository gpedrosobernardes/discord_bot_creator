import re
import typing
from json import JSONDecodeError

import emoji
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QDialog,
    QGroupBox,
    QLabel,
    QFrame,
    QComboBox,
    QPushButton,
    QListWidget,
    QRadioButton,
    QSpinBox,
    QLineEdit,
)

import interfaces.paths as path
from functions import load_json, save_json, have_in
from interpreter.conditions import conditions_keys


class MessageWindow:
    def __init__(self, app):
        self.app = app
        self.name = None
        self.janela = QDialog()
        self.janela.setWindowIcon(QIcon("source/icons/window-icon.svg"))
        self.janela.setMinimumSize(800, 600)
        self.janela.setWindowTitle("Mensagem")

        left_layout = QVBoxLayout()
        mid_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        # Layouts
        frame_preenchimento = QFrame(self.janela)
        frame_preenchimento.setContentsMargins(10, 10, 10, 10)

        # Widgets
        self.name_text = QLabel("Nome:", frame_preenchimento)
        self.name_entry = QLineEdit(frame_preenchimento)

        expected_message_text = QLabel("Mensagem esperada", frame_preenchimento)
        self.expected_message = QLineEdit(frame_preenchimento)

        reply_text = QLabel("Resposta", frame_preenchimento)
        self.reply = QLineEdit(frame_preenchimento)

        reactions_text = QLabel("Reações", frame_preenchimento)
        self.reactions = QComboBox()
        self.reactions.addItems([""] + [v["en"] for v in emoji.EMOJI_DATA.values()])

        conditions_text = QLabel("Condições", frame_preenchimento)
        self.conditions = QComboBox()
        self.conditions.addItems([""] + conditions_keys)

        adicionar = QPushButton("Adicionar", frame_preenchimento)

        # Layout setup
        for widget in [
            self.name_text,
            self.name_entry,
            expected_message_text,
            self.expected_message,
            reply_text,
            self.reply,
            reactions_text,
            self.reactions,
            conditions_text,
            self.conditions,
        ]:
            left_layout.addWidget(widget)

        left_layout.addStretch()
        left_layout.addWidget(adicionar)

        # Listboxes setup
        frame_das_listas = QFrame(self.janela)

        listbox_conditions_text = QLabel("Condições", frame_das_listas)
        self.listbox_conditions = QListWidget(frame_das_listas)

        listbox_reactions_text = QLabel("Reações", frame_das_listas)
        self.listbox_reactions = QListWidget(frame_das_listas)

        listbox_messages_text = QLabel("Mensagens", frame_das_listas)
        self.listbox_messages = QListWidget(frame_das_listas)

        listbox_replies_text = QLabel("Respostas", frame_das_listas)
        self.listbox_replies = QListWidget(frame_das_listas)

        remover = QPushButton("Remover", frame_das_listas)
        remover_todos = QPushButton("Remover todos", frame_das_listas)

        # Adding widgets to layout
        for widget in [
            listbox_conditions_text,
            self.listbox_conditions,
            listbox_replies_text,
            self.listbox_replies,
            listbox_messages_text,
            self.listbox_messages,
            listbox_reactions_text,
            self.listbox_reactions,
            remover,
            remover_todos,
        ]:
            mid_layout.addWidget(widget)

        frame_options = QFrame(self.janela)

        # Pin or delete options using QCheckBox instead of QRadioButton
        self.group_pin_or_del = QGroupBox("Tratativa", frame_options)
        layout_pin_or_del = QVBoxLayout(self.group_pin_or_del)

        self.pin_checkbox = QRadioButton("Fixar")

        layout_pin_or_del.addWidget(self.pin_checkbox)
        self.delete_checkbox = QRadioButton("Remover")
        layout_pin_or_del.addWidget(self.delete_checkbox)

        # Kick or ban options using QCheckBox instead of QRadioButton
        self.group_kick_or_ban = QGroupBox("Penalidade", frame_options)
        layout_kick_or_ban = QVBoxLayout(self.group_kick_or_ban)

        self.kick_checkbox = QRadioButton("Expulsar")
        layout_kick_or_ban.addWidget(self.kick_checkbox)
        self.ban_checkbox = QRadioButton("Banir")
        layout_kick_or_ban.addWidget(self.ban_checkbox)

        # Where to reply options using QCheckBox instead of QRadioButton
        self.group_where_reply = QGroupBox("Onde responder", frame_options)
        layout_frame_where_reply = QVBoxLayout(self.group_where_reply)

        self.group_checkbox = QRadioButton("Grupo")
        self.group_checkbox.setObjectName("group")
        layout_frame_where_reply.addWidget(self.group_checkbox)
        self.private_checkbox = QRadioButton("Privada")
        self.private_checkbox.setObjectName("private")
        layout_frame_where_reply.addWidget(self.private_checkbox)

        # Where to react options using QCheckBox instead of QRadioButton
        self.group_where_react = QGroupBox("Onde reagir")
        layout_where_reaction = QVBoxLayout(self.group_where_react)

        self.bot_checkbox = QRadioButton("Bot")
        self.bot_checkbox.setObjectName("bot")
        layout_where_reaction.addWidget(self.bot_checkbox)
        self.author_checkbox = QRadioButton("Autor")
        self.author_checkbox.setObjectName("author")
        layout_where_reaction.addWidget(self.author_checkbox)

        delay_label = QLabel("Delay:")
        self.delay = QSpinBox()

        # Save and quit button
        save_and_quit_button = QPushButton("Salvar e sair", frame_options)

        for widget in (
            self.group_pin_or_del,
            self.group_kick_or_ban,
            self.group_where_reply,
            self.group_where_react,
            delay_label,
            self.delay,
        ):
            right_layout.addWidget(widget)

        right_layout.addStretch()
        right_layout.addWidget(save_and_quit_button)

        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout)
        main_layout.addLayout(mid_layout)
        main_layout.addLayout(right_layout)

        self.janela.setLayout(main_layout)

        remover.clicked.connect(self.remove_all_selected_on_listbox)
        remover_todos.clicked.connect(self.remove_all_on_listbox)
        save_and_quit_button.clicked.connect(self.on_save_and_quit)
        adicionar.clicked.connect(self.insert_any_on_listbox)

    def on_save_and_quit(self):
        self.save_and_quit()

    def on_save(self):
        self.save()

    @staticmethod
    def insert_on_listbox(
        listbox: QListWidget, entry: typing.Union[QLineEdit, QComboBox], limit: int = 0
    ):
        """insere um valor na listbox especificada e apaga o conteúdo da entry especificada,
        se um limite for especificado ele vai checar se o limite da listbox não foi atingido
        """
        value = entry.text() if isinstance(entry, QLineEdit) else entry.currentText()
        if value:
            tamanho_listbox = listbox.count()
            if not tamanho_listbox > limit or limit == 0:
                listbox.addItem(value)
                entry.clear()

    def insert_any_on_listbox(self):
        for listbox, entrada in zip(self.__all_listbox(), self.__all_entries()):
            # se for o reactions, no discord o limite de reações por mensagem é de 20,
            # ou seja, a gente precisa limitar a quantidade de reactions.
            self.insert_on_listbox(
                listbox, entrada, limit=19 if entrada == self.reactions else 0
            )

    def update_name(self):
        self.name = self.name_entry.text()
        self.name_entry.clear()
        self.name_text.setText(f"Nome: {self.name}")

    @staticmethod
    def remove_selected_on_listbox(listbox: QListWidget):
        """remove um item selecionado na listbox"""
        for item in listbox.selectedItems():
            listbox.takeItem(listbox.indexFromItem(item).row())

    def remove_all_selected_on_listbox(self):
        for listbox in self.__all_listbox():
            self.remove_selected_on_listbox(listbox)

    def remove_all_on_listbox(self):
        """remove todos os items em todas listbox"""
        for listbox in self.__all_listbox():
            listbox: QListWidget
            listbox.clear()

    def __all_listbox(self):
        return (
            self.listbox_messages,
            self.listbox_replies,
            self.listbox_reactions,
            self.listbox_conditions,
        )

    def __all_entries(self):
        return self.expected_message, self.reply, self.reactions, self.conditions

    def save(self):
        """salva toda a informação que o usuário preencheu na interface em forma de json, para que depois
        o interpretador do bot consiga interpretar"""
        try:
            dict_base = load_json(path.message_and_reply)
        except JSONDecodeError:
            name = "1"
            dict_base = dict()
        else:
            # talvez possamos passar essa responsabilidade para uma funcao apartada e no início da classe
            if not self.name:
                name = "1"
                chaves_dict_base = list(dict_base.keys())
                chaves_dict_base.reverse()
                for x in chaves_dict_base:
                    try:
                        chave = int(x)
                    except ValueError:
                        pass
                    else:
                        name = str(chave + 1)
                        break
            else:
                name = self.name
                if self.name:
                    name = self.name
                    del dict_base[self.name]

        # anti-bug
        self.name = name

        dict_base[name] = {}

        lista_expected_message = [
            self.listbox_messages.item(i).text()
            for i in range(self.listbox_messages.count())
        ]
        dict_base[name]["expected message"] = (
            lista_expected_message if not len(lista_expected_message) == 0 else None
        )

        lista_reply = [
            self.listbox_replies.item(i).text()
            for i in range(self.listbox_replies.count())
        ]
        dict_base[name]["reply"] = (
            list(map(lambda x: x.split("¨"), lista_reply))
            if have_in(lista_reply, "¨", reverse=True)
            else lista_reply if not len(lista_reply) == 0 else None
        )

        lista_reactions = [
            self.listbox_reactions.item(i).text()
            for i in range(self.listbox_reactions.count())
        ]
        dict_base[name]["reaction"] = (
            list(map(lambda x: re.findall(r":[a-zA-Z_0-9]+:", x), lista_reactions))
            if not len(lista_reactions) == 0
            else None
        )

        lista_conditions = [
            self.listbox_conditions.item(i).text()
            for i in range(self.listbox_conditions.count())
        ]
        dict_base[name]["conditions"] = (
            lista_conditions if not len(lista_conditions) == 0 else None
        )

        if self.pin_checkbox.isChecked():
            dict_base[name]["pin"] = True
        elif self.delete_checkbox.isChecked():
            dict_base[name]["delete"] = True

        selected_where_reply = self.__get_checked(self.group_where_reply)
        if selected_where_reply:
            dict_base[name]["where reply"] = selected_where_reply.objectName()

        selected_where_react = self.__get_checked(self.group_where_react)
        if selected_where_react:
            dict_base[name]["where reaction"] = selected_where_react.objectName()

        dict_base[name]["delay"] = self.delay.value()

        save_json(path.message_and_reply, dict_base)

    def save_and_quit(self):
        self.save()
        self.janela.destroy()

    @staticmethod
    def __get_checked(groupbox: QGroupBox):
        """Returns the checked radio button from the groupbox"""

        for child in groupbox.layout().children():
            child: QRadioButton
            if child.isChecked():
                return child


class EditMessageWindow(MessageWindow):
    def __init__(self, app, load):
        super().__init__(app)
        self.name = load
        self.name_entry.setText(self.name)
        self.name_entry.setEnabled(False)
        self.load_info()

    def load_info(self):
        if self.name:
            messages_json: dict = load_json(path.message_and_reply)
            todas_info: dict = messages_json[self.name]
            if "expected message" in todas_info:
                expected_message = todas_info["expected message"]
                if expected_message:
                    for x in expected_message:
                        self.listbox_messages.addItem(x)
            if "reply" in todas_info:
                reply = todas_info["reply"]
                if reply:
                    for x in reply:
                        (
                            self.listbox_replies.addItem("¨".join(x))
                            if type(x) == list
                            else self.listbox_replies.addItem(x)
                        )
            if "reaction" in todas_info:
                reaction = todas_info["reaction"]
                if reaction:
                    list(
                        map(
                            lambda x: self.listbox_reactions.addItem(" ".join(x)),
                            reaction,
                        )
                    )
            if "conditions" in todas_info:
                conditions = todas_info["conditions"]
                if conditions:
                    for x in conditions:
                        self.listbox_conditions.addItem(x)
            if "pin" in todas_info:
                pin = todas_info["pin"]
                if pin:
                    self.pin_checkbox.setChecked(True)
            if "delete" in todas_info:
                delete = todas_info["delete"]
                if delete:
                    self.delete_checkbox.setChecked(True)

            if "delay" in todas_info:
                delay = int(todas_info["delay"])
                self.delay.setValue(delay)

            if "where reply" in todas_info:
                where_reply = todas_info["where reply"]
                if where_reply == "group":
                    self.group_checkbox.setChecked(True)
                else:
                    self.private_checkbox.setChecked(True)

            if "where reaction" in todas_info:
                where_reaction = todas_info["where reaction"]
                if where_reaction == "author":
                    self.author_checkbox.setChecked(True)
                else:
                    self.bot_checkbox.setChecked(True)


class NewMessageWindow(MessageWindow):
    def on_save(self):
        super().on_save()
        self.app.add_message(self.name)

    def on_save_and_quit(self):
        super().on_save_and_quit()
        self.app.add_message(self.name)
