import tkinter as tk

class SearchBox(tk.Entry):
    def __init__(self, lista:list, master, master_overlap, 
                command=None, command_key_pressed=None,
                command_entry_pressed=None, activestyle='none',
                **options):
        super().__init__(master, **options)
        self.command = command
        self.command_key_pressed = command_key_pressed
        self.command_entry_pressed = command_entry_pressed
        self.master = master
        self.master_overlap = master_overlap
        self.lista = lista

        self.listbox = tk.Listbox(master=master_overlap, activestyle=activestyle, **options)
        self.listbox_is_visible = False
        self.listbox.bind('<<ListboxSelect>>', self.__listbox_pressed)
        self.bind('<Button-1>', self.__entry_pressed)
        self.bind('<Key>', self.__key_pressed)

        for x in self.lista:
            self.listbox.insert(tk.END, x)

    def __listbox_pressed(self, event):
        # por algum motivos essa bind em especial, quando é chamada por uma instancia da classe
        # é executada na outra tbm mas meio que da pra resolver de uma forma porca com um except 
        try:
            self.listbox.get(self.listbox.curselection())
        except tk.TclError:
            pass
        else:
            self.delete(0, tk.END)
            self.insert(0, self.listbox.get(self.listbox.curselection()))
            self.set_listbox_invisible()

    def __entry_pressed(self, event):
        if not self.command_entry_pressed == None:
            self.command_entry_pressed(self)
        if not self.listbox_is_visible:
            self.set_listbox_visible()
        else:
            self.set_listbox_invisible()
        self.focus_set()

    def set_listbox_visible(self):
        # eu preciso achar alguma maneira de conseguir a posição absoluta em relação a janela se não eu não consigo usar essa classe se o organizador tiver mais de dois frames
        wl, hl, xl ,yl = tuple(map(lambda x: int(x), self.listbox.winfo_geometry().replace('x','+').split('+')))
        w, h, x ,y = tuple(map(lambda x: int(x), self.winfo_geometry().replace('x','+').split('+')))
        rx, ry = tuple(map(lambda x: int(x), (self.winfo_rootx(),self.winfo_rooty())))
        jx, jy = tuple(map(lambda x: int(x), (self.winfo_toplevel().winfo_rootx(),self.winfo_toplevel().winfo_rooty())))
        # mw, mh, mx, my = self.master.winfo_geometry().replace('x','+').split('+')
        # posx, posy = (int(x)+int(mx), (int(y)+int(h))+int(my)) if self.winfo_parent().count('frame') == 2 else (int(x), int(y)+int(h))
        posx, posy = rx-jx, (ry-jy)+h
        self.master_overlap:tk.Frame

        self.master_overlap.config(width=wl, height=hl)
        self.master_overlap.place(x=posx,y=posy)
        self.listbox.place(x=1,y=1)
        self.listbox_is_visible = True

    def set_listbox_invisible(self):
        self.listbox.place_forget()
        self.master_overlap.place_forget()
        self.listbox_is_visible = False

    def __key_pressed(self, event):
        enter = '\r'
        entrada = str(event.widget.get()+event.char).lower() if not event.char == '\x08' else str(event.widget.get())[0:-1].lower()
        if not self.command_key_pressed == None:
            self.command_key_pressed(event)
        if event.char == enter and not self.command == None:
            if entrada in self.lista:
                self.command()
        else:
            if not self.listbox_is_visible:
                self.set_listbox_visible()
            lista_listbox = self.listbox.get(0,tk.END)
            lista_para_remover = list(filter(lambda x: not entrada in x, lista_listbox))
            lista_para_adicionar = list(filter(lambda x: entrada in x, self.lista))
            for x in lista_para_remover:
                self.listbox.delete(lista_listbox.index(x)-lista_para_remover.index(x))

            for x in lista_para_adicionar:
                if not x in lista_listbox:
                    self.listbox.insert(tk.END, x)