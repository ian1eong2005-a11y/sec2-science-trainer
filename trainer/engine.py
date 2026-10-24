"""Adaptive rules. Pure Python, no Streamlit, fully covered by tests/test_engine.py.

Per student, per category (calc / explain):
  * 5 correct in a row at a level -> level + 1 (max 5); both streaks reset.
  * 3 wrong in a row at a level  -> level - 1 (min 1); both streaks reset.
  * A correct answer resets the wrong streak; a wrong answer resets the correct streak.
  * Only the FIRST attempt at a question counts. Retries never change streaks or accuracy.
  * Explanation L1 (recall): a wrong question is re-served until the student gets it right.
"""
from dataclasses import dataclass, field
from typing import Iterable, Optional

from .config import DOWN_STREAK, MAX_LEVEL, MIN_LEVEL, RECENT_AVOID, START_LEVEL, UP_STREAK


@dataclass
class CatState:
    level: int = START_LEVEL
    correct_streak: int = 0
    wrong_streak: int = 0
    attempted: int = 0      # first attempts only
    correct: int = 0        # first attempts answered correctly
    best_level: int = START_LEVEL

    @property
    def accuracy(self) -> Optional[float]:
        return None if self.attempted == 0 else self.correct / self.attempted


def apply_first_attempt(state: CatState, correct: bool) -> Optional[str]:
    """Update streaks and level for a first attempt. Returns 'up', 'down' or None."""
    state.attempted += 1
    if correct:
        state.correct += 1
        state.correct_streak += 1
        state.wrong_streak = 0
        if state.correct_streak >= UP_STREAK and state.level < MAX_LEVEL:
            state.level += 1
            state.best_level = max(state.best_level, state.level)
            state.correct_streak = 0
            state.wrong_streak = 0
            return "up"
        return None
    state.wrong_streak += 1
    state.correct_streak = 0
    if state.wrong_streak >= DOWN_STREAK:
        state.wrong_streak = 0
        if state.level > MIN_LEVEL:
            state.level -= 1
            state.correct_streak = 0
            return "down"
    return None


def apply_retry(state: CatState, correct: bool) -> None:
    """A retry of the same question: never touches streaks, level or accuracy."""
    return None


def repeat_until_correct(category: str, level: int) -> bool:
    """Teacher rule: explanation recall questions (L1) come back until answered correctly."""
    return category == "explain" and level == 1


def levels_available(templates: Iterable, category: str) -> list:
    return sorted({t.level for t in templates if t.category == category})


def select_template(templates: Iterable, category: str, level: int, chapters: Iterable[int], recent_ids: Iterable[str], rng):
    """Pick a template at the student's level from the chosen chapters, avoiding recently seen ids.
    Fewer than 3 candidates at the level -> borrow from the adjacent levels. Nothing nearby -> nearest level that has content."""
    chapters = set(chapters)
    recent = set(list(recent_ids)[-RECENT_AVOID:])
    pool_all = [t for t in templates if t.category == category and t.chapter in chapters]
    if not pool_all:
        pool_all = [t for t in templates if t.category == category]
    if not pool_all:
        raise ValueError(f"no templates for category {category!r}")

    def at(lv):
        return [t for t in pool_all if t.level == lv]

    pool = at(level)
    if len(pool) < 3:
        pool = pool + at(level + 1) + at(level - 1)
    if not pool:
        nearest = sorted({t.level for t in pool_all}, key=lambda lv: (abs(lv - level), -lv))[0]
        pool = at(nearest)
    fresh = [t for t in pool if t.id not in recent]
    return rng.choice(fresh or pool)
