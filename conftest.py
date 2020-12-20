import json


def load_json_data(path):
    with open(path) as json_data:
        return json.load(json_data)
