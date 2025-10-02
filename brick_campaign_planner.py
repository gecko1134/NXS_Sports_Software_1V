
import streamlit as st, pathlib
from shared.ui import page_header

DOC = pathlib.Path("assets/docs/NXS_Brick_Naming_Campaign_Guide.docx")

def run(user):
    page_header("Legacy Brick & Naming Places – Planner", "Build donor capital through visible naming")
    if DOC.exists():
        with open(DOC, "rb") as f:
            st.download_button("Download Campaign Guide (.docx)", f, file_name=DOC.name)
    st.subheader("Quick Target Calculator")
    champion = st.number_input("Champion Brick ($1,000)", 0, 1000, 100)
    team = st.number_input("Team Tile ($500)", 0, 2000, 200)
    legacy = st.number_input("Legacy Brick ($250)", 0, 5000, 500)
    youth = st.number_input("Youth Tribute ($100)", 0, 10000, 1000)
    total = champion*1000 + team*500 + legacy*250 + youth*100
    st.metric("Projected Phase 1", f"${total:,.0f}")
