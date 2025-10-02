
import json, hashlib, os
USERS_FILE = os.path.join(os.path.dirname(__file__), "..", "config", "users.json")
def _hash(pw: str)->str: return hashlib.sha256(pw.encode()).hexdigest()
def _load_users():
    try: return json.load(open(USERS_FILE))
    except Exception: return {"users":[]}
def _save_users(data):
    os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
    json.dump(data, open(USERS_FILE,"w"), indent=2)
def verify_login(email: str, password: str):
    data = _load_users()
    for u in data.get("users", []):
        if u["email"].lower()==email.lower() and u.get("password_hash")==_hash(password):
            return {"email": u["email"], "name": u.get("name",""), "role": u.get("role","")}
    return None
def add_user(email: str, name: str, role: str, password: str):
    data = _load_users()
    if any(u["email"].lower()==email.lower() for u in data.get("users", [])):
        return False, "User already exists"
    data["users"].append({"email": email, "name": name, "role": role, "password_hash": _hash(password)})
    _save_users(data); return True, "Added"
def remove_user(email: str):
    data = _load_users(); before=len(data.get("users", []))
    data["users"]=[u for u in data.get("users", []) if u["email"].lower()!=email.lower()]
    _save_users(data); return True, f"Removed {before-len(data['users'])} user(s)"
def reset_password(email: str, new_password: str):
    data=_load_users(); changed=False
    for u in data.get("users", []):
        if u["email"].lower()==email.lower():
            u["password_hash"]=_hash(new_password); changed=True
    if changed: _save_users(data); return True, "Password updated"
    return False, "User not found"
