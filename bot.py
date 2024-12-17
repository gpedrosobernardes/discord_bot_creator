import asyncio

import discord
import emoji
from discord import Intents, LoginFailure

import interfaces.paths as paths
from core.config import instance as config
from core.functions import load_json, write_log, clear_txt, hora_atual, random_choose
from interpreter.conditions import MessageConditions
from interpreter.variable import Variable


class Bot:

    def __init__(self):
        self.client = discord.Client(intents=Intents.all())
        clear_txt(paths.log)

        @self.client.event
        async def on_ready():
            self.log("Bot iniciado!")

        @self.client.event
        async def on_message(message):
            self.log(f'Identificada mensagem "{message.content}".')
            message_and_reply_json = load_json(paths.message_and_reply)
            for key_message, actual in message_and_reply_json.items():

                to_read = [
                    "expected message",
                    "reply",
                    "reaction",
                    "conditions",
                    "delete",
                    "pin",
                    "delay",
                    "kick",
                    "ban",
                    "where reaction",
                    "where reply",
                ]
                to_insert = dict()

                for each in to_read:
                    to_insert[each] = None
                    if each in actual:
                        to_insert[each] = actual[each]

                await message_and_reply(
                    message=message,
                    conditions=to_insert["conditions"],
                    expected_message=to_insert["expected message"],
                    reply=to_insert["reply"],
                    reaction=to_insert["reaction"],
                    delete=to_insert["delete"],
                    pin=to_insert["pin"],
                    delay=to_insert["delay"],
                    kick=to_insert["kick"],
                    ban=to_insert["ban"],
                    where_reply=to_insert["where reply"],
                    where_reaction=to_insert["where reaction"],
                )

        @self.client.event
        async def apply_delay(delay):
            if delay:
                delay = int(delay)
                self.log(
                    f"Aguardando delay de {delay} segundos para a proxima execução!"
                )
                await asyncio.sleep(delay)

        @self.client.event
        async def send_reaction(reactions, message: discord.Message, where):
            if reactions:
                for reaction in reactions:
                    code_reaction = reaction
                    reaction = (
                        random_choose(reaction)
                        if isinstance(reaction, list)
                        else reaction
                    )
                    reaction = emoji.emojize(reaction)
                    try:
                        if where == "author":
                            await message.add_reaction(reaction)
                        elif where == "bot" and message.author.bot:
                            await message.add_reaction(reaction)
                        self.log(
                            f'Adicionando a reação "{code_reaction}" a mensagem "{emoji.demojize(message.content)}" do autor {message.author}.'
                        )
                    except discord.HTTPException:
                        print(reaction)

        @self.client.event
        async def send_reply(replies, message: discord.Message, where):
            if replies:
                for reply in replies:
                    reply = random_choose(reply) if isinstance(reply, list) else reply
                    reply = Variable(message).apply_variable(reply)
                    if where == "group":
                        await message.channel.send(reply)
                    elif where == "private":
                        dm_channel = await message.author.create_dm()
                        await dm_channel.send(reply)
                    self.log(
                        f'Enviando a resposta "{reply}" há mensagem "{emoji.demojize(message.content)}" do author {message.author}.'
                    )

        @self.client.event
        async def remove_message(delete, message: discord.Message):
            if delete and isinstance(message.channel, discord.GroupChannel):
                await message.delete()
                self.log(
                    f'Removendo mensagem "{emoji.demojize(message.content)}" do autor {message.author}.'
                )

        @self.client.event
        async def pin_message(pin, message: discord.Message):
            if pin:
                await message.pin()
                self.log(
                    f'Fixando mensagem "{emoji.demojize(message.content)}" do autor {message.author}.'
                )

        @self.client.event
        async def kick_member(kick, message: discord.Message):
            if kick and isinstance(message.channel, discord.GroupChannel):
                await message.author.kick()
                self.log(f'Expulsando jogador "{message.author.name}".')

        @self.client.event
        async def ban_member(ban, message: discord.Message):
            if ban and isinstance(message.channel, discord.GroupChannel):
                await message.author.ban()
                self.log(f'Banindo jogador "{message.author.name}".')

        async def message_and_reply(
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
            where_reply="group",
            where_reaction="author",
        ):

            message_condition = MessageConditions(
                message, expected_message=expected_message
            )
            all_condition_is_true = False
            conditions_to_confirm = []
            if conditions:
                for each_conditions in conditions:
                    conditions_to_confirm.append(
                        message_condition.string_conditions[each_conditions]
                    )
            # é importante adicionar a condição expected message se tiver alguma mensagem esperada porque, senão podem ocorrer erros inesperados.
            if expected_message:
                conditions_to_confirm.append(message.content in expected_message)

            all_condition_is_true = conditions_to_confirm.count(True) == len(
                conditions_to_confirm
            )

            self.log(f"Verificando condições {conditions_to_confirm}")

            if all_condition_is_true:
                await apply_delay(delay)
                await send_reply(reply, message, where_reply)
                await send_reaction(reaction, message, where_reaction)
                await remove_message(delete, message)
                await pin_message(pin, message)

    def log(self, message):
        formated_message = f"{hora_atual()}: {message}"
        write_log(formated_message, paths.log)
        return formated_message

    def run(self):
        try:
            self.client.run(config.get("token"))
        except LoginFailure as exception:
            self.log(str(exception))


class IntegratedBot(Bot):
    def __init__(self, app):
        self.app = app
        super().__init__()

        @self.client.event
        async def on_ready():
            self.log("Bot iniciado!")
            self.app.change_init_bot_button()

    def log(self, message):
        formated_message = super().log(message)
        self.app.log(formated_message + "\n")


if __name__ == "__main__":
    bot = Bot()
    bot.run()
