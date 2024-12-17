from datetime import datetime


def load_json(jsonfile) -> dict:
    import json

    with open(jsonfile, "r") as json_file:
        return json.load(json_file)


def save_json(jsonfile, dicti: dict):
    import json

    with open(jsonfile, "w") as json_file:
        dict_to_save = json.dumps(dicti)
        json_file.write(dict_to_save)


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
