import discord, asyncio, json
from functions import load_json, save_json

class Bot(discord.Client):
    def __init__(self):
        super().__init__()

        @self.event
        def on_message(message):
            pass

