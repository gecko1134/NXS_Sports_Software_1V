
import streamlit as st, json, pathlib
from shared.ui import page_header

RULES = pathlib.Path("assets/docs/membership_upgrade_rules.json")

def run(user):
    page_header("Membership Upgrade Rules", "AB tests, triggers, rewards")
    if not RULES.exists():
        st.error("Rules file not found.")
        return
    data = json.loads(RULES.read_text())
    st.json(data["meta"])
    st.subheader("Settings")
    st.json(data["settings"])
    st.subheader("Triggers")
    for t in data.get("triggers", []):
        with st.expander(f"{t.get('from_tier')} → {t.get('to_tier')}"):
            st.json(t)
