import discord, asyncio, json
from functions import load_json, save_json
from interpreter.interpreter import Interpreter
import interfaces.paths as paths

all_config = load_json(paths.config)
token = all_config["token"]

class Bot():
    def __init__(self):
        client = discord.Client()

        @client.event
        async def on_ready():
            print('bot rodando.')
            
        @client.event
        async def on_message(message):
            message_and_reply_json = load_json(paths.message_and_reply)
            for key_message in message_and_reply_json.keys():
                
                actual = message_and_reply_json[key_message]
                expected_message = actual["expected message"]

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
                
                await Interpreter.message_and_reply(self,
                    conditions = conditions,
                    expected_message = expected_message,
                    message = message,
                    reply = reply,
                    reaction = reaction)

        client.run(token)