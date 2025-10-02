
import streamlit as st
from shared.ui import page_header
from shared.auth import reset_password
def run(user):
    page_header("Change Password", "Update your own password")
    st.info(f"Signed in as: {user.get('email')}")
    pw1 = st.text_input("New Password", type="password")
    pw2 = st.text_input("Confirm New Password", type="password")
    if st.button("Change Password"):
        if not pw1 or pw1 != pw2: st.error("Passwords do not match."); return
        ok, msg = reset_password(user.get("email"), pw1); (st.success if ok else st.error)(msg)
