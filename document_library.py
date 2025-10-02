
import streamlit as st, os, pandas as pd, pathlib
from shared.ui import page_header
from shared.storage import load_json

DOCS_DIR = pathlib.Path("assets/docs")

def _link_for(path: pathlib.Path):
    # Streamlit download button
    with open(path, "rb") as f:
        st.download_button("Download", f, file_name=path.name, mime=None, key=str(path))

def run(user):
    page_header("Document Library", "Board, sponsor & ops files bundled")
    if not DOCS_DIR.exists():
        st.info("No documents found.")
        return
    groups = {
        "Leagues & Roadmaps": ["NXS_League_Roadmap_Timeline.pdf","NXS_Womens_Sports_League_Guide.pdf"],
        "Court & Pod Flyers": ["Court_Pod_Flyer_With_Layout.pdf","Pod_Catalog_Flyer.pdf"],
        "Campaigns": ["NXS_Dual_Campaign_Playbook.pdf"],
        "Data Sources": ["SportsKey_Product_Matrix_With_Courts.xlsx","NXS_Sports_Lounge___Playhouse_Pro_Forma.csv","membership_upgrade_rules.json"],
        "Other": ["SportAI_Master_FullCode_FIXED.zip","wp-nxs-upgrade-prompt.zip"],
    }
    for g, files in groups.items():
        with st.expander(g, expanded=True):
            for name in files:
                p = DOCS_DIR / name
                if p.exists():
                    st.write(f"**{name}**")
                    _link_for(p)
                else:
                    st.caption(f"Missing: {name}")
