"""End-to-end through Streamlit's AppTest: login, answer, tutor, retry, level up, recall repeat rule, dashboard row."""
import pathlib

import pytest
from streamlit.testing.v1 import AppTest

APP = str(pathlib.Path(__file__).resolve().parents[1] / "app.py")


def login(at, name="Amy Tan", cls="Sec 2 · 2TG1"):
    at.text_input[0].input(name)
    at.selectbox[0].select(cls)
    next(b for b in at.button if b.label == "Start").click()
    at.run()
    assert at.session_state["student_key"] == (name.casefold(), cls.split(" · ")[1])


def option_buttons(at):
    return [b for b in at.button if b.key and b.key.startswith("opt_")]


def click_option(at, letter):
    b = next(b for b in option_buttons(at) if b.key.startswith(f"opt_{letter}_"))
    b.click()
    at.run()


def current_question(at):
    return at.session_state["qs"]["question"]


@pytest.fixture
def at():
    app = AppTest.from_file(APP, default_timeout=60)
    app.run()
    assert not app.exception
    return app


def test_login_and_level_up_after_five_correct(at):
    login(at)
    assert "qs" in at.session_state
    for i in range(4):
        q = current_question(at)
        click_option(at, q.key)
        assert any("Correct!" in s.value for s in at.success), f"attempt {i}"
        next_btn = next(b for b in at.button if b.key and b.key.startswith("next_"))
        next_btn.click()
        at.run()
    q = current_question(at)
    click_option(at, q.key)
    assert any("Level up" in s.value for s in at.success)
    assert at.session_state["qs"]["event"] == "up"
    from trainer.store import get_store
    rec = get_store().get(at.session_state["student_key"])
    assert rec.states["calc"].level == 2 and rec.states["calc"].correct_streak == 0


def test_wrong_answer_opens_tutor_and_retry_gives_no_credit(at):
    login(at, name="Ben Lim")
    q = current_question(at)
    wrong = next(L for L in "ABCD" if L != q.key)
    click_option(at, wrong)
    qs = at.session_state["qs"]
    assert qs["phase"] == "hints" and qs["chat"][0][0] == "tutor" and wrong in qs["chat"][0][1]
    # hints never contain the correct option text
    for h in q.hints:
        assert q.options[q.key] not in h
    hint = next(b for b in at.button if b.key and b.key.startswith("hint_"))
    hint.click(); at.run()
    assert at.session_state["qs"]["hints_shown"] == 1
    retry = next(b for b in at.button if b.key and b.key.startswith("retry_"))
    retry.click(); at.run()
    assert at.session_state["qs"]["phase"] == "retry"
    # the wrong option is now disabled
    assert next(b for b in option_buttons(at) if b.key.startswith(f"opt_{wrong}_")).disabled
    click_option(at, q.key)
    assert at.session_state["qs"]["phase"] == "solved" and at.session_state["qs"]["retry_correct"]
    from trainer.store import get_store
    st_ = get_store().get(at.session_state["student_key"]).states["calc"]
    assert st_.correct_streak == 0 and st_.wrong_streak == 1 and st_.attempted == 1 and st_.correct == 0


def test_recall_l1_repeats_until_correct(at):
    login(at, name="Cara Ng")
    at.radio[0].set_value("explain"); at.run()
    q = current_question(at)
    assert q.category == "explain" and q.level == 1
    wrong = next(L for L in "ABCD" if L != q.key)
    click_option(at, wrong)
    retry = next(b for b in at.button if b.key and b.key.startswith("retry_"))
    retry.click(); at.run()
    q2 = current_question(at)
    assert q2.template_id == q.template_id                      # same question comes back
    assert q2.options[q2.key] == q.options[q.key]
    wrong2 = next(L for L in "ABCD" if L != q2.key)
    click_option(at, wrong2)
    assert at.session_state["qs"]["phase"] == "hints"           # still not released
    retry = next(b for b in at.button if b.key and b.key.startswith("retry_"))
    retry.click(); at.run()
    q3 = current_question(at)
    click_option(at, q3.key)
    assert at.session_state["qs"]["phase"] == "solved"


def test_teacher_dashboard_lists_students(at):
    login(at, name="Dev Raj")
    from trainer.store import get_store
    assert any(r["Name"] == "Dev Raj" and r["_online"] for r in get_store().rows())
    at.session_state["view"] = "teacher"
    at.run()
    assert at.text_input[0].label == "Teacher password"
    at.text_input[0].input("science")
    next(b for b in at.button if b.label == "Open dashboard").click(); at.run()
    assert at.session_state["teacher_ok"]
    assert not at.exception
