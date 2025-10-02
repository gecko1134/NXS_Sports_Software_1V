
import os, json, datetime, requests
import pandas as pd
import streamlit as st
from shared.ui import page_header
from shared.email import send_email

def _stripe_list_invoices():
    key = os.getenv("STRIPE_API_KEY")
    if not key: return []
    r = requests.get("https://api.stripe.com/v1/invoices?status=open&limit=100", auth=(key,""), timeout=20)
    if not r.ok: return []
    return r.json().get("data", [])

def _days_outstanding(created_ts):
    dt = datetime.datetime.fromtimestamp(created_ts)
    return (datetime.datetime.utcnow() - dt).days

def run(user):
    page_header("Receivables Dashboard", "Open invoices, days outstanding, and dunning emails")
    data = _stripe_list_invoices()
    if not data:
        st.info("No open invoices or missing STRIPE_API_KEY.")
        return
    rows = []
    for inv in data:
        rows.append({
            "invoice": inv.get("id"),
            "customer": (inv.get("customer_email") or inv.get("customer_name") or ""),
            "amount_due": inv.get("amount_due",0)/100.0,
            "created": inv.get("created"),
            "days_outstanding": _days_outstanding(inv.get("created",0)),
            "hosted_invoice_url": inv.get("hosted_invoice_url","")
        })
    df = pd.DataFrame(rows).sort_values("days_outstanding", ascending=False)
    st.dataframe(df)

    st.subheader("Dunning Email (SendGrid)")
    idx = st.selectbox("Select invoice row", list(range(len(df))), format_func=lambda i: f"{df.iloc[i]['invoice']} — {df.iloc[i]['customer']} (${df.iloc[i]['amount_due']:.2f})")
    cust_email = st.text_input("Customer email", df.iloc[idx]["customer"] or "billing@example.com")
    subject = st.text_input("Subject", "Invoice reminder — action requested")
    body = st.text_area("Body (HTML)", f"<p>Hello — this is a friendly reminder. Your invoice {df.iloc[idx]['invoice']} is outstanding ({df.iloc[idx]['days_outstanding']} days). <a href='{df.iloc[idx]['hosted_invoice_url']}'>Pay now</a>.</p>")
    if st.button("Send Reminder"):
        ok = send_email([cust_email], subject, body)
        st.success("Reminder sent." if ok else "Send failed.")
