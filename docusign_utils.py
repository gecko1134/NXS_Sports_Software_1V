
import urllib.parse, datetime
def build_docusign_link(summary: dict, meta: dict, branding: dict) -> str:
    base = branding.get("docusign_url", "#")
    params = {
        "pkg": meta.get("package_name","Custom"),
        "sponsor": meta.get("sponsor_name","Sponsor"),
        "price": str(summary.get("total_price","")),
        "impr": str(summary.get("total_impressions","")),
        "cpam": str(summary.get("cpam","")),
        "date": datetime.date.today().isoformat(),
        "min_ok_price": str(summary.get("guards",{}).get("min_ok_price","")),
        "meets_floor": "1" if summary.get("guards",{}).get("meets_floor_margin") else "0",
    }
    qs = urllib.parse.urlencode(params)
    return f"{base}?{qs}" if "?" not in base else f"{base}&{qs}"
