import json
import os

DATA_FILE = "data.json"

def save_data(data):
    with open(DATA_FILE, "w", encoding = "utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_data():
    if not os.path.exists(DATA_FILE):
        default_data = {"users": {}}
        save_data(default_data)
        return default_data
    with open(DATA_FILE, "r", encoding = "utf-8") as f:
        try: return json.load(f)
        except json.JSONDecodeError:
            default_data = {"users": {}}
            save_data(default_data)
            return default_data