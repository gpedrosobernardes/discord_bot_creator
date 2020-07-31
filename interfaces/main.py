import tkinter as tk
from interfaces.newmessage.main import NewMessage as nm

Arial = ("Arial",12)

class Main(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Bot Discord Easy Creator')

        adicionar_mensagem_button = tk.Button(
            master = self,
            text = 'Adicionar mensagem',
            font = Arial,
            command = lambda : nm.main(self)
        )

        adicionar_mensagem_button.pack()

        self.mainloop()

Main()