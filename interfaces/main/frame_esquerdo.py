import tkinter as tk
from interfaces.fonts import *
from functions import load_json, save_json
from interfaces.newmessage.main import NewMessage as nm
import interfaces.paths as path
import interfaces.colors as color
import json

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
            command = lambda: FrameEsquerdo.__edit_message(self),
            bg = color.azul_entrada
        )
        self.todas_mensagens = tk.Listbox(
            master = frame_esquerdo_mensagens,
            relief = tk.FLAT,
            height = 20,
            bg = color.azul_entrada
        )
        FrameEsquerdo.__load_info_messages(self)
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
            command = lambda : FrameEsquerdo.__remove_message(self),
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

    def __load_info_messages(self):
        try:
            all_messages = load_json(path.message_and_reply)
        except json.decoder.JSONDecodeError:
            pass
        else:
            for x in all_messages.keys():
                self.todas_mensagens.insert(tk.END, x)

    def __edit_message(self):
        lista_nomes = self.todas_mensagens.get(0, tk.END)
        selecionado:str = lista_nomes[self.todas_mensagens.curselection()[0]]
        nm.main(self, selecionado)

    def __remove_message(self):
        lista_nomes = self.todas_mensagens.get(0, tk.END)
        selecionado = self.todas_mensagens.curselection()[0]
        nome_selecionado:str = lista_nomes[selecionado]
        self.todas_mensagens.delete(selecionado)
        message_and_reply_json = load_json(path.message_and_reply)
        del message_and_reply_json[nome_selecionado]
        save_json(path.message_and_reply, message_and_reply_json)