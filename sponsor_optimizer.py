
import streamlit as st
from shared.ui import page_header, stat
from shared.storage import load_json, save_json, now_iso

def run(user):
    page_header("Sponsor Optimizer AI", "Auto-build packages & check inventory conflicts.")

    inv = load_json("data/sample/sponsorship_inventory.json", {"items":[]})
    st.write("Inventory (sample):")
    st.dataframe(inv["items"])
    st.write("Suggested Package:")
    st.json({
        "items":["Main Dome Banner North","Court A Center Logo"],
        "term_months":12,
        "price_total": 15000 + 25000,
        "impressions_est":"3.2M/yr"
    })

