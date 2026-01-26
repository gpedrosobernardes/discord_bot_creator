from datetime import datetime

import discord


class Variable:
    def __init__(self, message: discord.Message):
        now = datetime.now()

        self.keys = {
            "author name": message.author.name,
            "guild name": message.guild.name if message.guild else "N/A",
            "day": now.strftime("%d"),
            "month": now.strftime("%m"),
            "year": now.strftime("%Y"),
            "d-m-y": now.strftime("%d/%m/%Y"),
        }

    def apply_variable(self, string: str):
        return string.format(**self.keys)
