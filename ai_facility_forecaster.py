
import streamlit as st
from shared.ui import page_header, stat
from shared.storage import load_json, save_json, now_iso

def run(user):
    page_header("AI Facility Forecaster", "Forecasts usage & revenue next 90 days.")

    st.write("Demo forecast (static sample):")
    st.table([
        {"Date":"Next 7 days","Utilization":"78%","Expected Revenue":"$42,500"},
        {"Date":"Next 30 days","Utilization":"82%","Expected Revenue":"$182,000"},
        {"Date":"Next 90 days","Utilization":"85%","Expected Revenue":"$559,000"},
    ])
    st.info("Plug in your live SportsKey + Stripe to replace sample data.")

