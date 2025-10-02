
    import os, json
    import streamlit as st
    import requests
    from shared.ui import page_header

    def _post_stripe(path, data):
        key = os.getenv("STRIPE_API_KEY")
        if not key:
            return None, "Missing STRIPE_API_KEY"
        resp = requests.post(
            f"https://api.stripe.com/v1/{path}",
            data=data,
            auth=(key, ""),
            timeout=20
        )
        try:
            resp.raise_for_status()
            return resp.json(), None
        except Exception as e:
            return None, f"{e}: {resp.text[:500]}"

    def run(user):
        page_header("Sponsor Billing (Stripe)", "Create customers, products, and invoices")
        st.caption("Provide minimal data below; will try to create and send an invoice via Stripe API.")
        email = st.text_input("Sponsor email", "billing@example.com")
        name = st.text_input("Sponsor name", "Acme Health")
        product = st.text_input("Line item description", "NXS Sponsorship — Court A Center Logo")
        amount = st.number_input("Amount (USD cents)", 0, 100000000, 2500000, step=50000)
        if st.button("Create Invoice (send via Stripe)"):
            # 1) Create customer
            cust, err = _post_stripe("customers", {"email": email, "name": name})
            if err:
                st.error(f"Customer error: {err}"); return
            # 2) Create product & price
            prod, err = _post_stripe("products", {"name": product})
            if err:
                st.error(f"Product error: {err}"); return
            price, err = _post_stripe("prices", {"unit_amount": amount, "currency":"usd", "product": prod["id"]})
            if err:
                st.error(f"Price error: {err}"); return
            # 3) Create invoice item
            ii, err = _post_stripe("invoiceitems", {"customer": cust["id"], "price": price["id"]})
            if err:
                st.error(f"Invoice item error: {err}"); return
            # 4) Create & finalize invoice (auto email if account settings allow)
            inv, err = _post_stripe("invoices", {"customer": cust["id"], "collection_method":"send_invoice", "days_until_due": 30})
            if err:
                st.error(f"Invoice error: {err}"); return
            fin, err = _post_stripe(f"invoices/{inv['id']}/finalize", {})
            if err:
                st.error(f"Finalize error: {err}"); return
            st.success(f"Invoice created: {fin.get('id')} (status {fin.get('status')})")
            st.json(fin)
        st.divider()
        st.subheader("cURL template (manual)")
        st.code("""
# assumes STRIPE_API_KEY in env
curl https://api.stripe.com/v1/customers -u $STRIPE_API_KEY: -d email=billing@example.com -d name="Acme Health"
# then create product, price, invoice item, and invoice similarly
""", language="bash")
