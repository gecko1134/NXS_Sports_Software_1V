
import os, json
import urllib.request

def _post(url: str, payload: dict):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.read()

def slack(text: str):
    url = os.getenv("SLACK_WEBHOOK_URL")
    if not url: 
        print("[SLACK] missing SLACK_WEBHOOK_URL")
        return False
    _post(url, {"text": text})
    return True

def teams(text: str):
    url = os.getenv("TEAMS_WEBHOOK_URL")
    if not url:
        print("[TEAMS] missing TEAMS_WEBHOOK_URL")
        return False
    # Microsoft Teams expects "text" in JSON payload for simple cards
    _post(url, {"text": text})
    return True

def notify_all(text: str):
    a = slack(text)
    b = teams(text)
    return a or b
