import json

def clear_json_file(file_path):
    with open(file_path, 'w') as file:
        json.dump([], file)