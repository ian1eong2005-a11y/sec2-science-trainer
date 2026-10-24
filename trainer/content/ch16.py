"""Ch 16 Human Sexual Reproductive System: 25 calculation / data templates and 25 explanation items.
lo codes: 16.1 fertilisation and heredity, 16.2 puberty, 16.3 parts and functions, 16.4 menstrual cycle, 16.5 birth control,
16.6 STIs, 16.7 substance abuse in pregnancy, 16.8* variation and world population (G3)."""
import datetime

from .. import figs, sketches as S
from .base import fmt, md_table, nice, numeric_options, pick, register_explain, template, text_options

MONTHS = [("January", 31), ("March", 31), ("May", 31), ("July", 31), ("August", 31), ("October", 31)]


def _cal_fig(month, days, first_wd, start_day, period_len=5, ovul=None, extra=None):
    shaded = set(range(start_day, min(start_day + period_len, days + 1)))
    circled = {}
    if ovul and ovul <= days:
        circled[ovul] = "ovulation"
    if extra:
        circled.update(extra)
    return S.month_calendar(month, days, first_wd, shaded=shaded, circled=circled)


# ================================================================ CALCULATION / DATA
# ---------------------------------------------------------------- L1
@template("c16_cycle_bar_ovulation_day", chapter=16, level=1, lo="16.4")
def cycle_bar_ovulation_day(rng):
    period = nice(rng, 4, 5, 6)
    opts, key, mis = numeric_options(rng, 14, [
        (period, "That is the last day of menstruation, not ovulation."),
        (28, "Day 28 is the end of the cycle."),
        (7, "Ovulation is about half-way through the 28-day cycle."),
    ], unit="", sf=2)
    return dict(
        stem="Fig. 1 shows a 28-day menstrual cycle. On which day of the cycle does ovulation (release of an egg) usually occur?",
        figure=S.cycle_bar(period_days=period, ovulation=14),
        options=opts, key=key, misconceptions=mis,
        formula="in a 28-day cycle, ovulation is around day 14",
        working=["the arrow marked 'ovulation' is at **day 14**"],
        hints=["Find the arrow labelled ovulation in Fig. 1.", "Read the day number below it.", "It is about half-way through the cycle."],
    )


@template("c16_days_of_menstruation", chapter=16, level=1, lo="16.4")
def days_of_menstruation(rng):
    start = nice(rng, 3, 5, 8, 10, 12)
    length = nice(rng, 4, 5, 6)
    end = start + length - 1
    opts, key, mis = numeric_options(rng, length, [
        (end - start, "You subtracted the dates. Both the first and last day count, so add 1."),
        (end, "That is the date it ended, not the number of days."),
        (length + 2, "Count the days from the first to the last inclusive."),
    ], unit="days", sf=2)
    return dict(
        stem=f"A girl's period started on **{start} August** and ended on **{end} August**. Fig. 1 shows the month.\n\nFor how many days did menstruation last?",
        figure=_cal_fig("August", 31, 5, start, period_len=length),
        options=opts, key=key, misconceptions=mis,
        formula="number of days = last day − first day + 1",
        working=[f"{end} − {start} + 1 = **{length} days**"],
        hints=["Count the shaded days on the calendar.", "Include both the first and the last day.", f"From {start} to {end} inclusive."],
    )


@template("c16_puberty_table_read", chapter=16, level=1, lo="16.2")
def puberty_table_read(rng):
    rows = [["growth of pubic hair", "both"], ["voice deepens", "boys"], ["breasts develop", "girls"], ["menstruation begins", "girls"], ["shoulders broaden", "boys"], ["rapid increase in height", "both"]]
    chosen = rng.sample(rows, 5)
    ask = pick(rng, ["boys only", "girls only", "both boys and girls"])
    k = {"boys only": "boys", "girls only": "girls", "both boys and girls": "both"}[ask]
    n = sum(1 for r in chosen if r[1] == k)
    if n == 0:
        chosen[0] = [r for r in rows if r[1] == k][0]
        n = 1
    opts, key, mis = numeric_options(rng, n, [
        (5 - n, f"That is the number of changes NOT in the '{ask}' group."),
        (n + 1, "Count only the rows that match."),
        (5, "Not every change applies to this group."),
    ], unit="", sf=1)
    return dict(
        stem=f"The table shows changes at puberty.\n\n{md_table(['Change', 'Happens in'], chosen)}\n\nHow many of these changes happen in **{ask}**?",
        options=opts, key=key, misconceptions=mis,
        formula="count the rows that match the group",
        working=[f"rows marked '{k}': {n} → **{n}**"],
        hints=["Read the 'happens in' column.", f"Count the rows that say '{k}'.", "Check each row once."],
    )


@template("c16_bar_chart_sti_cases", chapter=16, level=1, lo="16.6")
def bar_chart_sti_cases(rng):
    stis = ["gonorrhoea", "syphilis", "HIV"]
    vals = [nice(rng, 1200, 1500, 1800), nice(rng, 300, 400, 500), nice(rng, 200, 250, 300)]
    i = rng.randint(0, 2)
    opts, key, mis = numeric_options(rng, vals[i], [(v, f"That is the bar for {s}.") for j, (s, v) in enumerate(zip(stis, vals)) if j != i], unit="cases", sf=3)
    return dict(
        stem=f"Fig. 1 shows the number of new cases of three sexually transmitted infections (STIs) reported in a country in one year. How many new cases of **{stis[i]}** were reported?",
        figure=S.bar_chart(stis, vals, "new cases", ymax=2000, ystep=500),
        options=opts, key=key, misconceptions=mis,
        formula="read the bar",
        working=[f"{stis[i]} → **{vals[i]} cases**"],
        hints=[f"Find the bar for {stis[i]}.", "Read its top against the scale.", "Each small square is 100 cases."],
    )


@template("c16_sperm_egg_lifespan_table", chapter=16, level=1, lo="16.4")
def sperm_egg_lifespan_table(rng):
    sperm = nice(rng, 3, 4, 5)
    egg = 1
    opts, key, mis = numeric_options(rng, sperm + egg, [
        (sperm, "That is how long the sperm live. Add the day the egg can also be fertilised."),
        (sperm - egg, "You subtracted. The fertile window covers the days the sperm can wait PLUS the day the egg lives."),
        (sperm * 2, "Check: sperm days + egg day."),
    ], unit="days", sf=2)
    return dict(
        stem=f"The table shows how long sex cells can survive in the female body.\n\n{md_table(['Cell', 'Survival time'], [['sperm', f'up to {sperm} days'], ['egg', f'about {egg} day after ovulation']])}\n\nFor roughly how many days around ovulation could sexual intercourse lead to pregnancy?",
        options=opts, key=key, misconceptions=mis,
        formula="fertile window ≈ days sperm survive before ovulation + day(s) the egg survives after",
        working=[f"{sperm} days (sperm waiting) + {egg} day (egg) = **{sperm + egg} days**"],
        hints=["Sperm that arrive before ovulation can wait for the egg.", "The egg can be fertilised for about a day after release.", "Add the two periods."],
    )


# ---------------------------------------------------------------- L2
@template("c16_ovulation_date", chapter=16, level=2, lo="16.4")
def ovulation_date(rng):
    month, days = pick(rng, MONTHS)
    start = rng.randint(1, 12)
    ovul = start + 13
    opts, key, mis = numeric_options(rng, ovul, [
        (start + 14, "Day 1 is the first day of bleeding, so day 14 is 13 days later, not 14."),
        (start + 7, "Ovulation is about day 14, not day 8."),
        (start + 27, "That is the start of the NEXT period (day 28 is the end of the cycle)."),
    ], unit=month, sf=2)
    return dict(
        stem=f"A woman's period starts on **{start} {month}**. Her cycle is a regular 28 days and ovulation occurs on day 14. Fig. 1 shows the month with the period shaded. On what date does ovulation occur?",
        figure=_cal_fig(month, days, rng.randint(0, 6), start),
        options=opts, key=key, misconceptions=mis,
        formula="day 1 = first day of bleeding; ovulation on day 14 = start date + 13",
        working=[f"{start} {month} is day 1", f"day 14 = {start} + 13 = **{ovul} {month}**"],
        hints=["Day 1 is the first day of bleeding.", "Day 14 is 13 days after day 1.", f"{start} + 13."],
    )


@template("c16_next_period_date", chapter=16, level=2, lo="16.4")
def next_period_date(rng):
    month, days = pick(rng, MONTHS)
    start = rng.randint(1, 3)
    nxt = start + 28
    opts, key, mis = numeric_options(rng, nxt, [
        (start + 27, "Day 28 is the LAST day of this cycle; the next period starts on the day after, day 29."),
        (start + 14, "That is about ovulation, not the next period."),
        (start + 30, "The cycle is 28 days, not 30."),
    ], unit=month, sf=2)
    return dict(
        stem=f"A woman's period starts on **{start} {month}** and her cycle is a regular 28 days. Fig. 1 shows the month. On what date will her **next** period start?",
        figure=_cal_fig(month, days, rng.randint(0, 6), start, ovul=start + 13),
        options=opts, key=key, misconceptions=mis,
        formula="next period = start date + 28 days (day 29 of this cycle = day 1 of the next)",
        working=[f"{start} + 28 = **{nxt} {month}**"],
        hints=["A 28-day cycle means the next day 1 is 28 days after this one.", "Add 28 to the start date.", f"{start} + 28."],
    )


@template("c16_cycle_phase_identify", chapter=16, level=2, lo="16.4")
def cycle_phase_identify(rng):
    day = pick(rng, [3, 8, 14, 20, 26])
    phases = {3: "menstruation: the uterus lining is breaking down", 8: "the uterus lining is thickening again", 14: "ovulation: an egg is released from an ovary", 20: "the lining stays thick, ready for a fertilised egg", 26: "the lining stays thick, ready for a fertilised egg"}
    correct = phases[day]
    others = [p for d, p in phases.items() if p != correct]
    others = list(dict.fromkeys(others))
    wrongs = {}
    for o in others[:3]:
        wrongs[o] = f"That happens on a different part of the cycle, not around day {day}."
    opts, key, mis = text_options(rng, correct, wrongs)
    return dict(
        stem=f"Fig. 1 shows a 28-day menstrual cycle. What is happening on **day {day}**?",
        figure=S.cycle_bar(marks={day: f"day {day}"}),
        options=opts, key=key, misconceptions=mis,
        formula="days 1–5 menstruation; days 6–13 lining thickens; day 14 ovulation; days 15–28 lining stays thick",
        working=[f"day {day} → **{correct}**"],
        hints=["Find the day on the bar in Fig. 1.", "Is it in the shaded part, near the ovulation arrow, or after it?", "Match that to the stage of the cycle."],
    )


@template("c16_birth_weight_table", chapter=16, level=2, lo="16.7")
def birth_weight_table(rng):
    non = nice(rng, 3.3, 3.4, 3.5)
    diff = nice(rng, 0.2, 0.3, 0.4)
    smk = round(non - diff, 1)
    pct = round(diff / non * 100)
    opts, key, mis = numeric_options(rng, pct, [
        (diff, "That is the difference in kg, not the percentage."),
        (round(diff / smk * 100), "Compare with the NON-smokers' value (the normal)."),
        (pct * 2, "Check: difference ÷ non-smokers' value × 100."),
    ], unit="%", sf=2)
    return dict(
        stem=f"The table shows the average birth mass of babies.\n\n{md_table(['Mother', 'Average birth mass / kg'], [['non-smoker', fmt(non)], ['smoked during pregnancy', fmt(smk)]])}\n\nBy what percentage is the average birth mass lower for babies of mothers who smoked?",
        options=opts, key=key, misconceptions=mis,
        formula="percentage lower = difference ÷ non-smoker value × 100",
        working=[f"difference = {fmt(non)} − {fmt(smk)} = {fmt(diff)} kg", f"{fmt(diff)} ÷ {fmt(non)} × 100 = **{pct}%**"],
        hints=["Find the difference between the two averages.", "Compare it with the non-smokers' average.", f"{fmt(diff)} ÷ {fmt(non)} × 100."],
    )


@template("c16_population_graph_read", chapter=16, level=2, lo="16.8*")
def population_graph_read(rng):
    pts = [(1800, 1.0), (1850, 1.3), (1900, 1.6), (1950, 2.5), (1975, 4.1), (2000, 6.1), (2025, 8.1)]
    yr = pick(rng, [1900, 1950, 1975, 2000])
    ans = dict(pts)[yr]
    opts, key, mis = numeric_options(rng, ans, [
        (dict(pts)[[p[0] for p in pts][[p[0] for p in pts].index(yr) + 1]], "You read the value for a later year."),
        (dict(pts)[[p[0] for p in pts][[p[0] for p in pts].index(yr) - 1]], "You read the value for an earlier year."),
        (8.1, "That is the population in 2025, not in the year asked."),
    ], unit="billion", sf=2)
    return dict(
        stem=f"Fig. 1 shows the world population since 1800. What was the world population in **{yr}**?",
        figure=S.xy_graph([("world population", pts)], "year", "population / billions", 2050, 10, 50, 2, xmin=1800, legend=False, markers=True),
        options=opts, key=key, misconceptions=mis,
        formula="read the graph at the given year",
        working=[f"{yr} → **{fmt(ans)} billion**"],
        hints=["Find the year on the horizontal axis.", "Go up to the line and across.", "Each small square on the vertical axis is 0.4 billion."],
    )


# ---------------------------------------------------------------- L3
@template("c16_fertile_days_date", chapter=16, level=3, lo="16.4")
def fertile_days_date(rng):
    month, days = pick(rng, MONTHS)
    start = rng.randint(1, 10)
    ovul = start + 13
    first, last = ovul - 4, ovul + 1
    opts, key, mis = text_options(rng, f"{first} to {last} {month}", {
        f"{start} to {start + 4} {month}": "Those are the days of menstruation; no egg is present then.",
        f"{ovul} {month} only": "Sperm survive several days, so intercourse a few days BEFORE ovulation can also lead to pregnancy.",
        f"{ovul + 5} to {ovul + 10} {month}": "By then the egg has died; those days are after the fertile window.",
    })
    return dict(
        stem=f"A woman's period starts on **{start} {month}** (28-day cycle, ovulation on day 14). Sperm survive about 4 days and the egg about 1 day. Fig. 1 shows the month. Between which dates could intercourse lead to pregnancy?",
        figure=_cal_fig(month, days, rng.randint(0, 6), start, ovul=ovul),
        options=opts, key=key, misconceptions=mis,
        formula="ovulation = start + 13; fertile window ≈ 4 days before ovulation to 1 day after",
        working=[f"ovulation: {start} + 13 = {ovul} {month}", f"fertile window: {ovul} − 4 to {ovul} + 1 = **{first} to {last} {month}**"],
        hints=["First find the ovulation date (day 14).", "Sperm can wait up to 4 days before the egg arrives.", "The egg lives about a day after ovulation."],
    )


@template("c16_sti_percent_change", chapter=16, level=3, lo="16.6")
def sti_percent_change(rng):
    before = nice(rng, 400, 500, 800)
    pct = nice(rng, 10, 20, 25, 40)
    direction = pick(rng, ["fell", "rose"])
    after = before * (100 - pct) / 100 if direction == "fell" else before * (100 + pct) / 100
    opts, key, mis = numeric_options(rng, pct, [
        (abs(before - after), "That is the change in cases, not the percentage."),
        (round(abs(before - after) / after * 100), "Divide by the ORIGINAL (2015) number."),
        (100 - pct, "That is the complement, not the percentage change."),
    ], unit="%", sf=3)
    return dict(
        stem=f"The table shows the number of new syphilis cases in a city.\n\n{md_table(['Year', 'New cases'], [['2015', str(before)], ['2025', fmt(after)]])}\n\nBy what percentage did the number of cases {'fall' if direction == 'fell' else 'rise'}?",
        options=opts, key=key, misconceptions=mis,
        formula="percentage change = change ÷ original × 100",
        working=[f"change = {fmt(abs(before - after))}", f"{fmt(abs(before - after))} ÷ {before} × 100 = **{pct}%**"],
        hints=["Find the change in cases.", "Compare it with the 2015 figure.", f"{fmt(abs(before - after))} ÷ {before} × 100."],
    )


@template("c16_cycle_length_irregular", chapter=16, level=3, lo="16.4")
def cycle_length_irregular(rng):
    L = nice(rng, 26, 30, 32, 35)
    start = rng.randint(1, 3)
    ovul_day = L - 14
    ovul_date = start + ovul_day - 1
    opts, key, mis = numeric_options(rng, ovul_date, [
        (start + 13, "That assumes a 28-day cycle. Ovulation is about 14 days BEFORE the next period, so for a longer or shorter cycle the day changes."),
        (start + L - 1, "That is the last day of the cycle."),
        (start + L // 2, "Count 14 days back from the next period, not half the cycle."),
    ], unit="March", sf=2)
    return dict(
        stem=f"A woman has a regular **{L}-day** cycle. Ovulation occurs about **14 days before** the next period. Her period starts on **{start} March** (Fig. 1). On what date does she ovulate?",
        figure=_cal_fig("March", 31, 6, start),
        options=opts, key=key, misconceptions=mis,
        formula="ovulation day = cycle length − 14; date = start + (ovulation day − 1)",
        working=[f"ovulation day = {L} − 14 = day {ovul_day}", f"date = {start} + {ovul_day - 1} = **{ovul_date} March**"],
        hints=["Ovulation is 14 days before the NEXT period, not always on day 14.", f"Cycle length {L} − 14 gives the ovulation day.", f"Day 1 is {start} March, so add (day − 1)."],
    )


@template("c16_contraception_effectiveness_table", chapter=16, level=3, lo="16.5")
def contraception_effectiveness_table(rng):
    rows = [["condom", nice(rng, 85, 87)], ["birth control pill", nice(rng, 91, 93)], ["rhythm method", nice(rng, 75, 78)], ["no method", 15]]
    rows = [[n, str(v)] for n, v in rows]
    couples = nice(rng, 100, 200, 500)
    method = pick(rng, ["condom", "birth control pill", "rhythm method"])
    eff = int([r[1] for r in rows if r[0] == method][0])
    preg = couples * (100 - eff) / 100
    opts, key, mis = numeric_options(rng, preg, [
        (couples * eff / 100, "That is the number of couples who did NOT become pregnant."),
        (100 - eff, "That is the percentage who became pregnant, not the number of couples."),
        (couples * (100 - eff) / 10, "A percentage is out of 100, not 10."),
    ], unit="couples", sf=3)
    return dict(
        stem=f"The table shows the percentage of couples who avoid pregnancy in a year using each method.\n\n{md_table(['Method', 'Couples avoiding pregnancy / %'], rows)}\n\nIf **{couples}** couples use the **{method}** for a year, how many would be expected to become pregnant?",
        options=opts, key=key, misconceptions=mis,
        formula="pregnancies = (100 − effectiveness %) ÷ 100 × number of couples",
        working=[f"{method}: {eff}% avoid pregnancy, so {100 - eff}% do not", f"{100 - eff}/100 × {couples} = **{fmt(preg)} couples**"],
        hints=["The table gives the percentage who AVOID pregnancy.", "The rest become pregnant: 100 − that percentage.", f"({100 - eff}/100) × {couples}."],
    )


@template("c16_population_growth_rate_graph", chapter=16, level=3, lo="16.8*")
def population_growth_rate_graph(rng):
    pts = [(1800, 1.0), (1850, 1.3), (1900, 1.6), (1950, 2.5), (1975, 4.1), (2000, 6.1), (2025, 8.1)]
    y1, y2 = pick(rng, [(1950, 2000), (1975, 2025), (1900, 1950), (2000, 2025)])
    d = dict(pts)
    inc = round(d[y2] - d[y1], 1)
    opts, key, mis = numeric_options(rng, inc, [
        (d[y2], f"That is the population in {y2}, not the increase."),
        (round(d[y2] + d[y1], 1), "You added. Increase = later − earlier."),
        (round(inc / 2, 1), "Check the subtraction."),
    ], unit="billion", sf=2)
    return dict(
        stem=f"Fig. 1 shows the world population since 1800. By how much did the population increase between **{y1} and {y2}**?",
        figure=S.xy_graph([("world population", pts)], "year", "population / billions", 2050, 10, 50, 2, xmin=1800, legend=False, markers=True),
        options=opts, key=key, misconceptions=mis,
        formula="increase = population in later year − population in earlier year",
        working=[f"{y2}: {d[y2]} billion; {y1}: {d[y1]} billion", f"increase = **{fmt(inc)} billion**"],
        hints=["Read the population in both years.", "Subtract the earlier from the later.", f"{d[y2]} − {d[y1]}."],
    )


# ---------------------------------------------------------------- L4
@template("c16_calendar_intercourse_likely", chapter=16, level=4, lo="16.4")
def calendar_intercourse_likely(rng):
    month, days = pick(rng, MONTHS)
    start = rng.randint(1, 8)
    ovul = start + 13
    day = pick(rng, [start + 2, ovul - 2, ovul, ovul + 7])
    likely = ovul - 4 <= day <= ovul + 1
    correct = "likely, because it is within the fertile window around ovulation" if likely else "unlikely, because no live egg is present on that date"
    wrong = "unlikely, because no live egg is present on that date" if likely else "likely, because it is within the fertile window around ovulation"
    opts, key, mis = text_options(rng, correct, {
        wrong: f"Ovulation is on {ovul} {month}; the fertile window is about {ovul - 4} to {ovul + 1} {month}. Check whether {day} {month} falls inside it.",
        "likely, because pregnancy can happen on any day of the cycle": "An egg is available for only about a day; pregnancy is possible only around ovulation.",
        "unlikely, because sperm die within an hour": "Sperm can survive for several days in the female body.",
    })
    return dict(
        stem=f"A woman's period starts on **{start} {month}** (28-day cycle, ovulation on day 14). Sperm live about 4 days and the egg about 1 day. Fig. 1 shows the month. Is pregnancy likely if intercourse takes place on **{day} {month}**?",
        figure=_cal_fig(month, days, rng.randint(0, 6), start, ovul=ovul, extra={day: "sex"} if day != ovul else None),
        options=opts, key=key, misconceptions=mis,
        formula="fertile window ≈ (ovulation − 4 days) to (ovulation + 1 day)",
        working=[f"ovulation: {ovul} {month}; fertile window: {ovul - 4} to {ovul + 1} {month}", f"{day} {month} is {'inside' if likely else 'outside'} the window → **{correct}**"],
        hints=["Work out the ovulation date first (start + 13).", "The fertile window is about 4 days before to 1 day after.", f"Is {day} {month} in that range?"],
    )


@template("c16_sti_graph_two_lines", chapter=16, level=4, lo="16.6")
def sti_graph_two_lines(rng):
    yrs = list(range(2015, 2026, 2))
    g = [(y, 1000 + 120 * (i)) for i, y in enumerate(yrs)]
    s = [(y, 300 + 60 * i) for i, y in enumerate(yrs)]
    y = pick(rng, yrs[1:])
    diff = dict(g)[y] - dict(s)[y]
    opts, key, mis = numeric_options(rng, diff, [
        (dict(g)[y], "That is the gonorrhoea figure, not the difference."),
        (dict(s)[y], "That is the syphilis figure."),
        (dict(g)[y] + dict(s)[y], "You added. Difference = gonorrhoea − syphilis."),
    ], unit="cases", sf=3)
    return dict(
        stem=f"Fig. 1 shows new cases of two bacterial STIs in a country. In **{y}**, how many more cases of gonorrhoea than syphilis were reported?",
        figure=S.xy_graph([("gonorrhoea", g), ("syphilis", s)], "year", "new cases", 2025, 2000, 2, 400, xmin=2015),
        options=opts, key=key, misconceptions=mis,
        formula="difference = gonorrhoea cases − syphilis cases in the same year",
        working=[f"{y}: gonorrhoea {dict(g)[y]}, syphilis {dict(s)[y]}", f"difference = **{diff} cases**"],
        hints=["Use the legend to identify the lines.", f"Read both at {y}.", "Subtract."],
    )


@template("c16_birth_weight_bar_chart", chapter=16, level=4, lo="16.7")
def birth_weight_bar_chart(rng):
    groups = ["none", "1–10 a day", "11–20 a day", "over 20 a day"]
    vals = [nice(rng, 3.4, 3.5), nice(rng, 3.2, 3.3), nice(rng, 3.0, 3.1), nice(rng, 2.7, 2.8)]
    diff = round(vals[0] - vals[3], 1)
    opts, key, mis = numeric_options(rng, diff, [
        (vals[3], "That is the birth mass for the heaviest-smoking group, not the difference."),
        (round(vals[0] - vals[1], 1), "That compares with the lightest-smoking group; the question asks about 'over 20 a day'."),
        (round(vals[0] + vals[3], 1), "You added."),
    ], unit="kg", dp=1)
    return dict(
        stem="Fig. 1 shows the average birth mass of babies grouped by the number of cigarettes their mothers smoked each day during pregnancy. How much lighter, on average, are the babies of mothers who smoked **over 20 a day** than those of **non-smokers**?",
        figure=S.bar_chart(groups, vals, "average birth mass / kg", ymax=4, ystep=1, xlabel="cigarettes smoked per day", size=(5.2, 3.0)),
        options=opts, key=key, misconceptions=mis,
        formula="difference = non-smokers' value − 'over 20' value",
        working=[f"{fmt(vals[0])} − {fmt(vals[3])} = **{fmt(diff)} kg**"],
        hints=["Read the first and last bars.", "Subtract.", "More smoking → lower birth mass."],
    )


@template("c16_sex_cells_table_chromosomes", chapter=16, level=4, lo="16.8*")
def sex_cells_table_chromosomes(rng):
    animal, half = pick(rng, [("human", 23), ("dog", 39), ("cat", 19), ("horse", 32), ("mouse", 20)])
    full = 2 * half
    opts, key, mis = numeric_options(rng, full, [
        (half, "That is the number in a SEX cell. A fertilised egg has the sperm's set PLUS the egg's set."),
        (full * 2, f"Each sex cell carries half a set ({half}), so together they make one full set, not two."),
        (half * 3, f"Only two sex cells fuse: {half} + {half}."),
    ], unit="chromosomes", sf=2)
    return dict(
        stem=f"The table shows the number of chromosomes (carrying genetic information) in the cells of a {animal}.\n\n{md_table(['Cell', 'Number of chromosomes'], [['sperm', str(half)], ['egg', str(half)], ['fertilised egg', '?']])}\n\nHow many chromosomes does the fertilised egg contain?",
        options=opts, key=key, misconceptions=mis,
        formula="fertilised egg = chromosomes from the sperm + chromosomes from the egg",
        working=[f"{half} (from the father) + {half} (from the mother) = **{full} chromosomes**", "half the genetic information comes from each parent"],
        hints=["Fertilisation joins the nucleus of a sperm with the nucleus of an egg.", "Each brings its own set.", f"{half} + {half}."],
    )


@template("c16_population_doubling", chapter=16, level=4, lo="16.8*")
def population_doubling(rng):
    pts = [(1800, 1.0), (1850, 1.3), (1900, 1.6), (1950, 2.5), (1975, 4.1), (2000, 6.1), (2025, 8.1)]
    y0, p0 = pick(rng, [(1850, 1.3), (1900, 1.6), (1950, 2.5)])
    target = 2 * p0
    # year when the straight-line graph reaches the target (interpolate), rounded to 5 years
    for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
        if ya <= target <= yb:
            y_hit = xa + (target - ya) / (yb - ya) * (xb - xa)
            break
    y_hit = int(round(y_hit / 5) * 5)
    ans = y_hit - y0
    opts, key, mis = numeric_options(rng, ans, [
        (ans + 25, "Read where the line reaches the doubled value, not a later point."),
        (ans - 20 if ans - 20 > 0 else ans + 50, f"The population had not yet reached {fmt(target)} billion at that time."),
        (y_hit, "That is the YEAR it doubled; the question asks how many years it took."),
    ], unit="years", sf=3)
    return dict(
        stem=f"Fig. 1 shows the world population. In **{y0}** it was **{fmt(p0)} billion**. Roughly how many years did it take to **double** to {fmt(target)} billion?",
        figure=S.xy_graph([("world population", pts)], "year", "population / billions", 2050, 10, 50, 2, xmin=1800, legend=False, markers=True),
        options=opts, key=key, misconceptions=mis,
        formula=f"find the year when the population reached 2 × {fmt(p0)} = {fmt(target)} billion; doubling time = that year − {y0}",
        working=[f"{fmt(target)} billion is reached at about {y_hit}", f"doubling time ≈ {y_hit} − {y0} = **{ans} years**"],
        hints=[f"Double {fmt(p0)} billion is {fmt(target)} billion.", f"Find where the line passes {fmt(target)} billion on the vertical axis and read the year.", f"Subtract {y0}."],
    )


# ---------------------------------------------------------------- L5
@template("c16_cycle_table_predict_next", chapter=16, level=5, lo="16.4")
def cycle_table_predict_next(rng):
    starts = [3, None, None]
    L = nice(rng, 27, 28, 29, 30)
    s1 = rng.randint(1, 3)
    dates = [("January", s1), ("January", s1 + L) if s1 + L <= 31 else ("February", s1 + L - 31)]
    d2m, d2 = dates[1]
    # third start
    total_from_jan1 = s1 + 2 * L
    if total_from_jan1 <= 31:
        d3m, d3 = "January", total_from_jan1
    elif total_from_jan1 <= 59:
        d3m, d3 = "February", total_from_jan1 - 31
    else:
        d3m, d3 = "March", total_from_jan1 - 59
    opts, key, mis = text_options(rng, f"{d3} {d3m}", {
        f"{d3 + 2 if d3 + 2 <= 28 else d3 - 2} {d3m}": "Check the cycle length from the first two dates and add it exactly.",
        f"{d2 + 28 if d2 + 28 <= 28 else d2 + 28 - 28} {'March' if d2m == 'February' else 'February'}": f"That assumes a 28-day cycle, but her cycle is {L} days.",
        f"{d3 - 7 if d3 > 7 else d3 + 7} {d3m}": "That is a week out; count the days carefully (January has 31 days, February 28).",
    })
    return dict(
        stem=f"A woman records the first day of two consecutive periods.\n\n{md_table(['Period', 'First day'], [['1st', f'{s1} January'], ['2nd', f'{d2} {d2m}']])}\n\nAssuming her cycle stays regular, on what date will the **3rd** period start? (January has 31 days; February has 28.)",
        options=opts, key=key, misconceptions=mis,
        formula="cycle length = gap between the first two start dates; next start = 2nd start + cycle length",
        working=[f"cycle length = {L} days", f"3rd period = {d2} {d2m} + {L} days = **{d3} {d3m}**"],
        hints=["First find her cycle length from the two dates given.", "Add that many days to the 2nd start date.", "Remember the month lengths."],
    )


@template("c16_sti_rate_per_100000", chapter=16, level=5, lo="16.6")
def sti_rate_per_100000(rng):
    pop = nice(rng, 2.0, 4.0, 5.0)   # million
    cases = nice(rng, 400, 600, 1000, 1500)
    rate = cases / (pop * 10)   # per 100 000
    opts, key, mis = numeric_options(rng, rate, [
        (cases / pop, "That is cases per MILLION. There are 10 lots of 100 000 in a million."),
        (cases, "That is the total number of cases, not the rate."),
        (rate * 10, "Divide the population in millions by 0.1 million (100 000)."),
    ], unit="per 100 000", sf=3)
    return dict(
        stem=f"A country of **{fmt(pop)} million** people reported **{cases}** new cases of gonorrhoea in a year.\n\n{md_table(['Population', 'New cases'], [[f'{fmt(pop)} million', str(cases)]])}\n\nWhat is the rate of new cases **per 100 000 people**?",
        options=opts, key=key, misconceptions=mis,
        formula="rate per 100 000 = cases ÷ (population ÷ 100 000)",
        working=[f"population = {fmt(pop)} million = {fmt(pop * 10)} lots of 100 000", f"rate = {cases} ÷ {fmt(pop * 10)} = **{fmt(rate)} per 100 000**"],
        hints=["How many groups of 100 000 people are in the population?", f"{fmt(pop)} million ÷ 100 000.", "Divide the cases by that number."],
    )


@template("c16_contraception_compare_couples", chapter=16, level=5, lo="16.5")
def contraception_compare_couples(rng):
    couples = nice(rng, 200, 400, 1000)
    e_condom, e_rhythm = nice(rng, 85, 88), nice(rng, 75, 78)
    diff = couples * (e_condom - e_rhythm) / 100
    opts, key, mis = numeric_options(rng, diff, [
        (couples * (100 - e_rhythm) / 100, "That is the total pregnancies with the rhythm method, not how many MORE than with condoms."),
        (e_condom - e_rhythm, "That is the percentage difference, not the number of couples."),
        (couples * (100 - e_condom) / 100, "That is the pregnancies with condoms."),
    ], unit="couples", sf=3)
    return dict(
        stem=f"The table shows how effective two methods are.\n\n{md_table(['Method', 'Couples avoiding pregnancy in a year / %'], [['condom', str(e_condom)], ['rhythm method', str(e_rhythm)]])}\n\n**{couples}** couples use each method for a year. How many **more** pregnancies are expected among the rhythm-method couples than among the condom couples?",
        options=opts, key=key, misconceptions=mis,
        formula="pregnancies = (100 − %) ÷ 100 × couples for each; subtract",
        working=[f"rhythm: {100 - e_rhythm}% of {couples} = {fmt(couples * (100 - e_rhythm) / 100)}", f"condom: {100 - e_condom}% of {couples} = {fmt(couples * (100 - e_condom) / 100)}", f"difference = **{fmt(diff)} couples**"],
        hints=["Find the pregnancies for each method separately.", "Pregnancies = couples × (100 − effectiveness)/100.", "Subtract the two."],
    )


@template("c16_cycle_bar_days_lining_thick", chapter=16, level=5, lo="16.4")
def cycle_bar_days_lining_thick(rng):
    period = nice(rng, 4, 5, 6)
    thick_days = 28 - 14   # days 15-28
    opts, key, mis = numeric_options(rng, thick_days, [
        (28 - period, "That is every day except menstruation. The lining is only FULLY thick after ovulation (days 15–28)."),
        (14 - period, "That is the number of days the lining is thickening (after the period, before ovulation)."),
        (28, "The lining breaks down during menstruation, so it is not thick all month."),
    ], unit="days", sf=2)
    return dict(
        stem=f"Fig. 1 shows a 28-day cycle with menstruation lasting {period} days and ovulation on day 14. For how many days **after ovulation** does the uterus lining stay thick, ready for a fertilised egg, before the next period begins?",
        figure=S.cycle_bar(period_days=period, ovulation=14),
        options=opts, key=key, misconceptions=mis,
        formula="days 15 to 28 inclusive = 28 − 14",
        working=["after ovulation: days 15–28", f"28 − 14 = **{thick_days} days**"],
        hints=["Ovulation is on day 14.", "Count from day 15 to day 28 inclusive.", "28 − 14."],
    )


@template("c16_population_factors_table", chapter=16, level=5, lo="16.8*")
def population_factors_table(rng):
    births = nice(rng, 30, 35, 40)
    deaths = nice(rng, 8, 10, 12)
    pop = nice(rng, 5, 10, 20)   # million
    growth = (births - deaths) * pop / 1000 * 1000  # thousand people... compute in thousands
    growth_thousand = (births - deaths) * pop   # per 1000 × millions = thousands
    opts, key, mis = numeric_options(rng, growth_thousand, [
        (births * pop, "You counted only births. Deaths reduce the population; use births − deaths."),
        ((births - deaths), "That is the growth per 1000 people, not for the whole population."),
        ((births + deaths) * pop, "You added deaths instead of subtracting them."),
    ], unit="thousand people", sf=3)
    return dict(
        stem=f"The table shows a country's figures for one year.\n\n{md_table(['Quantity', 'Value'], [['population', f'{pop} million'], ['births per 1000 people', str(births)], ['deaths per 1000 people', str(deaths)]])}\n\nBy how many people did the population grow that year (ignoring migration)?",
        options=opts, key=key, misconceptions=mis,
        formula="growth per 1000 = births − deaths; total growth = (growth per 1000) × population ÷ 1000",
        working=[f"growth per 1000 = {births} − {deaths} = {births - deaths}", f"{pop} million ÷ 1000 = {pop * 1000} thousand groups of 1000", f"growth = {births - deaths} × {pop * 1000} thousand ÷ 1000 = **{fmt(growth_thousand)} thousand people**"],
        hints=["Each 1000 people gains (births − deaths).", f"How many thousands are in {pop} million?", f"({births} − {deaths}) × {pop} thousand."],
    )


# ================================================================ EXPLANATION
EXPLAIN = [
    # ------------------------------------------------------------ L1
    dict(id="e16_fertilisation_definition", level=1, lo="16.1",
         stem="Fig. 1 shows the events of fertilisation. Fertilisation is",
         correct="the fusion of the nucleus of a sperm with the nucleus of an egg",
         wrongs={"the release of an egg from an ovary": "That is ovulation.", "the attachment of the embryo to the uterus lining": "That is implantation.", "the breakdown of the uterus lining": "That is menstruation."},
         hints=["Two sex cells are involved.", "Something joins together: which parts of the two cells?", "Nucleus + nucleus."],
         fig=lambda rng: S.flow_boxes(["sperm nucleus\n+ egg nucleus", "fertilised egg", "embryo"])),
    dict(id="e16_puberty_recall", level=1, lo="16.2",
         stem="The table lists changes.\n\n| Change |\n|---|\n| voice deepens |\n| menstruation begins |\n| pubic hair grows |\n\nWhich change happens in **boys only** at puberty?",
         correct="voice deepens",
         wrongs={"menstruation begins": "Menstruation happens in girls.", "pubic hair grows": "This happens in both boys and girls.", "breasts develop": "This happens in girls."},
         hints=["Some changes are shared, some are for one sex only.", "Which change is linked to the male voice?", "Deeper voice."]),
    dict(id="e16_ovary_function", level=1, lo="16.3",
         stem="Fig. 1 shows parts of the female reproductive system. What is the function of the ovaries (P)?",
         correct="to produce eggs and female sex hormones",
         wrongs={"to produce sperm": "Sperm are made in the testes.", "to carry the egg to the uterus": "That is the oviduct.", "to hold the developing baby": "That is the uterus."},
         hints=["Ovaries are the female sex organs that make sex cells.", "Which sex cell is female?", "Eggs (and hormones)."],
         fig=lambda rng: S.labelled_parts("female reproductive system", [("P", "produces eggs"), ("Q", "where fertilisation happens"), ("R", "where the embryo develops"), ("S", "birth canal")])),
    dict(id="e16_sti_examples", level=1, lo="16.6",
         stem="The table lists infections.\n\n| Infection | Cause |\n|---|---|\n| gonorrhoea | bacteria |\n| syphilis | bacteria |\n| AIDS | virus (HIV) |\n| influenza | virus |\n\nWhich infection in the table is **not** a sexually transmitted infection?",
         correct="influenza",
         wrongs={"gonorrhoea": "Gonorrhoea is a bacterial STI.", "syphilis": "Syphilis is a bacterial STI.", "AIDS": "AIDS is caused by HIV, which is sexually transmitted."},
         hints=["STIs are passed on mainly through sexual contact.", "Which infection is spread by coughs and sneezes?", "Flu."]),
    dict(id="e16_menstruation_meaning", level=1, lo="16.4",
         stem="Fig. 1 shows a 28-day menstrual cycle. What happens during **menstruation** (the shaded days)?",
         correct="The thickened lining of the uterus breaks down and leaves the body through the vagina, with some blood.",
         wrongs={"An egg is released from the ovary.": "That is ovulation, around day 14.", "The lining of the uterus thickens.": "That happens AFTER menstruation, from about day 6.", "A fertilised egg attaches to the uterus.": "That is implantation; it only happens if fertilisation occurred."},
         hints=["The shaded days are the first few days of the cycle.", "What leaves the body during a period?", "The old lining."],
         fig=lambda rng: S.cycle_bar()),

    # ------------------------------------------------------------ L2
    dict(id="e16_identify_part_by_function", level=2, lo="16.3",
         hints=["Match the function to the part. Ovary: eggs. Oviduct: carries egg, fertilisation. Uterus: embryo develops. Vagina: receives sperm, birth canal.", "Testis: sperm. Sperm duct: carries sperm. Urethra: semen out.", "Find the letter with that job."],
         fig=lambda rng: S.labelled_parts("female reproductive system", [("P", "produces eggs"), ("Q", "where fertilisation happens"), ("R", "where the embryo develops"), ("S", "birth canal")]),
         variants=[
             dict(stem="Fig. 1 shows parts of the female system. Which part is the **oviduct**?", correct="Q", wrongs={"P": "P is the ovary, which produces eggs.", "R": "R is the uterus, where the embryo develops.", "S": "S is the vagina."}),
             dict(stem="Fig. 1 shows parts of the female system. Which part is the **uterus**?", correct="R", wrongs={"P": "P is the ovary.", "Q": "Q is the oviduct, where fertilisation happens.", "S": "S is the vagina, the birth canal."}),
             dict(stem="Fig. 1 shows parts of the female system. In which part does **fertilisation** normally occur?", correct="Q, the oviduct", wrongs={"P, the ovary": "The ovary releases the egg; fertilisation happens after that.", "R, the uterus": "The embryo develops here, but fertilisation has already happened.", "S, the vagina": "Sperm enter here, but meet the egg further along."}),
         ]),
    dict(id="e16_male_parts", level=2, lo="16.3",
         stem="The table describes parts of the male reproductive system.\n\n| Part | Function |\n|---|---|\n| X | produces sperm and male sex hormones |\n| Y | carries sperm from the testis |\n| Z | adds fluid containing nutrients to the sperm |\n\nWhich row names X, Y and Z correctly?",
         correct="X = testis, Y = sperm duct, Z = sex glands",
         wrongs={"X = sperm duct, Y = testis, Z = urethra": "The testis PRODUCES sperm; the sperm duct carries them.", "X = testis, Y = urethra, Z = sperm duct": "The sperm duct carries sperm from the testis; the urethra carries semen out of the body.", "X = sex glands, Y = sperm duct, Z = testis": "Sex glands add fluid; they do not make sperm."},
         hints=["Which part makes the sperm?", "Which is a tube that carries them?", "Which adds the fluid (sperm + fluid = semen)?"]),
    dict(id="e16_classify_birth_control", level=2, lo="16.5",
         hints=["Temporary methods can be stopped; permanent methods involve surgery that cannot easily be undone.", "Condom, pill, IUD, rhythm method: temporary. Vasectomy, tubal ligation: permanent.", "Match the description."],
         variants=[
             dict(stem="The table lists birth-control methods.\n\n| Method | How it works |\n|---|---|\n| condom | stops sperm entering the vagina |\n| birth control pill | stops ovulation |\n| vasectomy | sperm ducts cut and tied |\n| rhythm method | avoiding the fertile days |\n\nWhich method is **permanent**?", correct="vasectomy", wrongs={"condom": "A condom is used each time; it is temporary.", "birth control pill": "Stopping the pill restores fertility; it is temporary.", "rhythm method": "This is a temporary (and unreliable) method."}),
             dict(stem="The table lists birth-control methods.\n\n| Method | How it works |\n|---|---|\n| condom | stops sperm entering the vagina |\n| tubal ligation | oviducts cut and tied |\n| IUD | stops implantation |\n| spermicide | kills sperm |\n\nWhich method also reduces the risk of catching an STI?", correct="condom", wrongs={"tubal ligation": "It prevents pregnancy but gives no protection against infection.", "IUD": "It prevents implantation only.", "spermicide": "It kills sperm but does not stop infections passing."}),
         ]),
    dict(id="e16_bacterial_vs_viral_sti", level=2, lo="16.6",
         stem="The table shows STIs and their causes.\n\n| STI | Cause |\n|---|---|\n| gonorrhoea | bacteria |\n| syphilis | bacteria |\n| AIDS | virus (HIV) |\n\nWhich STIs can be cured with antibiotics?",
         correct="gonorrhoea and syphilis only",
         wrongs={"AIDS only": "Antibiotics do not work on viruses.", "all three": "AIDS is viral and cannot be cured with antibiotics.", "none of them": "Antibiotics kill bacteria, so the two bacterial STIs can be cured."},
         hints=["Antibiotics work against one type of microbe only.", "Which rows say 'bacteria'?", "Bacteria → antibiotics work; virus → they do not."]),
    dict(id="e16_substance_effects_identify", level=2, lo="16.7",
         stem="The table lists outcomes for babies.\n\n| Outcome |\n|---|\n| low birth mass |\n| premature birth |\n| poor organ development |\n| higher birth mass |\n\nWhich outcome is **not** linked to a mother smoking, drinking alcohol or taking drugs during pregnancy?",
         correct="higher birth mass",
         wrongs={"low birth mass": "Smoking and drugs reduce the baby's growth.", "premature birth": "Substance abuse raises the risk of early birth.", "poor organ development": "Alcohol and drugs can damage the developing organs."},
         hints=["Substances cross from the mother's blood to the baby.", "They harm growth and development.", "Which option is the opposite of harm to growth?"]),

    # ------------------------------------------------------------ L3
    dict(id="e16_blocked_oviducts", level=3, lo="16.3",
         stem="Fig. 1 shows parts of the female system. A woman's oviducts (Q) are both blocked. Which statement is correct?",
         correct="She cannot become pregnant, because sperm cannot reach the egg; she still ovulates and has periods.",
         wrongs={"She cannot become pregnant and her periods stop.": "The ovaries and uterus still work, so ovulation and menstruation continue.", "She can become pregnant, because the egg can go round the blockage.": "The oviduct is the only route for the egg and the sperm to meet.", "She cannot produce eggs.": "Eggs are made in the ovaries, which are not blocked."},
         hints=["Where do the sperm and egg normally meet?", "If that tube is blocked, can they meet?", "The ovaries and uterus still work as normal."],
         fig=lambda rng: S.labelled_parts("female reproductive system", [("P", "produces eggs"), ("Q", "where fertilisation happens"), ("R", "where the embryo develops"), ("S", "birth canal")])),
    dict(id="e16_how_method_works", level=3, lo="16.5",
         hints=["Each method blocks ONE step: ovulation, sperm meeting egg, or implantation.", "Which step does the description match?", "Trace the path from sperm to implantation."],
         fig=lambda rng: S.flow_boxes(["ovulation", "sperm meets egg\n(fertilisation)", "implantation\nin uterus"]),
         variants=[
             dict(stem="Fig. 1 shows the steps leading to pregnancy. How does the **birth control pill** prevent pregnancy?", correct="It stops ovulation, so no egg is released to be fertilised.", wrongs={"It kills sperm in the vagina.": "That is a spermicide.", "It forms a barrier that stops sperm entering the uterus.": "That is a condom or diaphragm.", "It stops the fertilised egg implanting.": "That is an IUD."}),
             dict(stem="Fig. 1 shows the steps leading to pregnancy. How does a **condom** prevent pregnancy?", correct="It stops sperm from entering the vagina, so sperm cannot meet the egg.", wrongs={"It stops ovulation.": "That is the pill.", "It kills the egg.": "No method works by killing the egg.", "It stops implantation.": "That is an IUD."}),
             dict(stem="Fig. 1 shows the steps leading to pregnancy. How does **tubal ligation** prevent pregnancy?", correct="The oviducts are cut and tied, so sperm cannot reach the egg.", wrongs={"The ovaries are removed.": "The ovaries are left in place and still release eggs.", "The uterus lining is removed.": "The uterus is not changed.", "Sperm production is stopped.": "That would be a change in the male, not the female."}),
         ]),
    dict(id="e16_hiv_antibiotics", level=3, lo="16.6",
         stem="The table shows two STIs.\n\n| STI | Cause | Treatable with antibiotics? |\n|---|---|---|\n| syphilis | bacteria | yes |\n| AIDS | HIV (virus) | no |\n\nWhy can AIDS not be cured with antibiotics?",
         correct="Antibiotics kill bacteria but have no effect on viruses, and AIDS is caused by a virus.",
         wrongs={"HIV is too small to be seen.": "Size is not the reason; the type of microbe is.", "Antibiotics only work on the skin.": "Antibiotics work throughout the body against bacteria.", "AIDS is not an infection.": "AIDS is an infection caused by HIV."},
         hints=["What type of microbe does each STI have?", "What do antibiotics act on?", "Virus ≠ bacteria."]),
    dict(id="e16_heredity_apply", level=3, lo="16.1",
         stem="Fig. 1 shows fertilisation. A baby has her father's eye colour and her mother's hair colour. Which statement explains this?",
         correct="The fertilised egg received genetic information from both the sperm and the egg, so the child inherits characteristics from both parents.",
         wrongs={"The baby copied her parents after birth.": "Eye and hair colour are inherited, not learnt.", "Only the mother passes on genetic information.": "The sperm nucleus also carries genetic information.", "The father's genes control the eyes and the mother's control the hair in every child.": "Which features come from which parent varies from child to child."},
         hints=["What does each sex cell carry in its nucleus?", "Both nuclei fuse at fertilisation.", "Information from both → features from both."],
         fig=lambda rng: S.flow_boxes(["sperm nucleus\n(father's information)", "fertilised egg\n(both)", "egg nucleus\n(mother's information)"])),
    dict(id="e16_premarital_sex_risks", level=3, lo="16.5",
         stem="The table lists possible consequences.\n\n| Consequence |\n|---|\n| unwanted pregnancy |\n| catching an STI |\n| emotional distress |\n| improved school results |\n\nWhich consequence is **not** a recognised risk of pre-marital sex for teenagers?",
         correct="improved school results",
         wrongs={"unwanted pregnancy": "Pregnancy is a real risk whenever intercourse takes place.", "catching an STI": "STIs are spread by sexual contact.", "emotional distress": "Teenagers often report regret or distress."},
         hints=["Three of the rows are harms.", "Which row is not a harm at all?", "The odd one out."]),

    # ------------------------------------------------------------ L4
    dict(id="e16_cycle_no_fertilisation_explain", level=4, lo="16.4",
         stem="Fig. 1 shows a 28-day cycle. Explain why menstruation starts again at the end of the cycle if the egg is not fertilised.",
         correct="The thick uterus lining is no longer needed, so it breaks down and is shed, starting a new cycle.",
         wrongs={"The unfertilised egg grows into the lining and must be removed.": "An unfertilised egg dies within a day; it does not grow.", "The ovaries release blood to clean the uterus.": "The blood comes from the breakdown of the lining, not from the ovaries.", "The lining thickens even more and overflows.": "The lining breaks down; it does not keep growing."},
         hints=["Why does the lining thicken in the first place?", "What happens if no embryo arrives to use it?", "Not needed → shed."],
         fig=lambda rng: S.cycle_bar()),
    dict(id="e16_hiv_white_cells_explain", level=4, lo="16.6",
         stem="Fig. 1 shows how HIV affects the body. Why does a person with AIDS fall ill with infections that healthy people fight off easily?",
         correct="HIV destroys white blood cells, so the body can no longer defend itself against other infections.",
         wrongs={"HIV makes the blood too thick to flow.": "HIV affects the immune system, not blood thickness.", "HIV causes the infections directly.": "The other infections are caught from elsewhere; HIV weakens the DEFENCES.", "HIV removes all the red blood cells.": "HIV targets white cells, which fight infection."},
         hints=["Which blood cells fight infection?", "What does HIV do to them?", "Fewer defenders → more infections."],
         fig=lambda rng: S.flow_boxes(["HIV enters\nthe blood", "white blood cells\ndestroyed", "body cannot\nfight infections", "AIDS"])),
    dict(id="e16_smoking_pregnancy_explain", level=4, lo="16.7",
         stem="Fig. 1 shows average birth mass against cigarettes smoked. Explain the trend.",
         correct="Harmful substances from the smoke pass from the mother's blood to the baby, reducing the oxygen and nutrients it gets, so it grows less.",
         wrongs={"Smoking mothers eat less, so the baby gets less food.": "The main effect is through the substances in smoke reaching the baby's blood.", "Smoke makes the baby heavier because of the tar.": "The graph shows the opposite: LOWER birth mass.", "The trend is a coincidence.": "The steady fall with more cigarettes shows a real link."},
         hints=["What passes from mother to baby through the placenta?", "Smoke contains carbon monoxide and other poisons.", "Less oxygen and food → smaller baby."],
         fig=lambda rng: S.bar_chart(["none", "1–10", "11–20", "over 20"], [3.5, 3.3, 3.1, 2.8], "average birth mass / kg", ymax=4, ystep=1, xlabel="cigarettes per day")),
    dict(id="e16_siblings_differ_explain", level=4, lo="16.8*",
         stem="Fig. 1 shows fertilisation. Why do two children of the same parents look similar but not identical?",
         correct="Each child receives half its genetic information from each parent, but a different combination each time, so they share some features and differ in others.",
         wrongs={"Each child gets exactly the same information, so differences come only from food.": "Diet cannot explain different eye colours; the genetic combinations differ.", "The first child gets the father's information and the second the mother's.": "Every child gets half from EACH parent.", "Siblings are not related genetically.": "They share parents and therefore much genetic information."},
         hints=["Each sex cell carries half of a parent's information.", "Is it the same half every time?", "Same parents, different combinations."],
         fig=lambda rng: S.flow_boxes(["half from father", "child", "half from mother"])),
    dict(id="e16_abortion_not_birth_control", level=4, lo="16.5",
         stem="The table compares two actions.\n\n| Action | When | Possible effects |\n|---|---|---|\n| using a condom | before intercourse | prevents fertilisation |\n| abortion | after pregnancy begins | can damage the uterus, infertility, distress |\n\nWhy is abortion **not** considered a method of birth control?",
         correct="It ends a pregnancy that has already begun instead of preventing one, and it carries physical and emotional risks.",
         wrongs={"Because it is always illegal.": "Legality varies; the reason is what it does and its risks.", "Because it is more effective than other methods.": "Effectiveness is not the issue.", "Because it only works for men.": "It involves the pregnant woman."},
         hints=["Birth control PREVENTS pregnancy.", "When does abortion happen: before or after?", "Compare the 'when' column."]),

    # ------------------------------------------------------------ L5
    dict(id="e16_evaluate_rhythm_method", level=5, lo="16.5",
         stem="The table shows a woman's last six cycle lengths.\n\n| Cycle | 1 | 2 | 3 | 4 | 5 | 6 |\n|---|---|---|---|---|---|---|\n| length / days | 26 | 31 | 28 | 33 | 27 | 30 |\n\nShe plans to use the rhythm method (avoiding the fertile days). Which comment is most accurate?",
         correct="Her cycles vary a lot, so the fertile days cannot be predicted reliably and the method is likely to fail.",
         wrongs={"The method will work well because she knows her cycle.": "Knowing PAST cycles does not help when the length varies by a week.", "She should assume every cycle is 28 days.": "Only one of the six cycles was 28 days.", "The rhythm method is reliable for everyone.": "It is one of the least reliable methods even with regular cycles."},
         hints=["The rhythm method depends on predicting ovulation.", "How much do her cycle lengths vary?", "Unpredictable ovulation → unreliable method."]),
    dict(id="e16_evaluate_antibiotic_claim", level=5, lo="16.6",
         stem="The table shows STIs.\n\n| STI | Cause |\n|---|---|\n| gonorrhoea | bacteria |\n| syphilis | bacteria |\n| AIDS | virus |\n\nA student claims: 'All STIs can be cured by taking antibiotics, so they are not serious.' Which response is best?",
         correct="Incorrect: only the bacterial STIs respond to antibiotics; AIDS is viral and cannot be cured, and untreated STIs cause serious harm.",
         wrongs={"Correct: antibiotics cure every infection.": "Antibiotics do not work on viruses.", "Incorrect: no STI can be cured.": "The bacterial STIs CAN be cured with antibiotics.", "Correct: STIs are never serious.": "Untreated STIs can cause infertility, damage to organs and death."},
         hints=["Check each STI's cause.", "What do antibiotics kill?", "Even curable STIs can cause harm before treatment."]),
    dict(id="e16_population_growth_evaluate", level=5, lo="16.8*",
         stem="The table shows changes in a country over 100 years.\n\n| Factor | 1920 | 2020 |\n|---|---|---|\n| babies dying before age 5 / % | 25 | 1 |\n| average lifespan / years | 45 | 82 |\n| births per woman | 5 | 2 |\n| population / millions | 10 | 30 |\n\nWhich explanation of the population growth is best supported by the data?",
         correct="Better medicine, food and sanitation meant far fewer deaths and longer lives, so the population grew even though births per woman fell.",
         wrongs={"Women had more babies in 2020.": "Births per woman FELL from 5 to 2.", "The population grew because lifespan fell.": "Lifespan ROSE from 45 to 82.", "The population did not change.": "It tripled from 10 to 30 million."},
         hints=["Compare the death-related rows with the birth row.", "Which changed in a way that adds people?", "Fewer deaths + longer lives."]),
    dict(id="e16_predict_intercourse_day5", level=5, lo="16.4",
         stem="Fig. 1 shows a 28-day cycle. A couple has intercourse on day 5 of the woman's cycle. Sperm live up to 4 days and the egg about 1 day after ovulation on day 14. Predict whether pregnancy is likely.",
         correct="Unlikely: the sperm will have died by day 9, five days before an egg is released.",
         wrongs={"Likely: sperm can wait inside the body until ovulation.": "Sperm survive only about 4 days, so they die long before day 14.", "Likely: an egg is present during menstruation.": "No egg is present; the egg is released on day 14.", "Unlikely: intercourse during menstruation can never cause pregnancy.": "It CAN, in short cycles where ovulation is early; the reason here is the timing of sperm survival."},
         hints=["When is the egg released?", "How long can sperm from day 5 survive?", "Do the two overlap?"],
         fig=lambda rng: S.cycle_bar(marks={5: "sex"})),
    dict(id="e16_evaluate_prenatal_advice", level=5, lo="16.7",
         stem="The table shows two pieces of advice given to a pregnant woman.\n\n| Advice | Reason given |\n|---|---|\n| 'A glass of wine a day is fine; it relaxes you.' | relaxation helps the baby |\n| 'Avoid alcohol completely.' | alcohol crosses to the baby's blood and can harm its development |\n\nWhich advice is better supported by science, and why?",
         correct="Avoiding alcohol: alcohol passes from the mother's blood to the baby and can harm the development of its organs and brain.",
         wrongs={"The daily wine: relaxation outweighs any risk.": "No amount of alcohol is known to be safe for the developing baby.", "Either is fine because the placenta blocks alcohol.": "The placenta does NOT block alcohol; it passes through.", "The daily wine: the baby has its own blood, so it is unaffected.": "Substances in the mother's blood cross to the baby's blood."},
         hints=["How do substances reach the baby?", "Does alcohol cross the placenta?", "Risk to development."]),
]

register_explain(EXPLAIN, chapter=16)
