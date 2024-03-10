import json

def json_loader(file):
    with open(file) as f:
        data = json.load(f)
        return data