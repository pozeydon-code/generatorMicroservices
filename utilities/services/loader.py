import json

def load_service_definitions(json_path):
    with open(json_path, "r") as f:
        return json.load(f)
