
def write_doc(text: str, out_pdf_path: str):
    try:
        from reportlab.lib.pagesizes import LETTER
        from reportlab.pdfgen import canvas
        from reportlab.lib.units import inch
        import io, os
        buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=LETTER)
        t = c.beginText(0.75*inch, 10.5*inch); t.setFont("Helvetica", 10)
        for line in text.splitlines():
            while len(line)>110: t.textLine(line[:110]); line=line[110:]
            t.textLine(line)
        c.drawText(t); c.showPage(); c.save()
        open(out_pdf_path,"wb").write(buf.getvalue()); return out_pdf_path, "pdf"
    except Exception:
        html_path = out_pdf_path.replace(".pdf",".html")
        open(html_path,"w").write("<pre>"+text+"</pre>"); return html_path, "html"
