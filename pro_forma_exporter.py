
import os, json, io, datetime
import pandas as pd
import streamlit as st
from shared.ui import page_header
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER
def _write_pdf(path, header, rows):
    buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=LETTER)
    x, y = 72, 750; c.setFont("Helvetica-Bold", 16); c.drawString(x, y, header); y -= 20; c.setFont("Helvetica", 10)
    for k, v in rows.items():
        c.drawString(x, y, f"{k}: {v}"); y -= 14
        if y < 100: c.showPage(); x, y = 72, 750; c.setFont("Helvetica", 10)
    c.showPage(); c.save(); buf.seek(0); open(path, "wb").write(buf.read())
def run(user):
    page_header("Pro-Forma Exporter", "Bank/Board summary → PDF + XLSX")
    f = st.file_uploader("Upload P&L CSV (Date, Revenue, Cost)", type=["csv"])
    if not f: st.stop()
    df = pd.read_csv(f); num = df.select_dtypes(include="number")
    revenue = float(num.iloc[:,0].sum()) if num.shape[1] >= 1 else 0.0
    cost = float(num.iloc[:,1].sum()) if num.shape[1] >= 2 else 0.0
    profit = revenue - cost
    os.makedirs("exports", exist_ok=True)
    pdf_path = "exports/Pro_Forma_Summary.pdf"; _write_pdf(pdf_path, "NXS Pro-Forma Summary", {
        "Total Revenue": f"${revenue:,.0f}","Total Cost": f"${cost:,.0f}","Profit": f"${profit:,.0f}","Generated": datetime.date.today().isoformat()
    })
    xlsx_path = "exports/Pro_Forma_Summary.xlsx"
    with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="P&L Source")
        pd.DataFrame([{"Revenue": revenue, "Cost": cost, "Profit": profit}]).to_excel(writer, index=False, sheet_name="Summary")
    st.success("Exports ready"); st.download_button("Download PDF", open(pdf_path,"rb"), file_name="Pro_Forma_Summary.pdf")
    st.download_button("Download XLSX", open(xlsx_path,"rb"), file_name="Pro_Forma_Summary.xlsx")
