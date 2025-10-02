
import streamlit as st

def page_header(title: str, subtitle: str = ""):
    st.title(title)
    if subtitle:
        st.caption(subtitle)

def tag(text: str):
    st.markdown(f"<span style='padding:3px 8px;border-radius:12px;border:1px solid #ddd;font-size:0.8rem'>{text}</span>", unsafe_allow_html=True)

def stat(label: str, value: str):
    st.metric(label, value)


def icon_header(emoji: str, title: str, subtitle: str = ""):
    st.markdown(f"<h2 style='display:flex;align-items:center;gap:8px'>{emoji} {title}</h2>", unsafe_allow_html=True)
    if subtitle:
        st.caption(subtitle)

def section_intro(text: str):
    st.markdown(f"<div style='border-left:4px solid #334155;padding:8px 12px;margin:8px 0;color:#94a3b8'>{text}</div>", unsafe_allow_html=True)
