
import streamlit as st, pathlib
from shared.ui import page_header

DOC = pathlib.Path("assets/docs/NXS_Player_Lab_Strategy_Guide.docx")

def run(user):
    page_header("Player Lab Strategy Guide", "Elite training zone: tiers & funding")
    if DOC.exists():
        with open(DOC, "rb") as f:
            st.download_button("Download Strategy Guide (.docx)", f, file_name=DOC.name)
    st.markdown("- Sponsors: $250k (10-year naming), Operators: $100k bays, Co-Owners: $25k equipment shares, Donors: $10k recognition.")
    st.caption("Full guide in the download.")
