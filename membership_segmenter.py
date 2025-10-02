
import streamlit as st
from shared.ui import page_header, stat
from shared.storage import load_json, save_json, now_iso

def run(user):
    page_header("Membership Segmenter", "Slice by age, sport, usage, region.")

    st.write("Segments (demo): Families w/ 2+ sports, Elite Athletes, Off‑peak Users")

