import json
from pathlib import Path

CONFIG_FILE = Path.home() / ".sbcli.json"

def save_url(context: str, url: str):
    with open(CONFIG_FILE, "w") as f:
        json.dump({context: {"url": url}}, f)

def get_url(context: str):
    if not CONFIG_FILE.exists():
        return None
    with open(CONFIG_FILE, "r") as f:
        data = json.load(f)
        return data.get(context, {}).get("url")
