import tkinter as tk
from interfaces.tkclasses.SearchBox import SearchBox as sb
from interfaces.fonts import *

class FrameDireito:
    def main(self):
        frame_direito_bot = tk.Frame(
            master = self.camada_1
        )
        log_do_bot = tk.Text(
            master = frame_direito_bot,
            font = arial,
            width = 50,
        )
        frame_inferior = tk.Frame(
            master = frame_direito_bot
        )
        frame_superior = tk.Frame(
            master = frame_direito_bot
        )
        inserir_token = sb(
            lista = [],
            master = frame_inferior,
            master_overlap = self.camada_2,
        )
        token_atual = tk.Label(
            master = frame_inferior,
            text = f'Seu token atual é:\n'
                    '{token}'
        )
        executar_o_bot = tk.Button(
            master = frame_inferior,
            text = 'Executar o bot',
            font = arial,
            relief = tk.FLAT
        )

        frame_direito_bot.grid(
            row = 1,
            column = 2
        )
        frame_superior.grid(
            row = 1,
            column = 1
        )
        log_do_bot.grid(
            row = 1,
            column = 1
        )
        frame_inferior.grid(
            row = 2,
            column = 1,
        )
        token_atual.grid(
            row = 1,
            column = 1
        )
        inserir_token.grid(
            row = 2,
            column = 1
        )
        executar_o_bot.grid(
            row = 1,
            column = 2
        )