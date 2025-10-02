
import os, json, base64
try: import requests
except Exception: requests=None
def send_email(to_email, subject, text, attachment_path=None):
    api_key=os.getenv("SENDGRID_API_KEY")
    if not api_key: return {"ok":False,"error":"Missing SENDGRID_API_KEY"}
    if requests is None: return {"ok":False,"error":"requests module unavailable"}
    data={"personalizations":[{"to":[{"email":to_email}]}],
          "from":{"email":os.getenv("SENDGRID_FROM_EMAIL","no-reply@nationalsportsdome.com"),
                  "name":os.getenv("SENDGRID_FROM_NAME","National Sports Dome")},
          "subject":subject,"content":[{"type":"text/plain","value":text}]}
    if attachment_path and os.path.exists(attachment_path):
        b64=base64.b64encode(open(attachment_path,"rb").read()).decode("utf-8")
        data["attachments"]=[{"content":b64,"filename":os.path.basename(attachment_path),
                              "type":"application/pdf","disposition":"attachment"}]
    r=requests.post("https://api.sendgrid.com/v3/mail/send",
                    headers={"Authorization":f"Bearer {api_key}","Content-Type":"application/json"},
                    data=json.dumps(data))
    return {"ok":200<=r.status_code<300,"status":r.status_code,"error":getattr(r,'text','')}
