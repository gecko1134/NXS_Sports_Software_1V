
import os, io, json, datetime
import streamlit as st
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from shared.ui import page_header
from shared.storage import load_json, save_json

OUTDIR = "exports"
EVENTS = "data/contracts/events.json"

def _draw_line(c, x, y, w=3*inch):
    c.line(x, y, x+w, y)

def run(user):
    page_header("Contract PDF Generator", "Creates a printable sponsorship agreement with signature blocks")
    latest = load_json("data/proposals/latest_proposal.json", {})
    sponsor = st.text_input("Sponsor", latest.get("sponsor",""))
    asset = st.text_input("Asset/Placement", latest.get("placement",""))
    term = st.number_input("Term (months)", 1, 120, 12)
    price = st.number_input("Annual Price ($)", 0, 10_000_000, int(latest.get("price_floor", 0)))
    escalator = st.slider("Annual Escalator (%)", 0, 10, 5)
    effective = st.date_input("Effective Date")
    notes = st.text_area("Special Terms", "Standard brand guidelines; creative approval; makegood for closures.")

    if st.button("Generate Contract PDF"):
        os.makedirs(OUTDIR, exist_ok=True)
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=LETTER)
        W, H = LETTER
        x, y = inch, H - inch

        c.setFont("Helvetica-Bold", 16); c.drawString(x, y, "NXS Sponsorship Agreement"); y -= 24
        c.setFont("Helvetica", 10)
        c.drawString(x, y, f"Sponsor: {sponsor}"); y -= 14
        c.drawString(x, y, f"Asset/Placement: {asset}"); y -= 14
        c.drawString(x, y, f"Term: {term} months"); y -= 14
        c.drawString(x, y, f"Annual Price: ${price:,.0f}"); y -= 14
        c.drawString(x, y, f"Escalator: {escalator}% per annum"); y -= 14
        c.drawString(x, y, f"Effective Date: {effective.isoformat()}"); y -= 24

        c.setFont("Helvetica-Bold", 12); c.drawString(x, y, "Key Terms"); y -= 14
        c.setFont("Helvetica", 10)
        for line in notes.split("\n"):
            c.drawString(x, y, line[:100]); y -= 12

        y -= 24
        c.setFont("Helvetica-Bold", 12); c.drawString(x, y, "Signature Blocks"); y -= 18
        c.setFont("Helvetica", 10)
        c.drawString(x, y, "Sponsor Authorized Signatory:"); y -= 14
        _draw_line(c, x, y); y -= 8
        c.drawString(x, y, "Name / Title:"); y -= 14
        _draw_line(c, x, y); y -= 24

        c.drawString(x, y, "NXS Authorized Signatory:"); y -= 14
        _draw_line(c, x, y); y -= 8
        c.drawString(x, y, "Name / Title:"); y -= 14
        _draw_line(c, x, y); y -= 24

        c.setFont("Helvetica-Oblique", 9)
        c.drawString(x, y, "Optional e-sign: route via DocuSign/Adobe Sign; upload executed PDF to system.")
        c.showPage(); c.save()
        buf.seek(0)
        out = f"{OUTDIR}/NXS_Contract_{sponsor.replace(' ','_')}.pdf"
        with open(out, "wb") as f: f.write(buf.read())
        st.success(f"Saved {out}")
        with open(out, "rb") as f:
            st.download_button("Download Contract PDF", f, file_name=os.path.basename(out))
