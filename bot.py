import discord, asyncio, json
from functions import load_json, save_json
from interpreter import Interpreter

source_path = 'source/'
config_path = source_path+'config.json'
message_and_reply_path = source_path+"message and reply.json"

all_config = load_json(config_path)
token = all_config["token"]

class Bot():
    def __init__(self):
        client = discord.Client()

        @client.event
        async def on_ready():
            print('bot rodando.')
            
        @client.event
        async def on_message(any_message):
            dici = load_json(message_and_reply_path)
            for x in dici.keys():
                actual = dici[x]
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
                    multi_reply = actual['multi reply']
                except KeyError:
                    multi_reply = None
                
                await Interpreter.message_and_reply(
                    Interpreter,
                    not any_message.author.bot,
                    expected_message = expected_message,
                    any_message = any_message,
                    reply = reply,
                    reaction = reaction,
                    multi_reply = multi_reply)

        client.run(token)