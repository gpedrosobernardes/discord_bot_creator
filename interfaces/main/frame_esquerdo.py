import tkinter as tk
from interfaces.fonts import *

class FrameEsquerdo:
    def main(self):
        frame_esquerdo_mensagens = tk.Frame(
            master = self.camada_1,
        )
        editar_mensagem_button = tk.Button(
            master = frame_esquerdo_mensagens,
            text = 'Editar mensagem',
            font = arial,
            relief = tk.FLAT
        )
        todas_mensagens = tk.Listbox(
            master = frame_esquerdo_mensagens,
            relief = tk.FLAT,
            height = 20
        )
        adicionar_mensagem_button = tk.Button(
            master = frame_esquerdo_mensagens,
            text = 'Adicionar mensagem',
            font = arial,
            command = lambda : nm.main(self),
            relief = tk.FLAT
        )

        frame_esquerdo_mensagens.grid(
            row = 1,
            column = 1
        )
        todas_mensagens.pack()
        editar_mensagem_button.pack()
        adicionar_mensagem_button.pack()


