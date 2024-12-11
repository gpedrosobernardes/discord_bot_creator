import tkinter as tk
from json import JSONDecodeError
import re

from functions import load_json, save_json, have_in
from interfaces.colors import *
from interfaces.fonts import *
import interfaces.paths as path
import emoji

from interfaces.tkclasses.SearchBox import SearchBox
from interpreter.conditions import conditions_keys


class MessageWindow:
    def __init__(self, app):
        self.app = app
        self.name = None
        self.variable_where_reaction = tk.StringVar()

        self.janela = tk.Toplevel(
            bg = azul_escuro,
        )
        self.janela.iconbitmap(path.interface_logo)
        self.janela.minsize(
            width = 733,
            height = 458 
        )
        self.camada_1 = tk.Frame(
            master = self.janela,
            bg = azul_escuro
        )
        self.camada_2 = tk.Frame(
            master = self.janela
        )
        self.camada_1.pack(
            fill = tk.BOTH,
            expand = True
        )

        frame_preenchimento = tk.Frame(
            master = self.camada_1,
            bg = azul_frame,
            borderwidth = 10,
        )
        self.name_text = tk.Label(
            master = frame_preenchimento,
            text = "Nome:",
            font = arial,
            bg = azul_frame,
        )
        self.name_entry = tk.Entry(
            master = frame_preenchimento,
            font = arial,
            bg = azul_entrada,
            relief = tk.FLAT,
            borderwidth = 1,
            selectbackground = azul_selecionado
        )
        expected_message_text = tk.Label(
            master = frame_preenchimento,
            text = "Mensagem esperada",
            font = arial,
            bg = azul_frame,
        )
        expected_message = tk.Entry(
            master = frame_preenchimento,
            font = arial,
            bg = azul_entrada,
            relief = tk.FLAT,
            borderwidth = 1,
            selectbackground = azul_selecionado
        )
        reply_text = tk.Label(
            master = frame_preenchimento,
            text = 'Resposta',
            font = arial,
            bg = azul_frame,
        )
        reply = tk.Entry(
            master = frame_preenchimento,
            font = arial,
            bg = azul_entrada,
            relief = tk.FLAT,
            borderwidth = 1,
            selectbackground = azul_selecionado
        )
        reactions_text = tk.Label(
            master = frame_preenchimento,
            text = 'Reações',
            font = arial,
            bg= azul_frame,
        )
        reactions = SearchBox(
            master = frame_preenchimento,
            font = arial,
            lista = [v["en"] for v in emoji.EMOJI_DATA.values()],
            master_overlap = self.camada_2,
            bg = azul_entrada,
            relief = tk.FLAT,
            borderwidth = 1,
            selectbackground = azul_selecionado
        )
        conditions_text = tk.Label(
            master = frame_preenchimento,
            text = 'Condições',
            font = arial,
            bg = azul_frame,
        )
        conditions = SearchBox(
            master = frame_preenchimento,
            font = arial,
            lista = conditions_keys,
            master_overlap = self.camada_2,
            bg = azul_entrada,
            relief = tk.FLAT,
            borderwidth = 1,
            selectbackground = azul_selecionado
        )
        adicionar = tk.Button(
            master = frame_preenchimento,
            text = 'Adicionar',
            command = self.insert_any_on_listbox,
            bg = azul_entrada,
            relief = tk.FLAT,
            borderwidth = 1,
        )
        self.name_text.pack(
            fill = tk.X,
            expand = True
        )
        self.name_entry.pack(
            fill = tk.X,
            expand = True
        )
        conditions_text.pack(
            fill = tk.X,
            expand = True
        )
        conditions.pack(
            fill = tk.X,
            expand = True
        )
        expected_message_text.pack(
            fill = tk.X,
            expand = True
        )
        expected_message.pack(
            fill = tk.X,
            expand = True
        )
        reply_text.pack(
            fill = tk.X,
            expand = True
        )
        reply.pack(
            fill = tk.X,
            expand = True
        )
        reactions_text.pack(
            fill = tk.X,
            expand = True
        )
        reactions.pack(
            fill = tk.X,
            expand = True
        )
        adicionar.pack(
            fill = tk.X,
            expand = True,
            pady = 10
        )
        frame_preenchimento.pack(
            side = tk.LEFT,
            fill = tk.BOTH,
            expand = True
        )

        expected_message.bind('<Return>', lambda event: self.insert_on_listbox(self.listbox_messages, expected_message))
        reply.bind('<Return>', lambda event: self.insert_on_listbox(self.listbox_replys, reply))
        reactions.bind('<Return>', lambda event: self.insert_on_listbox(self.listbox_reactions, reactions, limit = 19))
        conditions.bind('<Return>', lambda event: self.insert_on_listbox(self.listbox_conditions, conditions))
        self.name_entry.bind('<Return>', lambda event: self.update_name())

        self.lista_de_entradas = [expected_message, reply, reactions, conditions]

        frame_das_listas = tk.LabelFrame(
            master = self.camada_1,
            text = 'Listas',
            bg = azul_frame,
            relief = tk.FLAT,
            bd = 10
        )
        listbox_conditions_text = tk.Label(
            master = frame_das_listas,
            text = 'Condições',
            bg = azul_frame
        )
        self.listbox_conditions = tk.Listbox(
            master = frame_das_listas,
            selectmode = tk.MULTIPLE,
            bg = azul_entrada,
            relief = tk.FLAT,
            borderwidth = 1,
            activestyle = 'none',
            selectbackground = azul_selecionado
        )
        listbox_reactions_text = tk.Label(
            master = frame_das_listas,
            text = 'Reações',
            bg = azul_frame
        )
        self.listbox_reactions = tk.Listbox(
            master = frame_das_listas,
            selectmode = tk.MULTIPLE,
            bg = azul_entrada,
            relief = tk.FLAT,
            borderwidth = 1,
            activestyle = 'none',
            selectbackground = azul_selecionado
        )
        listbox_messages_text = tk.Label(
            master = frame_das_listas,
            text = 'Mensagens',
            bg = azul_frame
        )
        self.listbox_messages = tk.Listbox(
            master = frame_das_listas,
            selectmode = tk.MULTIPLE,
            bg =azul_entrada,
            relief = tk.FLAT,
            borderwidth = 1,
            activestyle = 'none',
            selectbackground = azul_selecionado
        )
        listbox_replys_text = tk.Label(
            master= frame_das_listas,
            text = 'Respostas',
            bg= azul_frame,
        )
        self.listbox_replys = tk.Listbox(
            master = frame_das_listas,
            selectmode = tk.MULTIPLE,
            bg = azul_entrada,
            relief = tk.FLAT,
            borderwidth = 1,
            activestyle = 'none',
            selectbackground = azul_selecionado
        )
        remover = tk.Button(
            master = frame_das_listas,
            text = 'Remover',
            command = self.remove_selected_on_listbox,
            bg = azul_entrada,
            relief = tk.FLAT,
            borderwidth = 1
        )
        remover_todos = tk.Button(
            master = frame_das_listas,
            text = 'Remover todos',
            command = self.remove_all_on_listbox,
            bg = azul_entrada,
            relief = tk.FLAT,
            borderwidth = 1
        )
        listbox_conditions_text.grid(
            row = 0,
            column = 1,
            padx = 10
        )
        self.listbox_conditions.grid(
            row = 1,
            column = 1,
            padx = 10
        )
        listbox_replys_text.grid(
            row = 2,
            column = 1,
            padx = 10
        )
        self.listbox_replys.grid(
            row = 3,
            column = 1,
            padx = 10
        )
        listbox_messages_text.grid(
            row = 0,
            column = 2,
            padx = 10
        )
        self.listbox_messages.grid(
            row = 1,
            column = 2,
            padx = 10
        )
        listbox_reactions_text.grid(
            row = 2,
            column = 2,
            padx = 10
        )
        self.listbox_reactions.grid(
            row = 3,
            column = 2,
            padx = 10
        )
        remover.grid(
            row = 4,
            column = 1,
            pady = 10
        )
        remover_todos.grid(
            row = 4,
            column = 2,
            pady = 10
        )
        frame_das_listas.pack(
            padx = 50,
            side = tk.LEFT,
            fill = tk.Y,
            expand = True
        )

        self.lista_de_listbox = [
            self.listbox_messages,
            self.listbox_replys,
            self.listbox_reactions,
            self.listbox_conditions]

        self.listbox_messages.bind('<Delete>', lambda event: self.remove_selected_on_currently_listbox(self.listbox_messages))
        self.listbox_replys.bind('<Delete>', lambda event: self.remove_selected_on_currently_listbox(self.listbox_replys))
        self.listbox_reactions.bind('<Delete>', lambda event: self.remove_selected_on_currently_listbox(self.listbox_reactions))
        self.listbox_conditions.bind('<Delete>', lambda event: self.remove_selected_on_currently_listbox(self.listbox_conditions))

        frame_inferior = tk.Frame(
            master=self.camada_1,
            bg=azul_frame,
            bd=10
        )
        frame_delay = tk.Frame(
            master=frame_inferior,
            bg=azul_frame
        )
        delay_text = tk.Label(
            master=frame_delay,
            text='Delay',
            bg=azul_frame
        )
        self.delay_variable = tk.StringVar()
        self.delay_variable.set('0')

        self.delay = tk.Spinbox(
            master=frame_delay,
            bg=azul_entrada,
            textvariable=self.delay_variable,
            width=10,
            from_=0,
            to=10,
            vcmd=(frame_delay.register(self.delayvalidate), '%P'),
            validate='key'
        )
        save = tk.Button(
            master=frame_inferior,
            text='Salvar',
            command=self.on_save,
            bg=azul_entrada,
            relief=tk.FLAT,
            borderwidth=1
        )
        frame_pin_or_del = tk.Frame(
            master=frame_inferior,
            bg=azul_frame
        )
        self.pin_or_del = tk.StringVar()
        self.pin_or_del.set('None')
        pin = tk.Radiobutton(
            master=frame_pin_or_del,
            text='Fixar',
            variable=self.pin_or_del,
            value='Fixar',
            bg=azul_frame,
        )
        delete = tk.Radiobutton(
            master=frame_pin_or_del,
            text='Remover',
            variable=self.pin_or_del,
            value='Remover',
            bg=azul_frame,
        )
        frame_kick_or_ban = tk.Frame(
            master=frame_inferior,
            bg=azul_frame
        )
        self.kick_or_del = tk.StringVar()
        self.kick_or_del.set('None')
        kick = tk.Radiobutton(
            master=frame_kick_or_ban,
            text='Expulsar',
            variable=self.kick_or_del,
            value='Expulsar',
            bg=azul_frame
        )
        ban = tk.Radiobutton(
            master=frame_kick_or_ban,
            text='Banir',
            variable=self.kick_or_del,
            value='Banir',
            bg=azul_frame
        )
        self.variable_where_reply = tk.StringVar()
        self.variable_where_reply.set('group')
        frame_where_reply = tk.Frame(
            master=frame_inferior,
            bg=azul_frame
        )
        label_where_reply = tk.Label(
            master=frame_where_reply,
            text='Onde responder',
            bg=azul_frame,
        )
        group = tk.Radiobutton(
            master=frame_where_reply,
            text='Grupo',
            bg=azul_frame,
            variable=self.variable_where_reply,
            value='group'
        )
        private = tk.Radiobutton(
            master=frame_where_reply,
            text='Privada',
            bg=azul_frame,
            variable=self.variable_where_reply,
            value='private'
        )

        self.variable_where_reaction.set('author')
        frame_where_reaction = tk.Frame(
            master=frame_inferior,
            bg=azul_frame
        )
        label_where_reaction = tk.Label(
            master=frame_where_reaction,
            text='Onde reagir',
            bg=azul_frame,
        )
        bot = tk.Radiobutton(
            master=frame_where_reaction,
            text='Bot',
            variable=self.variable_where_reaction,
            bg=azul_frame,
            value='bot',
        )
        author = tk.Radiobutton(
            master=frame_where_reaction,
            text='Autor',
            variable=self.variable_where_reaction,
            bg=azul_frame,
            value='author'
        )
        save_and_quit = tk.Button(
            master=frame_inferior,
            text='Salvar e sair',
            command=self.on_save_and_quit,
            bg=azul_entrada,
            relief=tk.FLAT,
            borderwidth=1,
        )
        save.grid(
            row=1,
            column=1,
            padx=10,
            pady=10
        )
        save_and_quit.grid(
            row=2,
            column=1,
        )
        frame_pin_or_del.grid(
            row=3,
            column=1,
            pady=10
        )
        pin.grid(
            row=1,
            column=1,
            sticky=tk.W
        )
        delete.grid(
            row=2,
            column=1,
            sticky=tk.W
        )
        frame_kick_or_ban.grid(
            row=4,
            column=1,
        )
        kick.grid(
            row=1,
            column=1,
            sticky=tk.W
        )
        ban.grid(
            row=2,
            column=1,
            sticky=tk.W
        )
        frame_where_reply.grid(
            row=5,
            column=1
        )
        label_where_reply.grid(
            row=1,
            column=1
        )
        group.grid(
            row=2,
            column=1,
            sticky=tk.W
        )
        private.grid(
            row=3,
            column=1,
            sticky=tk.W
        )
        frame_where_reaction.grid(
            row=6,
            column=1
        )
        label_where_reaction.grid(
            row=1,
            column=1
        )
        bot.grid(
            row=2,
            column=1,
            sticky=tk.W
        )
        author.grid(
            row=3,
            column=1,
            sticky=tk.W
        )
        frame_delay.grid(
            row=7,
            column=1,
            pady=10
        )
        delay_text.grid(
            row=1,
            column=1
        )
        self.delay.grid(
            row=2,
            column=1
        )
        frame_inferior.pack(
            side=tk.BOTTOM,
            fill=tk.Y,
            expand=True
        )

        pin.bind('<Button-3>', lambda event: self.pin_or_del.set('None'))
        delete.bind('<Button-3>', lambda event: self.pin_or_del.set('None'))
        kick.bind('<Button-3>', lambda event: self.kick_or_del.set('None'))
        ban.bind('<Button-3>', lambda event: self.kick_or_del.set('None'))

    def on_save_and_quit(self):
        self.save_and_quit()

    def on_save(self):
        self.save()

    @staticmethod
    def delayvalidate(P):
        if re.search(r'^[0-9]?$|^10$', P):
            return True
        else:
            return False

    @staticmethod
    def insert_on_listbox(listbox: tk.Listbox, entry: tk.Entry, limit: int = 0):
        """insere um valor na listbox especificada e apaga o conteúdo da entry especificada,
        se um limite for especificado ele vai checar se o limite da listbox não foi atingido """
        if not entry.get() == '':
            tamanho_listbox = len(set(listbox.get(0, tk.END)))
            if not tamanho_listbox > limit or limit == 0:
                listbox.insert(tk.END, entry.get())
                entry.delete(0, tk.END)

    def insert_any_on_listbox(self):
        for x in range(4):
            entrada_atual: tk.Entry = self.lista_de_entradas[x]
            listbox_atual: tk.Listbox = self.lista_de_listbox[x]
            if x == 2:
                # x = 2 se refere ao listbox de reactions no discord o limite de reações por mensagem é de 20
                # ou seja a gente precisa limitar a quantidade de reactions.
                self.insert_on_listbox(listbox_atual, entrada_atual, limit=19)
            else:
                self.insert_on_listbox(listbox_atual, entrada_atual)
        self.update_name()

    def update_name(self):
        self.name = self.name_entry.get()
        self.name_entry.delete(0, tk.END)
        self.name_text['text'] = f"Nome: {self.name}"

    def remove_selected_on_listbox(self):
        """remove um item selecionado na listbox"""
        for lb in self.lista_de_listbox:
            lb: tk.Listbox
            if len(lb.curselection()) > 0:
                selecionados = lb.curselection()
                for x in selecionados:
                    lb.delete(x - selecionados.index(x))

    @staticmethod
    def remove_selected_on_currently_listbox(lb: tk.Listbox):
        """remove os items da listbox especificada"""
        selecionados = lb.curselection()
        for x in selecionados:
            lb.delete(x - selecionados.index(x))

    def remove_all_on_listbox(self):
        """remove todos os items em todas listbox"""
        for x in self.lista_de_listbox:
            x: tk.Listbox
            x.delete(0, tk.END)

    def save(self):
        """salva toda a informação que o usuário preencheu na interface em forma de json, para que depois
        o interpretador do bot consiga interpretar"""
        try:
            dict_base = load_json(path.message_and_reply)
        except JSONDecodeError:
            name = '1'
            dict_base = dict()
        else:
            # talvez possamos passar essa responsabilidade para uma funcao apartada e no início da classe
            if not self.name:
                name = '1'
                chaves_dict_base = list(dict_base.keys())
                chaves_dict_base.reverse()
                for x in chaves_dict_base:
                    try:
                        chave = int(x)
                    except ValueError:
                        pass
                    else:
                        name = str(chave + 1)
                        break
            else:
                name = self.name
                if self.name:
                    name = self.name
                    del dict_base[self.name]

        # anti-bug
        self.name = name

        dict_base[name] = {}

        lista_expected_message = self.listbox_messages.get(0, tk.END)
        dict_base[name]['expected message'] = lista_expected_message if not len(lista_expected_message) == 0 else None

        lista_reply = self.listbox_replys.get(0, tk.END)
        dict_base[name]['reply'] = list(map(lambda x: x.split('¨'), lista_reply)) if have_in(lista_reply, '¨',
                                                                                             reverse=True) else lista_reply if not len(
            lista_reply) == 0 else None

        lista_reactions = self.listbox_reactions.get(0, tk.END)
        dict_base[name]['reaction'] = list(
            map(lambda x: re.findall(r':[a-zA-Z_0-9]+:', x), lista_reactions)) if not len(
            lista_reactions) == 0 else None

        lista_conditions = self.listbox_conditions.get(0, tk.END)
        dict_base[name]['conditions'] = lista_conditions if not len(lista_conditions) == 0 else None

        if self.pin_or_del.get() == 'Fixar':
            dict_base[name]['pin'] = True
        elif self.pin_or_del.get() == 'Remover':
            dict_base[name]['delete'] = True

        dict_base[name]['where reply'] = self.variable_where_reply.get()

        dict_base[name]['where reaction'] = self.variable_where_reaction.get()

        dict_base[name]['delay'] = self.delay.get()

        save_json(path.message_and_reply, dict_base)

    def save_and_quit(self):
        self.save()
        self.janela.destroy()


class EditMessageWindow(MessageWindow):
    def __init__(self, app, load):
        super().__init__(app)
        self.name = load
        self.name_entry.insert(0, self.name)
        self.name_entry.config(state=tk.DISABLED)
        self.load_info()

    def load_info(self):
        if self.name:
            messages_json: dict = load_json(path.message_and_reply)
            todas_info: dict = messages_json[self.name]
            if 'expected message' in todas_info:
                expected_message = todas_info['expected message']
                if expected_message:
                    for x in expected_message:
                        self.listbox_messages.insert(tk.END, x)
            if 'reply' in todas_info:
                reply = todas_info['reply']
                if reply:
                    for x in reply:
                        self.listbox_replys.insert(tk.END, '¨'.join(x)) if type(
                            x) == list else self.listbox_replys.insert(tk.END, x)
            if 'reaction' in todas_info:
                reaction = todas_info['reaction']
                if reaction:
                    list(map(lambda x: self.listbox_reactions.insert(tk.END, ' '.join(x)), reaction))
            if 'conditions' in todas_info:
                conditions = todas_info['conditions']
                if conditions:
                    for x in conditions:
                        self.listbox_conditions.insert(tk.END, x)
            if 'pin' in todas_info:
                pin = todas_info['pin']
                if pin:
                    self.pin_or_del.set('Fixar')
            if 'delete' in todas_info:
                delete = todas_info['delete']
                if delete:
                    self.pin_or_del.set('Remover')

            if 'delay' in todas_info:
                delay = todas_info['delay']
                self.delay_variable.set(delay)

            if 'where reply' in todas_info:
                where_reply = todas_info['where reply']
                self.variable_where_reply.set(where_reply)

            if 'where reaction' in todas_info:
                where_reaction = todas_info['where reaction']
                self.variable_where_reaction.set(where_reaction)


class NewMessageWindow(MessageWindow):
    def on_save(self):
        super().on_save()
        self.app.add_message(self.name)

    def on_save_and_quit(self):
        super().on_save_and_quit()
        self.app.add_message(self.name)
