
import json, importlib, os, streamlit as st
from shared.auth import verify_login
from shared.ui import page_header
st.set_page_config(page_title="NXS Master OS", page_icon="🏟️", layout="wide")
@st.cache_data
def load_cfg():
    return json.load(open("config/app.json")), json.load(open("config/roles.json"))
app, roles = load_cfg()
if "user" not in st.session_state: st.session_state.user=None
def login_form():
    st.sidebar.header("Login")
    email=st.sidebar.text_input("Email","admin@nxscomplex.org")
    pw=st.sidebar.text_input("Password", type="password", value="admin123")
    if st.sidebar.button("Sign in"):
        u=verify_login(email,pw)
        if u: st.session_state.user=u; st.sidebar.success(f"Welcome, {u['name']}")
        else: st.sidebar.error("Invalid credentials")
if not st.session_state.user:
    page_header(app["app_name"], "Secure access required"); login_form(); st.stop()
user=st.session_state.user
page_header(app["app_name"], f"Role: {user['role']} • v{app['version']}")
allowed=roles.get(user["role"], [])
section=st.sidebar.selectbox("Section",[n for n in app["nav_order"] if n in allowed])
mods=app["modules"].get(section, []); names=[m.split(".")[-1] for m in mods]
choice=st.sidebar.radio("Tool", names); target=mods[names.index(choice)]
importlib.import_module(target).run(user)
