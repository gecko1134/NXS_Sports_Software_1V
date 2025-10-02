
import streamlit as st
from shared.ui import page_header, stat
from shared.storage import load_json, save_json, now_iso

def run(user):
    page_header("Incident Reports", "Log safety or facility incidents.")

    st.text_area("Describe incident")
    st.selectbox("Severity", ["Low","Medium","High"])
    st.file_uploader("Photos")
    st.button("Submit (demo)")

