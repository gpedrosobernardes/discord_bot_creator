import tkinter as tk
from interfaces.fonts import *
import interfaces.paths as path
import interfaces.colors as color
from interfaces.commands.main import MainCommands as mc

class FrameDireito:
    def main(self):
        frame_direito_bot = tk.Frame(
            master = self.camada_1,
            bg = color.azul_frame,
            borderwidth = 10
        )
        self.log_do_bot = tk.Text(
            master = frame_direito_bot,
            font = arial,
            width = 50,
            bg = color.azul_entrada,
            relief = tk.FLAT,
            state = tk.DISABLED,
            selectbackground = color.azul_selecionado
        )
        frame_entrada_comandos = tk.Frame(
            master = frame_direito_bot,
            bg = color.azul_frame
        )
        self.entrada_comandos = tk.Entry(
            master = frame_entrada_comandos,
            font = arial,
            bg = color.azul_entrada,
            #width = 48,
            relief = tk.FLAT
        )
        sep_entrada_comandos = tk.Frame(
            master = frame_entrada_comandos,
            width = 5,
            bg = color.azul_frame,
        )
        button_entrada_comandos = tk.Button(
            master = frame_entrada_comandos,
            font = ('Arial', 8),
            text = '>',
            command = lambda : mc.entry_command(self),
            bg = color.azul_entrada,
            relief = tk.FLAT,
            activebackground = color.azul_pressed,
        )
        frame_inserir_token = tk.Frame(
            master = frame_direito_bot,
            bg = color.azul_frame
        )
        self.inserir_token = tk.Entry(
            master = frame_inserir_token,
            bg = color.azul_entrada,
            relief = tk.FLAT,
            validatecommand = (frame_inserir_token.register(FrameDireito.validate_token), self, '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W'),
            validate = "key"
        )
        sep_inserir_token = tk.Frame(
            master = frame_inserir_token,
            bg = color.azul_frame,
            width = 5
        )
        self.button_inserir_token = tk.Button(
            master = frame_inserir_token,
            bg = color.azul_entrada,
            font = ('Arial', 7),
            relief = tk.FLAT,
            text = '>',
            command = lambda : mc.update_token(self),
            activebackground = color.azul_pressed,
        )
        self.token = mc.get_token(self)
        self.token_atual = tk.Label(
            master = frame_direito_bot,
            text = 'Token:\n'
                   f'{self.token}',
            bg = color.azul_frame,
            justify = tk.LEFT
            
        )
        self.executar_o_bot = tk.Button(
            master = frame_direito_bot,
            text = 'Executar o bot',
            font = arial,
            relief = tk.FLAT,
            command = lambda : mc.init_or_finish_bot(self),
            bg = color.azul_entrada,
            activebackground = color.azul_pressed,
        )
        frame_direito_bot.pack(
            side = tk.RIGHT,
            fill = tk.Y
        )
        self.log_do_bot.grid(
            row = 1,
            column = 1,
            sticky = tk.W
        )
        frame_entrada_comandos.grid(
            row = 2,
            column = 1,
            sticky = tk.W+tk.E,
            pady = 5
        )
        self.entrada_comandos.pack(
            side = tk.LEFT,
            fill = tk.BOTH,
            expand = 1
        )
        sep_entrada_comandos.pack(
            side = tk.LEFT,
        )
        button_entrada_comandos.pack(
            side = tk.LEFT,
        )
        self.token_atual.grid(
            row = 3,
            column = 1,
            sticky = tk.W
        )
        frame_inserir_token.grid(
            row = 4,
            column = 1,
            sticky = tk.W+tk.E
        )
        self.inserir_token.pack(
            side = tk.LEFT,
            fill = tk.BOTH,
            expand = 1
        )
        sep_inserir_token.pack(
            side = tk.LEFT,
        )
        self.button_inserir_token.pack(
            side = tk.LEFT,
        )
        self.executar_o_bot.grid(
            row = 5,
            column = 1,
            pady = 10,
            sticky = tk.E
        )

        self.entrada_comandos.bind('<Return>', lambda event: mc.entry_command(self))
        self.inserir_token.bind('<Return>', lambda event: mc.update_token(self))

    def validate_token(self, d, i, P, s, S, v, V, W):
        import re
        if re.search(r'^[a-z0-9]{0,24}\.[a-z0-9]{0,6}\.[a-z0-9\-_]{0,27}$|^[a-z0-9]{0,24}\.[a-z0-9]{0,6}$|^[a-z0-9]{0,24}$', P, flags=re.IGNORECASE):
            return True
        else:
            return False