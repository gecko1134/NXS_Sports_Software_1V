
import os, json
import pandas as pd
import streamlit as st
from shared.ui import page_header
try:
    import gspread
    from google.oauth2.service_account import Credentials
except Exception:
    gspread = None
    Credentials = None

def _load_sheet(key: str, worksheet: str = None):
    if gspread is None: 
        return None, "Install gspread and google-auth to use Sheets."
    raw = os.getenv("GSERVICE_ACCOUNT_JSON")
    if not raw and os.path.exists("secrets/service_account.json"):
        raw = open("secrets/service_account.json","r").read()
    if not raw:
        return None, "Add service account JSON to GSERVICE_ACCOUNT_JSON or secrets/service_account.json"
    creds = Credentials.from_service_account_info(json.loads(raw), scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"])
    client = gspread.authorize(creds)
    sh = client.open_by_key(key)
    ws = sh.worksheet(worksheet) if worksheet else sh.sheet1
    df = pd.DataFrame(ws.get_all_records())
    return df, None

def run(user):
    page_header("Budget vs Actuals (Board View)", "Upload budget; load actuals; compare by category/month")
    st.subheader("Budget (CSV)")
        st.caption("Tip: try sample → data/sample/budget_sample.csv & data/sample/actuals_sample.csv")
    bcsv = st.file_uploader("Upload Budget CSV (columns: Category, Month, Amount)", type=["csv"], key="budget_csv")
    budget_df = None
    if bcsv:
        budget_df = pd.read_csv(bcsv)
        st.dataframe(budget_df.head(50))

    st.subheader("Actuals (CSV or Google Sheets)")
    acsv = st.file_uploader("Upload Actuals CSV (optional)", type=["csv"], key="actuals_csv")
    actuals_df = None
    if acsv:
        actuals_df = pd.read_csv(acsv)
        st.dataframe(actuals_df.head(50))
    else:
        key = st.text_input("Google Sheet Key")
        tab = st.text_input("Worksheet name (optional)")
        if st.button("Load Actuals from Sheets") and key:
            actuals_df, err = _load_sheet(key, tab or None)
            if err:
                st.error(err)
            else:
                st.dataframe(actuals_df.head(50))

    if budget_df is not None and actuals_df is not None and not budget_df.empty and not actuals_df.empty:
        st.subheader("Variance")
        # Normalize columns
        for df in (budget_df, actuals_df):
            if 'Month' in df.columns:
                df['Month'] = df['Month'].astype(str)
            if 'Category' in df.columns:
                df['Category'] = df['Category'].astype(str)
        bg = budget_df.groupby(['Category','Month'])['Amount'].sum().reset_index(name='Budget')
        ac = actuals_df.groupby(['Category','Month'])['Amount'].sum().reset_index(name='Actual')
        merged = pd.merge(bg, ac, on=['Category','Month'], how='outer').fillna(0)
        merged['Variance'] = merged['Actual'] - merged['Budget']
        st.dataframe(merged.sort_values(['Category','Month']))
        try:
            st.line_chart(merged.pivot(index='Month', columns='Category', values='Variance').fillna(0))
        except Exception:
            pass
    else:
        st.caption("Upload both budget and actuals to compute variance.")
