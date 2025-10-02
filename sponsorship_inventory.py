
import streamlit as st
from shared.ui import page_header, stat
from shared.storage import load_json, save_json, now_iso

def run(user):
    page_header("Sponsorship Inventory", "What’s available vs sold, pricing & terms.")

    path = "data/sample/sponsorship_inventory.json"
    inv = load_json(path, {"items":[]})
    st.dataframe(inv["items"])
    if st.button("Mark 'banner_1' as sold (demo)"):
        for it in inv["items"]:
            if it["id"]=="banner_1":
                it["available"]=False
                it["sponsor"]="Demo Sponsor"
                it["years_remaining"]=1
        save_json(path, inv)
        st.success("Updated!")

