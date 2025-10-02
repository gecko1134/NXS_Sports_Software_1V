
import os, json, datetime
def load_branding(base_path: str):
    try: return json.load(open(os.path.join(base_path, "shared", "branding.json")))
    except Exception:
        return {"facility_address":"Proctor, MN","facility_website":"nationalsportsdome.com","unsubscribe_url":"#","theme":{"mode":"light","accent":"#0B5FFF"}}
def _fmt(n):
    try: return f"{int(n):,}"
    except Exception:
        try: return f"{float(n):,.2f}"
        except Exception: return str(n)
def render_email_from_summary(template_path: str, data: dict, logo_url: str=None, view_pdf_url: str="#", schedule_url: str="#", base_path: str=".") -> str:
    html = open(template_path).read()
    summary = data.get("summary", {}); meta = data.get("meta", {}); items = data.get("items", [])
    if not items and data.get("bundle"): items = [{"name": a, "qty": q, "impressions": "", "value": ""} for a, q in data["bundle"]]
    row_tpl = '<tr><td class="td">{name}</td><td class="td" align="right">{qty}</td><td class="td" align="right">{impressions}</td><td class="td" align="right">${value}</td></tr>'
    rows = "\n".join([row_tpl.format(name=it.get("name",""), qty=_fmt(it.get("qty","")), impressions=_fmt(it.get("impressions","")), value=_fmt(it.get("value",""))) for it in items])
    brand = load_branding(base_path)
    repl = {
        "{{LOGO_URL}}": logo_url or brand.get("logo_url",""),
        "{{PACKAGE_NAME}}": meta.get("package_name","Custom"),
        "{{SPONSOR_NAME}}": meta.get("sponsor_name","Sponsor"),
        "{{TODAY}}": datetime.date.today().strftime("%b %d, %Y"),
        "{{TOTAL_PRICE}}": _fmt(summary.get("total_price","")),
        "{{TOTAL_IMPRESSIONS}}": _fmt(summary.get("total_impressions","")),
        "{{CPAM}}": _fmt(summary.get("cpam","")),
        "{{TERM_YEARS}}": str(meta.get("term_years","")),
        "{{SEASON}}": meta.get("season","standard"),
        "{{EXCLUSIVITY}}": "Yes" if meta.get("exclusivity") else "No",
        "{{ITEM_ROWS}}": rows,
        "{{VIEW_PDF_URL}}": view_pdf_url,
        "{{SCHEDULE_URL}}": schedule_url or brand.get("calendly_url","#"),
        "{{DOCUSIGN_URL}}": meta.get("docusign_url", brand.get("docusign_url","#")),
        "{{GUARDRAIL_PASS}}": "Pass" if summary.get("guards",{}).get("meets_floor_margin") else "Revise",
        "{{MIN_OK_PRICE}}": _fmt(summary.get("guards",{}).get("min_ok_price","")),
        "{{FLOOR_PRICE}}": _fmt(summary.get("guards",{}).get("total_floor","")),
        "{{FACILITY_ADDRESS}}": meta.get("facility_address", brand.get("facility_address","Proctor, MN")),
        "{{FACILITY_WEBSITE}}": meta.get("facility_website", brand.get("facility_website","nationalsportsdome.com")),
        "{{UNSUB_URL}}": meta.get("unsub_url", brand.get("unsubscribe_url","#"))
    }
    for k,v in repl.items(): html = html.replace(k, str(v))
    accent = brand.get("theme",{}).get("accent","#0B5FFF")
    html = f"<style>:root{{--brand:{accent};}}</style>" + html
    return html
