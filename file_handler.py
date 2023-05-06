import json
def read_from_json(file_name):
    file = open(file_name, "r", encoding="utf-8")
    model = json.load(file)
    file.close()
    return model