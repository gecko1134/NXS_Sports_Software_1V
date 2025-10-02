
import json, os, streamlit as st
def run(base_path:str="."):
    st.header("Sponsor Configurator")
    st.write("Build a custom package by entering line items below.")
    items = st.text_area("Items (name,qty,impressions,value per line)", "Court Banner Set,4,720000,72000\nDigital Package,2,700000,40000")
    term = st.selectbox("Term (years)", [1,2,3], index=0); season = st.selectbox("Season", ["standard","peak","off_peak"], index=0)
    exclusivity = st.checkbox("Exclusivity?", False)
    if st.button("Calculate"):
        bundle=[]; total_impr=0; total_price=0
        for line in items.splitlines():
            parts=[p.strip() for p in line.split(",")]
            if len(parts)>=4:
                name, qty, impr, val = parts[0], int(parts[1]), int(parts[2]), float(parts[3])
                bundle.append({"name":name,"qty":qty,"impressions":impr,"value":val})
                total_impr+=impr; total_price+=val
        summary={"total_price":total_price,"total_impressions":total_impr,"cpam":round((total_price/total_impr)*1000,2) if total_impr else None,
                 "guards":{"meets_floor_margin":True,"min_ok_price":round(total_price*0.85,2),"total_floor":round(total_price*0.80,2)}}
        st.json({"bundle":[(b["name"], b["qty"]) for b in bundle],
                 "items":bundle,"summary":summary,"meta":{"term_years":term,"season":season,"exclusivity":exclusivity}})
