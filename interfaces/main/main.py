import tkinter as tk
from interfaces.main.frame_direito import FrameDireito as fd
from interfaces.main.frame_esquerdo import FrameEsquerdo as fe
import interfaces.colors as color
from interfaces.fonts import *

class Main(tk.Tk):
    def __init__(self):
        import interfaces.paths as path
        super().__init__()
        self.iconbitmap(path.interface_logo)
        self.title('Bot Discord Easy Creator')
        
        self.config(
            bg = color.azul_escuro,
        )
        self.bot_is_running = False

        self.minsize(
            width = 808,
            height = 543
        )

        self.camada_1 = tk.Frame(
            master = self,
            bg = color.azul_escuro
        )
        self.camada_2 = tk.Frame(
            master = self,
        )
        self.camada_1.pack(
            fill = tk.BOTH,
            expand = 1
        )

        fd.main(self)
        fe.main(self)

        self.mainloop()