from typing import List

from discord import abc


def bot_mentions_count(mentions: List[abc.User]) -> int:
    return len(list(filter(lambda m: m.bot, mentions)))


def mentions_count(mentions: List[abc.User]) -> int:
    return len(mentions)


def mentions_someone(mentions: List[abc.User], someone: abc.User) -> bool:
    return any(map(lambda m: m == someone, mentions))