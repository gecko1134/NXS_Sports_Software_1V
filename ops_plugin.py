
import os, streamlit as st
from shared.sportskey_client import SportsKeyClient
CATEGORY="Ops Tools"
def register(app_state: dict):
    role=app_state.get("role","Guest")
    cats=app_state.setdefault("categories", {})
    if role in ["Admin","Board","Sponsor"]:
        cats.setdefault(CATEGORY, []).append(("SportsKey Availability", ui))
def ui():
    st.subheader("SportsKey Availability (Live)")
    rid=st.text_input("Resource ID", "TURF_A")
    date_from=st.text_input("Date From (YYYY-MM-DD)", "2025-10-01")
    date_to=st.text_input("Date To (YYYY-MM-DD)", "2025-10-07")
    if st.button("Fetch Availability"):
        try:
            client = SportsKeyClient(); data = client.get_availability(rid, date_from, date_to); st.json(data)
        except Exception as e: st.error(str(e))
