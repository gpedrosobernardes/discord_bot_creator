import asyncio
import interfaces.paths as paths
import discord
from functions import load_json, save_json, write_log, clear_txt, hora_atual

class Bot():
    def __init__(self):
        client = discord.Client()
        token = load_json(paths.config)['token']
        clear_txt(paths.log)

        @client.event
        async def on_ready():
            write_log(hora_atual()+' Bot inicializado.', paths.log)
            
        @client.event
        async def on_message(message):
            from interpreter.interpreter import Interpreter
            message_and_reply_json = load_json(paths.message_and_reply)
            for key_message in message_and_reply_json.keys():
                
                actual = message_and_reply_json[key_message]

                to_read = [
                    'expected message',
                    'reply',
                    'reaction',
                    'conditions',
                    'delete',
                    'pin',
                    'delay',
                    'kick',
                    'ban',
                    'where reaction',
                    'where reply'
                ]
                to_insert = dict()

                for each in to_read:
                    to_insert[each] = None
                    if each in actual:
                        to_insert[each] = actual[each]
                
                await Interpreter.message_and_reply(self,
                    message = message,
                    conditions = to_insert['conditions'],
                    expected_message = to_insert['expected message'],
                    reply = to_insert['reply'],
                    reaction = to_insert['reaction'],
                    delete = to_insert['delete'],
                    pin = to_insert['pin'],
                    delay = to_insert['delay'],
                    kick = to_insert['kick'],
                    ban = to_insert['ban'],
                    where_reply = to_insert['where reply'],
                    where_reaction = to_insert['where reaction']
                )

        client.run(token)

try:
    Bot()
except discord.errors.LoginFailure:
    write_log(hora_atual()+' Falha no login.', paths.log)
    