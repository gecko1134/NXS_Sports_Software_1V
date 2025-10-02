
import os, base64, json, requests
import streamlit as st
from shared.ui import page_header
from shared.storage import load_json
from shared.email import send_email

def _load_pdf(path):
    if not os.path.exists(path):
        return None
    return base64.b64encode(open(path,"rb").read()).decode("utf-8")

def _post(url, headers, payload):
    r = requests.post(url, headers=headers, data=json.dumps(payload), timeout=30)
    return r.status_code, r.text[:2000]

def run(user):
    page_header("E‑Sign Envelope Creator", "Send Contract PDF to DocuSign or Adobe Sign")

    pdf = st.text_input("Contract PDF path", "exports/NXS_Contract_Acme_Health.pdf")
    sponsor_email = st.text_input("Sponsor signer email", "signer@example.com")
    sponsor_name = st.text_input("Sponsor signer name", "Jane Doe")

    st.subheader("DocuSign (JWT/Token)")
    ds_base = st.text_input("DocuSign API Base", os.getenv("DS_BASE","https://demo.docusign.net/restapi"))
    ds_account = st.text_input("DocuSign Account ID", os.getenv("DS_ACCOUNT_ID",""))
    ds_token = st.text_input("DocuSign Access Token", os.getenv("DS_ACCESS_TOKEN",""), type="password")

    if st.button("Send via DocuSign"):
        content = _load_pdf(pdf)
        if not content: st.error("PDF not found"); return
        url = f"{ds_base}/v2.1/accounts/{ds_account}/envelopes"
        headers = {"Authorization": f"Bearer {ds_token}", "Content-Type":"application/json"}
        payload = {
            "emailSubject":"NXS Sponsorship Agreement",
            "documents":[{"documentBase64": content, "documentId":"1","fileExtension":"pdf","name":"NXS Contract"}],
            "recipients":{"signers": ( [{"email": nxs_email, "name": nxs_name, "recipientId":"1","routingOrder":"1"},  {"email": sponsor_email, "name": sponsor_name, "recipientId":"2","routingOrder":"2"}]  if enable_gate else  [{"email": sponsor_email, "name": sponsor_name, "recipientId":"1","routingOrder":"1"}] )},
            "status":"sent"
        }
        code, text = _post(url, headers, payload)
        st.write("Status", code); st.code(text)

    st.subheader("Adobe Sign (OAuth Token)")
    as_base = st.text_input("Adobe Sign API Base", os.getenv("AS_BASE","https://api.na4.adobesign.com/api/rest/v6"))
    as_token = st.text_input("Adobe Access Token", os.getenv("AS_ACCESS_TOKEN",""), type="password")
    if st.button("Send via Adobe Sign"):
        content = _load_pdf(pdf)
        if not content: st.error("PDF not found"); return
        headers = {"Authorization": f"Bearer {as_token}", "Content-Type":"application/json"}
        # 1) Create transient document
        import requests as rq
        td = rq.post(f"{as_base}/transientDocuments",
                     headers={"Authorization": f"Bearer {as_token}"},
                     files={"File": ("contract.pdf", base64.b64decode(content), "application/pdf")})
        if not td.ok:
            st.error(f"Transient upload failed: {td.text[:500]}"); return
        doc_id = td.json().get("transientDocumentId")
        payload = {
            "fileInfos":[{"transientDocumentId": doc_id}],
            "name":"NXS Sponsorship Agreement",
            "participantSetsInfo": ( [{"memberInfos":[{"email": nxs_email}], "order":1, "role":"SIGNER"},  {"memberInfos":[{"email": sponsor_email}], "order":2, "role":"SIGNER"}] if enable_gate else  [{"memberInfos":[{"email": sponsor_email}], "order":1, "role":"SIGNER"}]),
            "signatureType":"ESIGN","state":"IN_PROCESS"
        }
        code, text = _post(f"{as_base}/agreements", headers, payload)
        st.write("Status", code); st.code(text)
