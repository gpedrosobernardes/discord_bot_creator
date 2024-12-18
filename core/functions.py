from datetime import datetime


def random_choose(lista: list):
    from random import choice

    return choice(lista)


def have_in(lista: list, string: str, reverse=False) -> bool:
    if not reverse:
        for x in lista:
            if x in string:
                return True
        return False
    else:
        for x in lista:
            if string in x:
                return True
        return False


def get_time(string: str):
    return datetime.now().strftime(string)
