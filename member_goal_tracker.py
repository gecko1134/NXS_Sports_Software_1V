
import streamlit as st
from shared.ui import page_header, stat
from shared.storage import load_json, save_json, now_iso

def run(user):
    page_header("Member Goal Tracker", "Wellness goals, streaks, rewards.")

    st.checkbox("Completed workout today?")
    st.progress(0.6)
    st.success("10‑day streak!")

