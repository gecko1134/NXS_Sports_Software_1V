
import os, json, importlib, pkgutil, streamlit as st
st.set_page_config(page_title="SportAI — Master Dashboard", layout="wide")
BASE_PATH = os.path.dirname(__file__)
def load_users():
    try: return json.load(open(os.path.join(BASE_PATH,"auth","users.json")))
    except Exception: return []
def login():
    st.sidebar.subheader("Sign in")
    email=st.sidebar.text_input("Email"); pwd=st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Sign in"):
        for u in load_users():
            if u["email"]==email and u["password"]==pwd:
                st.session_state["user"]=u; st.success(f"Welcome, {u['role']}"); return u
        st.error("Invalid credentials"); return None
    return st.session_state.get("user")
user = login(); role = user["role"] if user else "Guest"
categories = {}
for _, modname, ispkg in pkgutil.iter_modules([os.path.join(BASE_PATH,"plugins")]):
    if not ispkg:
        mod=importlib.import_module(f"plugins.{modname}")
        if hasattr(mod,"register"): mod.register({"base_path": BASE_PATH, "role": role, "categories": categories})
st.sidebar.title("SportAI — Tools")
if not categories: st.info("No tools available. Sign in as Admin/Sponsor/Board.")
else:
    cat=st.sidebar.selectbox("Category", sorted(categories.keys()))
    tools=categories[cat]; names=[n for n,_ in tools]
    tool=st.sidebar.radio("Tool", names, index=0)
    for n, comp in tools:
        if n==tool: comp(); break
st.sidebar.markdown("---")
st.sidebar.markdown("**Forgot password?**")
reset_email = st.sidebar.text_input("Reset email")
if st.sidebar.button("Send reset token"):
    try:
        from auth.password_reset import request_reset
        token = request_reset(BASE_PATH, reset_email); st.sidebar.success("Token generated"); st.sidebar.code(token)
    except Exception as e: st.sidebar.error(str(e))
reset_token = st.sidebar.text_input("Reset token")
new_pass = st.sidebar.text_input("New password", type="password")
if st.sidebar.button("Reset now"):
    try:
        from auth.password_reset import reset_password
        ok, msg = reset_password(BASE_PATH, reset_token, new_pass)
        st.sidebar.success(msg) if ok else st.sidebar.error(msg)
    except Exception as e: st.sidebar.error(str(e))
