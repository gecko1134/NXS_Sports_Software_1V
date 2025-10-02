
# FastAPI microservice that serves a proposal landing page and captures interest.
# Run locally: uvicorn webhooks.proposal_landing:app --reload --port 8081
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
import os, json

app = FastAPI()
PROPOSAL_PATH = "data/proposals/latest_proposal.json"
INTERESTS = "data/proposals/interests.json"

def _load_latest():
    if os.path.exists(PROPOSAL_PATH):
        return json.load(open(PROPOSAL_PATH))
    return {}

def _save_interest(rec):
    os.makedirs("data/proposals", exist_ok=True)
    try:
        data = json.load(open(INTERESTS))
    except Exception:
        data = {"submissions":[]}
    data["submissions"].append(rec)
    json.dump(data, open(INTERESTS,"w"), indent=2)

@app.get("/p/{proposal_id}", response_class=HTMLResponse)
async def page(proposal_id: str, request: Request):
    p = _load_latest()
    if p.get("proposal_id") != proposal_id:
        # In a fuller version, look up by ID; for now we serve latest
        pass
    html = f"""
    <html><head><title>NXS Proposal</title></head>
    <body style='font-family:Arial'>
      <h1>NXS Sponsor Proposal</h1>
      <p><b>Sponsor:</b> {p.get('sponsor','')}<br/>
         <b>Placement:</b> {p.get('placement','')}<br/>
         <b>Price Floor:</b> ${p.get('price_floor',0):,.0f}</p>
      <h3>Fast-Track</h3><p>If this package fits, you can reserve immediately:</p>{pl if 'pl' in globals() else ''}<script>/* Stripe Payment Link injected server-side */</script><h3>Tell us you're interested</h3>
      <form method='post' action='/p/{p.get('proposal_id')}/interest'>
        <label>Your Name</label><br/><input name='name' required/><br/>
        <label>Email</label><br/><input name='email' type='email' required/><br/>
        <label>Notes</label><br/><textarea name='notes'></textarea><br/><br/>
        <button type='submit'>I'm Interested</button>
      </form>
      <p style='margin-top:24px;color:#666'>Proposal ID: {p.get('proposal_id')}</p>
    </body></html>
    """
    return HTMLResponse(html)

@app.post("/p/{proposal_id}/interest")
async def interest(proposal_id: str, name: str = Form(...), email: str = Form(...), notes: str = Form("")):
    _save_interest({"proposal_id": proposal_id, "name": name, "email": email, "notes": notes})
    return JSONResponse({"ok": True, "message": "Thank you — we’ll follow up shortly."})
