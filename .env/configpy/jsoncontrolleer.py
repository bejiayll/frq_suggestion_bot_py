import json 

def dump(file: str, data: dict):
    with open(file, "w") as f:
        json.dump(data, f)

def load(file: str):
    with open(file, 'r') as f:
        return json.load(f)
