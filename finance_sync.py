
import os, json, io
import streamlit as st
import pandas as pd
from shared.ui import page_header

def _load_sheet_via_service_account(sheet_key: str, worksheet: str = None):
    try:
        import gspread
        from google.oauth2.service_account import Credentials
    except Exception as e:
        st.warning("Install gspread and google-auth to use Sheets sync.")
        return None
    raw = os.getenv("GSERVICE_ACCOUNT_JSON")
    if not raw and os.path.exists("secrets/service_account.json"):
        raw = open("secrets/service_account.json","r").read()
    if not raw:
        st.info("Add Google service account JSON to GSERVICE_ACCOUNT_JSON env var or secrets/service_account.json")
        return None
    creds = Credentials.from_service_account_info(json.loads(raw), scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"])
    client = gspread.authorize(creds)
    sh = client.open_by_key(sheet_key)
    ws = sh.worksheet(worksheet) if worksheet else sh.sheet1
    data = ws.get_all_records()
    return pd.DataFrame(data)

def run(user):
    page_header("Finance Sync", "QuickBooks CSV or Google Sheets → dashboard")
    st.subheader("CSV Import")
    f = st.file_uploader("Upload QuickBooks/Export CSV", type=["csv"])
    if f:
        df = pd.read_csv(f)
        st.dataframe(df.head(200))
        st.metric("Rows", len(df))
    st.subheader("Google Sheets (Service Account)")
    key = st.text_input("Sheet Key (from URL)", "")
    tab = st.text_input("Worksheet name (leave blank for first)", "")
    if st.button("Load Sheet") and key:
        df = _load_sheet_via_service_account(key, tab or None)
        if df is not None:
            st.dataframe(df.head(200))
            st.metric("Rows", len(df))
