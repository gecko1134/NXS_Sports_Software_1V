
import os, json, base64
from typing import List, Optional, Tuple

def _post_sendgrid(api_key: str, to: List[str], subject: str, html: str, attachments: Optional[List[Tuple[str, bytes]]] = None):
    import requests
    url = "https://api.sendgrid.com/v3/mail/send"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "personalizations": [{"to": [{"email": x} for x in to]}],
        "from": {"email": os.getenv("SENDGRID_FROM","no-reply@nxscomplex.org"), "name":"NXS"},
        "subject": subject,
        "content": [{"type":"text/html","value": html}]
    }
    if attachments:
        payload["attachments"] = [{
            "content": base64.b64encode(data).decode("utf-8"),
            "filename": fname
        } for fname, data in attachments]
    r = requests.post(url, headers=headers, data=json.dumps(payload), timeout=20)
    r.raise_for_status()
    return True

def send_email(to: List[str], subject: str, html: str, attachments: Optional[List[Tuple[str, bytes]]] = None):
    api_key = os.getenv("SENDGRID_API_KEY")
    if api_key:
        try:
            return _post_sendgrid(api_key, to, subject, html, attachments)
        except Exception as e:
            print(f"[SENDGRID ERROR] {e}; falling back to dev stub")
    # Dev stub
    size = 0
    if attachments:
        size = sum(len(b) for _, b in attachments)
    print(f"[DEV EMAIL] to={to} subject={subject} len(html)={len(html)} attachments={len(attachments or [])} total_bytes={size}")
    return True
