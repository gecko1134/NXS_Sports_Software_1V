
import streamlit as st, json, os
from shared.ui import page_header, section_intro
from shared.storage import save_json, now_iso
def run(user):
    page_header("Ad Launcher","Create a sponsor proposal draft")
    section_intro("Pick placement and inputs; we’ll price via a floor formula and save a JSON draft.")
    placement=st.selectbox("Placement",["Digital Pack","Venue Signage","Sideline/Seating","Scoreboard","Court Pod Bundle"])
    media=st.number_input("Media Value ($)",0,10000000,200000,5000)
    activation=st.number_input("Activation Value ($)",0,10000000,80000,5000)
    exclus=st.slider("Exclusivity",1.0,2.5,1.4,0.05)
    goodwill=st.slider("Goodwill (%)",0,35,15,1)
    opp=st.number_input("Opportunity Cost ($)",0,1000000,25000,5000)
    sponsor=st.text_input("Sponsor","Acme Health")
    notes=st.text_area("Notes","12-month term; 5% escalator")
    floor=(media+activation)*exclus*(1+goodwill/100)+opp
    st.metric("Suggested Floor", f"${floor:,.0f}")
    if st.button("Save Draft"):
        proposal={"ts":now_iso(),"sponsor":sponsor,"placement":placement,"inputs":{"media":media,"activation":activation,"exclusivity":exclus,"goodwill_pct":goodwill,"opportunity_cost":opp},"price_floor":floor,"status":"Draft"}
        save_json("data/proposals/latest_proposal.json", proposal)
        st.success("Saved data/proposals/latest_proposal.json"); st.json(proposal)
