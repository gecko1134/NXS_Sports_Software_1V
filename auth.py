
import json, hashlib, os

USERS_FILE = os.path.join(os.path.dirname(__file__), "..", "config", "users.json")

def _hash(pw: str)->str:
    return hashlib.sha256(pw.encode()).hexdigest()

def verify_login(email: str, password: str):
    try:
        with open(USERS_FILE, "r") as f:
            data = json.load(f)
    except Exception:
        return None
    user = next((u for u in data.get("users", []) if u["email"].lower()==email.lower()), None)
    if not user:
        return None
    if user.get("password_hash") == _hash(password):
        return {"email": user["email"], "name": user["name"], "role": user["role"]}
    return None
