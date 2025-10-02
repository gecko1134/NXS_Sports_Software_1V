
import streamlit as st, pandas as pd, pathlib
from shared.ui import page_header

CSV = pathlib.Path("assets/docs/NXS_Sports_Lounge___Playhouse_Pro_Forma.csv")

def run(user):
    page_header("Sports Lounge & Playhouse – Pro Forma", "Revenue & cost model (CSV preview)")
    if not CSV.exists():
        st.error("CSV not found.")
        return
    try:
        df = pd.read_csv(CSV)
    except Exception:
        df = pd.read_csv(CSV, encoding="latin-1")
    st.dataframe(df.head(200))
    # Basic KPIs if columns present
    cols = {c.lower(): c for c in df.columns}
    if "revenue" in cols and "cost" in cols:
        rev = float(df[cols["revenue"]].fillna(0).sum())
        cost = float(df[cols["cost"]].fillna(0).sum())
        profit = rev - cost
        st.metric("Total Revenue", f"${rev:,.0f}")
        st.metric("Total Cost", f"${cost:,.0f}")
        st.metric("Projected Profit", f"${profit:,.0f}")
    st.caption("Load complete CSV for full analysis and charts.")
