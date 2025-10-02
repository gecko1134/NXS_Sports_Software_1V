
import streamlit as st, json
def run(base_path:str="."):
    st.header("Compare Packages")
    budget = st.number_input("Budget hint ($)", 10000, value=150000, step=5000)
    if st.button("Generate 3 Options"):
        pkgs={
            "Starter":{"bundle":[("Court Banner Set",2)],"summary":{"total_price":36000,"total_impressions":360000,"cpam":100.0,"guards":{"meets_floor_margin":True,"min_ok_price":32000,"total_floor":30000}}},
            "Balanced":{"bundle":[("Court Banner Set",4),("Digital Package",2)],"summary":{"total_price":112000,"total_impressions":1420000,"cpam":78.87,"guards":{"meets_floor_margin":True,"min_ok_price":98000,"total_floor":91000}}},
            "Impact":{"bundle":[("Venue Naming – Dome",1),("Court Banner Set",8),("Digital Package",4)],"summary":{"total_price":890000,"total_impressions":5400000,"cpam":164.81,"guards":{"meets_floor_margin":True,"min_ok_price":720000,"total_floor":650000}}}
        }
        st.json(pkgs)
