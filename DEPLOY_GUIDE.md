
# NXS Master OS — Deploy Guide

## Streamlit Cloud (quickest)
1) Run `deploy/init_repo.sh` to init git and push to GitHub.
2) In Streamlit Cloud, create an app pointing to `main_app.py` on `main` branch.
3) Set Secrets:
   - SENDGRID_API_KEY, SENDGRID_FROM
   - GOOGLE_DRIVE_SERVICE_JSON
   - PROPOSAL_HOST, PROPOSAL_PIXEL_HOST
   - SPORTSKEY_API_BASE, SPORTSKEY_API_TOKEN
   - QBO_CLIENT_ID, QBO_CLIENT_SECRET, QBO_REDIRECT_URI, QBO_REALM_ID
4) Click Deploy.

## Optional Microservices
- Run proposal events: `uvicorn webhooks.proposal_events:app --port 8080`
- Run proposal landing: `uvicorn webhooks.proposal_landing:app --port 8081`

## GitHub Actions
- `ci/holds_post.yml` posts suggested holds on weekdays at ~11am CT.
- `ci/finance_snapshot.yml` writes daily KPI snapshots.
- `ci/lint.yml` runs flake8 on pushes/PRs.
