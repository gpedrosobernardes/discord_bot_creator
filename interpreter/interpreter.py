import asyncio
import emoji
import discord
from functions import random_choose

class Interpreter:
    async def message_and_reply(self,
        *conditions,
        expected_message,
        message: discord.Message,
        reply = None,
        reaction = None):

        self.expected_message = expected_message
        
        all_condiction_is_true = conditions.count(True) == len(conditions)
        all_condiction_is_false = conditions.count(False) == len(conditions)
        
        message_condiction = message.content == expected_message if type(expected_message) == str else message.content in expected_message

        if all_condiction_is_true and message_condiction:
            await Interpreter.send_reply(self, reply, message)
            await Interpreter.send_reaction(self, reaction, message)

    async def send_reaction(self, reaction, message:discord.Message):
        if reaction:
            if type(reaction) == list:
                for each_reaction in reaction:
                    each_reaction = random_choose(each_reaction) if type(each_reaction) == list else each_reaction
                    each_reaction = emoji.emojize(each_reaction, use_aliases = True)
                    try:
                        await message.add_reaction(each_reaction)
                    except discord.HTTPException:
                        print(each_reaction)
            else:
                try:
                    reaction = emoji.emojize(reaction, use_aliases = True)
                    await message.add_reaction(reaction)
                except discord.HTTPException:
                    print(reaction)

    async def send_reply(self, reply, message:discord.Message):
        if reply:
            if type(reply) == list:
                for each_reply in reply:
                    each_reply = random_choose(each_reply) if type(each_reply) == list else each_reply
                    await message.channel.send(each_reply)
            else:
                await message.channel.send(each_reply)
