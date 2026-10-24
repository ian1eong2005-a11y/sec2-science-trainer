"""Constants for the Sec 2 Science adaptive trainer. Change class lists and rules here only."""

APP_TITLE = "Sec 2 Science Trainer"
SCHOOL = "Queenstown Secondary School"

# Login dropdown, grouped by level. To add a class, add its name to the right list.
CLASSES = {
    "Sec 2": ["2TG1", "2TG2", "2TG3", "2TG4", "2TG5", "2TG6", "2TG7", "2TG8", "2TG9"],
}
CLASS_LIST = [c for group in CLASSES.values() for c in group]

# Lower Secondary Science (2021 syllabus, G2/G3), Sec 2 chapters as taught at QTSS.
CHAPTERS = {
    9: "Application of Forces and Transfer of Energy",
    10: "Transfer of Heat Energy and its Effects",
    11: "Chemical Changes",
    12: "Interactions within Ecosystems",
    13: "Electrical Systems",
    14: "Human Digestive System",
    15: "Transport Systems in Living Things",
    16: "Human Sexual Reproductive System",
}

CATEGORIES = {
    "calc": "Calculation & data",
    "explain": "Explanation",
}

LEVEL_NAMES = {
    1: "L1 - one formula or one reading",
    2: "L2 - one conversion, reading or rearrangement",
    3: "L3 - two steps, with a figure or table",
    4: "L4 - graphs and data interpretation",
    5: "L5 - multi-step, unfamiliar context or a trap",
}
EXPLAIN_LEVEL_NAMES = {
    1: "L1 - recall and definitions",
    2: "L2 - identify and classify",
    3: "L3 - apply a concept",
    4: "L4 - explain with reasoning",
    5: "L5 - evaluate and predict",
}

# Adaptive rules (confirmed by the teacher, 24 Oct 2026)
UP_STREAK = 5          # correct in a row at a level -> level + 1
DOWN_STREAK = 3        # wrong in a row at a level -> level - 1
MIN_LEVEL, MAX_LEVEL = 1, 5
START_LEVEL = 1
RECENT_AVOID = 10      # do not repeat any of the last N template ids

ONLINE_SECONDS = 120   # "online" on the dashboard if active within this many seconds
DASHBOARD_REFRESH_S = 5

DEFAULT_TEACHER_PASSWORD = "science"   # used only when no TEACHER_PASSWORD secret / env var is set

G = 10.0               # N/kg, as used in school papers
