import discord, asyncio, json
from functions import load_json, save_json
from interpreter import Interpreter
from emojis import emojis

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
                actual = dici[x]
                expected_message = actual["expected message"]
                reply = actual['reply']
                try:
                    reaction = emojis[actual['reaction']]
                except KeyError:
                    pass
                await Interpreter.message_and_reply(Interpreter, not any_message.author.bot, expected_message=expected_message, any_message=any_message, reply=reply, reaction=reaction)

        client.run(token)

Bot()