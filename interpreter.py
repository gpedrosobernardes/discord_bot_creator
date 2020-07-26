import asyncio
import random
import emoji

class Interpreter:
    async def message_and_reply(self, *conditions, expected_message, any_message, reply:str,reaction=None):
        
        all_condiction_is_true = conditions.count(True) == len(conditions)
        all_condiction_is_false = conditions.count(False) == len(conditions)
        reply = reply[random.randint(0, (len(reply)-1))] if type(reply) == list else reply
        canal = any_message.channel

        if type(expected_message) == str:
            if all_condiction_is_true and any_message.content == expected_message:
                await canal.send(reply)
                if reaction:
                    await any_message.add_reaction(emoji.emojize(reaction))

        elif type(expected_message) == list:
            if all_condiction_is_true and any_message.content in expected_message:
                await canal.send(reply)
                if reaction:
                    await any_message.add_reaction(emoji.emojize(reaction))

