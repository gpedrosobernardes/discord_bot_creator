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
            state = tk.DISABLED
        )
        frame_entrada_comandos = tk.Frame(
            master = frame_direito_bot,
            bg = color.azul_frame
        )
        self.entrada_comandos = tk.Entry(
            master = frame_entrada_comandos,
            font = arial,
            bg = color.azul_entrada,
            width = 40,
            relief = tk.FLAT
        )
        button_entrada_comandos = tk.Button(
            master = frame_entrada_comandos,
            # font = arial,
            text = '>',
            command = lambda : mc.entry_command(self),
            bg = color.azul_entrada,
            relief = tk.FLAT
        )
        frame_inserir_token = tk.Frame(
            master = frame_direito_bot,
            bg = color.azul_frame
        )
        self.inserir_token = tk.Entry(
            master = frame_inserir_token,
            bg = color.azul_entrada,
            relief = tk.FLAT
        )
        self.button_inserir_token = tk.Button(
            master = frame_inserir_token,
            bg = color.azul_entrada,
            relief = tk.FLAT,
            text = '>',
            command = lambda : mc.update_token(self)
        )
        self.token = mc.get_token(self)
        self.token_atual = tk.Label(
            master = frame_direito_bot,
            text = 'Seu token atual é:\n'
                   f'{self.token}',
            bg = color.azul_frame
        )
        self.executar_o_bot = tk.Button(
            master = frame_direito_bot,
            text = 'Executar o bot',
            font = arial,
            relief = tk.FLAT,
            command = lambda : mc.init_or_finish_bot(self),
            bg = color.azul_entrada,
        )
        frame_direito_bot.grid(
            row = 1,
            column = 2
        )
        self.log_do_bot.grid(
            row = 1,
            column = 1,
            columnspan = 2
        )
        frame_entrada_comandos.grid(
            row = 2,
            column = 1,
            columnspan = 2,
            sticky = tk.W+tk.E
        )
        self.entrada_comandos.grid(
            row = 1,
            column = 1,
            sticky = tk.W+tk.E
        )
        button_entrada_comandos.grid(
            row = 1,
            column = 2,
            sticky = tk.E
        )
        self.token_atual.grid(
            row = 3,
            column = 1,
            sticky = tk.W
        )
        frame_inserir_token.grid(
            row = 4,
            column = 1,
            sticky = tk.W
        )
        self.inserir_token.grid(
            row = 1,
            column = 1,
        )
        self.button_inserir_token.grid(
            row = 1,
            column = 2,
        )
        self.executar_o_bot.grid(
            row = 3,
            column = 2,
            rowspan = 2,
            # sticky = tk.E
        )

        self.entrada_comandos.bind('<Return>', lambda event: mc.entry_command(self))
        self.inserir_token.bind('<Return>', lambda event: mc.update_token(self))