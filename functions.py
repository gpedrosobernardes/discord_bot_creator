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