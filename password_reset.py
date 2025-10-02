
import os, json, time, secrets
TOKENS_FILE = "auth/reset_tokens.json"
USERS_FILE = "auth/users.json"
def _load_users(base): return json.load(open(os.path.join(base, USERS_FILE)))
def _save_users(base, data): json.dump(data, open(os.path.join(base, USERS_FILE),"w"), indent=2)
def _load_tokens(base):
    try: return json.load(open(os.path.join(base, TOKENS_FILE)))
    except Exception: return {}
def _save_tokens(base, tokens): json.dump(tokens, open(os.path.join(base, TOKENS_FILE),"w"), indent=2)
def request_reset(base, email):
    tokens = _load_tokens(base); token = secrets.token_urlsafe(24)
    tokens[token] = {"email": email, "created": time.time()}; _save_tokens(base, tokens); return token
def reset_password(base, token, new_password):
    tokens = _load_tokens(base); entry = tokens.get(token)
    if not entry: return False, "Invalid token"
    if time.time() - entry["created"] > 3600*24: return False, "Token expired"
    users = _load_users(base)
    for u in users:
        if u["email"] == entry["email"]:
            u["password"] = new_password; _save_users(base, users)
            del tokens[token]; _save_tokens(base, tokens); return True, "Password updated"
    return False, "User not found"
