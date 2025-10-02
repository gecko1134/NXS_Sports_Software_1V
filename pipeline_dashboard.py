
import streamlit as st, json, glob, os, pandas as pd
from shared.ui import page_header
from shared.storage import load_json
def run(user):
    page_header("Pipeline Dashboard","Sent → Viewed → Interested")
    latest=load_json("data/proposals/latest_proposal.json",{})
    st.json(latest or {"status":"No proposal"})
    # placeholder tables
    st.subheader("Events"); st.table(pd.DataFrame([{"proposal_id": latest.get("proposal_id","demo"), "event":"sent"}]))
    st.subheader("Interests"); st.table(pd.DataFrame([{"proposal_id": latest.get("proposal_id","demo"), "name":"Demo"}]))
