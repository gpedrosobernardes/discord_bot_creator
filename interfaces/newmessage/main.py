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

        Commands.load_info(self)