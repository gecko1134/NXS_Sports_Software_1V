
import os, glob, json
import streamlit as st
from shared.ui import page_header, icon_header, section_intro

def run(user):
    icon_header("🧭", "Board Walkthrough Mode", "Guided tour with preloaded demo data")
    section_intro("This demo loads proposals, pipeline activity, invoices, and a board packet so you can click through all the highlights without setup.")

    st.subheader("Quick Links")
    st.markdown("- Marketing → **Pipeline Dashboard** — select any of the demo proposals")
    st.markdown("- Sponsorship Tools → **Deal Desk** — review latest proposal & inventory")
    st.markdown("- Sponsorship Tools → **Sponsor Proposal PDF Exporter** — try export (email draft auto-builds)")
    st.markdown("- Governance & Compliance → **Board Packet Compiler** — packet already generated (exports/)")
    st.markdown("- Finance Tools → **Revenue Recognition** — see booked → billed → collected")
    st.markdown("- Finance Tools → **Receivables Dashboard** — dunning emails from open invoices (if Stripe key set)")
    st.markdown("- Finance Tools → **Budget vs Actuals** — load the sample CSVs in data/sample/")

    st.subheader("Demo Proposals Found")
    props = sorted(glob.glob("data/proposals/proposal_*.json"))
    for p in props:
        d = json.load(open(p))
        st.write(f"• {os.path.basename(p)} — {d.get('sponsor')} | {d.get('placement')} | status: {d.get('status')}")

    st.info("Tip: Use dark mode + new headers for a clean presentation. All demo data is local and safe to modify.")
