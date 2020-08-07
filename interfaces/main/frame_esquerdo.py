import tkinter as tk
from interfaces.fonts import *
from interfaces.newmessage.main import NewMessage as nm
from interfaces.commands.main import MainCommands
import interfaces.paths as path
import interfaces.colors as color

class FrameEsquerdo:
    def main(self):
        frame_esquerdo_mensagens = tk.Frame(
            master = self.camada_1,
            bg = color.azul_frame,
            borderwidth = 10
        )
        editar_mensagem_button = tk.Button(
            master = frame_esquerdo_mensagens,
            text = 'Editar mensagem',
            font = arial,
            relief = tk.FLAT,
            command = lambda: MainCommands.edit_message(self),
            bg = color.azul_entrada
        )
        self.todas_mensagens = tk.Listbox(
            master = frame_esquerdo_mensagens,
            relief = tk.FLAT,
            height = 20,
            bg = color.azul_entrada
        )
        MainCommands.load_info_messages(self)
        adicionar_mensagem_button = tk.Button(
            master = frame_esquerdo_mensagens,
            text = 'Adicionar mensagem',
            font = arial,
            command = lambda : nm.main(self),
            relief = tk.FLAT,
            bg = color.azul_entrada
        )
        remover_mensagem_button = tk.Button(
            master = frame_esquerdo_mensagens,
            text = 'Remover mensagem',
            command = lambda : MainCommands.remove_message(self),
            font = arial,
            relief = tk.FLAT,
            bg = color.azul_entrada,
        )
        frame_esquerdo_mensagens.grid(
            row = 1,
            column = 1,
            padx = 50
        )
        self.todas_mensagens.pack(
            pady = 10
        )
        editar_mensagem_button.pack()
        adicionar_mensagem_button.pack(
            pady = 10
        )
        remover_mensagem_button.pack()