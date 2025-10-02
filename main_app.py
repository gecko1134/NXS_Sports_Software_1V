
import json, importlib, os
import streamlit as st
from shared.auth import verify_login
from shared.ui import page_header

st.set_page_config(page_title="NXS Master OS", page_icon="🏟️", layout="wide")

@st.cache_data
def load_cfg():
    with open("config/app.json","r") as f:
        app = json.load(f)
    with open("config/roles.json","r") as f:
        roles = json.load(f)
    return app, roles

app, roles = load_cfg()

if "user" not in st.session_state:
    st.session_state.user = None

def login_form():
    st.sidebar.header("Login")
    email = st.sidebar.text_input("Email", value="admin@nxscomplex.org")
    pw = st.sidebar.text_input("Password", type="password", value="admin123")
    if st.sidebar.button("Sign in"):
        user = verify_login(email, pw)
        if user:
            st.session_state.user = user
            st.sidebar.success(f"Welcome, {user['name']}")
        else:
            st.sidebar.error("Invalid credentials")

if not st.session_state.user:
    page_header(app["app_name"], "Secure access required")
    st.info("Use demo accounts: admin/board/sponsor/member @ nxscomplex.org with password *role*123")
    login_form()
    st.stop()

user = st.session_state.user
page_header(app["app_name"], f"Role: {user['role']} • v{app['version']}")

# Role-based navigation
role_nav = roles.get(user["role"], [])
allowed_nav = [n for n in app["nav_order"] if n in role_nav]
section = st.sidebar.selectbox("Section", allowed_nav)

# Load modules for section
modules = app["modules"].get(section, [])
mod_names = [m.split(".")[-1] for m in modules]
choice = st.sidebar.radio("Tool", mod_names)

# Import and run module
target = modules[mod_names.index(choice)]
mod = importlib.import_module(target)
mod.run(user)
