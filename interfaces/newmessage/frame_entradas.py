import tkinter as tk
from interfaces.tkclasses.SearchBox import SearchBox as Sb
from interfaces.commands.newmessage import Commands
from interfaces.colors import *
from interfaces.fonts import *
import source.emojis as emojis

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
            bg = azul_frame,
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
            bg = azul_frame,
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
            bg= azul_frame,
        )
        reactions = Sb(
            master = frame_preenchimento,
            font = arial,
            lista = emojis.emojis,
            master_overlap = self.camada_2,
            bg = azul_entrada,
            relief = tk.FLAT,
            borderwidth = 1
        )
        condictions_text = tk.Label(
            master = frame_preenchimento,
            text = 'Condições',
            font = arial,
            bg = azul_frame,
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
        condictions_text.pack(
            fill = tk.X,
            expand = True
        )
        condictions.pack(
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

        expected_message.bind('<Return>', lambda event: Commands.insert_on_listbox(self, self.listbox_messages, expected_message))
        reply.bind('<Return>', lambda event: Commands.insert_on_listbox(self, self.listbox_replys, reply))
        reactions.bind('<Return>', lambda event: Commands.insert_on_listbox(self, self.listbox_reactions, reactions, limit = 19))
        condictions.bind('<Return>', lambda event: Commands.insert_on_listbox(self, self.listbox_condictions, condictions))

        self.lista_de_entradas = [expected_message, reply, reactions, condictions]