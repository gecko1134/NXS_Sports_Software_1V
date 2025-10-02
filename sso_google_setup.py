
import streamlit as st
from shared.ui import page_header
def run(user):
    page_header("SSO (Google) — Setup Helper", "Scaffold and instructions")
    st.markdown("1) Create Google OAuth Client (Web) → 2) Add redirect URI → 3) Store creds → 4) Hook callback.\nEnv: GOOGLE_OAUTH_CLIENT_ID, GOOGLE_OAUTH_CLIENT_SECRET, GOOGLE_OAUTH_REDIRECT_URI")
