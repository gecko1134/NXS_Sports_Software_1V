
import os, json
import streamlit as st
from shared.ui import page_header

def _status(ok): return "✅" if ok else "—"

def run(user):
    page_header("System Health Monitor", "Keys, services, and data checks")
    checks = {
        "SendGrid": bool(os.getenv("SENDGRID_API_KEY")),
        "Stripe": bool(os.getenv("STRIPE_API_KEY")),
        "Google Drive": bool(os.getenv("GOOGLE_DRIVE_SERVICE_JSON")),
        "SportsKey API Base": bool(os.getenv("SPORTSKEY_API_BASE")),
        "SportsKey Token": bool(os.getenv("SPORTSKEY_API_TOKEN")),
        "Proposal Host": bool(os.getenv("PROPOSAL_HOST")),
        "Proposal Pixel Host": bool(os.getenv("PROPOSAL_PIXEL_HOST")),
        "QBO Client ID": bool(os.getenv("QBO_CLIENT_ID")),
        "Slack Webhook": bool(os.getenv("SLACK_WEBHOOK_URL")) or bool(os.getenv("TEAMS_WEBHOOK_URL")),
    }
    st.table([{"Integration": k, "Status": _status(v)} for k,v in checks.items()])
    st.caption("Green check = configured. Update environment variables or Streamlit secrets to enable missing services.")
