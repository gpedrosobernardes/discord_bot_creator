def load_json(jsonfile) -> dict:
    import json
    with open(jsonfile, 'r') as json_file:
        return json.load(json_file)

def save_json(jsonfile, dicti: dict):
    import json
    with open(jsonfile, 'w') as json_file:
        dict_to_save = json.dumps(dicti)
        json_file.write(dict_to_save)

def random_choose(lista:list):
    import random
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
