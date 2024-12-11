import tkinter as tk
from json import JSONDecodeError
from threading import Thread
from core.config import instance as config
import interfaces.colors as color
from bot import IntegratedBot
from interfaces.fonts import *
from interfaces import paths
from functions import load_json, save_json


from interfaces.newmessage.main import EditMessageWindow, NewMessageWindow


class Main(tk.Tk):
    def __init__(self):
        super().__init__()
        self.iconbitmap(paths.interface_logo)
        self.title('Bot Discord Easy Creator')
        self.message_window = None
        self.bot = IntegratedBot(self)
        self.bot_thread = Thread(target=self.bot.run)
        
        self.config(
            bg = color.azul_escuro,
        )
        self.bot_is_running = False
        self.new_name = None

        self.minsize(
            width = 810,
            height = 600
        )

        self.camada_1 = tk.Frame(
            master = self,
            bg = color.azul_escuro
        )
        self.camada_2 = tk.Frame(
            master = self,
        )
        self.camada_1.pack(
            fill = tk.BOTH,
            expand = 1
        )

        frame_direito_bot = tk.Frame(
            master=self.camada_1,
            bg=color.azul_frame,
            borderwidth=10
        )
        self.log_do_bot = tk.Text(
            master=frame_direito_bot,
            font=arial,
            width=50,
            bg=color.azul_entrada,
            relief=tk.FLAT,
            state=tk.DISABLED,
            selectbackground=color.azul_selecionado
        )
        frame_entrada_comandos = tk.Frame(
            master=frame_direito_bot,
            bg=color.azul_frame
        )
        self.entrada_comandos = tk.Entry(
            master=frame_entrada_comandos,
            font=arial,
            bg=color.azul_entrada,
            # width = 48,
            relief=tk.FLAT
        )
        sep_entrada_comandos = tk.Frame(
            master=frame_entrada_comandos,
            width=5,
            bg=color.azul_frame,
        )
        button_entrada_comandos = tk.Button(
            master=frame_entrada_comandos,
            font=('Arial', 8),
            text='>',
            command=lambda: self.entry_command(),
            bg=color.azul_entrada,
            relief=tk.FLAT,
            activebackground=color.azul_pressed,
        )
        frame_inserir_token = tk.Frame(
            master=frame_direito_bot,
            bg=color.azul_frame
        )
        self.inserir_token = tk.Entry(
            master=frame_inserir_token,
            bg=color.azul_entrada,
            relief=tk.FLAT,
            # validatecommand=(
            # frame_inserir_token.register(self.validate_token), '%P'),
            validate="key"
        )
        sep_inserir_token = tk.Frame(
            master=frame_inserir_token,
            bg=color.azul_frame,
            width=5
        )
        self.button_inserir_token = tk.Button(
            master=frame_inserir_token,
            bg=color.azul_entrada,
            font=('Arial', 7),
            relief=tk.FLAT,
            text='>',
            command=lambda: self.update_token(),
            activebackground=color.azul_pressed,
        )
        self.token = self.get_token()
        self.token_atual = tk.Label(
            master=frame_direito_bot,
            text='Token:\n'
                 f'{self.token}',
            bg=color.azul_frame,
            justify=tk.LEFT

        )
        self.executar_o_bot = tk.Button(
            master=frame_direito_bot,
            text='Executar o bot',
            font=arial,
            relief=tk.FLAT,
            command=self.init_bot,
            bg=color.azul_entrada,
            activebackground=color.azul_pressed,
        )
        frame_direito_bot.pack(
            side=tk.RIGHT,
            fill=tk.Y
        )
        self.log_do_bot.grid(
            row=1,
            column=1,
            sticky=tk.W
        )
        frame_entrada_comandos.grid(
            row=2,
            column=1,
            sticky=tk.W + tk.E,
            pady=5
        )
        self.entrada_comandos.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=1
        )
        sep_entrada_comandos.pack(
            side=tk.LEFT,
        )
        button_entrada_comandos.pack(
            side=tk.LEFT,
        )
        self.token_atual.grid(
            row=3,
            column=1,
            sticky=tk.W
        )
        frame_inserir_token.grid(
            row=4,
            column=1,
            sticky=tk.W + tk.E
        )
        self.inserir_token.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=1
        )
        sep_inserir_token.pack(
            side=tk.LEFT,
        )
        self.button_inserir_token.pack(
            side=tk.LEFT,
        )
        self.executar_o_bot.grid(
            row=5,
            column=1,
            pady=10,
            sticky=tk.E
        )

        self.entrada_comandos.bind('<Return>', lambda event: self.entry_command())
        self.inserir_token.bind('<Return>', lambda event: self.update_token())

        frame_esquerdo_mensagens = tk.Frame(
            master=self.camada_1,
            bg=color.azul_frame,
            borderwidth=10
        )
        editar_mensagem_button = tk.Button(
            master=frame_esquerdo_mensagens,
            text='Editar mensagem',
            font=arial,
            relief=tk.FLAT,
            command=lambda: self.edit_message(),
            bg=color.azul_entrada,
            activebackground=color.azul_pressed,
        )
        self.todas_mensagens = tk.Listbox(
            master=frame_esquerdo_mensagens,
            relief=tk.FLAT,
            font=arial,
            height=20,
            bg=color.azul_entrada,
            activestyle='none',
            selectbackground=color.azul_selecionado
        )
        adicionar_mensagem_button = tk.Button(
            master=frame_esquerdo_mensagens,
            text='Adicionar mensagem',
            font=arial,
            command=self.open_new_message_window,
            relief=tk.FLAT,
            bg=color.azul_entrada,
            activebackground=color.azul_pressed,
        )
        remover_mensagem_button = tk.Button(
            master=frame_esquerdo_mensagens,
            text='Apagar mensagem',
            command=lambda: self.remove_message(),
            font=arial,
            relief=tk.FLAT,
            bg=color.azul_entrada,
            activebackground=color.azul_pressed,
        )
        remover_todas_mensagens_button = tk.Button(
            master=frame_esquerdo_mensagens,
            text='Apagar todas mensagens',
            command=lambda: self.remove_all_message(),
            font=arial,
            relief=tk.FLAT,
            bg=color.azul_entrada,
            activebackground=color.azul_pressed,
        )
        frame_esquerdo_mensagens.pack(
            side=tk.LEFT,
            fill=tk.Y,
        )
        self.todas_mensagens.pack(
            pady=5,
            fill=tk.X
        )
        editar_mensagem_button.pack(
            pady=5,
            fill=tk.X
        )
        adicionar_mensagem_button.pack(
            pady=5,
            fill=tk.X
        )
        remover_mensagem_button.pack(
            pady=5,
            fill=tk.X
        )
        remover_todas_mensagens_button.pack(
            pady=5,
            fill=tk.X
        )

        self.load_info_messages()

    def open_new_message_window(self):
        if self.message_window:
            self.message_window.janela.destroy()
        self.message_window = NewMessageWindow(self)

    # @staticmethod
    # def validate_token(P):
    #     if re.search(
    #             r'^[a-z0-9]{0,24}\.[a-z0-9]{0,6}\.[a-z0-9\-_]{0,27}$|^[a-z0-9]{0,24}\.[a-z0-9]{0,6}$|^[a-z0-9]{0,24}$',
    #             P, flags=re.IGNORECASE):
    #         return True
    #     else:
    #         return False

    @staticmethod
    def get_token():
        """retorna o token atual salvo no arquivo "config.json"."""
        return config.get("token")

    def init_bot(self):
        self.bot_thread.start()

    def change_init_bot_button(self):
        self.executar_o_bot.config(command=self.turnoff_bot, text="Desligar o bot")

    def turnoff_bot(self):
        pass

    def entry_command(self):
        """Responsável por definir comandos para a entry do log do bot."""
        entrada:str = self.entrada_comandos.get()
        if entrada in ['/clear', '/limpar']:
            self.log_do_bot['state'] = tk.NORMAL
            self.log_do_bot.delete("0.0", tk.END)
            self.log_do_bot['state'] = tk.DISABLED
            self.entrada_comandos.delete(0, tk.END)

    def update_token(self):
        """atualiza o token no arquivo "config.json" e na interface."""

        token:str = self.inserir_token.get()
        self.inserir_token.delete(0, tk.END)
        config.set("token", token)
        config.save()
        self.token_atual['text'] = f'Seu token atual é:\n{token}'

    def edit_message(self):
        """abre a interface NewMessage e carrega as informações salvas"""
        lista_nomes = self.todas_mensagens.get(0, tk.END)
        try:
            selecionado:str = lista_nomes[self.todas_mensagens.curselection()[0]]
        except IndexError:
            pass
        else:
            self.message_window = EditMessageWindow(self, selecionado)

    def add_message(self, message: str):
        self.todas_mensagens.insert(tk.END, message)

    def remove_message(self):
        """remove a mensagem selecionada do listbox de mensagens e a deleta do arquivo "message and
        reply.json"."""
        lista_nomes = self.todas_mensagens.get(0, tk.END)
        try:
            selecionado = self.todas_mensagens.curselection()[0]
        except IndexError:
            pass
        else:
            nome_selecionado:str = lista_nomes[selecionado]
            self.todas_mensagens.delete(selecionado)
            message_and_reply_json = load_json(paths.message_and_reply)
            del message_and_reply_json[nome_selecionado]
            save_json(paths.message_and_reply, message_and_reply_json)

    def remove_all_message(self):
        self.todas_mensagens.delete(0, tk.END)
        dict_to_save = dict()
        save_json(paths.message_and_reply, dict_to_save)

    def load_info_messages(self):
        """carrega todas as mensagens do arquivo "message and reply.json" e insere no listbox de
        mensagens."""
        try:
            all_messages = load_json(paths.message_and_reply)
        except JSONDecodeError:
            pass
        else:
            for x in all_messages.keys():
                self.todas_mensagens.insert(tk.END, x)

    def log(self, message):
        self.log_do_bot['state'] = tk.NORMAL
        self.log_do_bot.insert(tk.END, message)
        self.log_do_bot['state'] = tk.DISABLED