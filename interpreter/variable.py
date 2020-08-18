import discord
from datetime import datetime

class Variable:
    def __init__(self, message: discord.Message):
        self.keys = {
            "<author name>" : message.author.name, # if isinstance(message.channel, discord.GroupChannel) else message.author.nick
            "<guild name>" : message.guild.name if isinstance(message.channel, discord.GroupChannel) else None,
            "<day>" : self.__get_time('%d'),
            "<month>" : self.__get_time('%m'),
            "<year>" : self.__get_time('%Y'),
            "<d-m-y>" : self.__get_time('%d/%m/%Y'),
        }
    def __get_time(self, string:str):
        return datetime.now().strftime(string)

    def apply_variable(self, string:str):
        for key, value in self.keys.items():
            if value == None:
                continue
            string = string.replace(key, value)
        return string