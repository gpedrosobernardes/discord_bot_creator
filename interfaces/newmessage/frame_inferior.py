import tkinter as tk
from interfaces.colors import *
from interfaces.fonts import *
from interfaces.commands.newmessage import Commands

class FrameInferior:
    def main(self):
        frame_inferior = tk.Frame(
            master = self.camada_1,
            bg = azul_frame,
            bd = 10
        )
        enter = tk.Button(
            master = frame_inferior,
            text = 'Salvar',
            command = lambda : Commands.save_all_json(self),
            bg = azul_entrada,
            relief = tk.FLAT,
            borderwidth = 1
        )
        enter.grid(
            row = 1,
            column = 1,
            padx = 10,
            pady = 10
        )
        frame_inferior.pack(
            side = tk.BOTTOM,
            fill = tk.Y,
            expand = True
        )