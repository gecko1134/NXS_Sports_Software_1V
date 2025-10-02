
import streamlit as st
from shared.ui import page_header, stat
from shared.storage import load_json, save_json, now_iso

def run(user):
    page_header("AI Risk Alerts", "Flags legal/financial/ops issues early.")

    st.error("Revenue slip of 7% vs. plan in last 14 days.")
    st.info("Grant deadline: IRRRB Pre-App due Nov 15, 2025.")
    st.warning("Open incidents this week: 2. Add notes and assign owners in Ops.")

