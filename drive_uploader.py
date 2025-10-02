
import os, json, glob
import streamlit as st
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from shared.ui import page_header

def _get_drive():
    # Use service account JSON from env or secrets file
    raw = os.getenv("GOOGLE_DRIVE_SERVICE_JSON")
    if not raw and os.path.exists("secrets/drive_service.json"):
        raw = open("secrets/drive_service.json","r").read()
    if not raw:
        st.error("Missing Google Drive service JSON (GOOGLE_DRIVE_SERVICE_JSON or secrets/drive_service.json)")
        return None
    sa_path = "service_tmp.json"
    with open(sa_path,"w") as f: f.write(raw)
    gauth = GoogleAuth()
    gauth.ServiceAuth(sa_path)
    return GoogleDrive(gauth)

def run(user):
    page_header("Upload Board Packet to Google Drive", "One click upload of the latest packet to your Drive folder")
    folder_id = st.text_input("Drive Folder ID", "")
    files = sorted(glob.glob("exports/Board_Packet_*.pdf"))
    if not files:
        st.info("No board packet found. Build one in Board Packet Compiler first.")
        return
    latest = files[-1]
    st.write(f"Latest packet: **{latest}**")
    if st.button("Upload to Drive"):
        drive = _get_drive()
        if not drive or not folder_id:
            st.error("Drive not configured or Folder ID missing.")
            return
        f = drive.CreateFile({"title": os.path.basename(latest), "parents":[{"id": folder_id}]})
        f.SetContentFile(latest)
        f.Upload()
        link = f.get("alternateLink", "(uploaded)")
        st.success(f"Uploaded to Drive. Link: {link}")
