
import os, json, streamlit as st
from datetime import datetime
from shared.export_utils import write_doc

def run(base_path:str=".", package_label:str="Custom", data:dict=None):
    st.header("Export Summary")
    pkg_label = st.text_input("Package Label", value=package_label)
    payload = st.text_area("JSON payload (bundle + summary)", value=json.dumps(data or {
        "bundle":[("Court Banner Set",4),("Digital Package",2)],
        "summary":{"total_price":120000,"total_impressions":800000,"cpam":150.0,"guards":{"meets_floor_margin":True,"min_ok_price":90000,"total_floor":82000}},
        "meta":{"term_years":1,"season":"standard","exclusivity":False}
    }, indent=2))
    sponsor_path=None; admin_path=None
    if st.button("Export Files"):
        try:
            obj = json.loads(payload)
        except Exception as e:
            st.error(f"Invalid JSON: {e}"); return
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        base = os.path.join(base_path, "exports"); os.makedirs(base, exist_ok=True)
        sponsor_text = f"Sponsor Summary\nPackage: {pkg_label}\n{json.dumps(obj, indent=2)}"
        admin_text = f"INTERNAL APPROVAL — {pkg_label}\n{json.dumps(obj.get('summary',{}), indent=2)}"
        sponsor_path, _ = write_doc(sponsor_text, os.path.join(base, f"{pkg_label}_{ts}_sponsor.pdf"))
        admin_path, _ = write_doc(admin_text, os.path.join(base, f"{pkg_label}_{ts}_internal.pdf"))
        st.success("Exported PDFs"); st.write(f"Sponsor: {sponsor_path}"); st.write(f"Internal: {admin_path}")
    st.markdown("### Share / Upload")
    if st.button("Upload Sponsor PDF to Google Drive"):
        try:
            from shared.gdrive_utils import upload_file
            meta = upload_file(sponsor_path or admin_path, filename=os.path.basename(sponsor_path or admin_path))
            st.success(f"Drive: {meta.get('webViewLink')}")
        except Exception as e:
            st.warning(f"Drive upload skipped: {e}")
    st.markdown("### Email (Plain + HTML Template)")
    to = st.text_input("To (email)", "")
    if st.button("Send Plain Email"):
        try:
            from shared.email_utils import send_email
            msg = f"Sponsorship summary for {pkg_label}\n\n" + (sponsor_path or "")
            res = send_email(to, f"Sponsor Summary — {pkg_label}", msg, sponsor_path)
            st.write(res)
        except Exception as e:
            st.error(str(e))
    sponsor_name = st.text_input("Sponsor Name", "Sponsor")
    logo_url = st.text_input("Logo URL", "https://via.placeholder.com/240x80?text=NSD+Logo")
    schedule_url = st.text_input("Schedule URL", "#")
    if st.button("Send HTML Template Email"):
        try:
            from shared.email_templates.renderer import render_email_from_summary, load_branding
            from shared.sendgrid_html import send_html_email
            from shared.docusign_utils import build_docusign_link
            obj = json.loads(payload)
            brand = load_branding(base_path)
            obj.setdefault("meta",{}); obj["meta"].update({"sponsor_name": sponsor_name, "package_name": pkg_label})
            ds_link = build_docusign_link(obj.get("summary",{}), obj.get("meta",{}), brand)
            obj["meta"]["docusign_url"] = ds_link
            html = render_email_from_summary(os.path.join(base_path, "shared", "email_templates", "sponsor_summary.html"),
                                             obj, logo_url=logo_url, view_pdf_url="#", schedule_url=schedule_url, base_path=base_path)
            res = send_html_email(to, f"Sponsorship Summary — {pkg_label}", html, sponsor_path)
            st.write(res); st.code(ds_link)
        except Exception as e:
            st.error(f"Template email error: {e}")
    st.markdown("### Branding & CTA")
    theme_mode = st.selectbox("Theme mode", ["light","dark"], index=0)
    accent_hex = st.text_input("Accent color (hex)", value="#0B5FFF")
    cal_url = st.text_input("Calendly URL", value="#")
    docusign_url = st.text_input("DocuSign URL", value="#")
    if st.button("Save Branding"):
        try:
            brand_path = os.path.join(base_path, "shared", "branding.json")
            import json
            brand = json.load(open(brand_path)) if os.path.exists(brand_path) else {}
            brand.setdefault("theme",{}); brand["theme"]["mode"]=theme_mode; brand["theme"]["accent"]=accent_hex
            if cal_url!="#": brand["calendly_url"]=cal_url
            if docusign_url!="#": brand["docusign_url"]=docusign_url
            json.dump(brand, open(brand_path,"w"), indent=2); st.success("Branding saved.")
        except Exception as e: st.error(str(e))
    st.markdown("### DocuSign")
    gen_ds = st.checkbox("Generate DocuSign link from this deal", value=True)
    if gen_ds:
        try:
            from shared.email_templates.renderer import load_branding
            from shared.docusign_utils import build_docusign_link
            obj = json.loads(payload); brand = load_branding(base_path)
            obj.setdefault("meta",{}); obj["meta"].setdefault("package_name", pkg_label)
            link = build_docusign_link(obj.get("summary",{}), obj.get("meta",{}), brand); st.code(link)
            obj["meta"]["docusign_url"] = link; payload = json.dumps(obj, indent=2)
        except Exception as e: st.warning(str(e))
