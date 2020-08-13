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
        save = tk.Button(
            master = frame_inferior,
            text = 'Salvar',
            command = lambda : Commands.save_all_json(self, self.load),
            bg = azul_entrada,
            relief = tk.FLAT,
            borderwidth = 1
        )
        frame_radiobutton = tk.Frame(
            master = frame_inferior,
            bg = azul_frame
        )
        self.pin_or_del = tk.StringVar()
        self.pin_or_del.set('None')
        pin = tk.Radiobutton(
            master = frame_radiobutton,
            text = 'Fixar',
            variable = self.pin_or_del,
            value = 'Fixar',
            bg = azul_frame,
        )
        delete = tk.Radiobutton(
            master = frame_radiobutton,
            text = 'Remover',
            variable = self.pin_or_del,
            value = 'Remover',
            bg = azul_frame,
        )
        do_nothing = tk.Radiobutton(
            master = frame_radiobutton,
            text = 'Fazer nada',
            variable = self.pin_or_del,
            value = 'None',
            bg = azul_frame,
        )
        save_and_quit = tk.Button(
            master = frame_inferior,
            text = 'Salvar e sair',
            command = lambda : Commands.save_and_quit(self),
            bg = azul_entrada,
            relief = tk.FLAT,
            borderwidth = 1, 
        )
        save.grid(
            row = 1,
            column = 1,
            padx = 10,
            pady = 10
        )
        save_and_quit.grid(
            row = 2,
            column = 1,
        )
        frame_radiobutton.grid(
            row = 3,
            column = 1,
            pady = 10
        )
        pin.grid(
            row = 1,
            column = 1,
            sticky = tk.W
        )
        delete.grid(
            row = 2,
            column = 1,
            sticky = tk.W
        )
        do_nothing.grid(
            row = 3,
            column = 1,
            sticky = tk.W
        )
        frame_inferior.pack(
            side = tk.BOTTOM,
            fill = tk.Y,
            expand = True
        )