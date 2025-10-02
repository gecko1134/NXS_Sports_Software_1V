
import os, zipfile, datetime
import streamlit as st
from shared.ui import page_header

def run(user):
    page_header("Data Export / Backup", "Create a ZIP of key data folders for safekeeping")
    st.caption("Includes: data/, exports/, config/")
    if st.button("Create Backup ZIP"):
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        out = f"exports/NXS_Backup_{ts}.zip"
        os.makedirs("exports", exist_ok=True)
        with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
            for folder in ["data","exports","config"]:
                for root, _, files in os.walk(folder):
                    for f in files:
                        full = os.path.join(root, f)
                        z.write(full, full)
        st.success(f"Backup created: {out}")
        with open(out, "rb") as f:
            st.download_button("Download Backup", f, file_name=os.path.basename(out))
