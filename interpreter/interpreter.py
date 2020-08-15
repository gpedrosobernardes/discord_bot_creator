import asyncio
import emoji
import discord
from functions import random_choose, write_log, hora_atual
from interpreter.conditions import MessageConditions
from interpreter.variable import Variable, apply_variable
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
        delay
    ):

        self.expected_message = expected_message

        message_condition = MessageConditions(
            message,
            expected_message = expected_message
        )

        all_condition_is_true = False
        if conditions:
            conditions_to_confirm = []
            for each_conditions in conditions:
                conditions_to_confirm.append(message_condition.string_conditions[each_conditions])
            # if expected_message:
            #     conditions_to_confirm.append(message_condition.string_conditions['expected message'])
            
            all_condition_is_true = conditions_to_confirm.count(True) == len(conditions_to_confirm)

        if all_condition_is_true or conditions == None:
            await Interpreter.apply_delay(self, delay)
            await Interpreter.send_reply(self, reply, message)
            await Interpreter.send_reaction(self, reaction, message)
            await Interpreter.remove_message(self, delete, message)
            await Interpreter.pin_message(self, pin, message)

    async def apply_delay(self, delay):
        if delay:
            delay = int(delay)
            await asyncio.sleep(delay)

    async def send_reaction(self, reaction, message:discord.Message):
        if reaction:
            for each_reaction in reaction:
                code_reaction = each_reaction
                each_reaction = random_choose(each_reaction) if type(each_reaction) == list else each_reaction
                each_reaction = emoji.emojize(each_reaction, use_aliases = True)
                try:
                    await message.add_reaction(each_reaction)
                    write_log(hora_atual()+f' Adicionando a reação "{code_reaction}" a mensagem "{message.content}" do autor {message.author}.', path.log)
                except discord.HTTPException:
                    print(each_reaction)

    async def send_reply(self, reply, message: discord.Message):
        if reply:
            variables = Variable(message).keys
            for each_reply in reply:
                each_reply = random_choose(each_reply) if type(each_reply) == list else each_reply
                each_reply = apply_variable(each_reply, variables)
                await message.channel.send(each_reply)
                write_log(hora_atual()+f' Enviando a resposta "{each_reply}" há mensagem "{message.content}" do author {message.author}.', path.log)

    async def remove_message(self, delete, message: discord.Message):
        if delete:
            await message.delete()
            write_log(hora_atual()+f' Removendo mensagem "{message.content}" do autor {message.author}.',path.log)
    
    async def pin_message(self, pin, message: discord.Message):
        if pin:
            await message.pin()
            write_log(hora_atual()+f' Fixando mensagem "{message.content}" do autor {message.author}.',path.log)
