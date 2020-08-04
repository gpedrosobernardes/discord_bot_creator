import tkinter as tk
from interfaces.main.frame_direito import FrameDireito as fd
from interfaces.main.frame_esquerdo import FrameEsquerdo as fe
from interfaces.colors import *
from interfaces.fonts import *
from interfaces.tkclasses.SearchBox import SearchBox as sb

class Main(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Bot Discord Easy Creator')

        self.camada_1 = tk.Frame(
            master = self,
        )
        self.camada_2 = tk.Frame(
            master = self,
        )
        self.camada_1.pack()

        fd.main(self)
        fe.main(self)

        self.mainloop()

Main()