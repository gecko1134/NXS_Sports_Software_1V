
import streamlit as st
from shared.ui import page_header, stat
from shared.storage import load_json, save_json, now_iso

def run(user):
    page_header("PDF Grant Exporter", "Bundle forms and narratives to PDF.")

    st.text_input("Grant Name")
    st.file_uploader("Attach Forms", accept_multiple_files=True)
    st.button("Build PDF Packet (demo)")

