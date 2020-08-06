import discord, asyncio, json
from functions import load_json, save_json
from interpreter.interpreter import Interpreter

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
        async def on_message(message):
            message_and_reply_json = load_json(message_and_reply_path)
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
                except KeyError:
                    multi_reply = None
                
                await Interpreter.message_and_reply(self,
                    not message.author.bot,
                    expected_message = expected_message,
                    message = message,
                    reply = reply,
                    reaction = reaction)

        client.run(token)

Bot()