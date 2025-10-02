
import streamlit as st
from shared.ui import page_header, stat
from shared.storage import load_json, save_json, now_iso

def run(user):
    page_header("Grant Match AI", "Find grants & draft boilerplates.")

    st.write("Matches (sample):")
    st.table([
        {"Program":"MN Angel Tax Credit","Status":"Eligible","Next Step":"Prep app package"},
        {"Program":"IRRRB","Status":"Lead Identified","Next Step":"Draft pre-app"},
    ])
    st.button("Generate Draft Narrative (demo)")

