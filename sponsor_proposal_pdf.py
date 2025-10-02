
import streamlit as st
from shared.ui import page_header, stat
from shared.storage import load_json, save_json, now_iso

def run(user):
    page_header("Sponsor Proposal PDF", "Export a one-pager proposal (demo).")

    st.text_input("Sponsor Name", key="sp_name")
    st.text_area("Package Summary", key="sp_pkg")
    if st.button("Export PDF (demo)"):
        st.info("PDF generator hook ready — connect to real template engine.")

