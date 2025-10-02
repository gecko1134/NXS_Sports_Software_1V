
import streamlit as st, pathlib, base64
from shared.ui import page_header
PDF = pathlib.Path("assets/docs/Double_Credits_Flyer.pdf")
def run(user):
    page_header("Double Credits – Off-Peak Promo", "1:1 credit return during off-peak with weekly caps")
    if not PDF.exists():
        st.error("Document not found.")
        return
    with open(PDF,"rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    st.markdown(f'<iframe src="data:application/pdf;base64,{b64}" width="100%" height="800"></iframe>', unsafe_allow_html=True)
