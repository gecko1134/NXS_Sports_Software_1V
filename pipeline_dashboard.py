
import os, json, pandas as pd
import streamlit as st
from shared.ui import page_header, icon_header, section_intro
from shared.storage import load_json

def run(user):
        section_intro("""See proposal funnel, reasons, and channel conversion at a glance.""")
    icon_header('📊', "Sales Pipeline Dashboard", "Sent → Viewed → Interested → Won")

    latest = load_json("data/proposals/latest_proposal.json", {})
        
# Multi‑proposal selector
import glob, os, json
prop_files = sorted(glob.glob("data/proposals/*.json"))
candidates = [p for p in prop_files if p.endswith(".json") and os.path.basename(p) not in ("events.json","interests.json","reasons.json")]
label_map = {}
for p in candidates:
    try:
        d = json.load(open(p))
        label_map[p] = f"{os.path.basename(p)} — {d.get('sponsor','?')} | {d.get('placement','?')}"
    except Exception:
        label_map[p] = os.path.basename(p)
if candidates:
    sel = st.selectbox("Select proposal", candidates, format_func=lambda p: label_map.get(p,p))
    latest = json.load(open(sel))
else:
    st.warning("No proposal JSON files found. Create one in Ad Launcher.")

    events = load_json("data/proposals/events.json", {"events":[]})
    interests = load_json("data/proposals/interests.json", {"submissions":[]})
    ev = events.get("events", [])
    subs = interests.get("submissions", [])

    # Aggregate status for latest proposal_id
    pid = latest.get("proposal_id")
    sent = sum(1 for e in ev if e.get("proposal_id")==pid and e.get("event")=="sent")
    viewed = sum(1 for e in ev if e.get("proposal_id")==pid and e.get("event")=="viewed")
    interested = sum(1 for s in subs if s.get("proposal_id")==pid)

    st.subheader("Funnel (current proposal)")
    stages = pd.DataFrame({
        "stage":["Sent","Viewed","Interested"],
        "count":[sent, viewed, interested]
    })
    st.bar_chart(stages.set_index("stage"))

    st.subheader("Events Log")
    if ev:
        st.dataframe(pd.DataFrame(ev))
    else:
        st.caption("No events yet. Run the webhook service and email proposals with the tracking pixel.")

    st.subheader("Interest Submissions")
    if subs:
        st.dataframe(pd.DataFrame(subs))
    else:
        st.caption("No interest submissions yet. Landing page form submissions will appear here.")

    st.subheader("Mark Won")
    won = st.checkbox("Mark latest proposal as WON", value=False)
    if won:
        latest["status"] = "Won"
        os.makedirs("data/proposals", exist_ok=True)
        json.dump(latest, open("data/proposals/latest_proposal.json","w"), indent=2)
        st.success("Marked as WON.")


st.subheader("Won/Lost Reasons")
reasons_path = "data/proposals/reasons.json"
reasons = load_json(reasons_path, {"decisions":[]})
outcome = st.selectbox("Set outcome", ["—","Won","Lost"], index=0)
reason = st.text_input("Reason (e.g., Budget, Timing, Competition, Scope)")
channel = st.selectbox("Channel", ["Email","Call","In-Person","Event","Referral","Website","Other"], index=0)
if st.button("Save Decision") and pid and outcome in ["Won","Lost"]:
    reasons["decisions"].append({
        "proposal_id": pid,
        "outcome": outcome,
        "reason": reason or "(unspecified)",
        "channel": channel or "(unspecified)",
        "ts": __import__("datetime").datetime.utcnow().isoformat()+"Z"
    })
    import json, os
    os.makedirs("data/proposals", exist_ok=True)
    json.dump(reasons, open(reasons_path,"w"), indent=2)
    st.success("Decision saved.")

st.subheader("Conversion by Channel")
# Build channel-level conversion from events + interests + decisions
rows = []
# derive channel from decisions; fall back to 'Email' when not set
by_channel = {}
for d in reasons.get("decisions", []):
    ch = d.get("channel","Other")
    by_channel.setdefault(ch, {"won":0,"lost":0,"total":0})
    by_channel[ch]["total"] += 1
    if d.get("outcome")=="Won":
        by_channel[ch]["won"] += 1
    elif d.get("outcome")=="Lost":
        by_channel[ch]["lost"] += 1
for ch, agg in by_channel.items():
    conv = (agg["won"]/agg["total"]*100) if agg["total"] else 0.0
    rows.append({"channel": ch, "won": agg["won"], "lost": agg["lost"], "total": agg["total"], "conversion_%": round(conv,1)})
import pandas as pd
if rows:
    dfc = pd.DataFrame(rows).sort_values("conversion_%", ascending=False)
    st.dataframe(dfc, hide_index=True)
    st.bar_chart(dfc.set_index("channel")["conversion_%"])
else:
    st.caption("No decisions saved yet — conversion by channel populates after you mark proposals Won/Lost.")
