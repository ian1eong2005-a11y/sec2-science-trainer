"""Student view: one question at a time, scripted hint tutor after a wrong answer, level banners."""
import random
import time

import streamlit as st

from .config import CATEGORIES, CHAPTERS, DOWN_STREAK, EXPLAIN_LEVEL_NAMES, LEVEL_NAMES, UP_STREAK
from .content import TEMPLATES
from .engine import apply_first_attempt, levels_available, repeat_until_correct, select_template
from .marking import mark_answer
from .store import Attempt

WRITE_FROM_LEVEL = 3      # explanation questions at this level and above are first answered in the student's own words

_rng = random.Random()


def _qs():
    return st.session_state.setdefault("qs", {})


def _serve(store, rec, cat, chapters):
    state = rec.states[cat]
    tpl = select_template(TEMPLATES, cat, state.level, chapters, rec.recent[cat], _rng)
    q = tpl.make(_rng.randrange(1_000_000_000))
    rec.recent[cat].append(tpl.id)
    rec.current[cat] = q
    st.session_state["qs"] = dict(
        cat=cat, question=q, level=state.level, phase="answer", wrong=set(), hints_shown=0, hints_used=0,
        formula_shown=False, chat=[], event=None, retry_correct=False, serial=_rng.randrange(1 << 30), served_at=time.time(),
        mode="write" if (cat == "explain" and q.level >= WRITE_FROM_LEVEL) else "choose", typed="",
    )
    store.touch(rec.key)
    return st.session_state["qs"]


def _answer(store, rec, letter):
    qs = _qs()
    q, cat = qs["question"], qs["cat"]
    state = rec.states[cat]
    correct = letter == q.key
    if qs["phase"] == "answer":                                 # first attempt: the only one that counts
        qs["event"] = apply_first_attempt(state, correct)
        store.log_attempt(rec.key, Attempt(time.time(), cat, q.template_id, q.chapter, qs["level"], letter, q.key, correct, False, 0))
        if correct:
            qs["phase"] = "solved"
        else:
            qs["wrong"].add(letter)
            qs["phase"] = "hints"
            qs["chat"] = [("tutor", f"Not quite. You chose **{letter}**. " + q.misconceptions.get(letter, "That value does not follow from the correct method."))]
    else:                                                       # retry: no streak credit
        store.log_attempt(rec.key, Attempt(time.time(), cat, q.template_id, q.chapter, qs["level"], letter, q.key, correct, True, qs["hints_used"]))
        if correct:
            qs["phase"] = "solved"
            qs["retry_correct"] = True
        else:
            qs["wrong"].add(letter)
            if repeat_until_correct(cat, qs["level"]):
                qs["phase"] = "hints"
                qs["chat"].append(("tutor", f"Still not it. You chose **{letter}**. " + q.misconceptions.get(letter, "Think again about the definition.")))
            else:
                qs["phase"] = "revealed"
    store.touch(rec.key)


def _check_typed(store, rec, text):
    """First attempt given in the student's own words. Every key idea present -> correct; otherwise the tutor says
    which ideas are missing and the student retries with the options (no streak credit, as for any retry)."""
    qs = _qs()
    q, cat = qs["question"], qs["cat"]
    state = rec.states[cat]
    hits, total, missing, ok = mark_answer(text, q.keypoints, q.options[q.key])
    qs["typed"] = text
    qs["event"] = apply_first_attempt(state, ok)
    store.log_attempt(rec.key, Attempt(time.time(), cat, q.template_id, q.chapter, qs["level"], "typed", q.key, ok, False, 0))
    if ok:
        qs["phase"] = "solved"
        qs["chat"] = [("tutor", f"Your answer covers all {total} key idea{'s' if total > 1 else ''}. Wording does not have to match the model answer.")]
    else:
        qs["phase"] = "hints"
        qs["mode"] = "choose"
        if q.keypoints:
            got = f"You have {hits} of {total} key ideas. " if hits else "None of the key ideas came through yet. "
            qs["chat"] = [("tutor", got + "Still missing: " + "; ".join(f"**{m}**" for m in missing) + ". Use the hints, then choose the best option below.")]
        else:
            qs["chat"] = [("tutor", "Your answer does not yet say the main idea the question is looking for. Use the hints, then choose the best option below.")]
    store.touch(rec.key)


def _box(colour):
    return f'<span style="display:inline-block;width:16px;height:16px;border-radius:3px;margin:0 2px;vertical-align:middle;background:{colour}"></span>'


def _streak_strip(state):
    boxes = _box("#2e9e5b") * state.correct_streak + _box("#dcdfe4") * max(0, UP_STREAK - state.correct_streak)
    wrong = _box("#d64545") * state.wrong_streak + _box("#dcdfe4") * max(0, DOWN_STREAK - state.wrong_streak)
    return f"Correct in a row: {boxes}&nbsp;&nbsp;&nbsp; Wrong in a row: {wrong}"


def render_student(store, rec):
    store.touch(rec.key)
    ss = st.session_state

    with st.sidebar:
        st.markdown(f"### {rec.name}\n{rec.cls}")
        for cat, label in CATEGORIES.items():
            s = rec.states[cat]
            acc = "–" if s.accuracy is None else f"{round(100 * s.accuracy)}%"
            st.markdown(f"**{label}**: L{s.level} · {s.attempted} done · {acc} correct")
        if st.button("Log out", width="stretch"):
            for k in ("student_key", "qs", "category", "chapters"):
                ss.pop(k, None)
            st.rerun()

    # ---- practice settings
    cat = st.radio("Practise", list(CATEGORIES), format_func=CATEGORIES.get, horizontal=True,
                   index=list(CATEGORIES).index(ss.get("category", "calc")), key="category_radio")
    if cat != ss.get("category"):
        ss["category"] = cat
        ss.pop("qs", None)
    with st.expander("Chapters", expanded=False):
        chapters = st.multiselect("Practise these chapters", list(CHAPTERS), default=ss.get("chapters", list(CHAPTERS)),
                                  format_func=lambda c: f"Ch {c} {CHAPTERS[c]}", key="chapters_ms")
    if not chapters:
        chapters = list(CHAPTERS)
    if chapters != ss.get("chapters"):
        ss["chapters"] = chapters
        ss.pop("qs", None)

    state = rec.states[cat]
    names = LEVEL_NAMES if cat == "calc" else EXPLAIN_LEVEL_NAMES
    st.markdown(f"#### {CATEGORIES[cat]} · Level {state.level}")
    st.caption(names[state.level])
    st.markdown(_streak_strip(state), unsafe_allow_html=True)

    if cat == "explain" and state.level < WRITE_FROM_LEVEL:
        st.caption(f"From L{WRITE_FROM_LEVEL} you will answer explanation questions in your own words first.")

    top = max(levels_available(TEMPLATES, cat))
    if state.level > top:
        st.info(f"You have cleared all the {CATEGORIES[cat].lower()} levels available so far (up to L{top}). More are on the way; keep practising at L{top}.")

    qs = ss.get("qs")
    if not qs or qs.get("cat") != cat:
        qs = _serve(store, rec, cat, chapters)
    q = qs["question"]

    # ---- the question
    st.divider()
    g3 = " · G3 only" if q.lo.endswith("*") else ""
    st.caption(f"Ch {q.chapter} {CHAPTERS[q.chapter]} · L{q.level}{g3}")
    st.markdown(q.stem)
    if q.figure:
        st.image(q.figure, caption="Fig. 1", width=480)

    phase = qs["phase"]
    answering = phase in ("answer", "retry")

    # ---- own-words answer first (explanation questions from L3 up)
    if qs.get("mode") == "write" and phase == "answer":
        st.markdown("**Answer in your own words.** Exact wording is not needed: the checker looks for the key ideas.")
        typed = st.text_area("Your answer", value=qs.get("typed", ""), height=110, key=f"typed_{qs['serial']}", label_visibility="collapsed",
                             placeholder="Write one or two sentences…")
        c1, c2 = st.columns([2, 1])
        with c1:
            if st.button("✔ Check my answer", type="primary", width="stretch", key=f"check_{qs['serial']}", disabled=len(typed.strip()) < 8):
                _check_typed(store, rec, typed)
                st.rerun()
        with c2:
            if st.button("Show the options instead", width="stretch", key=f"opts_{qs['serial']}"):
                qs["mode"] = "choose"
                st.rerun()
        if q.keypoints:
            st.caption(f"The checker is looking for {len(q.keypoints)} key idea{'s' if len(q.keypoints) > 1 else ''}.")
        return

    if qs.get("mode") == "write" and phase == "solved" and qs.get("typed"):
        with st.chat_message("user"):
            st.markdown(qs["typed"])
        for role, text in qs["chat"]:
            with st.chat_message("assistant"):
                st.markdown(text)

    for letter, text in q.options.items():
        disabled = (not answering) or (letter in qs["wrong"])
        label = f"**{letter}**&nbsp;&nbsp; {text}"
        if phase in ("solved", "revealed") and letter == q.key:
            label = f"✅ {label}"
        elif letter in qs["wrong"]:
            label = f"❌ {label}"
        if st.button(label, key=f"opt_{letter}_{qs['serial']}", width="stretch", disabled=disabled):
            _answer(store, rec, letter)
            st.rerun()

    # ---- banners
    if qs["event"] == "up":
        st.success(f"Level up! You are now on **L{state.level}**: {names[state.level]}")
    elif qs["event"] == "down":
        st.warning(f"Back to **L{state.level}** to consolidate. You will move up again after {UP_STREAK} correct in a row.")

    # ---- outcome panels
    if phase == "solved":
        if qs["retry_correct"]:
            st.info("Correct on the second try. Retries do not count towards your streak, so keep going.")
        else:
            st.success("Correct!")
        with st.expander("Show working"):
            for line in q.working:
                st.markdown(f"- {line}")
        if st.button("Next question ➜", type="primary", width="stretch", key=f"next_{qs['serial']}"):
            _serve(store, rec, cat, chapters)
            st.rerun()

    elif phase == "revealed":
        st.error(f"The correct answer is **{q.key}**: {q.options[q.key]}")
        st.markdown("**Working**")
        for line in q.working:
            st.markdown(f"- {line}")
        if st.button("Next question ➜", type="primary", width="stretch", key=f"next_{qs['serial']}"):
            _serve(store, rec, cat, chapters)
            st.rerun()

    elif phase == "hints":
        if qs.get("typed"):
            with st.chat_message("user"):
                st.markdown(qs["typed"])
        _tutor_panel(store, rec, qs, q)

    elif phase == "retry":
        st.info("Choose again." if not repeat_until_correct(cat, qs["level"]) else "Choose again. This question comes back until you get it right.")
        with st.expander("Tutor chat"):
            for role, text in qs["chat"]:
                with st.chat_message("assistant" if role == "tutor" else "user"):
                    st.markdown(text)


def _tutor_panel(store, rec, qs, q):
    st.markdown("##### 🧑‍🏫 Tutor")
    for role, text in qs["chat"]:
        with st.chat_message("assistant" if role == "tutor" else "user"):
            st.markdown(text)
    n = qs["hints_shown"]
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button(f"💡 Give me a hint ({min(n + 1, 3)}/3)", disabled=n >= 3, width="stretch", key=f"hint_{qs['serial']}_{n}"):
            qs["chat"].append(("student", "Give me a hint"))
            qs["chat"].append(("tutor", q.hints[n]))
            qs["hints_shown"] = n + 1
            qs["hints_used"] += 1
            store.touch(rec.key)
            st.rerun()
    with c2:
        if st.button("📐 Show formula", disabled=(not q.formula) or qs["formula_shown"], width="stretch", key=f"formula_{qs['serial']}"):
            qs["chat"].append(("student", "What is the formula?"))
            qs["chat"].append(("tutor", f"Use: **{q.formula}**. Now put the numbers from the question into it."))
            qs["formula_shown"] = True
            qs["hints_used"] += 1
            store.touch(rec.key)
            st.rerun()
    with c3:
        if st.button("🔁 Try again", type="primary", width="stretch", key=f"retry_{qs['serial']}"):
            if repeat_until_correct(qs["cat"], qs["level"]):
                qs["question"] = q.shuffled(_rng)        # same question, new order
                qs["wrong"] = set()
            qs["phase"] = "retry"
            qs["serial"] = _rng.randrange(1 << 30)
            store.touch(rec.key)
            st.rerun()
    if n == 0:
        st.caption("The tutor gives one hint at a time and never the answer. Ask for the formula if you are stuck on the first step.")
