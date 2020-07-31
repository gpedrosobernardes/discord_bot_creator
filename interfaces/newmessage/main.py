import tkinter as tk
from functions import load_json
from interfaces.commands.newmessage import Commands
from interfaces.newmessage.frame_entradas import FrameEntrada as fe
from interfaces.newmessage.frame_inferior import FrameInferior as fi
from interfaces.newmessage.frame_listas import FrameListas as fl
from interfaces.colors import *
from interfaces.fonts import *

class NewMessage:
    def main(self):
        self.lista_reactions = load_json('source/emojis.json')['emojis']
        self.lista_condictions = ['testando','testando 2','testando 3']

        self.janela = tk.Toplevel(
            master = self,
            bg= azul_escuro,
        )
        self.camada_1 = tk.Frame(
            master = self.janela,
            bg= azul_escuro
        )
        self.camada_2 = tk.Frame(
            master = self.janela
        )
        self.camada_1.place(
            relx = 0.5, rely = 0.5, anchor=tk.CENTER
        )

        fe.main(self)
        fl.main(self)
        fi.main(self)