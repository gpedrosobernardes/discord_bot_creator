import tkinter as tk
from interfaces.fonts import *
from functions import load_json
from interfaces.newmessage.main import NewMessage as nm

class FrameEsquerdo:
    def main(self):
        frame_esquerdo_mensagens = tk.Frame(
            master = self.camada_1,
        )
        editar_mensagem_button = tk.Button(
            master = frame_esquerdo_mensagens,
            text = 'Editar mensagem',
            font = arial,
            relief = tk.FLAT,
            command = lambda: FrameEsquerdo.__edit_message(self)
        )
        self.todas_mensagens = tk.Listbox(
            master = frame_esquerdo_mensagens,
            relief = tk.FLAT,
            height = 20
        )
        FrameEsquerdo.__load_info_messages(self)
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
        self.todas_mensagens.pack()
        editar_mensagem_button.pack()
        adicionar_mensagem_button.pack()

    def __load_info_messages(self):
        all_messages = load_json('source/message and reply.json')
        for x in all_messages.keys():
            self.todas_mensagens.insert(tk.END, x)

    def __edit_message(self):
        lista_nomes = self.todas_mensagens.get(0, tk.END)
        selecionado:str = lista_nomes[self.todas_mensagens.curselection()[0]]
        nm.main(self, selecionado)