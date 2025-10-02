
import os, streamlit as st
from modules.sponsorship import sponsor_configurator, sponsor_compare, sponsor_export
CATEGORY="Sponsorship Tools"
def register(app_state: dict):
    base=app_state["base_path"]; role=app_state.get("role","Guest")
    cats=app_state.setdefault("categories", {})
    entries=[]
    if role in ["Admin","Sponsor","Board"]:
        entries.append(("Configurator", lambda: sponsor_configurator.run(base)))
        entries.append(("Compare", lambda: sponsor_compare.run(base)))
    if role in ["Admin","Board"]:
        entries.append(("Export", lambda: sponsor_export.run(base)))
    if entries: cats.setdefault(CATEGORY, []).extend(entries)
