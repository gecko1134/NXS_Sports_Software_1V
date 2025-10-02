
# FastAPI webhooks to record "fully executed" contract events from DocuSign/Adobe Sign.
# Run: uvicorn webhooks.esign_webhooks:app --reload --port 8082
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import json, os, datetime

app = FastAPI()

def _auto_invoice_and_pipeline(sponsor_email: str, sponsor_name: str, amount_cents: int = 0):
    # Create minimal Stripe invoice and mark pipeline as Won + Invoiced
    try:
        import requests, os, json
        key = os.getenv("STRIPE_API_KEY")
        if key and sponsor_email:
            cust = requests.post("https://api.stripe.com/v1/customers", data={"email":sponsor_email,"name":sponsor_name or sponsor_email}, auth=(key,""), timeout=20).json()
            prod = requests.post("https://api.stripe.com/v1/products", data={"name":"NXS Sponsorship"}, auth=(key,""), timeout=20).json()
            price = requests.post("https://api.stripe.com/v1/prices", data={"unit_amount": amount_cents or 100000, "currency":"usd", "product": prod["id"]}, auth=(key,""), timeout=20).json()
            requests.post("https://api.stripe.com/v1/invoiceitems", data={"customer":cust["id"], "price": price["id"]}, auth=(key,""), timeout=20)
            inv = requests.post("https://api.stripe.com/v1/invoices", data={"customer": cust["id"], "collection_method":"send_invoice", "days_until_due": 30}, auth=(key,""), timeout=20).json()
            requests.post(f"https://api.stripe.com/v1/invoices/{inv['id']}/finalize", auth=(key,""), timeout=20)
    except Exception as e:
        print("Auto invoice failed:", e)
    # Update pipeline latest proposal status
    try:
        latest_path = "data/proposals/latest_proposal.json"
        if os.path.exists(latest_path):
            latest = json.load(open(latest_path))
            latest["status"] = "Won + Invoiced"
            json.dump(latest, open(latest_path,"w"), indent=2)
    except Exception as e:
        print("Pipeline update failed:", e)

LOG = "data/contracts/events.json"

def _load():
    if os.path.exists(LOG):
        return json.load(open(LOG))
    return {"events":[]}

def _save(data):
    os.makedirs("data/contracts", exist_ok=True)
    json.dump(data, open(LOG,"w"), indent=2)

@app.post("/webhook/docusign")
async def docusign(req: Request):
    payload = await req.json()
    data = _load()
    data["events"].append({
        "ts": datetime.datetime.utcnow().isoformat()+"Z",
        "source": "docusign",
        "envelope_id": payload.get("envelopeId"),
        "status": payload.get("status"),
        "sponsor": payload.get("sponsor"),
        "executed": payload.get("status") in ["completed","completedEnvelope"]
    })
    _save(data)
        if data['events'][-1].get('executed'):
        _auto_invoice_and_pipeline(payload.get('sponsor_email') or payload.get('sponsor'), payload.get('sponsor'), 0)
    return JSONResponse({"ok": True})

@app.post("/webhook/adobesign")
async def adobesign(req: Request):
    payload = await req.json()
    data = _load()
    data["events"].append({
        "ts": datetime.datetime.utcnow().isoformat()+"Z",
        "source": "adobesign",
        "agreement_id": payload.get("agreementId"),
        "status": payload.get("status"),
        "sponsor": payload.get("sponsor"),
        "executed": payload.get("status") in ["SIGNED","APPROVED","COMPLETED"]
    })
    _save(data)
        if data['events'][-1].get('executed'):
        _auto_invoice_and_pipeline(payload.get('sponsor_email') or payload.get('sponsor'), payload.get('sponsor'), 0)
    return JSONResponse({"ok": True})
