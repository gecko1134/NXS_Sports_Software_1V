
import streamlit as st, json
from shared.ui import page_header
from shared.storage import load_json
def run(user):
    page_header("AI Scheduler Optimizer","Preview bookings and export holds (demo)")
    st.json(load_json("data/sample/bookings.json", {"bookings":[{"resource":"Court A","start":"2025-10-03T17:00:00","end":"2025-10-03T18:00:00"}]}))
    if st.button("Export suggested holds (CSV)"):
        import csv, os; os.makedirs("exports", exist_ok=True)
        with open("exports/suggested_holds.csv","w",newline="") as f: 
            import csv; w=csv.writer(f); w.writerow(["resource","start","end"]); w.writerow(["Court A","2025-10-04 13:00","2025-10-04 14:00"])
        st.success("Saved exports/suggested_holds.csv")
