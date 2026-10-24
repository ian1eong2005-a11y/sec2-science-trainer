# Sec 2 Science Trainer

Adaptive self-study MCQ trainer for Sec 2 Lower Secondary Science (2021 G2/G3 syllabus), Chapters 9–16:
Application of Forces and Transfer of Energy · Transfer of Heat Energy · Chemical Changes · Interactions within Ecosystems ·
Electrical Systems · Human Digestive System · Transport Systems in Living Things · Human Sexual Reproductive System.
Streamlit app, no database. Built from the G3 Physics trainer (same engine, new content).

## How it works

- Students log in with **name + class** (no password). Teacher view is password protected.
- Two categories: **Calculation & data** (200 parametrised templates: numbers change every serve, diagrams drawn to match)
  and **Explanation** (400 items adapted from the chapter worksheets and tests; many have several variants, options always shuffled).
- Each chapter has **15 templates per level** (5 calculation + 10 explanation at L1–L5), 600 in all.
- **Own-words answers:** explanation questions from L3 up are first answered in the student's own words. A scripted checker
  (`trainer/marking.py`, no LLM) looks for the question's **key ideas**, accepting rephrasing: synonyms, different word order,
  different word endings. All ideas present → correct; otherwise the tutor names the missing ideas and the student retries with
  the options (no streak credit, as for any retry). Students can also skip straight to the options.
- **5 correct in a row → level up. 3 wrong in a row → level down.** Everyone starts at L1.
- A wrong answer opens the scripted **tutor**: a message about the chosen option, up to 3 hints, the formula / key fact on request,
  then one retry (correct retries never count towards the streak). Explanation L1 questions come back, reshuffled, until answered correctly.
- **Every question has a diagram or a table.**
- **Teacher dashboard** (sidebar → Teacher, or `?teacher=1`): who is online, levels, streaks, accuracy, last 20 attempts,
  reset / clear / CSV. Refreshes every 5 s. Data lives in memory only and disappears when the app restarts.
- G3-only content is tagged "G3 only" under the question (its `lo` code ends in `*`).

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Default local teacher password is `science`. Set `TEACHER_PASSWORD` as an environment variable or in `.streamlit/secrets.toml` to change it.

## Deploy on Streamlit Community Cloud

1. Push this folder to a GitHub repo.
2. share.streamlit.io → **Create app** → pick the repo, branch `main`, main file `app.py`.
3. Advanced settings → **Secrets**:
   ```toml
   TEACHER_PASSWORD = "choose-something"
   ```
4. Deploy. Share the `*.streamlit.app` URL (or a QR code) with students.

Every push to `main` redeploys automatically. Live data is cleared on each redeploy.

## Tests

```bash
python -m pytest -q
```

`tests/test_engine.py` covers the level rules; `tests/test_content.py` checks the inventory (10 per level per chapter) and builds
every template with 20 seeds (four distinct options, key present, a misconception message for every wrong option, three hints,
a figure or a table, a PNG figure whenever the stem says "Fig. 1", and no hint that contains the answer); `tests/test_app.py` runs the
app end to end.

## Adding a question

One template = one Python function (calculation / data) or one dict (explanation), in `trainer/content/chNN.py`.

Calculation / data: copy any existing one.

```python
@template("c10_my_question", chapter=10, level=2, lo="10.3")
def my_question(rng):
    T0 = nice(rng, 20, 25, 30)
    ...
    opts, key, mis = numeric_options(rng, answer, [(wrong1, "why a student gets this"), ...], unit="°C")
    return dict(stem=..., options=opts, key=key, misconceptions=mis, formula=..., working=[...], hints=[h1, h2, h3],
                figure=S.bar_chart(...))          # or put a markdown table in the stem
```

Explanation: add a dict to the chapter's `EXPLAIN` list (`chNN.py` or `chNNb.py`).

```python
dict(id="e10_my_item", level=3, lo="10.4",
     stem="...", correct="...", wrongs={"wrong text": "why it is wrong", ...},
     hints=[h1, h2, h3], fig=lambda rng: S.room_heater("floor"),   # optional variants=[{stem, correct, wrongs, fig?}, ...]
     keypoints=[KP("warmer air is less dense", "less dense", "lower density", "lighter"),
                KP("so it rises", "rise", "goes up")]),              # for own-words answers: each idea = label + accepted phrasings
```

A key idea is credited when ANY of its phrasings is found in the answer (all the phrasing's content words present, any order,
any word endings; a 5+ letter word also matches a longer word that starts with it). Items without `keypoints` fall back to
matching most of the correct option's content words. `tests/test_marking.py` shows what is accepted.

Diagram drawers live in `trainer/sketches.py` (charts, food webs, circuits, pH scale, thermometer, calendar, …) and `trainer/figs.py`
(graphs, force diagrams, blocks). Keep the per-level counts at 5 + 5 per chapter (or change `PER_LEVEL` in `tests/test_content.py`),
then run the tests.

## Adding a class

Edit the `CLASSES` dict in `trainer/config.py`, e.g. add `"2TG10"` to the `"Sec 2"` list.
