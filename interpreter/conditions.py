import discord
from functions import have_in

conditions_keys = ['expected message','not expected message','mention someone','not mention someone','mention everyone','not mention everyone','pinned','not pinned','author is expected','not author is expected','author is bot','not author is bot','number in message','not number in message','symbols in message', 'not symbols in message']
symbols = ["'",'"','!','@','#','$','%','¨','&','*','(',')','-','_','+','=','§','`','´','[','{','ª','~','^',']','}','º',',','.','<','>',':',';','?','/','°','|']
numbers = ['1','2','3','4','5','6','7','8','9']

class MessageConditions:
    def __init__(self,
        message : discord.Message,
        expected_author : discord.Member = None,
        expected_message = None,
        ):

        self.message = message

        self.expected_message = False if expected_message == None else self.message.content == expected_message if type(expected_message) == str else message.content in expected_message
        self.not_expected_message = not self.expected_message
        self.mention_someone = True if len(self.message.mentions) >= 1 else False
        self.not_mention_someone = not self.mention_someone
        self.mention_everyone = self.message.mention_everyone
        self.not_mention_everyone = not self.mention_everyone
        self.pinned = self.message.pinned
        self.not_pinned = not self.pinned
        self.author_is_expected = False if expected_author == None else self.message.author == expected_author
        self.not_author_is_expected = not self.author_is_expected
        self.author_is_bot = self.message.author.bot
        self.not_author_is_bot = not self.author_is_bot
        self.number_in_message = have_in(numbers, self.message.content)
        self.not_number_in_message = not self.number_in_message
        self.symbols_in_message = have_in(symbols, self.message.content)
        self.not_symbols_in_message = not self.symbols_in_message


        self.string_conditions = {
            'expected message' : self.expected_message,
            'not expected message' : self.not_expected_message,
            'mention someone' : self.mention_someone,
            'not mention someone' : self.not_mention_someone,
            'mention everyone' : self.mention_everyone,
            'not mention everyone' : self.not_mention_everyone,
            'pinned' : self.pinned,
            'not pinned' : self.not_pinned,
            'author is expected' : self.author_is_expected,
            'not author is expected' : self.not_author_is_expected,
            'author is bot' : self.author_is_bot,
            'not author is bot' : self.not_author_is_bot,
            'number in message' : self.number_in_message,
            'not number in message' : self.not_number_in_message,
            'symbols in message' : self.symbols_in_message,
            'not symbols in message' : self.not_symbols_in_message
        }