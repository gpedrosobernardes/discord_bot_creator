import json
from functions import load_json, save_json
import interfaces.paths as path
import tkinter as tk

class MainCommands:
    def load_info_messages(self):
        try:
            all_messages = load_json(path.message_and_reply)
        except json.decoder.JSONDecodeError:
            pass
        else:
            for x in all_messages.keys():
                self.todas_mensagens.insert(tk.END, x)

    def edit_message(self):
        lista_nomes = self.todas_mensagens.get(0, tk.END)
        selecionado:str = lista_nomes[self.todas_mensagens.curselection()[0]]
        nm.main(self, selecionado)

    def remove_message(self):
        lista_nomes = self.todas_mensagens.get(0, tk.END)
        selecionado = self.todas_mensagens.curselection()[0]
        nome_selecionado:str = lista_nomes[selecionado]
        self.todas_mensagens.delete(selecionado)
        message_and_reply_json = load_json(path.message_and_reply)
        del message_and_reply_json[nome_selecionado]
        save_json(path.message_and_reply, message_and_reply_json)

    def refresh_messages(self):
        self.todas_mensagens.delete(0,tk.END)
        MainCommands.load_info_messages(self)