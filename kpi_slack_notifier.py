
import os, json, glob
import streamlit as st
from shared.ui import page_header
from shared.notify import notify_all

def _latest(path_pattern):
    files = sorted(glob.glob(path_pattern))
    return files[-1] if files else None

def run(user):
    page_header("KPI Slack Notifier", "Post latest KPI snapshot to Slack/Teams")
    snap = _latest("data/snapshots/*.json")
    if not snap:
        st.info("No KPI snapshots found. Use Finance KPI Snapshot module first.")
        return
    data = json.load(open(snap))
    msg = f"NXS KPIs — Revenue: ${data['kpis']['revenue']:,.0f} • Cost: ${data['kpis']['cost']:,.0f} • Profit: ${data['kpis']['profit']:,.0f}"
    st.code(msg)
    if st.button("Send to Slack/Teams"):
        ok = notify_all(msg)
        st.success("Posted." if ok else "No webhook configured.")
