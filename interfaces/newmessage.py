import tkinter as tk
from functions import load_json
from interfaces.tkclasses.SearchBox import SearchBox as Sb
from interfaces.commands.newmessage import Commands

arial = ("Arial",12)

class NewMessage:
    def interface(self):

        lista_reactions = load_json('source/emojis.json')['emojis']
        lista_condictions = ['testando','testando 2','testando 3']

        janela = tk.Toplevel(
            master = self
        )
        janela_width = 600
        janela_height = 700
        janela.geometry(f'{janela_height}x{janela_width}')
        camada_1 = tk.Frame(
            master = janela
        )
        camada_2 = tk.Frame(
            master = janela
        )
        frame_inferior = tk.Frame(
            master=camada_1,
        )
        enter = tk.Button(
            master = frame_inferior,
            text   = 'Confirmar',
            command = lambda : Commands.save_all_json(self)
        )
        enter.grid(
            row    = 1,
            column = 1,
            padx   = 10,
            pady   = 10
        )
        frame_das_listas = tk.LabelFrame(
            master = camada_1,
            text   = 'Listas'
        )
        # filhos do frames das lista
        listbox_condictions_text = tk.Label(
            master = frame_das_listas,
            text = 'Condições'
        )
        self.listbox_condictions = tk.Listbox(
            master = frame_das_listas,
            selectmode= tk.MULTIPLE
        )
        listbox_reactions_text = tk.Label(
            master = frame_das_listas,
            text = 'Reações'
        )
        self.listbox_reactions = tk.Listbox(
            master = frame_das_listas,
            selectmode= tk.MULTIPLE
        )
        listbox_messages_text = tk.Label(
            master= frame_das_listas,
            text = 'Mensagens'
        )
        self.listbox_messages = tk.Listbox(
            master = frame_das_listas,
            selectmode= tk.MULTIPLE
        )
        listbox_replys_text = tk.Label(
            master= frame_das_listas,
            text = 'Respostas'
        )
        self.listbox_replys = tk.Listbox(
            master = frame_das_listas,
            selectmode= tk.MULTIPLE
        )
        remover = tk.Button(
            master= frame_das_listas,
            text= 'Remover',
            command = lambda: Commands.remove_selected_on_listbox(self)
        )
        remover_todos = tk.Button(
            master= frame_das_listas,
            text= 'Remover todos',
            command = lambda : Commands.remove_all_on_listbox(self)
        )
        listbox_condictions_text.grid(
            row    = 0,
            column = 1,
            sticky = tk.W+tk.E
        )
        self.listbox_condictions.grid(
            row    = 1,
            column = 1,
            sticky = tk.W+tk.E
        )
        listbox_replys_text.grid(
            row    = 2,
            column = 1,
            sticky = tk.W+tk.E
        )
        self.listbox_replys.grid(
            row    = 3,
            column = 1,
            sticky = tk.W+tk.E
        )
        listbox_messages_text.grid(
            row    = 0,
            column = 2,
            sticky = tk.W+tk.E
        )
        self.listbox_messages.grid(
            row    = 1,
            column = 2,
            sticky = tk.W+tk.E
        )
        listbox_reactions_text.grid(
            row    = 2,
            column = 2,
            sticky = tk.W+tk.E
        )
        self.listbox_reactions.grid(
            row    = 3,
            column = 2,
            sticky = tk.W+tk.E
        )
        remover.grid(
            row= 4,
            column = 1,
        )
        remover_todos.grid(
            row = 4,
            column = 2,
        )
        frame_preenchimento = tk.Frame(
            master=camada_1
        )
        expected_message_text = tk.Label(
            master = frame_preenchimento,
            text   = "Mensagem esperada",
            font   = arial,
        )
        expected_message = tk.Entry(
            master = frame_preenchimento,
            font   = arial,
        )
        expected_message.bind('<Return>', lambda event: Commands.insert_on_listbox(self, listbox_messages, expected_message))
        reply_text = tk.Label(
            master = frame_preenchimento,
            text   = 'Resposta',
            font   = arial,
        )
        reply = tk.Entry(
            master= frame_preenchimento,
            font = arial
        )
        reply.bind('<Return>', lambda event: Commands.insert_on_listbox(self, listbox_replys, reply))
        reactions_text = tk.Label(
            master = frame_preenchimento,
            text   = 'Reações',
            font   = arial,
        )
        reactions = Sb(
            master         = frame_preenchimento,
            font           = arial,
            lista          = lista_reactions,
            master_overlap = camada_2,
        )
        reactions.bind('<Return>', lambda event: Commands.insert_on_listbox(self, listbox_reactions, reactions))
        condictions_text = tk.Label(
            master = frame_preenchimento,
            text   = 'Condições',
            font   = arial,
        )
        condictions = Sb(
            master         = frame_preenchimento,
            font           = arial,
            lista          = lista_condictions,
            master_overlap = camada_2
        )
        condictions.bind('<Return>', lambda event: Commands.insert_on_listbox(self, listbox_condictions, condictions))
        condictions_text.grid(
            row    = 1,
            column = 1,
            sticky = tk.W
        )
        condictions.grid(
            row    = 2,
            column = 1
        )
        adicionar = tk.Button(
            master  = frame_preenchimento,
            text    = 'Adicionar',
            command = lambda : Commands.insert_any_on_listbox(self)
        )
        expected_message_text.grid(
            row    = 3,
            column = 1,
            sticky = tk.W
        )
        expected_message.grid(
            row    = 4,
            column = 1
        )
        reply_text.grid(
            row    = 5,
            column = 1,
            sticky = tk.W
        )
        reply.grid(
            row    = 6,
            column = 1
        )
        reactions_text.grid(
            row    = 7,
            column = 1,
            sticky = tk.W
        )
        reactions.grid(
            row    = 8,
            column = 1
        )
        adicionar.grid(
            row    = 9,
            column = 1
        )
        frame_preenchimento.grid(
            row    = 1,
            column = 1,
            ipadx  = 10,
            ipady  = 10,
        )
        frame_das_listas.grid(
            row    = 1,
            column = 2,
            ipadx  = 10,
            ipady  = 10,
        )
        frame_inferior.grid(
            row=2,
            column =1,
            columnspan=2
        )
        camada_1.place(
            x = 0,
            y = 0
        )

        self.lista_de_entradas = [expected_message, reply, reactions, condictions]
        self.lista_de_listbox = [self.listbox_messages, self.listbox_replys, self.listbox_reactions, self.listbox_condictions]

        #opção set delay no bot