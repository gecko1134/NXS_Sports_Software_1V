
    import os, pathlib
    import streamlit as st
    from shared.ui import page_header

    CFG = pathlib.Path(".streamlit/config.toml")

    def _write_theme(mode: str):
        dark = [theme]
base="dark"
primaryColor="#22c55e"
backgroundColor="#0b1220"
secondaryBackgroundColor="#0f172a"
textColor="#e2e8f0"
[server]
headless=true
[client]
toolbarMode="auto"

        light = [theme]
base="light"
primaryColor="#0ea5e9"
backgroundColor="#ffffff"
secondaryBackgroundColor="#f8fafc"
textColor="#0f172a"
[server]
headless=true
[client]
toolbarMode="auto"

        CFG.parent.mkdir(parents=True, exist_ok=True)
        CFG.write_text(dark if mode=="Dark" else light)

    def run(user):
        page_header("Theme Switcher", "Toggle between dark and light themes")
        mode = st.radio("Theme", ["Dark","Light"])
        if st.button("Apply"):
            _write_theme(mode)
            st.success("Theme updated. Restart app to see changes.")
