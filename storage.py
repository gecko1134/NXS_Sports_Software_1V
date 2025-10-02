
import json, os, datetime
def load_json(path, default=None):
    try:
        return json.load(open(path))
    except Exception: return default
def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(data, open(path,"w"), indent=2)
def now_iso():
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat()+"Z"
