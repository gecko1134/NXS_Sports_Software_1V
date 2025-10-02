
import json, os, datetime

def load_json(path: str, default=None):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception:
        return default

def save_json(path: str, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def now_iso():
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat()+"Z"
