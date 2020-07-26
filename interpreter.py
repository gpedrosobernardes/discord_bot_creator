import asyncio

class Interpreter:
    async def message_and_reply(self, *conditions, expected_message:str, any_message, reply:str,reaction=None):
        
        all_condiction_is_true = conditions.count(True) == len(conditions)
        all_condiction_is_false = conditions.count(False) == len(conditions)

        canal = any_message.channel
        if all_condiction_is_true and any_message.content == expected_message:
            await canal.send(reply)
            if reaction:
                await any_message.add_reaction(reaction)
