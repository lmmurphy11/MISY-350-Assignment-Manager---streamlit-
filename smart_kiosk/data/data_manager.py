import json
from pathlib import Path

# record information into a json file
def load_data(json_path: Path):
    if json_path.exists():
        with open(json_path, "r") as f:
            return json.load(f)
    else:
        return []


# read information from a json file
def save_data(json_path: Path, json_file: list):
    with open(json_path, "w") as f:
        json.dump(json_file, f)
