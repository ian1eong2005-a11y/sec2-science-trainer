"""Sec 2 Science adaptive trainer - Streamlit entry point.

Run locally:   streamlit run app.py
Teacher view:  sidebar -> Teacher, or append ?teacher=1 to the URL.
"""
import streamlit as st

from trainer.config import APP_TITLE, CLASSES, SCHOOL
from trainer.store import get_store
from trainer.ui_student import render_student
from trainer.ui_teacher import render_teacher

st.set_page_config(page_title=APP_TITLE, page_icon="🔬", layout="centered", initial_sidebar_state="collapsed")

st.markdown(
    """<style>
    div.stButton > button { min-height: 2.9rem; text-align: left; justify-content: flex-start; }
    div.stButton > button p { text-align: left; }
    .block-container { padding-top: 1.6rem; max-width: 760px; }
    </style>""",
    unsafe_allow_html=True,
)


store = get_store()          # one in-memory store per server process, shared by every browser session
ss = st.session_state

teacher_mode = st.query_params.get("teacher") == "1" or ss.get("view") == "teacher"
with st.sidebar:
    st.markdown(f"## 🔬 {APP_TITLE}")
    st.caption(SCHOOL)
    if teacher_mode:
        if st.button("← Student view"):
            ss["view"] = "student"
            st.query_params.clear()
            st.rerun()
    else:
        if st.button("Teacher"):
            ss["view"] = "teacher"
            st.rerun()

if teacher_mode:
    render_teacher(store)
    st.stop()

rec = store.get(ss["student_key"]) if "student_key" in ss else None
if rec is None:
    if "student_key" in ss:
        ss.pop("student_key", None)
        ss.pop("qs", None)
        st.info("Your session was reset. Please log in again.")
    st.markdown(f"## 🔬 {APP_TITLE}")
    st.markdown("Train yourself on Sec 2 Science (Chapters 9–16): calculation and data questions, and explanation questions. Get **5 in a row** right to move up a level; **3 wrong in a row** moves you down one.")
    with st.form("login"):
        name = st.text_input("Your name", placeholder="e.g. Aisyah")
        options = [f"{grp} · {c}" for grp, cs in CLASSES.items() for c in cs]
        cls = st.selectbox("Class", options, index=None, placeholder="choose your class")
        go = st.form_submit_button("Start", type="primary", width="stretch")
    if go:
        if len(name.strip()) < 2:
            st.error("Please enter your name.")
        elif not cls:
            st.error("Please choose your class.")
        else:
            rec = store.login(name, cls.split(" · ")[1])
            ss["student_key"] = rec.key
            ss.pop("qs", None)
            st.rerun()
    st.stop()

render_student(store, rec)
