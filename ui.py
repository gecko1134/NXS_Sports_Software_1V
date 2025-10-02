
import streamlit as st
def page_header(title: str, subtitle: str = ""):
    st.title(title); 
    if subtitle: st.caption(subtitle)
def icon_header(emoji: str, title: str, subtitle: str = ""):
    st.markdown(f"<h2 style='display:flex;align-items:center;gap:8px'>{emoji} {title}</h2>", unsafe_allow_html=True)
    if subtitle: st.caption(subtitle)
def section_intro(text: str):
    st.markdown(f"<div style='border-left:4px solid #334155;padding:8px 12px;margin:8px 0;color:#94a3b8'>{text}</div>", unsafe_allow_html=True)
