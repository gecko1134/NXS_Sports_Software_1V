
import streamlit as st, json, pathlib, datetime
from shared.ui import page_header
from shared.email import send_email
from shared.storage import load_json, save_json, now_iso

RULES = pathlib.Path("assets/docs/membership_upgrade_rules.json")
LOG = pathlib.Path("data/nudge_log.json")

def _load_rules():
    data = load_json(str(RULES), {})
    return data

def _log(event):
    log = load_json(str(LOG), {"events":[]})
    log["events"].append(event)
    save_json(str(LOG), log)

def run(user):
    page_header("Membership Nudges (Live)", "In-app banners + email triggers from rules")
    if not RULES.exists():
        st.error("membership_upgrade_rules.json not found in assets/docs")
        return
    rules = _load_rules()
    st.json(rules.get("meta", {}))
    triggers = rules.get("triggers", [])

    st.subheader("Simulate Member")
    email = st.text_input("Member email", "member@example.com")
    current_tier = st.selectbox("Current tier", ["Explorer","Family Plus","Athlete Elite","Annual","VIP"])
    usage_hours = st.number_input("Usage hours (last 30d)", 0, 200, 6)
    spend_30d = st.number_input("Spend in last 30d ($)", 0, 10000, 120)
    offpeak_ratio = st.slider("Off-peak usage ratio", 0.0, 1.0, 0.4, 0.05)

    st.subheader("Eligible Nudges")
    eligible = []
    for t in triggers:
        if t.get("from_tier")==current_tier:
            cond = t.get("conditions",{})
            ok = True
            if "min_usage_hours_30d" in cond and usage_hours < cond["min_usage_hours_30d"]:
                ok = False
            if "min_spend_30d" in cond and spend_30d < cond["min_spend_30d"]:
                ok = False
            if "min_offpeak_ratio" in cond and offpeak_ratio < cond["min_offpeak_ratio"]:
                ok = False
            if ok:
                eligible.append(t)

    if eligible:
        for e in eligible:
            with st.expander(f"{e.get('from_tier')} → {e.get('to_tier')}"):
                st.success(e.get("banner_text","Upgrade available!"))
                if st.button(f"Send Email: {e.get('email_subject','Upgrade Offer')}", key=e.get('to_tier')):
                    html = f"<p>{e.get('email_body','Upgrade today!')}</p>"
                    send_email([email], e.get('email_subject','Upgrade Offer'), html)
                    _log({"ts": now_iso(), "member": email, "offer": f"{e.get('from_tier')}->{e.get('to_tier')}", "channel":"email"})
                    st.toast("Email sent (dev stub).")
    else:
        st.info("No upgrade nudges match this member profile.")
