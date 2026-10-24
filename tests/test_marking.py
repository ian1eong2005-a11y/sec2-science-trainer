"""Typed answers are marked on key ideas, not exact words."""
from trainer.marking import mark_answer, phrase_in, tokens

CONVECTION = [
    {"label": "the air near the heater warms up", "any": ["air is heated", "air warms", "warm air", "heated air", "hot air"]},
    {"label": "warmer air is less dense", "any": ["less dense", "lower density", "lighter"]},
    {"label": "the less dense air rises", "any": ["rises", "goes up", "moves up", "floats up"]},
    {"label": "cooler, denser air sinks to replace it", "any": ["cooler air sinks", "cold air sinks", "denser air sinks", "cooler air moves in", "cold air replaces", "cooler air takes its place"]},
]


def test_rephrased_answers_are_accepted():
    for text in [
        "The air near the heater is heated, becomes less dense and rises. Cooler denser air sinks to take its place.",
        "Hot air has a lower density so it goes up, and the cold air sinks down to replace it.",
        "heated air is lighter and floats up; colder air moves in underneath and sinks",
    ]:
        hits, total, missing, ok = mark_answer(text, CONVECTION, "")
        assert ok, (text, missing)


def test_missing_ideas_are_reported():
    hits, total, missing, ok = mark_answer("The warm air rises.", CONVECTION, "")
    assert not ok and hits == 2 and total == 4
    assert "warmer air is less dense" in missing and "cooler, denser air sinks to replace it" in missing


def test_fallback_uses_correct_option_text():
    correct = "It carries blood away from the heart."
    assert mark_answer("an artery carries the blood away from the heart", None, correct)[3]
    assert mark_answer("it is a tube in the body", None, correct)[3] is False


def test_synonyms_and_stemming():
    ans = tokens("The hotter part expands, becoming lighter, so it ascends quickly")
    assert phrase_in("warm expand", ans)
    assert phrase_in("less dense", ans)
    assert phrase_in("rises fast", ans)


def test_order_free_matching():
    ans = tokens("because its concentration is higher outside the cell, oxygen diffuses in")
    assert phrase_in("diffuses from higher concentration", ans)
