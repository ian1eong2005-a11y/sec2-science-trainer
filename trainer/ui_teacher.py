"""Teacher view: live table of who is logged in and their levels, refreshed every few seconds."""
import os
import time

import pandas as pd
import streamlit as st

from .config import CATEGORIES, CHAPTERS, CLASS_LIST, DASHBOARD_REFRESH_S, DEFAULT_TEACHER_PASSWORD, MAX_LEVEL


def _password_and_source():
    """(password, where it came from): 'secret' (Streamlit secrets), 'env' or 'default'."""
    try:
        if "TEACHER_PASSWORD" in st.secrets:
            return str(st.secrets["TEACHER_PASSWORD"]), "secret"
    except Exception:
        pass
    if os.environ.get("TEACHER_PASSWORD"):
        return os.environ["TEACHER_PASSWORD"], "env"
    return DEFAULT_TEACHER_PASSWORD, "default"


def teacher_password() -> str:
    return _password_and_source()[0]


def render_teacher(store):
    st.markdown("### Teacher dashboard")
    if not st.session_state.get("teacher_ok"):
        with st.form("teacher_login"):
            pw = st.text_input("Teacher password", type="password")
            if st.form_submit_button("Open dashboard", type="primary"):
                if pw == teacher_password():
                    st.session_state["teacher_ok"] = True
                    st.rerun()
                else:
                    st.error("Wrong password.")
        if _password_and_source()[1] == "default":
            st.caption("No TEACHER_PASSWORD secret is set, so the default local password applies. Set one in Streamlit Cloud → Secrets before use with students.")
        return

    _live(store)

    st.divider()
    with st.expander("Admin"):
        rows = store.rows()
        names = {r["_key"]: f"{r['Name']} ({r['Class']})" for r in rows}
        pick = st.selectbox("Student", list(names), format_func=names.get, index=None, placeholder="choose a student")
        l1, l2, l3 = st.columns([2, 2, 1])
        with l1:
            cat = st.selectbox("Category", list(CATEGORIES), format_func=CATEGORIES.get, key="admin_cat")
        with l2:
            lvl = st.selectbox("Level", list(range(1, MAX_LEVEL + 1)), format_func=lambda v: f"L{v}", key="admin_level")
        with l3:
            st.markdown("<div style='height:1.7rem'></div>", unsafe_allow_html=True)
            if st.button("Set level", disabled=pick is None, width="stretch"):
                store.set_level(pick, cat, lvl)
                st.rerun()
        st.caption("Set level moves a student straight to that level (streaks reset). Own-words answers appear for Explanation from L3.")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Reset this student", disabled=pick is None, width="stretch"):
                store.reset_student(pick)
                st.rerun()
        with c2:
            sure = st.checkbox("I am sure")
            if st.button("Clear ALL live data", type="primary", disabled=not sure, width="stretch"):
                store.clear()
                st.rerun()
        if st.button("Log out of teacher view"):
            st.session_state.pop("teacher_ok", None)
            st.rerun()


@st.fragment(run_every=DASHBOARD_REFRESH_S)
def _live(store):
    rows = store.rows()
    online = sum(r["_online"] for r in rows)
    t1, t2, t3 = st.columns(3)
    t1.metric("Students online", online)
    t2.metric("Logged in since restart", len(rows))
    t3.metric("Questions attempted", sum(r["Attempted"] for r in rows))
    st.caption(f"Live · refreshes every {DASHBOARD_REFRESH_S} s · last {time.strftime('%H:%M:%S')} · online = active in the last 2 minutes")

    f1, f2 = st.columns([2, 1])
    with f1:
        classes = st.multiselect("Class", CLASS_LIST, default=[], placeholder="all classes", key="dash_classes")
    with f2:
        only_online = st.toggle("Online only", value=False, key="dash_online")
    shown = [r for r in rows if (not classes or r["Class"] in classes) and (not only_online or r["_online"])]

    if not shown:
        st.info("No students yet. They appear here within a few seconds of logging in.")
        return

    df = pd.DataFrame(shown).drop(columns=["_key", "_online"])
    st.dataframe(
        df, hide_index=True, width="stretch",
        column_config={
            "Online": st.column_config.TextColumn("Online"),
            "Calc level": st.column_config.ProgressColumn("Calc level", min_value=0, max_value=MAX_LEVEL, format="L%d"),
            "Explain level": st.column_config.ProgressColumn("Explain level", min_value=0, max_value=MAX_LEVEL, format="L%d"),
            "Accuracy %": st.column_config.NumberColumn("Accuracy %", format="%d%%"),
            "Last chapter": st.column_config.NumberColumn("Last ch"),
        },
    )

    with st.expander("Level distribution"):
        dist = pd.DataFrame({
            "Calculation": [sum(r["Calc level"] == lv for r in shown) for lv in range(1, MAX_LEVEL + 1)],
            "Explanation": [sum(r["Explain level"] == lv for r in shown) for lv in range(1, MAX_LEVEL + 1)],
        }, index=[f"L{lv}" for lv in range(1, MAX_LEVEL + 1)])
        st.bar_chart(dist, color=["#1f5fa6", "#c77d12"])

    with st.expander("Student detail (last 20 attempts)"):
        names = {r["_key"]: f"{r['Name']} ({r['Class']})" for r in shown}
        pick = st.selectbox("Student", list(names), format_func=names.get, key="dash_detail_pick")
        rec = store.get(pick) if pick else None
        if rec and rec.attempts:
            att = pd.DataFrame([{
                "Time": time.strftime("%H:%M:%S", time.localtime(a.ts)),
                "Category": CATEGORIES.get(a.category, a.category),
                "Ch": a.chapter,
                "Level": f"L{a.level}",
                "Question": a.template_id,
                "Chose": a.chosen,
                "Key": a.key,
                "Correct": a.correct,
                "Retry": a.retry,
                "Hints": a.hints_used,
            } for a in rec.attempts[-20:]][::-1])
            st.dataframe(att, hide_index=True, width="stretch")
        elif rec:
            st.caption("No attempts yet.")

    st.download_button("Download CSV", df.to_csv(index=False).encode("utf-8"), file_name=f"trainer_{time.strftime('%Y%m%d_%H%M')}.csv", mime="text/csv")
