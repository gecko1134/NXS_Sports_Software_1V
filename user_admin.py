
import streamlit as st, json, os
from shared.ui import page_header
from shared.auth import add_user, remove_user, reset_password
USERS_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "config", "users.json")
def run(user):
    page_header("User Admin", "Add/remove users and reset passwords (Admin only)")
    if user.get("role") != "Admin":
        st.warning("Admins only."); return
    st.subheader("Add User")
    col1, col2 = st.columns(2)
    with col1:
        email = st.text_input("Email"); name = st.text_input("Name")
    with col2:
        role = st.selectbox("Role", ["Admin","Board","Sponsor","Team","Member","Coach"])
        pw = st.text_input("Temp Password", type="password")
    if st.button("Create User"):
        ok, msg = add_user(email, name, role, pw or "changeme123")
        (st.success if ok else st.error)(msg)
    st.subheader("Existing Users")
    try:
        data = json.load(open(USERS_FILE))
        st.table([{"email": u["email"], "name": u.get("name",""), "role": u.get("role","")} for u in data.get("users", [])])
    except Exception: st.info("No users file found")
    st.subheader("Reset Password")
    r_email = st.text_input("User Email"); r_pw = st.text_input("New Password", type="password")
    if st.button("Set Password"):
        ok, msg = reset_password(r_email, r_pw); (st.success if ok else st.error)(msg)
    st.subheader("Remove User")
    d_email = st.text_input("Email to remove")
    if st.button("Remove User"):
        ok, msg = remove_user(d_email); (st.success if ok else st.error)(msg)
