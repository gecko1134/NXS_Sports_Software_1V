
import streamlit as st
from shared.ui import page_header, stat
from shared.storage import load_json, save_json, now_iso

def run(user):
    page_header("Ticketing Integration", "Events & payments (Stripe/PayPal hooks).")

    st.write("Create a ticketed event (demo)")
    st.text_input("Event Name")
    st.number_input("Price", min_value=0, value=15)
    st.date_input("Event Date")
    st.button("Create Checkout Link (demo)")

st.subheader("Stripe Checkout (Payment Link)")
price_id = st.text_input("Stripe Price ID (recurring or one-time)", value="price_XXXX")
qty = st.number_input("Quantity", 1, 100, 1)
if st.button("Generate Stripe cURL (copy & run locally)"):
    curl = f"""curl https://api.stripe.com/v1/payment_links   -u $STRIPE_API_KEY:   -d "line_items[0][price]"="{price_id}"   -d "line_items[0][quantity]"="{qty}"   -d "after_completion[type]"="redirect"   -d "after_completion[redirect][url]"="https://nxscomplex.org/thanks""""
    st.code(curl, language="bash")
    st.caption("Set STRIPE_API_KEY in your shell, paste this in a terminal, and Stripe returns a Payment Link URL.")


