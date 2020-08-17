import discord
from datetime import datetime

class Variable:
    def __init__(self, message: discord.Message):
        self.message = message

        self.author_name = self.message.author.name
        self.guild_name = self.message.guild.name

        self.keys = {
            "<author name>" : self.author_name,
            "<guild name>" : self.guild_name,
            "<day>" : self.__get_time('%d'),
            "<month>" : self.__get_time('%m'),
            "<year>" : self.__get_time('%Y'),
            "<d-m-y>" : self.__get_time('%d/%m/%Y'),
        }
    def __get_time(self, string:str):
        return datetime.now().strftime(string)

    def apply_variable(self, string:str):
        for each_key in self.keys.keys():
            string = string.replace(each_key, self.keys[each_key])
        return string