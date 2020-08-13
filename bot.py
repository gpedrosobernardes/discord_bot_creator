import asyncio
import interfaces.paths as paths

class Bot():
    def __init__(self):
        from functions import load_json, save_json
        import discord
        client = discord.Client()
        token = load_json(paths.config)['token']

        @client.event
        async def on_ready():
            print('bot rodando.')
            
        @client.event
        async def on_message(message):
            from interpreter.interpreter import Interpreter
            message_and_reply_json = load_json(paths.message_and_reply)
            for key_message in message_and_reply_json.keys():
                
                actual = message_and_reply_json[key_message]

                try:
                    expected_message = actual["expected message"]
                except KeyError:
                    expected_message = None
                try:
                    reply = actual['reply']
                except KeyError:
                    reply = None
                try:
                    reaction = actual['reaction']
                except KeyError:
                    reaction = None
                try:
                    conditions = actual['conditions']
                except KeyError:
                    conditions = None
                try:
                    delete = actual['delete']
                except KeyError:
                    delete = None
                try:
                    pin = actual['pin']
                except KeyError:
                    pin = None
                
                await Interpreter.message_and_reply(self,
                    conditions = conditions,
                    expected_message = expected_message,
                    message = message,
                    reply = reply,
                    reaction = reaction,
                    delete = delete,
                    pin = pin)

        client.run(token)