import random

import pytest

from trainer.config import DOWN_STREAK, MAX_LEVEL, MIN_LEVEL, UP_STREAK
from trainer.engine import CatState, apply_first_attempt, apply_retry, levels_available, repeat_until_correct, select_template


def run(state, pattern):
    events = []
    for ch in pattern:
        events.append(apply_first_attempt(state, ch == "c"))
    return events


def test_level_up_after_exactly_five_correct():
    s = CatState()
    ev = run(s, "c" * (UP_STREAK - 1))
    assert s.level == 1 and all(e is None for e in ev)
    assert apply_first_attempt(s, True) == "up"
    assert s.level == 2 and s.correct_streak == 0 and s.wrong_streak == 0


def test_level_down_after_exactly_three_wrong():
    s = CatState(level=3)
    ev = run(s, "w" * (DOWN_STREAK - 1))
    assert s.level == 3 and all(e is None for e in ev)
    assert apply_first_attempt(s, False) == "down"
    assert s.level == 2 and s.correct_streak == 0 and s.wrong_streak == 0


def test_wrong_resets_correct_streak_and_vice_versa():
    s = CatState()
    run(s, "cccc")
    assert s.correct_streak == 4
    apply_first_attempt(s, False)
    assert s.correct_streak == 0 and s.wrong_streak == 1
    apply_first_attempt(s, True)
    assert s.wrong_streak == 0 and s.correct_streak == 1


def test_interleaved_never_moves():
    s = CatState(level=3)
    run(s, "ccwwccwwccccwwcccc")
    assert s.level == 3


def test_floor_and_ceiling():
    s = CatState(level=MIN_LEVEL)
    assert run(s, "w" * 9) == [None] * 9
    assert s.level == MIN_LEVEL
    t = CatState(level=MAX_LEVEL)
    assert run(t, "c" * 12) == [None] * 12
    assert t.level == MAX_LEVEL and t.correct_streak == 12


def test_climb_and_fall():
    s = CatState()
    run(s, "c" * 10)
    assert s.level == 3
    run(s, "w" * 3)
    assert s.level == 2
    run(s, "w" * 3)
    assert s.level == 1


def test_accuracy_counts_first_attempts_only():
    s = CatState()
    run(s, "cwc")
    apply_retry(s, True)
    apply_retry(s, False)
    assert s.attempted == 3 and s.correct == 2 and s.accuracy == pytest.approx(2 / 3)
    assert s.level == 1 and s.correct_streak == 1


def test_repeat_rule_only_for_explain_l1():
    assert repeat_until_correct("explain", 1)
    assert not repeat_until_correct("explain", 2)
    assert not repeat_until_correct("calc", 1)


class T:
    def __init__(self, id, category, chapter, level):
        self.id, self.category, self.chapter, self.level = id, category, chapter, level


def test_select_template_prefers_level_and_avoids_recent():
    tpls = [T(f"a{i}", "calc", 1, 2) for i in range(5)] + [T("b1", "calc", 1, 3), T("x1", "calc", 2, 2)]
    rng = random.Random(1)
    picks = {select_template(tpls, "calc", 2, [1], [], rng).id for _ in range(50)}
    assert picks <= {f"a{i}" for i in range(5)}
    picks = {select_template(tpls, "calc", 2, [1], ["a0", "a1", "a2", "a3"], rng).id for _ in range(50)}
    assert picks == {"a4"}


def test_select_template_borrows_when_thin():
    tpls = [T("l2", "calc", 1, 2), T("l3a", "calc", 1, 3), T("l3b", "calc", 1, 3), T("l4", "calc", 1, 4)]
    rng = random.Random(2)
    picks = {select_template(tpls, "calc", 3, [1], [], rng).id for _ in range(60)}
    assert picks == {"l2", "l3a", "l3b", "l4"}          # fewer than 3 at L3 -> neighbours join the pool


def test_select_template_falls_back_to_nearest_level_and_any_chapter():
    tpls = [T("r1", "explain", 1, 1), T("r2", "explain", 2, 2)]
    rng = random.Random(3)
    assert select_template(tpls, "explain", 5, [1, 2], [], rng).id == "r2"     # nearest available below
    assert select_template(tpls, "explain", 1, [9], [], rng).id in {"r1", "r2"}  # no content in chapter 9 -> any chapter
    assert levels_available(tpls, "explain") == [1, 2]
