import json

def open_json(path):
    with open(path, 'r', encoding='utf-8') as file:
        file = json.load(file)
    return file