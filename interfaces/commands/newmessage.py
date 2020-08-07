import tkinter as tk
from functions import load_json, save_json, have_in
import interfaces.paths as path
import json

class Commands:
    def insert_on_listbox(self, listbox:tk.Listbox, entry:tk.Entry, limit:int = 0):
        ''' insere um valor na listbox especificada e apaga o conteudo da entry especificada,
        se um limite for expecificado ele vai checar se o limite da listbox não foi atingido '''
        if not entry.get() == '':
            tamanho_listbox = len(set(listbox.get(0,tk.END)))
            if not tamanho_listbox > limit or limit == 0:
                listbox.insert(tk.END, entry.get())
                entry.delete(0, tk.END)

    def insert_any_on_listbox(self):
        for x in range(4):
            entrada_atual:tk.Entry = self.lista_de_entradas[x]
            listbox_atual:tk.Listbox = self.lista_de_listbox[x]
            if x == 2:
                # x = 2 se refere ao listbox de reactions no discord o limite de reações por mensagem é de 20
                # ou seja a gente precisa limitar a quantidade de reactions.
                Commands.insert_on_listbox(self, listbox_atual, entrada_atual, limit = 19)
            else:
                Commands.insert_on_listbox(self, listbox_atual, entrada_atual)

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
        try:
            dict_base = load_json(path.message_and_reply)
        except json.decoder.JSONDecodeError:
            name = '1'
            dict_base = dict()
        else:
            chaves_dict_base = list(dict_base.keys())
            chaves_dict_base.reverse()
            if not self.load:
                name = '1'
                for x in chaves_dict_base:
                    try:
                        chave = int(x)
                    except ValueError:
                        pass
                    else:
                        name = str(chave+1)
                        break
            else:
                name = self.load
        finally:
            dict_base[name] = {}

            lista_expected_message = self.listbox_messages.get(0, tk.END)
            dict_base[name]['expected message'] = lista_expected_message if not len(lista_expected_message) == 0 else None

            lista_reply = self.listbox_replys.get(0, tk.END)
            dict_base[name]['reply'] = list(map(lambda x: x.split('¨'), lista_reply)) if have_in(lista_reply, '¨', reverse = True) else lista_reply if not len(lista_reply) == 0 else None

            lista_reactions = self.listbox_reactions.get(0, tk.END)
            dict_base[name]['reaction'] = list(map(lambda x: x.split('¨'), lista_reactions)) if have_in(lista_reactions, '¨', reverse = True) else lista_reactions if not len(lista_reactions) == 0 else None

            lista_conditions = self.listbox_conditions.get(0, tk.END)
            dict_base[name]['conditions'] = lista_conditions if not len(lista_conditions) == 0 else None

            save_json(path.message_and_reply, dict_base)