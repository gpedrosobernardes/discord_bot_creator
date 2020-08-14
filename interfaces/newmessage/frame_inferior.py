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
        frame_delay = tk.Frame(
            master = frame_inferior,
            bg = azul_frame
        )
        delay_text = tk.Label(
            master = frame_delay,
            text = 'Delay',
            bg = azul_frame
        )
        self.delay_variable = tk.StringVar()
        self.delay_variable.set('10')

        vcmddelay = (frame_delay.register(FrameInferior.delayvalidate)
                    , self, '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        self.delay = tk.Spinbox(
            master = frame_delay,
            bg = azul_entrada,
            textvariable = self.delay_variable,
            width = 10,
            from_=0,
            to= 10,
            vcmd = vcmddelay,
            validate = 'key'
        )
        save = tk.Button(
            master = frame_inferior,
            text = 'Salvar',
            command = lambda : Commands.save_all_json(self),
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
        frame_delay.grid(
            row = 4,
            column = 1
        )
        delay_text.grid(
            row = 1,
            column = 1
        )
        self.delay.grid(
            row = 2,
            column = 1
        )
        frame_inferior.pack(
            side = tk.BOTTOM,
            fill = tk.Y,
            expand = True
        )

    def delayvalidate(self, d, i, P, s, S, v, V, W):
        import re
        if re.search(r'^[0-9]?$|^10$', P):
            return True
        else:
            return False