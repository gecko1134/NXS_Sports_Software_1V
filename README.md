
# NXS Master Operating System (Streamlit)

**Generated:** 2025-10-02 13:43:52

A unified, role-based dashboard that runs ~90% of operations via AI, automation, and delegation.
This is a working scaffold you can deploy today; wire real APIs as you go.

## Quickstart

```bash
pip install -r requirements.txt
streamlit run main_app.py
```

### Demo Logins
- admin@nxscomplex.org / admin123
- board@nxscomplex.org / board123
- sponsor@nxscomplex.org / sponsor123
- member@nxscomplex.org / member123

## Structure
- `main_app.py` — launcher with login, roles, dynamic module loader
- `modules/*` — tools grouped by function; each exposes `run(user)`
- `shared/*` — helpers for auth, UI, storage, email
- `config/*` — users, roles, app navigation
- `data/sample/*` — seed data (replace with live sources)
- `assets/email_templates/*` — HTML email templates

## Wire Real Integrations (Next)
- SportsKey bookings & memberships
- Stripe/PayPal payments
- SendGrid emails (`shared/email.py`)
- QuickBooks/Sheets sync
- FlippingBook & WordPress embeds
- Grant APIs (MNvest, Wefunder, etc.)

## Deployment
- Local: `streamlit run main_app.py`
- Streamlit Cloud: push to GitHub and deploy
- Subdomains: map `portal.nxscomplex.org` and `admin.nxscomplex.org` to your deployment

## Notes
- Passwords are hashed in `config/users.json`.
- Add or restrict access via `config/roles.json`.
- Add modules to nav in `config/app.json`.

---
© NXS


## Email (SendGrid)
Set environment variables before running to send real emails:
```
export SENDGRID_API_KEY="YOUR_KEY"
export SENDGRID_FROM="no-reply@nxscomplex.org"
```
In Streamlit Cloud, add them in **App secrets**.

## SportsKey Matrix
Place **assets/docs/SportsKey_Product_Matrix_With_Courts.xlsx** with columns like:
`Resource, PodType, Rate_Prime, Rate_OffPeak, Duration_min`

## Proposal PDFs
Create a proposal in **Marketing → Ad Launcher**, then export in **Sponsorship Tools → Sponsor Proposal PDF Exporter**.
Files save to `exports/`.


## Governance & Compliance
- **Board Packet Compiler:** select PDFs in `assets/docs/` to merge into a monthly packet in `exports/`.

## Finance Sync
- **CSV:** upload any QuickBooks/Exports.
- **Google Sheets:** add service account JSON to env `GSERVICE_ACCOUNT_JSON` or `secrets/service_account.json`.

## Sponsorship Auto-Renewal Alerts
- Scans `data/sample/sponsorship_inventory.json`; emails sponsors due in **90/60/30** days (adjustable).

## Stripe Checkout
- In Ticketing Integration, generate a **Payment Link** cURL. Set `STRIPE_API_KEY` before running.


## Proposal → Email
- Create a proposal (Marketing → Ad Launcher), export to PDF (Sponsorship Tools → Proposal PDF Exporter), then email it with attachment (Sponsorship Tools → Email Proposal to Prospect).
- Requires `SENDGRID_API_KEY`.

## Google Drive Upload (Board Packet)
- Add service account JSON to env `GOOGLE_DRIVE_SERVICE_JSON` or `secrets/drive_service.json`.
- Use Governance & Compliance → Upload Board Packet to Google Drive.
- Provide a target Folder ID.

## Finance KPI Snapshot
- Upload `data/finance_source.csv` via the module, then snapshots are written daily on app open; optional CI workflow at `ci/finance_snapshot.yml`.


## Proposal Webhooks (Sent/Viewed)
- Local events service: `uvicorn webhooks.proposal_events:app --reload --port 8080`
- Mark sent: `POST /webhook/proposal/{proposal_id}/sent`
- Track views: embed an image pointing to `/t/{proposal_id}.png` in the proposal email/body.
- Ad Launcher shows a pipeline badge (Sent/Viewed) based on `data/proposals/events.json`.

## Monthly Board Email
- Governance → Board Monthly Email: attaches latest Board Packet and includes KPI headline.
- CI example provided to run on the 1st of each month (requires artifacts in repo).

## Renewal Sequence Attachments
- Sponsor Auto-Renewal Alerts now supports **90/60/30** templates and optional attachment of `exports/proposal.pdf`.


## Proposal Landing Pages
- Run: `uvicorn webhooks.proposal_landing:app --reload --port 8081`
- Public URL: `/p/{proposal_id}` renders the latest proposal details and an interest form.
- Submissions saved to `data/proposals/interests.json`.

## SportsKey Holds — API Push (stub)
- In AI Scheduler Optimizer, click **Create Holds Request JSON** to save `exports/holds_requests.json`.
- Replace with live POST once SportsKey API keys/endpoints are available.

## QuickBooks Online Connector
- Use **Finance Tools → QuickBooks Online (QBO) Connector**.
- Start with **CSV fallback** for immediate trendlines; add OAuth credentials later for live P&L/Cash Flow.


## Email Proposal: Landing URL + Tracking
- Set `PROPOSAL_HOST` to serve landing pages (defaults to `http://localhost:8081`).
- Set `PROPOSAL_PIXEL_HOST` for the tracking pixel (defaults to `http://localhost:8080`).
- Module builds CTA + 1x1 pixel automatically in the email body preview.

## SportsKey Live POST
- In AI Scheduler Optimizer, set `SPORTSKEY_API_BASE` and `SPORTSKEY_API_TOKEN` or paste them into the UI to POST holds JSON.

## QBO OAuth Helper
- Finance Tools → QBO OAuth Helper generates an authorize URL and exchanges the auth code for tokens saved to `data/qbo/tokens.json`.


## Sales Pipeline Dashboard
- Marketing → Sales Pipeline Dashboard shows Sent/View/Interest funnel using `data/proposals/events.json` and `data/proposals/interests.json`.

## Scheduled Holds (Weekdays 11am CT)
- GitHub Actions workflow at `ci/holds_post.yml` posts suggested holds automatically.
- Store `SPORTSKEY_API_BASE` and `SPORTSKEY_API_TOKEN` in repo secrets.
- Manual override exists in **AI Scheduler Optimizer** (POST Holds Now).

## Proposal Email Auto-Draft
- After exporting a proposal PDF, an email draft with landing URL + tracking pixel is saved at `data/proposals/email_draft.html`. The Email Proposal module loads it automatically.


## One‑Click Deploy (Repo Scaffold)
- Use `deploy/init_repo.sh` to initialize and push to GitHub quickly.
- See `deploy/DEPLOY_GUIDE.md` for Streamlit Cloud, microservices, and Actions.


## Deal Desk
- Sponsorship Tools → Deal Desk: See inventory + proposal + generate a quick contract (text) on one screen, then email it as an attachment.

## Slack/Teams Notifications
- Set `SLACK_WEBHOOK_URL` and/or `TEAMS_WEBHOOK_URL` to receive alerts for:
  - Sponsor renewal emails sent
  - Holds posted to SportsKey
  - Proposal viewed (tracking pixel)

## Payment Link CTA (Landing Page)
- Set `STRIPE_PAYMENT_LINK` to inject a "Payment Link" button on the proposal landing page (`/p/{proposal_id}`).


## Contract PDFs + E‑Sign
- **Sponsorship Tools → Contract PDF Generator** creates a print‑ready agreement with signature blocks.
- Run **DocuSign/Adobe Sign Webhooks** service:
  ```bash
  uvicorn webhooks.esign_webhooks:app --reload --port 8082
  ```
  POST your e‑signature platform events to `/webhook/docusign` or `/webhook/adobesign` to log "executed".

## Sponsor Billing (Stripe)
- **Finance Tools → Sponsor Billing**: creates customer → product/price → invoice via Stripe if `STRIPE_API_KEY` is set.
- Fallback: cURL template included if you prefer manual steps.


## E‑Sign Envelope Creator
- **Sponsorship Tools → E‑Sign Envelope Creator** sends your Contract PDF through **DocuSign** or **Adobe Sign** when you paste access tokens & IDs.

## Receivables Dashboard
- **Finance Tools → Receivables Dashboard** pulls open Stripe invoices, shows **days outstanding**, and sends **dunning emails** via SendGrid.

## Auto-Invoice on Executed Contracts
- The e‑sign webhook service now auto-creates a Stripe invoice and marks the pipeline **Won + Invoiced** when the webhook indicates an executed agreement.


## Counter-Signature (NXS First)
- In **E-Sign Envelope Creator**, enable "Require NXS counter-signature first" to route NXS signer before the sponsor.

## Revenue Recognition Tracker
- **Finance Tools → Revenue Recognition** shows Booked (from pipeline), Billed (Stripe open+paid), Collected (Stripe paid).

## Budget vs Actuals
- **Finance Tools → Budget vs Actuals (Board View)**: upload a Budget CSV and either an Actuals CSV or a Google Sheet to see variances and trend charts.


## UI Polish
- Dark theme enabled via `.streamlit/config.toml` (tweak colors as needed).
- New helpers: `icon_header(emoji, title, subtitle)` and `section_intro(text)` used across key modules.

## Samples
- Budget/Actuals sample CSVs in `data/sample/`. Point the Budget vs Actuals module at them to see variance visuals.
- Ad Launcher can now **save multiple proposals**; the Pipeline Dashboard adds a selector to switch between proposals.


## Board Walkthrough Mode
- Governance & Compliance → **Board Walkthrough Mode** gives you quick links and loads demo data:
  - Multiple proposals (draft/sent/won), events, interests, and reasons
  - Finance source CSV & daily snapshot
  - A ready-to-download Board Packet in `exports/`
- Use this for investor/board demos with no extra setup.


## Settings → Theme Switcher
- Toggle between Dark/Light; updates `.streamlit/config.toml` (restart app to apply).

## Ops → Health Monitor
- Quick view of what keys/integrations are configured (SendGrid, Stripe, SportsKey, etc.).

## Finance → KPI Slack Notifier
- Posts the latest KPI snapshot to Slack/Teams via your webhook(s).

## DevOps → Docker
- `deploy/Dockerfile` + `deploy/run.sh` + `.env.example` for containerized runs.
- Build & run: `bash deploy/run.sh`

## Ops → Data Export / Backup
- Creates a ZIP of `data/`, `exports/`, and `config/` for off-site storage.
