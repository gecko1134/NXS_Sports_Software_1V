
import streamlit as st
from shared.ui import page_header, stat
from shared.storage import load_json, save_json, now_iso

def run(user):
    page_header("Board Financial Summary", "One-click board packet exports.")

    st.write("KPIs:")
    col1,col2,col3 = st.columns(3)
    col1.metric("MRR","$128,400","+4.1%")
    col2.metric("Bookings (30d)","1,284","+3.6%")
    col3.metric("Avg Utilization","81%","+2%")
    st.button("Export Board PDF (demo)")

