import discord, asyncio, json
from functions import load_json, save_json
from interpreter import Interpreter

config_path = 'config.json'
all_config = load_json(config_path)
token = all_config["token"]
message_and_reply_path = "message and reply.json"

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
                expected_message = dici[x]["expected message"]
                reply = dici[x]['reply']
                await Interpreter.message_and_reply(True, expected_message=expected_message, any_message=any_message, reply=reply)

        client.run(token)

Bot()