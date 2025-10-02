
    import os, json, pandas as pd
    import streamlit as st
    from shared.ui import page_header, icon_header, section_intro
    from shared.storage import load_json
    from shared.email import send_email

    def run(user):
        section_intro("""One screen to review inventory, finalize terms, and generate/send the contract.""")
        icon_header('🤝', "Deal Desk", "Inventory + Proposal + Contract (one screen)")
        inv = load_json("data/sample/sponsorship_inventory.json", {"items":[]})
        latest = load_json("data/proposals/latest_proposal.json", {})
        st.subheader("Inventory")
        st.dataframe(pd.DataFrame(inv.get("items", [])))

        st.subheader("Proposal")
        st.json(latest or {"status":"No proposal yet"})

        st.subheader("Contract Generator (Quick)")
        sponsor = st.text_input("Sponsor", latest.get("sponsor",""))
        asset = st.text_input("Asset/Placement", latest.get("placement",""))
        term = st.number_input("Term (months)", 1, 120, 12)
        price = st.number_input("Annual Price ($)", 0, 10_000_000, int(latest.get("price_floor", 0)))
        escalator = st.slider("Annual Escalator (%)", 0, 10, 5)
        notes = st.text_area("Special Terms", "Standard brand guidelines; creative approval; makegood for closures.")

        if st.button("Generate Contract (Text)"):
            contract = f"""
NXS Sponsorship Agreement
Sponsor: {sponsor}
Asset: {asset}
Term: {term} months
Annual Price: ${price:,.0f}
Escalator: {escalator}% per annum

Key Terms:
{notes}

Agreed and accepted by Sponsor and NXS.
"""
            os.makedirs("exports", exist_ok=True)
            open("exports/contract.txt","w").write(contract)
            st.success("Saved exports/contract.txt")
            st.code(contract, language="text")

        st.subheader("Send Contract via Email (attachment)")
        to = st.text_input("Recipient email", "deals@example.com")
        if st.button("Email Contract"):
            if os.path.exists("exports/contract.txt"):
                ok = send_email([to], f"Contract — {sponsor}", "<p>Attached is your NXS contract.</p>", attachments=[("NXS_Contract.txt", open("exports/contract.txt","rb").read())])
                st.success("Contract emailed." if ok else "Send failed.")
            else:
                st.error("Generate the contract first.")
