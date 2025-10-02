
import os, datetime, pathlib
import streamlit as st
from PyPDF2 import PdfMerger
from shared.ui import page_header

DOCS = pathlib.Path("assets/docs")

def run(user):
    page_header("Board Packet Compiler", "Select PDFs to merge and export a monthly packet")
    # Collect PDFs in assets/docs
    pdfs = [p for p in DOCS.glob("*.pdf")]
    if not pdfs:
        st.info("No PDFs found in assets/docs")
        return
    choices = st.multiselect("Choose documents", pdfs, default=pdfs[:4], format_func=lambda p: p.name)
    if st.button("Build Packet") and choices:
        os.makedirs("exports", exist_ok=True)
        out = f"exports/Board_Packet_{datetime.date.today().strftime('%Y_%m')}.pdf"
        merger = PdfMerger()
        for p in choices:
            try:
                merger.append(str(p))
            except Exception as e:
                st.warning(f"Could not append {p.name}: {e}")
        merger.write(out); merger.close()
        st.success(f"Saved {out}")
        with open(out, "rb") as f:
            st.download_button("Download Board Packet", f, file_name=os.path.basename(out))
