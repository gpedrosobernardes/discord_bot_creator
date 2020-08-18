import asyncio
import emoji
import discord
from functions import random_choose, write_log, hora_atual
from interpreter.conditions import MessageConditions
from interpreter.variable import Variable
import interfaces.paths as path

class Interpreter:
    async def message_and_reply(self,
        message: discord.Message,
        conditions,
        expected_message,
        reply,
        reaction,
        delete,
        pin,
        delay,
        ban,
        kick,
        where_reply = 'group',
        where_reaction = 'author'
    ):

        self.expected_message = expected_message

        message_condition = MessageConditions(
            message,
            expected_message = expected_message
        )
        all_condition_is_true = False
        conditions_to_confirm = []
        if conditions:
            for each_conditions in conditions:
                conditions_to_confirm.append(message_condition.string_conditions[each_conditions])
        # é importante adicionar a condição expected message se tiver alguma mensagem esperada porque, senão podem ocorrer erros inesperados.
        if expected_message:
            conditions_to_confirm.append(message.content in expected_message)
        
        all_condition_is_true = conditions_to_confirm.count(True) == len(conditions_to_confirm)
            
        if all_condition_is_true:
            await Interpreter.apply_delay(self, delay)
            reply_sent = await Interpreter.send_reply(self, reply, message, where_reply)
            await Interpreter.send_reaction(self, reaction, message, where_reaction, reply_sent)
            await Interpreter.remove_message(self, delete, message)
            await Interpreter.pin_message(self, pin, message)

    async def apply_delay(self, delay):
        if delay:
            delay = int(delay)
            await asyncio.sleep(delay)

    async def send_reaction(self, reaction, message:discord.Message, where, bot_reply):
        if reaction:
            for r in reaction:
                code_reaction = r
                r = random_choose(r) if isinstance(r, list) else r
                r = emoji.emojize(r, use_aliases = True)
                try:
                    if where == 'author':
                        await message.add_reaction(r)
                    elif where == 'bot' and bot_reply:
                        await bot_reply.add_reaction(r)
                    write_log(hora_atual()+f' Adicionando a reação "{code_reaction}" a mensagem "{emoji.demojize(message.content)}" do autor {message.author}.', path.log)
                except discord.HTTPException:
                    print(r)

    async def send_reply(self, reply, message: discord.Message, where) -> discord.Message:
        if reply:
            for r in reply:
                r = random_choose(r) if isinstance(r, list) else r
                r = Variable(message).apply_variable(r)
                print(where)
                if where == 'group':
                    return await message.channel.send(r)
                elif where == 'private':
                    DMchannel = await message.author.create_dm()
                    return await DMchannel.send(r)
                write_log(hora_atual()+f' Enviando a resposta "{r}" há mensagem "{emoji.demojize(message.content)}" do author {message.author}.', path.log)

    async def remove_message(self, delete, message: discord.Message):
        if delete and isinstance(message.channel, discord.GroupChannel):
            await message.delete()
            write_log(hora_atual()+f' Removendo mensagem "{emoji.demojize(message.content)}" do autor {message.author}.',path.log)
    
    async def pin_message(self, pin, message: discord.Message):
        if pin:
            await message.pin()
            write_log(hora_atual()+f' Fixando mensagem "{emoji.demojize(message.content)}" do autor {message.author}.',path.log)

    async def kick_member(self, kick, message: discord.Message):
        if kick and isinstance(message.channel, discord.GroupChannel):
            await message.author.kick()
            write_log(hora_atual()+f' Expulsando jogador "{message.author.name}".')
    
    async def ban_member(self, ban, message: discord.Message):
        if ban and isinstance(message.channel, discord.GroupChannel):
            await message.author.ban()
            write_log(hora_atual()+f' Banindo jogador "{message.author.name}"."')