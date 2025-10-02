
import streamlit as st, os
from shared.ui import page_header
def run(user):
    page_header("Deal Desk","Review & generate quick contract text")
    sponsor=st.text_input("Sponsor","Acme Health")
    asset=st.text_input("Asset","Court A Center Logo")
    price=st.number_input("Annual Price ($)",0,10000000,250000)
    term=st.number_input("Term (months)",1,120,12)
    if st.button("Generate Contract"):
        txt=f"NXS Sponsorship Agreement\nSponsor: {sponsor}\nAsset: {asset}\nTerm: {term} months\nAnnual Price: ${price:,.0f}"
        os.makedirs("exports", exist_ok=True); open("exports/contract.txt","w").write(txt)
        st.success("Saved exports/contract.txt"); st.code(txt, language="text")
