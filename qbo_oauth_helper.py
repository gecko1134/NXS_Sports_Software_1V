
import os, json, urllib.parse
import streamlit as st
from shared.ui import page_header
from shared.storage import save_json, load_json

TOKENS = "data/qbo/tokens.json"

def run(user):
    page_header("QBO OAuth Helper (Minimal)", "Generates authorize URL and stores tokens after redirect")
    st.info("This is a minimal helper to guide the OAuth flow. Use with your own redirect receiver or a temporary localhost redirect tool.")
    cid = st.text_input("Client ID", os.getenv("QBO_CLIENT_ID",""))
    secret = st.text_input("Client Secret", os.getenv("QBO_CLIENT_SECRET",""), type="password")
    redirect = st.text_input("Redirect URI", os.getenv("QBO_REDIRECT_URI","http://localhost:8000/callback"))
    realm = st.text_input("Realm ID", os.getenv("QBO_REALM_ID",""))
    scope = "com.intuit.quickbooks.accounting openid profile email phone address"

    if st.button("Generate Authorize URL"):
        params = {
            "client_id": cid,
            "scope": scope,
            "redirect_uri": redirect,
            "response_type": "code",
            "state": "nxs-" + __import__("uuid").uuid4().hex
        }
        url = "https://appcenter.intuit.com/connect/oauth2?" + urllib.parse.urlencode(params)
        st.code(url, language="text")
        st.caption("Open in browser, approve, and paste the 'code' from redirect below.")

    st.subheader("Exchange Code for Tokens")
    code = st.text_input("Authorization Code")
    if st.button("Exchange Code"):
        import requests
        token_url = "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"
        auth = (cid + ":" + secret).encode("utf-8")
        b64 = __import__("base64").b64encode(auth).decode("utf-8")
        headers = {"Authorization": f"Basic {b64}", "Content-Type":"application/x-www-form-urlencoded"}
        data = {"grant_type":"authorization_code","code":code,"redirect_uri":redirect}
        r = requests.post(token_url, headers=headers, data=data, timeout=30)
        st.write("Status", r.status_code)
        st.code(r.text[:2000])
        if r.ok:
            os.makedirs("data/qbo", exist_ok=True)
            save_json(TOKENS, r.json())
            st.success("Tokens saved to data/qbo/tokens.json")

    if os.path.exists(TOKENS):
        st.subheader("Tokens on file")
        st.json(load_json(TOKENS, {}))
        st.caption("Use access_token with QBO reports endpoints; refresh_token to renew when expired.")
