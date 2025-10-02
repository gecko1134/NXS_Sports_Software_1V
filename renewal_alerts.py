
import pathlib, datetime, csv, os
import streamlit as st
from shared.ui import page_header
from shared.storage import load_json, save_json, now_iso
from shared.email import send_email
from shared.notify import notify_all

INV_PATH = pathlib.Path("data/sample/sponsorship_inventory.json")
OUTCSV = "exports/renewal_alerts.csv"

def _due_within(months_remaining, window):
    try:
        return 0 <= months_remaining <= window
    except Exception:
        return False

def run(user):
    page_header("Sponsor Auto-Renewal Alerts", "Email sponsors 90/60/30 days before term end")
    data = load_json(str(INV_PATH), {"items":[]})
    window = st.slider("Alert window (days)", 30, 120, 90, 30)
    today = datetime.date.today()

    due = []
    for it in data.get("items", []):
        term = int(it.get("term_months", 12) or 12)
        yrs = it.get("years_remaining")
        # Approx months remaining from years_remaining if present
        if yrs is not None:
            months_remaining = int(float(yrs) * 12)
        else:
            # Fallback: random-ish 6 months for demo
            months_remaining = 6
        days_remaining = months_remaining * 30
        if _due_within(months_remaining, window//30) and not it.get("available", True):
            sponsor = it.get("sponsor","Unknown Sponsor")
            due.append({
                "asset": it.get("name"),
                "sponsor": sponsor,
                "days_remaining": days_remaining,
                "email": f"renewals+{sponsor.replace(' ','').lower()}@nxscomplex.org"
            })

    if due:
        st.dataframe(due)
        if st.button("Send Renewal Emails"):
            for row in due:
                subj = f"Renewal: {row['asset']} — {row['days_remaining']} days"
                body = f"<p>Hi {row['sponsor']},</p><p>It’s time to renew your sponsorship asset: <b>{row['asset']}</b>.</p><p>Reply to confirm extension; standard escalator is 3–5%.</p>"
                send_email([row["email"]], subj, templates.get(tone, body), attachments=[("NXS_Proposal.pdf", proposal_bytes)] if proposal_bytes else None)
            os.makedirs("exports", exist_ok=True)
            with open(OUTCSV, "w", newline="") as f:
                w = csv.DictWriter(f, fieldnames=list(due[0].keys()))
                w.writeheader(); w.writerows(due)
            st.success(f"Emailed sponsors. Export saved to {OUTCSV}")
                notify_all("Sponsor renewal batch sent.")
    else:
        st.info("No sponsors due within window.")
