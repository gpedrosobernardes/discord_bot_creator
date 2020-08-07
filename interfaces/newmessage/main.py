import tkinter as tk
from functions import load_json
from interfaces.commands.newmessage import Commands
from interfaces.newmessage.frame_entradas import FrameEntrada as fe
from interfaces.newmessage.frame_inferior import FrameInferior as fi
from interfaces.newmessage.frame_listas import FrameListas as fl
from interfaces.colors import *
from interfaces.fonts import *
import interfaces.paths as path

class NewMessage:
    def main(self, load:str = None):
        self.load = load

        self.janela = tk.Toplevel(
            master = self,
            bg = azul_escuro,
        )
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

        fe.main(self)
        fl.main(self)
        fi.main(self)

        NewMessage.__load_info(self)

    def __load_info(self):
        if self.load:
            messages_json:dict = load_json(path.message_and_reply)
            todas_info:dict = messages_json[self.load]
            try:
                expected_message = todas_info['expected message']
                if type(expected_message) == str:
                    self.listbox_messages.insert(tk.END, expected_message)
                elif expected_message == None:
                    pass
                else:
                    for x in expected_message:
                        self.listbox_messages.insert(tk.END, x)
            except KeyError:
                pass
            try:
                reply = todas_info['reply']
                if type(reply) == str:
                    self.listbox_replys.insert(tk.END, reply)
                elif reply == None:
                    pass
                else:
                    for x in reply:
                        self.listbox_replys.insert(tk.END, x)
            except KeyError:
                pass
            try:
                reaction = todas_info['reaction']
                if type(reaction) == str:
                    self.listbox_reactions.insert(tk.END, reaction)
                elif reaction == None:
                    pass
                else:
                    for x in reaction:
                        self.listbox_reactions.insert(tk.END, x)
            except KeyError:
                pass
            try:
                conditions = todas_info['conditions']
                if type(conditions) == str:
                    self.listbox_conditions.insert(tk.END, conditions)
                elif conditions == None:
                    pass
                else:
                    for x in conditions:
                        self.listbox_conditions.insert(tk.END, x)
            except KeyError:
                pass