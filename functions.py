import json
import random

def load_json(jsonfile) -> dict:
    json_file = open(jsonfile, 'r')
    return json.load(json_file)

def save_json(jsonfile, dicti: dict):
    json_file = open(jsonfile, 'w')
    dict_to_save = json.dumps(dicti)
    json_file.write(dict_to_save)
    json_file.close()

def random_choose(lista:list):
    return lista[random.randint(0,(len(lista)-1))]

def have_in(lista:list, string:str, reverse = False):
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
