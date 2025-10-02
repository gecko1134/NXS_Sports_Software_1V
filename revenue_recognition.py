
import streamlit as st, json
from shared.ui import page_header
from shared.storage import load_json
def run(user):
    page_header("Revenue Recognition","Booked → Billed → Collected (demo)")
    latest=load_json("data/proposals/latest_proposal.json",{})
    booked=float(latest.get("price_floor",0.0) or 0.0)
    st.metric("Booked", f"${booked:,.0f}")
    st.metric("Billed", "$0")
    st.metric("Collected", "$0")
