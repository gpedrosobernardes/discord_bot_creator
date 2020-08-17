import interfaces.paths as path
import tkinter as tk

class MainCommands:
    def on_ready(self):
        MainCommands.load_info_messages(self)
    
    def load_info_messages(self):
        '''carrega todas as mensagens do arquivo "message and reply.json" e insere no listbox de 
        mensagens.'''
        import json
        from functions import load_json, save_json
        try:
            all_messages = load_json(path.message_and_reply)
        except json.decoder.JSONDecodeError:
            pass
        else:
            for x in all_messages.keys():
                self.todas_mensagens.insert(tk.END, x)

    def remove_message(self):
        '''remove a mensagem selecionada do listbox de mensagens e a deleta do arquivo "message and 
        reply.json".'''
        from functions import load_json, save_json
        lista_nomes = self.todas_mensagens.get(0, tk.END)
        try:
            selecionado = self.todas_mensagens.curselection()[0]
        except IndexError:
            pass
        else:
            nome_selecionado:str = lista_nomes[selecionado]
            self.todas_mensagens.delete(selecionado)
            message_and_reply_json = load_json(path.message_and_reply)
            del message_and_reply_json[nome_selecionado]
            save_json(path.message_and_reply, message_and_reply_json)

    def remove_all_message(self):
        from functions import save_json
        self.todas_mensagens.delete(0, tk.END)
        dict_to_save = dict()
        save_json(path.message_and_reply, dict_to_save)

    def refresh_messages(self):
        '''atualiza das mensagens do listbox de mensagens.'''
        self.todas_mensagens.delete(0,tk.END)
        MainCommands.load_info_messages(self)

    def get_token(self):
        '''retorna o token atual salvo no arquivo "config.json".'''
        from functions import load_json
        return load_json(path.config)['token']

    def init_or_finish_bot(self):
        import subprocess, sys, threading, time, os 
        def _init_bot():
            self.bot_is_running = True
            self.executar_o_bot['text'] = 'Encerrar o bot'
            self.process = subprocess.Popen(
                [sys.executable, path.bot],
            )
            while True:
                time.sleep(0.1)
                if self.process.poll() == 0:
                    self.bot_is_running = False
                    self.executar_o_bot['text'] = 'Executar o bot'
        def _finish_bot():
            self.bot_is_running = False
            self.process.kill()
            self.executar_o_bot['text'] = 'Executar o bot'
        def check_if_change():
            cached = 0
            time.sleep(1)
            while True:
                time.sleep(0.1)
                if os.stat(path.log).st_mtime != cached:
                    cached = os.stat(path.log).st_mtime
                    write()
                if self.bot_is_running == False:
                    break                  
        def write():
            with open(path.log, 'r') as log:
                try:
                    string = log.readlines()[-1]
                except IndexError:
                    string = None
            if string:
                self.log_do_bot['state'] = tk.NORMAL
                self.log_do_bot.insert(tk.END, string)
                self.log_do_bot['state'] = tk.DISABLED
        if not self.bot_is_running:
            t = threading.Thread(target=_init_bot)
            t.start()
            tcc = threading.Thread(target=check_if_change)
            tcc.start()
        elif self.bot_is_running:
            _finish_bot()

    def entry_command(self):
        '''metodo responsavel por definir comandos para a entry do log do bot.'''
        entrada:str = self.entrada_comandos.get()
        if entrada in ['/clear','/limpar']:
            self.log_do_bot['state'] = tk.NORMAL
            self.log_do_bot.delete("0.0", tk.END)
            self.log_do_bot['state'] = tk.DISABLED
            self.entrada_comandos.delete(0, tk.END)

    def update_token(self):
        '''atualiza o token no arquivo "config.json" e na interface.'''
        from functions import load_json, save_json
        entrada:str = self.inserir_token.get()
        if len(entrada) == 59:
            self.inserir_token.delete(0, tk.END)
            current_dict = load_json(path.config)
            current_dict['token'] = entrada
            save_json(path.config, current_dict)
            self.token_atual['text'] = f'Seu token atual é:\n{entrada}'

    def edit_message(self):
        '''abre a interface NewMessage e carrega as informações salvas'''
        from interfaces.newmessage.main import NewMessage as nm
        lista_nomes = self.todas_mensagens.get(0, tk.END)
        try:
            selecionado:str = lista_nomes[self.todas_mensagens.curselection()[0]]
        except IndexError:
            pass
        else:
            nm.main(self, selecionado)