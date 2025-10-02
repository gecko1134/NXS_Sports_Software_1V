
import streamlit as st
from shared.ui import page_header, stat
from shared.storage import load_json, save_json, now_iso

def run(user):
    page_header("Mobile QR Check‑in", "Event/booking check-ins with QR.")

    st.write("Scan demo:")
    st.code("NXS-CHK-2025-10-03-ABCD")
    st.success("Scanned! Check‑in recorded (demo).")

