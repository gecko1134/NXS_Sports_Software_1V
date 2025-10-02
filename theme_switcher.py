
import streamlit as st, pathlib
from shared.ui import page_header
CFG=pathlib.Path(".streamlit/config.toml")
def run(user):
    page_header("Theme Switcher","Toggle between dark and light")
    mode=st.radio("Theme",["Dark","Light"])
    if st.button("Apply"):
        CFG.parent.mkdir(parents=True, exist_ok=True)
        if mode=="Dark":
            CFG.write_text("[theme]\nbase='dark'\nprimaryColor='#22c55e'")
        else:
            CFG.write_text("[theme]\nbase='light'\nprimaryColor='#0ea5e9'")
        st.success("Theme updated. Restart app to apply.")
