
import streamlit as st, pathlib, base64
from shared.ui import page_header, stat

PDF = pathlib.Path("assets/docs/Naming_Rights_Pricing_Floor.pdf")

def run(user):
    page_header("Naming Rights Pricing Floor", "Formula & quick calculator")
    col1, col2 = st.columns([2,1])
    with col1:
        if PDF.exists():
            with open(PDF,"rb") as f:
                import base64
                b64 = base64.b64encode(f.read()).decode("utf-8")
            st.markdown(f'<iframe src="data:application/pdf;base64,{b64}" width="100%" height="700"></iframe>', unsafe_allow_html=True)
        else:
            st.info("Upload the PDF to view the formula details.")

    with col2:
        st.subheader("Quick Calc")
        media = st.number_input("Media Value ($)", min_value=0, value=250000, step=5000)
        activation = st.number_input("Activation Value ($)", min_value=0, value=100000, step=5000)
        exclusivity = st.slider("Exclusivity Multiplier", 1.0, 2.5, 1.5, 0.05)
        goodwill = st.slider("Goodwill Hedge (%)", 0, 35, 20, 1)
        opp_cost = st.number_input("Opportunity Cost ($)", min_value=0, value=50000, step=5000)
        base = (media + activation) * exclusivity
        price_floor = base * (1 + goodwill/100.0) + opp_cost
        st.metric("Suggested Floor", f"${price_floor:,.0f}")
        st.caption("Escalators: 3–5%/yr; Term: 10–15 years; include revaluation triggers.")
