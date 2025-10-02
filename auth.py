
import json, hashlib, os
USERS = {"users":[
    {"email":"admin@nxscomplex.org","name":"Admin","role":"Admin","password_hash":hashlib.sha256("admin123".encode()).hexdigest()},
    {"email":"board@nxscomplex.org","name":"Board","role":"Board","password_hash":hashlib.sha256("board123".encode()).hexdigest()},
    {"email":"sponsor@nxscomplex.org","name":"Sponsor","role":"Sponsor","password_hash":hashlib.sha256("sponsor123".encode()).hexdigest()},
]}
def verify_login(email, password):
    h = hashlib.sha256(password.encode()).hexdigest()
    for u in USERS["users"]:
        if u["email"].lower()==email.lower() and u["password_hash"]==h:
            return {"email":u["email"],"name":u["name"],"role":u["role"]}
    return None
