
import streamlit as st
from shared.ui import page_header, icon_header, section_intro, stat
from shared.storage import load_json, save_json, now_iso

def run(user):
        section_intro("""AI fills off‑peak gaps, respects prime windows, and exports holds for Ops.""")
    icon_header('🗓️', "AI Scheduler Optimizer", "Fill gaps, honor priorities, maximize yield.")

    data = load_json("data/sample/bookings.json", {})
    st.json(data)
    st.info("Optimizer stub ready — integrate SportsKey API to activate.")



import pandas as pd, pathlib
st.subheader("SportsKey Product Matrix (Courts)")
xls = pathlib.Path("assets/docs/SportsKey_Product_Matrix_With_Courts.xlsx")
if xls.exists():
    try:
        df = pd.read_excel(xls)
        st.dataframe(df.head(50))
        st.caption("Loaded from assets/docs/SportsKey_Product_Matrix_With_Courts.xlsx")
    except Exception as e:
        st.warning(f"Could not read Excel: {e}")
else:
    st.caption("Upload matrix to assets/docs to enable rate & pod-aware scheduling.")


st.subheader("Usage Plan & Off-Peak Settings")
import json, pathlib, datetime
usage_cfg_path = pathlib.Path("config/usage_plan.json")
if usage_cfg_path.exists():
    usage_cfg = json.loads(usage_cfg_path.read_text())
else:
    usage_cfg = {
        "prime_hours": {"start":"17:00","end":"21:00","days":[1,2,3,4,5]},  # Mon-Fri 5–9pm
        "offpeak_hours": {"start":"13:00","end":"16:00","days":[1,2,3,4]},  # Mon-Thu 1–4pm
        "double_credits": {"enabled": True, "weekly_cap": 2}
    }
    usage_cfg_path.write_text(json.dumps(usage_cfg, indent=2))
st.json(usage_cfg)

def _is_within(t: datetime.time, start: str, end: str):
    s = datetime.datetime.strptime(start, "%H:%M").time()
    e = datetime.datetime.strptime(end, "%H:%M").time()
    return s <= t <= e

st.subheader("Eligible Double Credits (sample bookings)")
import pandas as pd
sample = load_json("data/sample/bookings.json", {"bookings":[]})
rows = []
for b in sample.get("bookings", []):
    st_time = datetime.datetime.fromisoformat(b["start"])
    day = st_time.isoweekday()  # 1=Mon
    t = st_time.time()
    eligible = False
    if usage_cfg.get("double_credits",{}).get("enabled"):
        oh = usage_cfg.get("offpeak_hours",{})
        if day in oh.get("days", []) and _is_within(t, oh.get("start","13:00"), oh.get("end","16:00")):
            eligible = True
    rows.append({
        "resource": b["resource"],
        "start": b["start"],
        "group": b.get("group",""),
        "double_credits": "✅" if eligible else "—"
    })
if rows:
    st.dataframe(pd.DataFrame(rows))

st.caption("Edit config/usage_plan.json to align with your official prime/non-prime windows and off-peak incentive rules.")


st.subheader("Rate-Aware Pod Fill Suggestions")
import pandas as pd, pathlib, datetime as dt

MATRIX = pathlib.Path("assets/docs/SportsKey_Product_Matrix_With_Courts.xlsx")
# Expect sheet with columns like: Resource, PodType, Rate_Prime, Rate_OffPeak, Duration_min
if MATRIX.exists():
    try:
        dfm = pd.read_excel(MATRIX)
        st.caption("Loaded SportsKey Product Matrix")
        st.dataframe(dfm.head(25))
        # Basic heuristic: suggest 60–90 min blocks in off-peak with highest $/hour per resource
        rate_cols = [c for c in dfm.columns if "Rate" in c]
        if rate_cols:
            dfm["rate_offpeak"] = dfm[[c for c in dfm.columns if "Off" in c or "off" in c][0]] if any(("Off" in c or "off" in c) for c in dfm.columns) else dfm[rate_cols[0]]
            dfm["rate_prime"] = dfm[[c for c in dfm.columns if "Prime" in c or "prime" in c][0]] if any(("Prime" in c or "prime" in c) for c in dfm.columns) else dfm[rate_cols[0]]
        else:
            dfm["rate_offpeak"] = 0.0
            dfm["rate_prime"] = 0.0

        # Build a 1-day grid (tomorrow) and find gaps from sample bookings
        sample = load_json("data/sample/bookings.json", {"bookings":[]})
        tomorrow = (dt.datetime.utcnow() + dt.timedelta(days=1)).date()
        resources = list(set([*dfm["Resource"].dropna().astype(str).tolist(), *[b.get("resource") for b in sample.get("bookings",[])] ]))
        grid = []
        for r in resources:
            # assume 08:00-22:00 day; mark booked windows
            slots = [(dt.time(h,0), dt.time(h+1,0)) for h in range(8,22)]
            booked_hours = set()
            for b in sample.get("bookings", []):
                if b.get("resource")==r:
                    stt = dt.datetime.fromisoformat(b["start"]).time().hour
                    endh = dt.datetime.fromisoformat(b["end"]).time().hour
                    for h in range(stt, endh):
                        booked_hours.add(h)
            # Suggest off-peak first
            for h in range(13,16):  # 1–4pm
                if h not in booked_hours:
                    # pick best product for this resource
                    opts = dfm[dfm["Resource"].astype(str)==str(r)]
                    if len(opts)==0:
                        continue
                    top = opts.sort_values("rate_offpeak", ascending=False).iloc[0]
                    grid.append({
                        "resource": r,
                        "start": f"{tomorrow} {h:02d}:00",
                        "end": f"{tomorrow} {h+1:02d}:00",
                        "pod": str(top.get("PodType","")),
                        "rate_offpeak": float(top.get("rate_offpeak",0)),
                        "double_credits": True
                    })
        if grid:
            st.write("**Suggested Fills (tomorrow off-peak):**")
            df_grid = pd.DataFrame(grid); st.dataframe(df_grid)
            if st.button("Export Suggested Holds (CSV)"):
                import csv, os
                os.makedirs("exports", exist_ok=True)
                fp = "exports/suggested_holds.csv"
                with open(fp, "w", newline="") as f:
                    writer = csv.DictWriter(f, fieldnames=grid[0].keys())
                    writer.writeheader()
                    writer.writerows(grid)
                st.success(f"Saved {fp}")
        else:
            st.info("No off-peak suggestions found; all hours appear booked or matrix incomplete.")
    except Exception as e:
        st.warning(f"Could not process matrix: {e}")
else:
    st.caption("Upload SportsKey_Product_Matrix_With_Courts.xlsx to assets/docs for rate-aware suggestions.")


st.subheader("Push Holds to SportsKey (stub)")
import os, json as _json
if st.button("Create Holds Request JSON"):
    os.makedirs("exports", exist_ok=True)
    try:
        df_grid  # from suggestions block above
        payload = df_grid.to_dict(orient="records") if 'df_grid' in locals() else []
    except Exception:
        payload = []
    _json.dump({"requests": payload, "source":"AI Scheduler"}, open("exports/holds_requests.json","w"), indent=2)
    st.success("Saved exports/holds_requests.json — ready for API import when keys are available.")
    st.caption("Next: add SportsKey API keys & endpoints and swap this stub to a live POST.")


st.subheader("Live POST to SportsKey API")
import requests
        from shared.notify import notify_all
api_base = st.text_input("SportsKey API Base URL", os.getenv("SPORTSKEY_API_BASE",""))
api_token = st.text_input("SportsKey API Token (Bearer)", os.getenv("SPORTSKEY_API_TOKEN",""), type="password")
if st.button("POST Holds Now"):
    try:
        import json as _json, pandas as _pd
        payload = df_grid.to_dict(orient="records") if 'df_grid' in locals() else []
        if not api_base or not api_token:
            st.error("Missing API base or token.")
        else:
            url = api_base.rstrip("/") + "/holds"
            resp = requests.post(url, headers={"Authorization": f"Bearer {api_token}", "Content-Type":"application/json"}, data=_json.dumps({"requests": payload}))
            st.write("Status", resp.status_code)
            st.code(resp.text[:2000])
            st.success("Posted to SportsKey (check response above).")
            notify_all("Holds posted to SportsKey.")
    except Exception as e:
        st.warning(f"POST failed: {e}")
