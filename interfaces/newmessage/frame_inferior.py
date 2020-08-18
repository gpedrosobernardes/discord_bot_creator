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
        self.delay_variable.set('0')

        self.delay = tk.Spinbox(
            master = frame_delay,
            bg = azul_entrada,
            textvariable = self.delay_variable,
            width = 10,
            from_=0,
            to= 10,
            vcmd = (frame_delay.register(FrameInferior.delayvalidate),
                    self, '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W'),
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
        frame_pin_or_del = tk.Frame(
            master = frame_inferior,
            bg = azul_frame
        )
        self.pin_or_del = tk.StringVar()
        self.pin_or_del.set('None')
        pin = tk.Radiobutton(
            master = frame_pin_or_del,
            text = 'Fixar',
            variable = self.pin_or_del,
            value = 'Fixar',
            bg = azul_frame,
        )
        delete = tk.Radiobutton(
            master = frame_pin_or_del,
            text = 'Remover',
            variable = self.pin_or_del,
            value = 'Remover',
            bg = azul_frame,
        )
        frame_kick_or_ban = tk.Frame(
            master = frame_inferior,
            bg = azul_frame
        )
        self.kick_or_del = tk.StringVar()
        self.kick_or_del.set('None')
        kick = tk.Radiobutton(
            master = frame_kick_or_ban,
            text = 'Expulsar',
            variable = self.kick_or_del,
            value = 'Expulsar',
            bg = azul_frame
        )
        ban = tk.Radiobutton(
            master = frame_kick_or_ban,
            text = 'Banir',
            variable = self.kick_or_del,
            value = 'Banir',
            bg = azul_frame
        )
        self.variable_where_reply = tk.StringVar()
        self.variable_where_reply.set('group')
        frame_where_reply = tk.Frame(
            master = frame_inferior,
            bg = azul_frame
        )
        label_where_reply = tk.Label(
            master = frame_where_reply,
            text = 'Onde responder',
            bg = azul_frame,
        )
        group = tk.Radiobutton(
            master = frame_where_reply,
            text = 'Grupo',
            bg = azul_frame,
            variable = self.variable_where_reply,
            value = 'group'
        )   
        private = tk.Radiobutton(
            master = frame_where_reply,
            text = 'Privada',
            bg = azul_frame,
            variable = self.variable_where_reply,
            value = 'private'
        )
        self.variable_where_reaction = tk.StringVar()
        self.variable_where_reaction.set('author')
        frame_where_reaction = tk.Frame(
            master = frame_inferior,
            bg = azul_frame
        )
        label_where_reaction = tk.Label(
            master = frame_where_reaction,
            text = 'Onde reagir',
            bg = azul_frame,
        )
        bot = tk.Radiobutton(
            master = frame_where_reaction,
            text = 'Bot',
            variable = self.variable_where_reaction,
            bg = azul_frame,
            value = 'bot',
        )
        author = tk.Radiobutton(
            master = frame_where_reaction,
            text = 'Autor',
            variable = self.variable_where_reaction,
            bg = azul_frame,
            value = 'author'
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
        frame_pin_or_del.grid(
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
        frame_kick_or_ban.grid(
            row = 4,
            column = 1,
        )
        kick.grid(
            row = 1,
            column = 1,
            sticky = tk.W
        )
        ban.grid(
            row = 2,
            column = 1,
            sticky = tk.W
        )
        frame_where_reply.grid(
            row = 5,
            column = 1
        )
        label_where_reply.grid(
            row = 1,
            column = 1
        )
        group.grid(
            row = 2,
            column = 1,
            sticky = tk.W
        )
        private.grid(
            row = 3,
            column = 1,
            sticky = tk.W
        )
        frame_where_reaction.grid(
            row = 6,
            column = 1
        )
        label_where_reaction.grid(
            row = 1,
            column = 1
        )
        bot.grid(
            row = 2,
            column = 1,
            sticky = tk.W
        )
        author.grid(
            row = 3,
            column = 1,
            sticky = tk.W
        )
        frame_delay.grid(
            row = 7,
            column = 1,
            pady = 10
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
        
        pin.bind('<Button-3>', lambda event: self.pin_or_del.set('None'))
        delete.bind('<Button-3>', lambda event: self.pin_or_del.set('None'))

    def delayvalidate(self, d, i, P, s, S, v, V, W):
        import re
        if re.search(r'^[0-9]?$|^10$', P):
            return True
        else:
            return False