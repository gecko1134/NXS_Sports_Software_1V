
import os, json, datetime
import streamlit as st
import pandas as pd
from shared.ui import page_header
from shared.storage import save_json, load_json

SRC = "data/finance_source.csv"  # optional cached source
OUTDIR = "data/snapshots"

def _calc_kpis(df: pd.DataFrame):
    lower = {c.lower(): c for c in df.columns}
    rev = df[lower.get("revenue", list(df.columns)[0])].astype(float).fillna(0).sum() if df.shape[1] else 0
    cost = df[lower.get("cost", list(df.columns)[1] if df.shape[1]>1 else 0)].astype(float).fillna(0).sum() if df.shape[1]>1 else 0
    profit = rev - cost
    return {"revenue": float(rev), "cost": float(cost), "profit": float(profit)}

def run(user):
    page_header("Finance KPI Snapshot", "Daily snapshot writer + simple scheduler")
    st.caption("Upload a finance CSV once; we will take a daily KPI snapshot when you open the app or click the button.")

    up = st.file_uploader("Upload finance CSV (Revenue/Cost columns)", type=["csv"])
    if up:
        with open(SRC, "wb") as f:
            f.write(up.read())
        st.success("Saved base finance_source.csv")

    if not os.path.exists(SRC):
        st.info("Upload a finance CSV to enable snapshots.")
        return

    df = pd.read_csv(SRC)
    kpis = _calc_kpis(df)
    st.json(kpis)

    os.makedirs(OUTDIR, exist_ok=True)
    today = datetime.date.today().isoformat()
    out = os.path.join(OUTDIR, f"{today}.json")

    if not os.path.exists(out):
        save_json(out, {"date": today, "kpis": kpis})
        st.success(f"Snapshot saved: {out}")
    else:
        st.caption("Snapshot for today already exists.")
    if st.button("Force Save Snapshot"):
        save_json(out, {"date": today, "kpis": kpis, "forced": True})
        st.success(f"Forced snapshot saved: {out}")
