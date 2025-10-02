
import os
import streamlit as st
from shared.ui import page_header
from shared.email import send_email

def run(user):
    page_header("Email Proposal to Prospect", "Attaches latest exported proposal PDF via SendGrid")
    pdf_path = "exports/proposal.pdf"
    if not os.path.exists(pdf_path):
        st.error("No proposal PDF found. Generate one in Sponsor Proposal PDF Exporter first.")
        return
    to = st.text_input("Prospect email", "deals@example.com")
    subj = st.text_input("Email subject", "NXS Proposal — Next Steps")
    import os
        default_html = "<p>Hi — attached is your proposal. Happy to review terms anytime.</p>"
        if os.path.exists("data/proposals/email_draft.html"):
            default_html = open("data/proposals/email_draft.html").read()
        body = st.text_area("Email body (HTML allowed)", default_html)

st.subheader("Landing Page & Tracking")
# Build landing URL using latest proposal_id; assumes FastAPI service at port 8081 locally
import json, os
latest = "data/proposals/latest_proposal.json"
landing = ""
pixel = ""
if os.path.exists(latest):
    data = json.load(open(latest))
    pid = data.get("proposal_id","")
    # Use env PROPOSAL_HOST to override (e.g., https://proposals.nxscomplex.org)
    host = os.getenv("PROPOSAL_HOST","http://localhost:8081")
    landing = f"{host}/p/{pid}"
    # Tracking pixel is served by events service on 8080 unless overridden by PROPOSAL_PIXEL_HOST
    pixel_host = os.getenv("PROPOSAL_PIXEL_HOST","http://localhost:8080")
    pixel = f'<img src="{pixel_host}/t/{pid}.png" width="1" height="1" style="display:none"/>'
    st.code(landing, language="text")
else:
    st.info("No latest_proposal.json found. Create one in Ad Launcher.")

insert_cta = st.checkbox("Insert CTA link to landing page", value=True)
insert_pixel = st.checkbox("Insert tracking pixel", value=True)

html_body = body
if landing and insert_cta:
    html_body += f'<p><a href="{landing}">View proposal & next steps</a></p>'
if pixel and insert_pixel:
    html_body += pixel
st.markdown("**Preview (HTML)**")
st.code(html_body, language="html")

    if st.button("Send Email"):
        with open(pdf_path, "rb") as f:
            ok = send_email([to], subj, html_body, attachments=[("NXS_Proposal.pdf", f.read())])
        if ok:
            st.success(f"Sent to {to}")
        else:
            st.warning("Send failed (check SENDGRID settings)")
