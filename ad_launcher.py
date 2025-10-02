
import streamlit as st
from shared.ui import page_header
from shared.storage import save_json, now_iso

def run(user):
    page_header("Ad Launcher", "Turn placements into instant sponsor proposals")
    st.subheader("Select Placement")
    placement = st.selectbox("Placement", [
        "Digital Pack (web+email+social)",
        "Venue Signage (banners/rails)",
        "Sideline/Seating Package",
        "Scoreboard Panel",
        "Court Pod Bundle (Quarter Pods x4)",
    ])
    st.subheader("Inputs for Pricing Floor")
    media = st.number_input("Media Value ($)", min_value=0, value=200000, step=5000)
    activation = st.number_input("Activation Value ($)", min_value=0, value=80000, step=5000)
    exclusivity = st.slider("Exclusivity Multiplier", 1.0, 2.5, 1.4, 0.05)
    goodwill = st.slider("Goodwill Hedge (%)", 0, 35, 15, 1)
    opp_cost = st.number_input("Opportunity Cost ($)", min_value=0, value=25000, step=5000)
    base = (media + activation) * exclusivity
    floor = base * (1 + goodwill/100.0) + opp_cost

    st.metric("Suggested Price Floor", f"${floor:,.0f}")
    sponsor_name = st.text_input("Prospect/Sponsor Name", "Acme Health")
    notes = st.text_area("Notes", "Launch Q1, 12-month term, renewal option +5% escalator")

    if st.button("Create Proposal Draft"):
        proposal = {
            "ts": now_iso(),
            "sponsor": sponsor_name,
            "placement": placement,
            "inputs": {"media": media, "activation": activation, "exclusivity": exclusivity, "goodwill_pct": goodwill, "opportunity_cost": opp_cost},
            "price_floor": floor,
            "notes": notes,
            "status": "Draft", "proposal_id": __import__("uuid").uuid4().hex
        }
        save_json("data/proposals/latest_proposal.json", proposal)
        st.success("Proposal saved to data/proposals/latest_proposal.json")
        st.json(proposal)


st.subheader("Pipeline (latest proposal status)")
from shared.storage import load_json
import os, json
latest_path = "data/proposals/latest_proposal.json"
if os.path.exists(latest_path):
    data = load_json(latest_path, {})
    pid = data.get("proposal_id")
    evlog = load_json("data/proposals/events.json", {"events":[]})
    sent = any(e.get("proposal_id")==pid and e.get("event")=="sent" for e in evlog.get("events",[]))
    viewed = any(e.get("proposal_id")==pid and e.get("event")=="viewed" for e in evlog.get("events",[]))
    st.write({"proposal_id": pid, "sent": sent, "viewed": viewed})
    st.caption("Run the webhook service and POST to /webhook/proposal/{proposal_id}/sent or embed image /t/{proposal_id}.png in your email to track opens.")


st.subheader("Save as new proposal file")
fname = st.text_input("Filename (under data/proposals/)", "proposal_demo.json")
if st.button("Save Proposal As"):
    import os, json
    os.makedirs("data/proposals", exist_ok=True)
    with open(os.path.join("data/proposals", fname), "w") as f:
        json.dump(proposal, f, indent=2)
    st.success(f"Saved data/proposals/{fname}")
