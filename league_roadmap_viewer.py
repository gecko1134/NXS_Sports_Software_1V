
import streamlit as st, pathlib, base64
from shared.ui import page_header
PDF = pathlib.Path("assets/docs/NXS_League_Roadmap_Timeline.pdf")
def run(user):
    page_header("League Roadmap Timeline", "NXS 5-Year Women’s Sports plan")
    if not PDF.exists():
        st.error("Document not found.")
        return
    st.caption("Embedded preview below; use the download in the Document Library for printing.")
    with open(PDF,"rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    st.markdown(f'<iframe src="data:application/pdf;base64,{b64}" width="100%" height="800"></iframe>', unsafe_allow_html=True)
