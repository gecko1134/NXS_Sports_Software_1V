
import streamlit as st
from shared.ui import page_header, stat
from shared.storage import load_json, save_json, now_iso

def run(user):
    page_header("Access Control", "Staff/role gates for admin tools.")

    st.write("Assign roles & manage tool access. (Demo UI)")
    st.selectbox("Select User", ["admin@nxscomplex.org","board@nxscomplex.org","sponsor@nxscomplex.org","member@nxscomplex.org"])
    st.selectbox("Role", ["Admin","Board","Sponsor","Member"])
    st.button("Save")

