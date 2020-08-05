import tkinter as tk
from functions import load_json, save_json
import interfaces.paths as path

class Commands:
    def insert_on_listbox(self, listbox:tk.Listbox, entry:tk.Entry):
        if not entry.get() == '':
            listbox.insert(tk.END, entry.get())
            entry.delete(0, tk.END)

    def insert_any_on_listbox(self):
        for x in range(4):
            entrada_atual:tk.Entry = self.lista_de_entradas[x]
            listbox_atual:tk.Listbox = self.lista_de_listbox[x]
            if not entrada_atual.get() == '':
                listbox_atual.insert(tk.END, entrada_atual.get())
                entrada_atual.delete(0, tk.END)

    def remove_selected_on_listbox(self):
        for lb in self.lista_de_listbox:
            lb:tk.Listbox
            if len(lb.curselection()) > 0:
                selecionados = lb.curselection()
                for x in selecionados:
                    lb.delete(x-selecionados.index(x))

    def remove_selected_on_currently_listbox(self, lb:tk.Listbox):
        selecionados = lb.curselection()
        for x in selecionados:
            lb.delete(x-selecionados.index(x))

    def remove_all_on_listbox(self):
        for x in self.lista_de_listbox:
            x:tk.Listbox
            x.delete(0,tk.END)

    def get_all_info_listbox(self) -> list:
        return list(map(lambda x: (x.get(0, tk.END)), self.lista_de_listbox))

    def save_all_json(self):
        dict_base = load_json(path.message_and_reply)
        chaves_dict_base = list(dict_base.keys())
        chaves_dict_base.reverse()
        if not self.load:
            for x in chaves_dict_base:
                try:
                    chave = int(x)
                except TypeError:
                    pass
                else:
                    name = str(chave+1)
                    break
            if not name:
                name = '1'
        else:
            name = self.load
        dict_base[name] = {}
        dict_base[name]['expected message'] = self.listbox_messages.get(0, tk.END)
        dict_base[name]['multi reply'] = self.listbox_replys.get(0, tk.END)
        dict_base[name]['reaction'] = self.listbox_reactions.get(0, tk.END)
        dict_base[name]['condictions'] = self.listbox_condictions.get(0, tk.END)
        save_json(path.message_and_reply, dict_base)