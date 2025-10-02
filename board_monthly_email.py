
    import os, glob, json, datetime
    import streamlit as st
    from shared.ui import page_header
    from shared.email import send_email

    def _latest_file(pattern):
        files = sorted(glob.glob(pattern))
        return files[-1] if files else None

    def run(user):
        page_header("Board Monthly Email", "Send Board Packet link + KPI summary")
        board_list = st.text_area("Board distribution list (comma-separated)", "board1@nxs.org, board2@nxs.org")
        packet = _latest_file("exports/Board_Packet_*.pdf")
        kpi = _latest_file("data/snapshots/*.json")
        st.write(f"Latest packet: {packet or 'None found'}")
        st.write(f"Latest KPI: {kpi or 'None found'}")

        subject = st.text_input("Subject", f"NXS Board Packet — {datetime.date.today().strftime('%B %Y')}")
        body = "<p>Attached is this month’s Board Packet.</p>"
        if kpi and os.path.exists(kpi):
            try:
                data = json.load(open(kpi))
                r, c, p = data["kpis"]["revenue"], data["kpis"]["cost"], data["kpis"]["profit"]
                body += f"<p>KPI Snapshot — Revenue: ${r:,.0f} • Cost: ${c:,.0f} • Profit: ${p:,.0f}</p>"
            except Exception:
                pass
        

# Add pipeline snapshot (latest proposal)
try:
    latest = json.load(open("data/proposals/latest_proposal.json"))
    events = json.load(open("data/proposals/events.json"))
    interests = json.load(open("data/proposals/interests.json"))
    pid = latest.get("proposal_id")
    sent = sum(1 for e in events.get("events",[]) if e.get("proposal_id")==pid and e.get("event")=="sent")
    viewed = sum(1 for e in events.get("events",[]) if e.get("proposal_id")==pid and e.get("event")=="viewed")
    interested = sum(1 for s in interests.get("submissions",[]) if s.get("proposal_id")==pid)
    body += f"<p>Pipeline — Sent: <b>{sent}</b> • Viewed: <b>{viewed}</b> • Interested: <b>{interested}</b></p>"
except Exception:
    pass

        if st.button("Send to Board"):
            attachments = []
            if packet and os.path.exists(packet):
                attachments.append((os.path.basename(packet), open(packet,"rb").read()))
            recipients = [x.strip() for x in board_list.split(",") if x.strip()]
            ok = send_email(recipients, subject, body, attachments=attachments or None)
            if ok:
                st.success("Board email sent.")
            else:
                st.warning("Send failed. Check SendGrid credentials.")

        st.subheader("CI recipe (GitHub Actions)")
        st.code("""
name: Monthly Board Email
on:
  schedule:
    - cron: "0 15 1 * *"   # 1st of each month 15:00 UTC
jobs:
  mail:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install requests
      - name: Send Email (requires artifacts in repo)
        env:
          SENDGRID_API_KEY: ${{ secrets.SENDGRID_API_KEY }}
          SENDGRID_FROM: "no-reply@nxscomplex.org"
        run: |
          python - <<'PY'
          import os, json, glob, requests, base64
          packet = sorted(glob.glob('exports/Board_Packet_*.pdf'))[-1]
          data = {'personalizations':[{'to':[{'email': 'board@nxs.org'}]}],
                  'from': {'email': os.getenv('SENDGRID_FROM')},
                  'subject':'Monthly Board Packet',
                  'content':[{'type':'text/html','value':'See attached packet.'}],
                  'attachments':[{'content': base64.b64encode(open(packet,'rb').read()).decode(),
                                   'filename': os.path.basename(packet)}]}
          r = requests.post('https://api.sendgrid.com/v3/mail/send',
                            headers={'Authorization': f'Bearer {os.getenv("SENDGRID_API_KEY")}',
                                     'Content-Type':'application/json'},
                            data=json.dumps(data)); r.raise_for_status()
          PY
""", language="yaml")
