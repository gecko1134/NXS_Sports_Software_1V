
import os, json
import streamlit as st
import pandas as pd
from shared.ui import page_header
try:
    import gspread
    from google.oauth2.service_account import Credentials
    _gs_ok = True
except Exception:
    _gs_ok = False
    gspread = None
    Credentials = None
def _load_sheet(sheet_key: str, worksheet: str = None):
    raw = os.getenv("GSERVICE_ACCOUNT_JSON")
    if not raw and os.path.exists("secrets/service_account.json"):
        raw = open("secrets/service_account.json","r").read()
    if not raw:
        return None, "Add service account JSON to GSERVICE_ACCOUNT_JSON or secrets/service_account.json"
    creds = Credentials.from_service_account_info(json.loads(raw), scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"])
    client = gspread.authorize(creds)
    sh = client.open_by_key(sheet_key)
    ws = sh.worksheet(worksheet) if worksheet else sh.sheet1
    data = ws.get_all_records()
    return pd.DataFrame(data), None
def run(user):
    page_header("Finance Sync", "QuickBooks exports (CSV) or Google Sheets (optional)")
    st.subheader("CSV Import")
    f = st.file_uploader("Upload finance CSV (Revenue / Cost columns preferred)", type=["csv"])
    if f:
        df = pd.read_csv(f); st.dataframe(df.head(200)); st.metric("Rows", len(df))
    st.subheader("Google Sheets (Service Account)")
    if not _gs_ok: st.info("Install gspread + google-auth to enable Sheets import (already in requirements).")
    key = st.text_input("Sheet Key"); tab = st.text_input("Worksheet (optional)")
    if st.button("Load from Sheets") and key:
        if not _gs_ok: st.error("gspread/google-auth not installed."); return
        df, err = _load_sheet(key, tab or None)
        if err: st.error(err)
        else: st.dataframe(df.head(200)); st.metric("Rows", len(df))
