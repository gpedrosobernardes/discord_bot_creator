import tkinter as tk
from interfaces.tkclasses.SearchBox import SearchBox as Sb
from interfaces.commands.newmessage import Commands
from interfaces.colors import *
from interfaces.fonts import *

class FrameEntrada:
    def main(self):
        frame_preenchimento = tk.Frame(
            master = self.camada_1,
            bg = azul_frame,
            borderwidth = 10,
        )
        expected_message_text = tk.Label(
            master = frame_preenchimento,
            text = "Mensagem esperada",
            font = arial,
            bg = azul_frame
        )
        expected_message = tk.Entry(
            master = frame_preenchimento,
            font = arial,
            bg= azul_entrada,
            relief = tk.FLAT,
            borderwidth = 1
        )
        reply_text = tk.Label(
            master = frame_preenchimento,
            text = 'Resposta',
            font = arial,
            bg = azul_frame
        )
        reply = tk.Entry(
            master = frame_preenchimento,
            font = arial,
            bg = azul_entrada,
            relief = tk.FLAT,
            borderwidth = 1
        )
        reactions_text = tk.Label(
            master = frame_preenchimento,
            text = 'Reações',
            font = arial,
            bg= azul_frame
        )
        reactions = Sb(
            master = frame_preenchimento,
            font = arial,
            lista = self.lista_reactions,
            master_overlap = self.camada_2,
            bg = azul_entrada,
            relief = tk.FLAT,
            borderwidth = 1
        )
        condictions_text = tk.Label(
            master = frame_preenchimento,
            text = 'Condições',
            font = arial,
            bg = azul_frame
        )
        condictions = Sb(
            master = frame_preenchimento,
            font = arial,
            lista = self.lista_condictions,
            master_overlap = self.camada_2,
            bg = azul_entrada,
            relief = tk.FLAT,
            borderwidth = 1
        )
        adicionar = tk.Button(
            master = frame_preenchimento,
            text = 'Adicionar',
            command = lambda : Commands.insert_any_on_listbox(self),
            bg = azul_entrada,
            relief = tk.FLAT,
            borderwidth = 1,
        )
        condictions_text.grid(
            row = 1,
            column = 1,
            sticky = tk.W,
        )
        condictions.grid(
            row = 2,
            column = 1
        )
        expected_message_text.grid(
            row = 3,
            column = 1,
            sticky = tk.W
        )
        expected_message.grid(
            row = 4,
            column = 1
        )
        reply_text.grid(
            row = 5,
            column = 1,
            sticky = tk.W
        )
        reply.grid(
            row = 6,
            column = 1
        )
        reactions_text.grid(
            row = 7,
            column = 1,
            sticky = tk.W
        )
        reactions.grid(
            row = 8,
            column = 1
        )
        adicionar.grid(
            row = 9,
            column = 1,
            pady = 10
        )
        frame_preenchimento.grid(
            row = 1,
            column = 1,
            sticky = tk.E,
            padx = 50
        )

        expected_message.bind('<Return>', lambda event: Commands.insert_on_listbox(self, self.listbox_messages, expected_message))
        reply.bind('<Return>', lambda event: Commands.insert_on_listbox(self, self.listbox_replys, reply))
        reactions.bind('<Return>', lambda event: Commands.insert_on_listbox(self, self.listbox_reactions, reactions))
        condictions.bind('<Return>', lambda event: Commands.insert_on_listbox(self, self.listbox_condictions, condictions))

        self.lista_de_entradas = [expected_message, reply, reactions, condictions]