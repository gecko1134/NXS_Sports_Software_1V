
import os, json, base64, requests
def send_email(to, subject, html, attachments=None):
    key = os.getenv("SENDGRID_API_KEY")
    if not key: 
        print("[DEV EMAIL]", to, subject, len(html)); 
        return True
    payload = {
        "personalizations":[{"to":[{"email": t} for t in to]}],
        "from":{"email": os.getenv("SENDGRID_FROM","no-reply@nxscomplex.org")},
        "subject": subject,
        "content":[{"type":"text/html","value": html}],
    }
    if attachments:
        payload["attachments"] = [{"content": base64.b64encode(b).decode(),"filename":fn} for fn,b in attachments]
    r = requests.post("https://api.sendgrid.com/v3/mail/send",
                      headers={"Authorization":f"Bearer {key}","Content-Type":"application/json"},
                      data=json.dumps(payload), timeout=20)
    return r.ok
