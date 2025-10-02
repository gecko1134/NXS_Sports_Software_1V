
import streamlit as st
from shared.ui import page_header, stat
from shared.storage import load_json, save_json, now_iso

def run(user):
    page_header("Membership Retention AI", "Find at‑risk members; trigger offers.")

    st.write("Churn risk cohort (sample): 27 members")
    st.button("Send 15% off Off‑Peak Credit Offer (demo)")

