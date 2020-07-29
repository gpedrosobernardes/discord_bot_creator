import tkinter as tk
from functions import load_json

arial = ("Arial",12)

class NewMessage:
    def interface(self):

        lista_reactions = load_json('source/emojis.json')['emojis']
        lista_condictions = ['testando','testando 2','testando 3']

        janela = tk.Toplevel(master=self)

        # filhos da janela

        enter = tk.Button(
            master=janela,
            text='Confirmar'
        )
        expected_message_text = tk.Label(
            master=janela,
            text = "Mensagem esperada",
            font = arial,
        )
        expected_message = tk.Entry(
            master= janela,
            font = arial,
        )
        reply_text = tk.Label(
            master = janela,
            text= 'Resposta',
            font= arial,
        )
        reply = tk.Entry(
            master= janela,
            font = arial
        )
        reactions_text = tk.Label(
            master = janela,
            text= 'Reações',
            font = arial,
        )

        reactions = tk.Entry(
            master=janela,
            font= arial
        )
        
        condictions_text = tk.Label(
            master=janela,
            text = 'Condições',
            font = arial,
        )
        condictions = tk.Entry(
            master=janela,
            font= arial
        )

        # posicionamento

        # filhos da janela
        condictions_text.grid(
            row=1, column=1,
        )
        condictions.grid(
            row=1, column=2
        )
        expected_message_text.grid(
            row=2, column=1,
        )
        expected_message.grid(
            row=2, column= 2
        )
        reply_text.grid(
            row=3, column=1,
        )
        reply.grid(
            row=3, column=2
        )
        reactions_text.grid(
            row=4, column=1,
        )
        reactions.grid(
            row=4, column=2
        )
        enter.grid(
            row=5, column=2,
            padx = 10, pady=10
        )