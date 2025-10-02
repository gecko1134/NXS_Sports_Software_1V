
# Simple FastAPI service to track proposal events (Sent/Viewed)
# Run locally: uvicorn webhooks.proposal_events:app --reload --port 8080
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response
import json, os, datetime
from shared.notify import notify_all

app = FastAPI()
LOG = "data/proposals/events.json"

def _load():
    if os.path.exists(LOG):
        return json.load(open(LOG))
    return {"events":[]}

def _save(data):
    os.makedirs("data/proposals", exist_ok=True)
    json.dump(data, open(LOG,"w"), indent=2)

@app.post("/webhook/proposal/{proposal_id}/{event}")
async def proposal_event(proposal_id: str, event: str, request: Request):
    data = _load()
    data["events"].append({"ts": datetime.datetime.utcnow().isoformat()+"Z", "proposal_id": proposal_id, "event": event})
    _save(data)
    return JSONResponse({"ok": True})

# 1x1 tracking pixel for Viewed
@app.get("/t/{proposal_id}.png")
async def track_open(proposal_id: str):
    data = _load()
    data["events"].append({"ts": datetime.datetime.utcnow().isoformat()+"Z", "proposal_id": proposal_id, "event": "viewed"})
    _save(data)
    # transparent png
    notify_all("Proposal viewed.")
        return Response(content=b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\x0cIDATx\x9cc``\x00\x00\x00\x02\x00\x01\xe2!\xbc3\x00\x00\x00\x00IEND\xaeB`\x82", media_type="image/png")
