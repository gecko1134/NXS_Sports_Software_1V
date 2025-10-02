
import os, glob
import streamlit as st
from shared.ui import page_header
from PyPDF2 import PdfMerger
def run(user):
    page_header("Board Packet Compiler", "Select PDFs and merge into a single packet")
    st.caption("Sources: assets/docs/*.pdf and exports/*.pdf")
    docs = sorted(glob.glob("assets/docs/*.pdf") + glob.glob("exports/*.pdf"))
    if not docs: st.info("No PDFs found. Put files under assets/docs/ or create exports first."); return
    picks = st.multiselect("Choose PDFs to merge", docs, default=docs[:4])
    if st.button("Build Packet") and picks:
        os.makedirs("exports", exist_ok=True); out = f"exports/Board_Packet_Merged.pdf"
        merger = PdfMerger()
        for p in picks:
            try: merger.append(p)
            except Exception as e: st.warning(f"Skipped {p}: {e}")
        merger.write(out); merger.close()
        st.success(f"Saved {out}"); st.download_button("Download Board Packet", open(out,"rb"), file_name="Board_Packet.pdf")
