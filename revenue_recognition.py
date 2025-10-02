
import os, json, datetime, requests, pandas as pd
import streamlit as st
from shared.ui import page_header, icon_header, section_intro
from shared.storage import load_json

def _stripe_invoices():
    key = os.getenv("STRIPE_API_KEY")
    if not key: return [], []
    r_open = requests.get("https://api.stripe.com/v1/invoices?status=open&limit=100", auth=(key,""), timeout=20)
    r_paid = requests.get("https://api.stripe.com/v1/invoices?status=paid&limit=100", auth=(key,""), timeout=20)
    open_list = r_open.json().get("data", []) if r_open.ok else []
    paid_list = r_paid.json().get("data", []) if r_paid.ok else []
    return open_list, paid_list

def _sum_amount(inv_list):
    return sum(v.get("amount_due",0) for v in inv_list) / 100.0

def run(user):
        section_intro("""Track revenue from booked to billed to collected, synced with Stripe.""")
    icon_header('📈', "Revenue Recognition Tracker", "Booked → Billed → Collected (Stripe + Pipeline)")
    latest = load_json("data/proposals/latest_proposal.json", {})
    status = latest.get("status","Draft")
    st.caption(f"Latest proposal status: **{status}**")

    open_inv, paid_inv = _stripe_invoices()
    booked = 0.0
    # If proposal is Won or Invoiced, treat price_floor as booked (illustrative)
    if status.lower().startswith("won"):
        booked = float(latest.get("price_floor", 0.0))
    billed = _sum_amount(open_inv) + _sum_amount(paid_inv)
    collected = _sum_amount(paid_inv)

    col1,col2,col3 = st.columns(3)
    col1.metric("Booked", f"${booked:,.0f}")
    col2.metric("Billed (Open + Paid)", f"${billed:,.0f}")
    col3.metric("Collected (Paid)", f"${collected:,.0f}")

    st.subheader("Detail")
    if open_inv:
        st.write("Open Invoices")
        st.dataframe(pd.DataFrame([{
            "invoice": i.get("id"),
            "customer": i.get("customer_email") or i.get("customer_name"),
            "amount_due": i.get("amount_due",0)/100.0,
            "hosted_invoice_url": i.get("hosted_invoice_url")
        } for i in open_inv]))
    if paid_inv:
        st.write("Paid Invoices")
        st.dataframe(pd.DataFrame([{
            "invoice": i.get("id"),
            "customer": i.get("customer_email") or i.get("customer_name"),
            "amount_paid": i.get("amount_paid",0)/100.0,
            "receipt_url": (i.get("charge","") and "")  # placeholder
        } for i in paid_inv]))
