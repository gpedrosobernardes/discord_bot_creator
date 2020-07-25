import discord, asyncio

class Bot(discord.Client):
    def __init__(self):
        super().__init__()

        @self.event
        def on_message(message):
            pass

