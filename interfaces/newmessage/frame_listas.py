import tkinter as tk
from interfaces.colors import *
from interfaces.fonts import *

class FrameListas:
    def main(self):
        frame_das_listas = tk.LabelFrame(
            master = self.camada_1,
            text   = 'Listas',
            bg= azul_frame
        )
        listbox_condictions_text = tk.Label(
            master = frame_das_listas,
            text = 'Condições',
            bg= azul_frame
        )
        self.listbox_condictions = tk.Listbox(
            master = frame_das_listas,
            selectmode= tk.MULTIPLE,
            bg=azul_entrada
        )
        listbox_reactions_text = tk.Label(
            master = frame_das_listas,
            text = 'Reações',
            bg= azul_frame
        )
        self.listbox_reactions = tk.Listbox(
            master = frame_das_listas,
            selectmode= tk.MULTIPLE,
            bg= azul_entrada,
        )
        listbox_messages_text = tk.Label(
            master= frame_das_listas,
            text = 'Mensagens',
            bg= azul_frame
        )
        self.listbox_messages = tk.Listbox(
            master = frame_das_listas,
            selectmode= tk.MULTIPLE,
            bg=azul_entrada
        )
        listbox_replys_text = tk.Label(
            master= frame_das_listas,
            text = 'Respostas',
            bg= azul_frame
        )
        self.listbox_replys = tk.Listbox(
            master = frame_das_listas,
            selectmode= tk.MULTIPLE,
            bg=azul_entrada
        )
        remover = tk.Button(
            master= frame_das_listas,
            text= 'Remover',
            command = lambda: Commands.remove_selected_on_listbox(self),
            bg= azul_entrada
        )
        remover_todos = tk.Button(
            master= frame_das_listas,
            text= 'Remover todos',
            command = lambda : Commands.remove_all_on_listbox(self),
            bg= azul_entrada
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
        frame_das_listas.grid(
            row    = 1,
            column = 2,
            ipadx  = 10,
            ipady  = 10,
            padx= 50
        )

        self.lista_de_listbox = [
            self.listbox_messages,
            self.listbox_replys,
            self.listbox_reactions,
            self.listbox_condictions]