import tkinter as tk
import interfaces.paths as path

class Commands:
    def insert_on_listbox(self, listbox:tk.Listbox, entry:tk.Entry, limit:int = 0):
        '''insere um valor na listbox especificada e apaga o conteudo da entry especificada,
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
        Commands.update_name(self)

    def update_name(self):
        self.load = self.name.get()
        self.name.delete(0, tk.END)
        self.name_text['text'] = f"Nome: {self.load}"

    def remove_selected_on_listbox(self):
        '''remove um item selecionado na listbox'''
        for lb in self.lista_de_listbox:
            lb:tk.Listbox
            if len(lb.curselection()) > 0:
                selecionados = lb.curselection()
                for x in selecionados:
                    lb.delete(x-selecionados.index(x))

    def remove_selected_on_currently_listbox(self, lb:tk.Listbox):
        '''remove os items da listbox especificada'''
        selecionados = lb.curselection()
        for x in selecionados:
            lb.delete(x-selecionados.index(x))

    def remove_all_on_listbox(self):
        '''remove todos os items em todas listbox'''
        for x in self.lista_de_listbox:
            x:tk.Listbox
            x.delete(0,tk.END)

    def save_all_json(self):
        '''salva toda a informação que o usuario preencheu na interface em forma de json, para que depois
        o interpretador do bot consiga interpretar'''
        import json
        from interfaces.commands.main import MainCommands
        from functions import load_json, save_json, have_in
        try:
            dict_base = load_json(path.message_and_reply)
        except json.decoder.JSONDecodeError:
            name = '1'
            dict_base = dict()
        else:
            if not self.load:
                name = '1'
                chaves_dict_base = list(dict_base.keys())
                chaves_dict_base.reverse()
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

        # self.load = name

        dict_base[name] = {}

        lista_expected_message = self.listbox_messages.get(0, tk.END)
        dict_base[name]['expected message'] = lista_expected_message if not len(lista_expected_message) == 0 else None

        lista_reply = self.listbox_replys.get(0, tk.END)
        dict_base[name]['reply'] = list(map(lambda x: x.split('¨'), lista_reply)) if have_in(lista_reply, '¨', reverse = True) else lista_reply if not len(lista_reply) == 0 else None

        lista_reactions = self.listbox_reactions.get(0, tk.END)
        dict_base[name]['reaction'] = list(map(lambda x: x.split('¨'), lista_reactions)) if have_in(lista_reactions, '¨', reverse = True) else lista_reactions if not len(lista_reactions) == 0 else None

        lista_conditions = self.listbox_conditions.get(0, tk.END)
        dict_base[name]['conditions'] = lista_conditions if not len(lista_conditions) == 0 else None

        if self.pin_or_del.get() == 'Fixar':
            dict_base[name]['pin'] = True
        elif self.pin_or_del.get() == 'Remover':
            dict_base[name]['delete'] = True
        
        dict_base[name]['delay'] = self.delay.get() if self.delay.get() != '0' else None

        save_json(path.message_and_reply, dict_base)
        MainCommands.refresh_messages(self)

    def save_and_quit(self):
        from interfaces.commands.main import MainCommands
        Commands.save_all_json(self)
        self.janela.destroy()
        MainCommands.refresh_messages(self)

    def load_info(self):
        from functions import load_json , save_json
        if self.load:
            messages_json:dict = load_json(path.message_and_reply)
            todas_info:dict = messages_json[self.load]
            if 'expected message' in todas_info:
                expected_message = todas_info['expected message']
                if expected_message == None:
                    pass
                else:
                    for x in expected_message:
                        self.listbox_messages.insert(tk.END, '¨'.join(x)) if type(x) == list else self.listbox_messages.insert(tk.END, x)
            if 'reply' in todas_info:
                reply = todas_info['reply']
                if reply == None:
                    pass
                else:
                    for x in reply:
                        self.listbox_replys.insert(tk.END, '¨'.join(x)) if type(x) == list else self.listbox_replys.insert(tk.END, x)
            if 'reaction' in todas_info:
                reaction = todas_info['reaction']
                if reaction == None:
                    pass
                else:
                    for x in reaction:
                        self.listbox_reactions.insert(tk.END, x)
            if 'conditions' in todas_info:
                conditions = todas_info['conditions']
                if conditions == None:
                    pass
                else:
                    for x in conditions:
                        self.listbox_conditions.insert(tk.END, x)
            if 'pin' in todas_info:
                pin = todas_info['pin']
                if pin == True:
                    self.pin_or_del.set('Fixar')
            if 'delete' in todas_info:
                delete = todas_info['delete']
                if delete == True:
                    self.pin_or_del.set('Remover')

            if 'delay' in todas_info:
                delay = todas_info['delay']
                self.delay_variable.set(delay)