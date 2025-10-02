
import os, pathlib
import streamlit as st
from shared.ui import page_header
DOCS = pathlib.Path("assets/docs")
def run(user):
    page_header("Document Library", "Browse and download key PDFs/CSVs/XLSX")
    if not DOCS.exists():
        st.info("assets/docs not found"); return
    files = sorted([p for p in DOCS.iterdir() if p.is_file()])
    if not files:
        st.info("No documents in assets/docs yet."); return
    for p in files:
        with st.expander(p.name, expanded=False):
            with open(p, "rb") as f:
                st.download_button("Download", f, file_name=p.name, key=str(p))
