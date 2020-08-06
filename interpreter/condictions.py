import discord

class MessageCondictions:
    def __init__(self,
        message : discord.Message,
        expected_author : discord.Member = None,

        ):

        self.message = message

        self.mention_everyone = self.message.mention_everyone
        self.pinned = self.message.pinned
        self.author_is_expected = False if expected_author == None else self.message.author == expected_author

        self.string_condictions = {
            'mention everyone' : self.mention_everyone,
            'pinned' : self.pinned,
            'author is expected' : self.author_is_expected
        }