
import streamlit as st
from shared.ui import page_header, stat
from shared.storage import load_json, save_json, now_iso

def run(user):
    page_header("AI Strategy Dashboard", "Your 'What should I do next?' panel")

    st.success("Top Recommendations")
    st.markdown("- Offer off-peak credit bonus Tue–Thu 1–4pm to lift utilization by ~6%.")
    st.markdown("- Send renewal offers to sponsors with terms ending in < 90 days.")
    st.markdown("- Bundle esports lounge with family memberships to reduce churn.")

