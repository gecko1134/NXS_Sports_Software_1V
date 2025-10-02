
import streamlit as st, os, zipfile, datetime
from shared.ui import page_header
def run(user):
    page_header("Data Export / Backup","Zip data/, exports/, config/")
    if st.button("Create Backup ZIP"):
        ts=datetime.datetime.now().strftime("%Y%m%d_%H%M%S"); out=f"exports/NXS_Backup_{ts}.zip"
        os.makedirs("exports", exist_ok=True)
        with zipfile.ZipFile(out,"w",zipfile.ZIP_DEFLATED) as z:
            for folder in ["data","exports","config"]:
                for root,_,files in os.walk(folder):
                    for f in files: z.write(os.path.join(root,f), os.path.join(root,f))
        st.success(f"Backup created: {out}"); st.download_button("Download Backup", open(out,"rb"), file_name=os.path.basename(out))
