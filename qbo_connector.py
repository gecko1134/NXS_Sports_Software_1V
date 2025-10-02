
import os, json, datetime
import streamlit as st
import pandas as pd
from shared.ui import page_header

def run(user):
    page_header("QuickBooks Online (QBO) Connector", "OAuth setup, CSV fallback, and trendlines")

    st.subheader("Option A — CSV Fallback (fastest)")
    csv_up = st.file_uploader("Upload QBO P&L export CSV", type=["csv"])
    if csv_up:
        df = pd.read_csv(csv_up)
        st.dataframe(df.head(200))
        num_cols = df.select_dtypes(include="number").columns.tolist()
        if len(num_cols) >= 1:
            st.line_chart(df[num_cols[0]])
        if len(num_cols) >= 2:
            st.area_chart(df[num_cols[:2]])

    st.subheader("Option B — Live OAuth (guide)")
    st.markdown("""
    1. Create an app in **Intuit Developer**.
    2. Add Redirect URI: `https://your-deployment.example.com/oauth/callback`.
    3. Store secrets in `st.secrets` or environment:
       - `QBO_CLIENT_ID`, `QBO_CLIENT_SECRET`, `QBO_REDIRECT_URI`, `QBO_REALM_ID`.
    4. Use an OAuth helper (e.g., `python-quickbooks` or direct REST) to obtain tokens and call:
       - `/v3/company/{realmId}/reports/ProfitAndLoss`
       - `/v3/company/{realmId}/reports/CashFlow`
    5. Save JSON into `data/qbo/` and visualize here.
    """)
    st.info("This module ships with the CSV path ready now; live OAuth can be added by inserting your client credentials and wiring the REST calls.")
