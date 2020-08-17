import tkinter as tk
from interfaces.fonts import *
from interfaces.newmessage.main import NewMessage as nm
from interfaces.commands.main import MainCommands as mc
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
            command = lambda: mc.edit_message(self),
            bg = color.azul_entrada,
            activebackground = color.azul_pressed,
        )
        self.todas_mensagens = tk.Listbox(
            master = frame_esquerdo_mensagens,
            relief = tk.FLAT,
            font = arial,
            height = 20,
            bg = color.azul_entrada,
            activestyle = 'none',
            selectbackground = color.azul_selecionado
        )
        adicionar_mensagem_button = tk.Button(
            master = frame_esquerdo_mensagens,
            text = 'Adicionar mensagem',
            font = arial,
            command = lambda : nm.main(self),
            relief = tk.FLAT,
            bg = color.azul_entrada,
            activebackground = color.azul_pressed,
        )
        remover_mensagem_button = tk.Button(
            master = frame_esquerdo_mensagens,
            text = 'Apagar mensagem',
            command = lambda : mc.remove_message(self),
            font = arial,
            relief = tk.FLAT,
            bg = color.azul_entrada,
            activebackground = color.azul_pressed,
        )
        remover_todas_mensagens_button = tk.Button(
            master = frame_esquerdo_mensagens,
            text = 'Apagar todas mensagens',
            command = lambda : mc.remove_all_message(self),
            font = arial,
            relief = tk.FLAT,
            bg = color.azul_entrada,
            activebackground = color.azul_pressed,
        )
        frame_esquerdo_mensagens.pack(
            side = tk.LEFT,
            fill = tk.Y,
        )
        self.todas_mensagens.pack(
            pady = 5,
            fill = tk.X
        )
        editar_mensagem_button.pack(
            pady = 5,
            fill = tk.X
        )
        adicionar_mensagem_button.pack(
            pady = 5,
            fill = tk.X
        )
        remover_mensagem_button.pack(
            pady = 5,
            fill = tk.X
        )
        remover_todas_mensagens_button.pack(
            pady = 5,
            fill = tk.X
        )