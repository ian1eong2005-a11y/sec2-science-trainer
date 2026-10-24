"""Shared building blocks for question templates."""
import math
import random
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional

LETTERS = "ABCD"


@dataclass
class Question:
    template_id: str
    category: str          # calc | explain
    chapter: int
    level: int
    seed: int
    stem: str              # markdown
    options: Dict[str, str]
    key: str
    working: List[str]
    hints: List[str]
    misconceptions: Dict[str, str]   # wrong letter -> why that answer is tempting
    formula: Optional[str] = None
    figure: Optional[bytes] = None
    lo: str = ""
    keypoints: Optional[list] = None   # explanation items: [{"label": idea, "any": [phrasings...]}] for typed answers

    def shuffled(self, rng: random.Random) -> "Question":
        """Same question, options in a new order (used when a recall question is re-served)."""
        items = list(self.options.items())
        rng.shuffle(items)
        new_opts, new_mis, new_key = {}, {}, None
        for new_letter, (old_letter, text) in zip(LETTERS, items):
            new_opts[new_letter] = text
            if old_letter == self.key:
                new_key = new_letter
            elif old_letter in self.misconceptions:
                new_mis[new_letter] = self.misconceptions[old_letter]
        return Question(**{**self.__dict__, "options": new_opts, "key": new_key, "misconceptions": new_mis})


@dataclass
class Template:
    id: str
    category: str
    chapter: int
    level: int
    lo: str
    make: Callable[[int], Question]


TEMPLATES: List[Template] = []


def template(id: str, chapter: int, level: int, lo: str, category: str = "calc"):
    """Register a generator. The wrapped function takes a random.Random and returns a dict with
    stem, options, key, working, hints, misconceptions and optionally formula, figure."""
    def deco(fn):
        def make(seed: int) -> Question:
            rng = random.Random(seed)
            fields = fn(rng)
            return Question(template_id=id, category=category, chapter=chapter, level=level, seed=seed, lo=lo, **fields)
        TEMPLATES.append(Template(id=id, category=category, chapter=chapter, level=level, lo=lo, make=make))
        return make
    return deco


# ------------------------------------------------------------------ numbers
def fmt(x, sf: Optional[int] = 3, dp: Optional[int] = None) -> str:
    """Plain number string: no float noise, 3 s.f. by default, or fixed decimals with dp."""
    if dp is not None:
        return f"{x:.{dp}f}"
    if sf:
        x = float(f"{x:.{sf}g}")
    s = f"{x:.6f}".rstrip("0").rstrip(".")
    return s if s not in ("", "-0") else "0"


def numeric_options(rng: random.Random, correct: float, wrongs, unit: str = "", sf: int = 3, dp: Optional[int] = None):
    """Four shuffled options for a numeric MCQ.
    wrongs: list of (value, reason). Duplicates (after formatting) and non-positive values are dropped; the list is padded
    with near values if needed. Returns (options dict, key letter, misconceptions dict)."""
    def text(v):
        return f"{fmt(v, sf, dp)} {unit}".strip()

    chosen = [(text(correct), None)]
    seen = {text(correct)}
    for v, reason in wrongs:
        if v is None or not math.isfinite(v) or v <= 0:
            continue
        t = text(v)
        if t in seen:
            continue
        seen.add(t)
        chosen.append((t, reason))
        if len(chosen) == 4:
            break
    for mult in (2, 0.5, 10, 0.1, 1.5, 4, 0.25, 3):
        if len(chosen) == 4:
            break
        t = text(correct * mult)
        if t not in seen:
            seen.add(t)
            chosen.append((t, "This value does not come from the correct formula with the numbers given."))
    rng.shuffle(chosen)
    options, misconceptions, key = {}, {}, None
    for letter, (t, reason) in zip(LETTERS, chosen):
        options[letter] = t
        if reason is None:
            key = letter
        else:
            misconceptions[letter] = reason
    return options, key, misconceptions


def text_options(rng: random.Random, correct: str, wrongs: Dict[str, str]):
    """Four shuffled options for a word-answer MCQ. wrongs: option text -> why it is wrong."""
    items = [(correct, None)] + list(wrongs.items())[:3]
    rng.shuffle(items)
    options, misconceptions, key = {}, {}, None
    for letter, (t, reason) in zip(LETTERS, items):
        options[letter] = t
        if reason is None:
            key = letter
        else:
            misconceptions[letter] = reason
    return options, key, misconceptions


def nice(rng: random.Random, *choices):
    return rng.choice(choices)


def pick(rng: random.Random, seq):
    """rng.choice for lists (keeps the call sites short)."""
    return rng.choice(list(seq))


# ------------------------------------------------------------------ explanation items
def register_explain(items, chapter: int):
    """Register fixed / variant-based Explanation MCQs from dicts.

    item keys: id, level, lo, stem, correct, wrongs {text: why wrong}, hints [3], optional fig (callable rng -> PNG bytes),
    optional working [..], optional variants [ {stem, correct, wrongs, fig?} ... ] - one variant is picked per serve so
    the question changes between attempts. Options are always shuffled."""
    for item in items:
        _register_one(item, chapter)


def _register_one(item, chapter):
    @template(item["id"], chapter=chapter, level=item["level"], lo=item.get("lo", ""), category="explain")
    def make(rng, item=item):
        v = rng.choice(item["variants"]) if item.get("variants") else item
        stem = v.get("stem", item.get("stem"))
        correct = v.get("correct", item.get("correct"))
        wrongs = v.get("wrongs", item.get("wrongs"))
        fig = v.get("fig", item.get("fig"))
        opts, key, mis = text_options(rng, correct, wrongs)
        return dict(stem=stem, options=opts, key=key, misconceptions=mis, hints=v.get("hints", item["hints"]),
                    working=v.get("working", item.get("working", [f"Correct answer: **{correct}**"])),
                    formula=item.get("formula"), figure=fig(rng) if callable(fig) else fig,
                    keypoints=v.get("keypoints", item.get("keypoints")))


def md_table(headers, rows):
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(c) for c in r) + " |")
    return "\n".join(out)
