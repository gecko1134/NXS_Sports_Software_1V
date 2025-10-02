
import streamlit as st, io, os, json
from shared.ui import page_header
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER
def run(user):
    page_header("Sponsor Proposal PDF Exporter","Exports latest_proposal.json → PDF")
    if not os.path.exists("data/proposals/latest_proposal.json"):
        st.info("Create a proposal in Ad Launcher first."); return
    d=json.load(open("data/proposals/latest_proposal.json"))
    if st.button("Generate PDF"):
        buf=io.BytesIO(); c=canvas.Canvas(buf, pagesize=LETTER)
        c.drawString(72,750,"NXS Sponsor Proposal")
        c.drawString(72,730,f"Sponsor: {d.get('sponsor')}")
        c.drawString(72,715,f"Placement: {d.get('placement')}")
        c.drawString(72,700,f"Price Floor: ${d.get('price_floor',0):,.0f}"); c.save(); buf.seek(0)
        os.makedirs("exports", exist_ok=True); out="exports/proposal.pdf"; open(out,"wb").write(buf.read())
        st.success("Saved exports/proposal.pdf"); st.download_button("Download Proposal PDF", open(out,"rb"), file_name="NXS_Proposal.pdf")
