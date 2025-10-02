
import streamlit as st, pandas as pd, os, datetime
from shared.ui import page_header
from shared.storage import save_json
def run(user):
    page_header("Finance KPI Snapshot","Upload a finance CSV; we snapshot daily KPIs")
    up=st.file_uploader("Upload finance CSV (Revenue, Cost)", type=["csv"])
    if up:
        df=pd.read_csv(up); st.dataframe(df.head(50))
        rev=float(df.select_dtypes(include="number").iloc[:,0].sum()); cost=float(df.select_dtypes(include="number").iloc[:,1].sum())
        kpis={"revenue":rev,"cost":cost,"profit":rev-cost}; st.json(kpis)
        os.makedirs("data/snapshots", exist_ok=True)
        save_json(f"data/snapshots/{datetime.date.today().isoformat()}.json", {"date":datetime.date.today().isoformat(),"kpis":kpis})
        st.success("Snapshot saved")
