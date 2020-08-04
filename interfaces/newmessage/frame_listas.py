import tkinter as tk
from interfaces.commands.newmessage import Commands
from interfaces.colors import *
from interfaces.fonts import *

class FrameListas:
    def main(self):
        frame_das_listas = tk.LabelFrame(
            master = self.camada_1,
            text = 'Listas',
            bg = azul_frame,
            relief = tk.FLAT,
            bd = 10
        )
        listbox_condictions_text = tk.Label(
            master = frame_das_listas,
            text = 'Condições',
            bg = azul_frame
        )
        self.listbox_condictions = tk.Listbox(
            master = frame_das_listas,
            selectmode = tk.MULTIPLE,
            bg = azul_entrada,
            relief = tk.FLAT,
            borderwidth = 1
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
            borderwidth = 1
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
            borderwidth = 1
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
            borderwidth = 1
        )
        remover = tk.Button(
            master = frame_das_listas,
            text = 'Remover',
            command = lambda: Commands.remove_selected_on_listbox(self),
            bg = azul_entrada,
            relief = tk.FLAT,
            borderwidth = 1
        )
        remover_todos = tk.Button(
            master = frame_das_listas,
            text = 'Remover todos',
            command = lambda : Commands.remove_all_on_listbox(self),
            bg = azul_entrada,
            relief = tk.FLAT,
            borderwidth = 1
        )
        listbox_condictions_text.grid(
            row = 0,
            column = 1,
            padx = 10
        )
        self.listbox_condictions.grid(
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
            self.listbox_condictions]

        self.listbox_messages.bind('<Delete>', lambda event: Commands.remove_selected_on_currently_listbox(self, self.listbox_messages))
        self.listbox_replys.bind('<Delete>', lambda event: Commands.remove_selected_on_currently_listbox(self, self.listbox_replys))
        self.listbox_reactions.bind('<Delete>', lambda event: Commands.remove_selected_on_currently_listbox(self, self.listbox_reactions))
        self.listbox_condictions.bind('<Delete>', lambda event: Commands.remove_selected_on_currently_listbox(self, self.listbox_condictions))

        # for x in self.lista_de_listbox:
        #     x.bind('<Delete>', lambda event: Commands.remove_selected_on_currently_listbox(self, x))