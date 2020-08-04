import tkinter as tk
from interfaces.tkclasses.SearchBox import SearchBox as sb
from interfaces.fonts import *
from functions import load_json
from multiprocessing import Process
from bot import Bot

class FrameDireito:
    def main(self):
        frame_direito_bot = tk.Frame(
            master = self.camada_1
        )
        frame_superior = tk.Frame(
            master = frame_direito_bot
        )
        self.log_do_bot = tk.Text(
            master = frame_superior,
            font = arial,
            width = 50,
        )
        self.entrada_comandos = tk.Entry(
            master = frame_superior,
            font = arial
        )
        button_enter_entrada_comandos = tk.Button(
            master = frame_superior,
            font = arial,
            text = '>',
            command = lambda : FrameDireito.__entry_command(self)
        )
        frame_inferior = tk.Frame(
            master = frame_direito_bot
        )
        inserir_token = sb(
            lista = [],
            master = frame_inferior,
            master_overlap = self.camada_2,
        )
        FrameDireito.__read_token(self)
        token_atual = tk.Label(
            master = frame_inferior,
            text = 'Seu token atual é:\n'
                   f'{self.token}'
        )
        self.executar_o_bot = tk.Button(
            master = frame_inferior,
            text = 'Executar o bot',
            font = arial,
            relief = tk.FLAT,
            command = lambda : FrameDireito.__init_or_finish_bot(self)
        )
        frame_direito_bot.grid(
            row = 1,
            column = 2
        )
        frame_superior.grid(
            row = 1,
            column = 1
        )
        self.log_do_bot.grid(
            row = 1,
            column = 1
        )
        self.entrada_comandos.grid(
            row = 2,
            column = 1
        )
        button_enter_entrada_comandos.grid(
            row = 2,
            column = 2
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
        self.executar_o_bot.grid(
            row = 1,
            column = 2
        )

        self.entrada_comandos.bind('<Return>', lambda event: FrameDireito.__entry_command(self))

    def __read_token(self):
        config_json = load_json('source/config.json')
        self.token = config_json['token']

    def __init_or_finish_bot(self):
        pass
        # preciso achar alguma maneira de executar o bot simutaneamente a interface,
        # mas o problema é que threading e multiprocessing não funcionam :(

    def __entry_command(self):
        entrada:str = self.entrada_comandos.get()
        if entrada in ['/clear','/limpar']:
            self.log_do_bot.delete("0.0", tk.END)
            self.entrada_comandos.delete(0, tk.END)
