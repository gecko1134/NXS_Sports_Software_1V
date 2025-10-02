
import streamlit as st, pathlib
from shared.ui import page_header

DOC1 = pathlib.Path("assets/docs/Nexus_Domes_Usage_and_Membership_Plan2.docx")
DOC2 = pathlib.Path("assets/docs/Facility_Usage_Model_Membership_Tiers_Exclusive_Club.docx")

def run(user):
    page_header("Usage & Membership Plans", "Capacity, prime windows, and Exclusive Club tiers")
    for doc in [DOC1, DOC2]:
        if doc.exists():
            with open(doc, "rb") as f:
                st.download_button(f"Download {doc.name}", f, file_name=doc.name, key=doc.name)
    st.info("These documents define prime vs non-prime windows, target member mix, and the Exclusive Club tiering.")
