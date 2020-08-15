import tkinter as tk

class SearchBox(tk.Entry):
    def __init__(self,
        lista: list,
        master,
        master_overlap, 
        activestyle = 'none',
        **options):
        
        super().__init__(
            master,
            **options
        )
        
        self.master = master
        self.master_overlap = master_overlap
        self.lista = lista
        
        self.listbox = tk.Listbox(
            master = master_overlap,
            activestyle = activestyle,
            **options
        )
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
        if not self.listbox_is_visible:
            self.set_listbox_visible()
        else:
            self.set_listbox_invisible()
        self.focus_set()

    def set_listbox_visible(self):
        wl, hl, xl ,yl = tuple(map(lambda x: int(x), self.listbox.winfo_geometry().replace('x','+').split('+')))
        w, h, x ,y = tuple(map(lambda x: int(x), self.winfo_geometry().replace('x','+').split('+')))
        rx, ry = tuple(map(lambda x: int(x), (self.winfo_rootx(),self.winfo_rooty())))
        jx, jy = tuple(map(lambda x: int(x), (self.winfo_toplevel().winfo_rootx(),self.winfo_toplevel().winfo_rooty())))
        posx, posy = rx-jx, (ry-jy)+h
            
        for child in self.master_overlap.winfo_children():
            child.pack_forget()
        self.master_overlap.place(x = posx, y = posy, width = w, height = 194)
        self.listbox.pack(fill = tk.X, expand = 1)
        self.listbox_is_visible = True
        self.update_listbox()

    def set_listbox_invisible(self):
        self.listbox.pack_forget()
        self.master_overlap.place_forget()
        self.listbox_is_visible = False

    def update_listbox(self, event = None):
        entrada = self.get() if not event else str(event.widget.get()+event.char).lower() if not event.char == '\x08' else str(event.widget.get())[0:-1].lower()

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

    def __key_pressed(self, event):
        if event.char == '\x08':
            self.after(10, lambda: self.update_listbox(event))
        else:
            self.update_listbox(event)