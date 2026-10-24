"""Ch 10 Transfer of Heat Energy and its Effects: 25 calculation / data templates and 25 explanation items.
lo codes: 10.1 temperature, 10.2 expansion and contraction, 10.3 conduction, 10.4 convection, 10.5 radiation, 10.6 applications, 10.7 climate."""
from .. import figs, sketches as S
from .base import fmt, md_table, nice, numeric_options, pick, register_explain, template, text_options

SOLIDS = [("copper", 17), ("aluminium", 23), ("steel", 12), ("glass", 9), ("brass", 19)]   # expansion per °C, ×10⁻⁶ (used only for relative comparisons)


def _cooling(T0, Troom, k, tmax, step):
    """Newton-style cooling points rounded to whole degrees."""
    import math
    return [(t, round(Troom + (T0 - Troom) * math.exp(-k * t))) for t in range(0, tmax + 1, step)]


# ================================================================ CALCULATION / DATA
# ---------------------------------------------------------------- L1
@template("c10_read_thermometer", chapter=10, level=1, lo="10.1")
def read_thermometer(rng):
    T = rng.randint(-4, 52) * 2
    opts, key, mis = numeric_options(rng, T if T > 0 else T + 0.0001, [
        (T + 10, "You read the labelled mark ABOVE the top of the liquid. Read the mark level with the top of the liquid."),
        (T - 10, "You read the labelled mark below. Count the small divisions (2 °C each) up to the top of the liquid."),
        (T + 2, "You are one small division out. Each small division on this thermometer is 2 °C."),
    ], unit="°C", sf=3) if T > 0 else numeric_options(rng, T + 100, [], unit="°C")
    if T <= 0:   # avoid non-positive answers in the option builder: shift to a positive reading
        T = 12
        opts, key, mis = numeric_options(rng, T, [(22, "You read the mark above."), (2, "You read the mark below."), (14, "One small division (2 °C) too many.")], unit="°C")
    return dict(
        stem="Fig. 1 shows a laboratory thermometer measuring the temperature of a liquid. What is the temperature?",
        figure=S.thermometer(T),
        options=opts, key=key, misconceptions=mis,
        formula="reading = labelled mark below the liquid level + number of small divisions × 2 °C",
        working=["the labelled marks are 10 °C apart, so each small division is 2 °C", f"the top of the liquid is level with **{T} °C**"],
        hints=["Find the two labelled marks the liquid top lies between.", "There are 5 small divisions between labelled marks, so each one is worth 2 °C.", "Start at the lower labelled mark and add 2 °C for each small division up to the liquid level."],
    )


@template("c10_temperature_rise_table", chapter=10, level=1, lo="10.1")
def temperature_rise_table(rng):
    T0 = nice(rng, 22, 24, 25, 26, 28, 30)
    rise = nice(rng, 8, 12, 15, 18, 25, 32, 45)
    T1 = T0 + rise
    opts, key, mis = numeric_options(rng, rise, [
        (T1, "That is the final temperature. The rise is final − initial."),
        (T1 + T0, "You added the two temperatures. The rise is the DIFFERENCE between them."),
        (rise + 2 if rise + 2 != T1 else rise - 2, "Check the subtraction."),
    ], unit="°C")
    return dict(
        stem=f"A beaker of water is heated. The table shows the thermometer readings.\n\n{md_table(['', 'Temperature / °C'], [['before heating', str(T0)], ['after heating', str(T1)]])}\n\nWhat is the rise in temperature of the water?",
        options=opts, key=key, misconceptions=mis,
        formula="temperature rise = final temperature − initial temperature",
        working=[f"rise = {T1} − {T0}", f"= **{rise} °C**"],
        hints=["A rise is a change: how far did the temperature go up?", "Subtract the starting temperature from the final temperature.", f"{T1} − {T0}."],
    )


@template("c10_celsius_to_kelvin", chapter=10, level=1, lo="10.1")
def celsius_to_kelvin(rng):
    T = nice(rng, 0, 20, 25, 27, 37, 50, 80, 100)
    K = T + 273
    opts, key, mis = numeric_options(rng, K, [
        (T, "That is still in °C. Add 273 to convert to kelvin."),
        (T - 273 if T > 273 else 273 - T, "You subtracted 273. Kelvin values are LARGER than Celsius values: add 273."),
        (K + 100, "Add 273, not 373."),
    ], unit="K")
    return dict(
        stem=f"The table shows the temperature of some objects.\n\n{md_table(['Object', 'Temperature / °C'], [['sample', str(T)]])}\n\nThe SI unit of temperature is the kelvin. What is the temperature of the sample in kelvin? (0 °C = 273 K)",
        options=opts, key=key, misconceptions=mis,
        formula="temperature in K = temperature in °C + 273",
        working=[f"T = {T} + 273", f"= **{K} K**"],
        hints=["0 °C corresponds to 273 on the kelvin scale, and a change of 1 °C is a change of 1 K.", "So every Celsius value is 273 lower than the kelvin value.", f"{T} + 273."],
    )


@template("c10_bar_chart_temp_rise", chapter=10, level=1, lo="10.5")
def bar_chart_temp_rise(rng):
    labels = ["dull black", "shiny silver", "white", "dull grey"]
    rises = [nice(rng, 18, 20, 22, 24), nice(rng, 6, 7, 8, 9), nice(rng, 10, 11, 12), nice(rng, 14, 15, 16)]
    order = list(range(4))
    rng.shuffle(order)
    labels = [labels[i] for i in order]
    rises = [rises[i] for i in order]
    ask = pick(rng, ["largest", "smallest"])
    i = rises.index(max(rises) if ask == "largest" else min(rises))
    correct = labels[i]
    wrongs = {}
    for L, r in zip(labels, rises):
        if L != correct:
            wrongs[L] = f"This can's temperature rose by {r} °C, which is not the {ask} rise."
    opts, key, mis = text_options(rng, correct, wrongs)
    return dict(
        stem=f"Four identical cans with different surfaces were placed the same distance from a heater for 10 minutes. Fig. 1 shows the rise in temperature of the water in each can. Which can had the **{ask}** temperature rise?",
        figure=S.bar_chart(labels, rises, "temperature rise / °C", ymax=30, ystep=5),
        options=opts, key=key, misconceptions=mis,
        formula="read the height of each bar and compare",
        working=["bar heights: " + ", ".join(f"{L} {r} °C" for L, r in zip(labels, rises)), f"{ask} rise = **{correct}**"],
        hints=["Compare the heights of the four bars.", f"Which bar is the {'tallest' if ask == 'largest' else 'shortest'}?", "Read its label on the horizontal axis."],
    )


@template("c10_expansion_table_read", chapter=10, level=1, lo="10.2")
def expansion_table_read(rng):
    L0 = nice(rng, 100.0, 120.0, 150.0, 200.0)
    rows, incs = [], []
    for name, a in rng.sample(SOLIDS, 3):
        inc = round(a * 100 * 1e-6 * L0 * 100, 1)  # for a 100 °C rise, in mm
        rows.append([name, fmt(L0), fmt(L0 + inc / 10, dp=2)])
        incs.append((name, inc))
    pick_name, inc = pick(rng, incs)
    L1 = float([r[2] for r in rows if r[0] == pick_name][0])
    ans = round((L1 - L0) * 10, 1)   # mm
    opts, key, mis = numeric_options(rng, ans, [
        (L1 - L0, "That is the increase in cm. The question asks for millimetres: 1 cm = 10 mm."),
        (L1 * 10, "That is the final length in mm. The INCREASE is final − original."),
        (ans * 10, "Check the conversion: 1 cm = 10 mm, not 100 mm."),
    ], unit="mm", sf=3)
    return dict(
        stem=f"Three rods, each **{fmt(L0)} cm** long at room temperature, were heated by 100 °C and measured again.\n\n{md_table(['Rod', 'Length before / cm', 'Length after / cm'], rows)}\n\nBy how many **millimetres** did the {pick_name} rod expand?",
        options=opts, key=key, misconceptions=mis,
        formula="increase in length = length after − length before; 1 cm = 10 mm",
        working=[f"increase = {fmt(L1, dp=2)} − {fmt(L0)} = {fmt(L1 - L0, sf=3)} cm", f"= {fmt(L1 - L0, sf=3)} × 10 = **{fmt(ans)} mm**"],
        hints=["Find the row for the rod named in the question.", "Subtract the original length from the new length to get the expansion in cm.", "Convert cm to mm by multiplying by 10."],
    )


# ---------------------------------------------------------------- L2
@template("c10_cooling_rate_table", chapter=10, level=2, lo="10.6")
def cooling_rate_table(rng):
    T0 = nice(rng, 80, 85, 90)
    drop_per_min = nice(rng, 2, 3, 4, 5)
    t = nice(rng, 4, 5, 6, 8, 10)
    T1 = T0 - drop_per_min * t
    opts, key, mis = numeric_options(rng, drop_per_min, [
        (T0 - T1, f"That is the total fall over {t} minutes. Rate means the fall PER MINUTE: divide by the time."),
        ((T0 - T1) * t, "You multiplied by the time. Divide the temperature fall by the time."),
        (T1 / t, "You used the final temperature instead of the fall in temperature."),
    ], unit="°C per minute", sf=3)
    return dict(
        stem=f"A cup of hot water cools in a room.\n\n{md_table(['Time / min', 'Temperature / °C'], [['0', str(T0)], [str(t), str(T1)]])}\n\nWhat is the average rate at which the temperature falls?",
        options=opts, key=key, misconceptions=mis,
        formula="rate of cooling = fall in temperature ÷ time taken",
        working=[f"fall = {T0} − {T1} = {T0 - T1} °C", f"rate = {T0 - T1} ÷ {t} = **{drop_per_min} °C per minute**"],
        hints=["First find how many degrees the water cooled in total.", f"Then share that fall equally over the {t} minutes.", f"({T0} − {T1}) ÷ {t}."],
    )


@template("c10_bar_chart_difference", chapter=10, level=2, lo="10.5")
def bar_chart_difference(rng):
    black = nice(rng, 20, 22, 24, 26, 28)
    silver = nice(rng, 6, 8, 9, 10, 12)
    white = nice(rng, 12, 13, 14, 15)
    diff = black - silver
    opts, key, mis = numeric_options(rng, diff, [
        (black, "That is the rise for the black can alone. The question asks how much MORE it rose than the silver can."),
        (black + silver, "You added the two rises. The difference is black − silver."),
        (black - white, "That is black − white. Compare the dull black can with the SHINY SILVER can."),
    ], unit="°C")
    return dict(
        stem="Three identical cans of water with different surfaces were left in the sun for 20 minutes. Fig. 1 shows the temperature rise of each. How much **more** did the water in the dull black can warm up than the water in the shiny silver can?",
        figure=S.bar_chart(["dull black", "shiny silver", "white"], [black, silver, white], "temperature rise / °C", ymax=30, ystep=5),
        options=opts, key=key, misconceptions=mis,
        formula="difference = rise (dull black) − rise (shiny silver)",
        working=[f"dull black: {black} °C; shiny silver: {silver} °C", f"difference = {black} − {silver} = **{diff} °C**"],
        hints=["Read the two bars you are asked to compare.", "'How much more' means subtract.", f"{black} − {silver}."],
    )


@template("c10_graph_read_temperature", chapter=10, level=2, lo="10.6")
def graph_read_temperature(rng):
    T0 = nice(rng, 80, 90)
    k = nice(rng, 0.06, 0.08, 0.1)
    pts = _cooling(T0, 25, k, 20, 2)
    t = nice(rng, 4, 6, 8, 10, 12, 14)
    ans = dict(pts)[t]
    opts, key, mis = numeric_options(rng, ans, [
        (dict(pts)[t + 2], "You read the temperature 2 minutes too late. Find the exact time on the horizontal axis first."),
        (dict(pts)[t - 2], "You read the temperature 2 minutes too early."),
        (T0 - ans, "That is the FALL in temperature since the start, not the temperature at that time."),
    ], unit="°C", sf=3)
    return dict(
        stem=f"Fig. 1 shows how the temperature of a cup of tea changes as it cools in a room. What is the temperature of the tea after **{t} minutes**?",
        figure=figs.graph(pts, 20, 100, 4, 20, xlabel="time / min", ylabel="temperature / °C"),
        options=opts, key=key, misconceptions=mis,
        formula="read the graph: time on the x-axis → up to the curve → across to the temperature axis",
        working=[f"at t = {t} min, go up to the curve and across", f"temperature = **{ans} °C**"],
        hints=["Find the given time on the horizontal axis.", "Go straight up to the curve, then straight across to the temperature axis.", "Each small square on the temperature axis is 4 °C."],
    )


@template("c10_density_after_expansion", chapter=10, level=2, lo="10.2")
def density_after_expansion(rng):
    m = nice(rng, 200, 400, 500, 800, 1000)
    V0 = nice(rng, 200, 250, 400, 500)
    V1 = V0 + nice(rng, 10, 20, 25, 50)
    rho1 = m / V1
    opts, key, mis = numeric_options(rng, rho1, [
        (m / V0, "That is the density BEFORE heating. The volume has increased, so use the new volume."),
        (V1 / m, "You divided the wrong way round. Density = mass ÷ volume."),
        (m * V1, "You multiplied. Density = mass ÷ volume."),
    ], unit="g/cm³", sf=3)
    return dict(
        stem=f"When a liquid is heated it expands but its mass stays the same.\n\n{md_table(['', 'Mass / g', 'Volume / cm³'], [['before heating', str(m), str(V0)], ['after heating', str(m), str(V1)]])}\n\nWhat is the density of the liquid **after** heating?",
        options=opts, key=key, misconceptions=mis,
        formula="density = mass ÷ volume; expansion increases volume, so density decreases",
        working=[f"density after = {m} ÷ {V1}", f"= **{fmt(rho1)} g/cm³** (less than before, {fmt(m / V0)} g/cm³)"],
        hints=["Density = mass ÷ volume. Which row of the table is 'after heating'?", "The mass has not changed, but the volume is larger.", f"{m} ÷ {V1}."],
    )


@template("c10_kelvin_table_difference", chapter=10, level=2, lo="10.1")
def kelvin_table_difference(rng):
    T_c = nice(rng, 15, 20, 25, 30)
    T_k = nice(rng, 300, 310, 320, 330, 350)
    ans = T_k - 273 - T_c
    opts, key, mis = numeric_options(rng, ans, [
        (T_k - T_c, "You subtracted a Celsius value from a kelvin value directly. Convert to the same unit first (K − 273 = °C)."),
        (T_k - 273, "That is Q's temperature in °C, not the difference between P and Q."),
        (T_c + 273 - T_k if T_c + 273 - T_k > 0 else ans + 273, "Convert Q to °C (subtract 273), then subtract P."),
    ], unit="°C", sf=3)
    return dict(
        stem=f"Two objects have their temperatures recorded in different units.\n\n{md_table(['Object', 'Temperature'], [['P', f'{T_c} °C'], ['Q', f'{T_k} K']])}\n\nHow much hotter is Q than P, in °C? (0 °C = 273 K)",
        options=opts, key=key, misconceptions=mis,
        formula="°C = K − 273; then difference = Q − P",
        working=[f"Q = {T_k} − 273 = {T_k - 273} °C", f"difference = {T_k - 273} − {T_c} = **{ans} °C**"],
        hints=["The two temperatures are in different units. Put them both in °C first.", "K − 273 gives °C.", f"({T_k} − 273) − {T_c}."],
    )


# ---------------------------------------------------------------- L3
@template("c10_graph_average_rate", chapter=10, level=3, lo="10.6")
def graph_average_rate(rng):
    T0 = nice(rng, 80, 90)
    k = nice(rng, 0.06, 0.08, 0.1)
    pts = _cooling(T0, 25, k, 20, 2)
    t1, t2 = pick(rng, [(0, 4), (0, 10), (2, 8), (4, 12), (6, 16), (10, 20)])
    d = dict(pts)
    ans = (d[t1] - d[t2]) / (t2 - t1)
    opts, key, mis = numeric_options(rng, ans, [
        (d[t1] - d[t2], "That is the total fall in temperature. Divide by the time interval to get the RATE."),
        ((d[t1] - d[t2]) / t2 if t1 else (d[t1] - d[t2]) / (t2 - t1) * 2, f"Divide by the time INTERVAL, {t2} − {t1} = {t2 - t1} min."),
        (d[t2] / (t2 - t1), "You used the final temperature rather than the fall in temperature."),
    ], unit="°C per minute", sf=3)
    return dict(
        stem=f"Fig. 1 shows the cooling curve of a cup of coffee. What is the average rate of cooling between **{t1} min and {t2} min**?",
        figure=figs.graph(pts, 20, 100, 4, 20, xlabel="time / min", ylabel="temperature / °C"),
        options=opts, key=key, misconceptions=mis,
        formula="average rate of cooling = (temperature at start − temperature at end) ÷ time interval",
        working=[f"at {t1} min: {d[t1]} °C; at {t2} min: {d[t2]} °C", f"fall = {d[t1] - d[t2]} °C over {t2 - t1} min", f"rate = {d[t1] - d[t2]} ÷ {t2 - t1} = **{fmt(ans)} °C per minute**"],
        hints=["Read the temperature at both times from the curve.", "Rate = fall in temperature ÷ time taken for that fall.", f"(T at {t1} − T at {t2}) ÷ {t2 - t1}."],
    )


@template("c10_two_curves_compare", chapter=10, level=3, lo="10.6")
def two_curves_compare(rng):
    T0 = 90
    kP, kQ = pick(rng, [(0.1, 0.05), (0.12, 0.06), (0.09, 0.04)])
    P = _cooling(T0, 25, kP, 20, 2)
    Q = _cooling(T0, 25, kQ, 20, 2)
    t = nice(rng, 6, 8, 10, 12, 16)
    diff = dict(Q)[t] - dict(P)[t]
    opts, key, mis = numeric_options(rng, diff, [
        (dict(P)[t], "That is P's temperature. The question asks for the DIFFERENCE between Q and P."),
        (dict(Q)[t], "That is Q's temperature. Subtract P's temperature from it."),
        (T0 - dict(P)[t], "That is how far P has cooled since the start, not the gap between the two cups."),
    ], unit="°C", sf=3)
    return dict(
        stem=f"Fig. 1 shows the cooling curves of two identical cups of water: cup P is uncovered and cup Q has a lid. How much **hotter** is the water in Q than in P after **{t} minutes**?",
        figure=S.xy_graph([("P (no lid)", P), ("Q (with lid)", Q)], "time / min", "temperature / °C", 20, 100, 4, 20),
        options=opts, key=key, misconceptions=mis,
        formula="difference = temperature of Q − temperature of P at the same time",
        working=[f"at {t} min: Q = {dict(Q)[t]} °C, P = {dict(P)[t]} °C", f"difference = {dict(Q)[t]} − {dict(P)[t]} = **{diff} °C**"],
        hints=["Find the given time, then read BOTH curves at that time.", "The cup with the lid loses heat more slowly, so it stays hotter.", f"Q at {t} min − P at {t} min."],
    )


@template("c10_expansion_percent", chapter=10, level=3, lo="10.2")
def expansion_percent(rng):
    L0 = nice(rng, 50, 80, 100, 120, 200)   # m (a bridge section)
    pct = nice(rng, 0.1, 0.2, 0.25, 0.5)
    inc = L0 * pct / 100
    ans_cm = inc * 100
    opts, key, mis = numeric_options(rng, ans_cm, [
        (inc, "That is the increase in metres. The question asks for centimetres: multiply by 100."),
        (L0 * pct, f"You found {pct}% as {pct} × {L0}. A percentage must be divided by 100 first."),
        ((L0 + inc) * 100, "That is the whole length in cm. The gap only needs to allow for the INCREASE."),
    ], unit="cm", sf=3)
    return dict(
        stem=f"A steel bridge section is **{L0} m** long in the morning. By afternoon it has expanded by **{fmt(pct)}%** of its length. The table shows the data.\n\n{md_table(['Quantity', 'Value'], [['length in the morning', f'{L0} m'], ['expansion', f'{fmt(pct)}% of length']])}\n\nWhat is the minimum gap, in **cm**, that must be left at one end for the expansion?",
        options=opts, key=key, misconceptions=mis,
        formula="increase = percentage ÷ 100 × original length; 1 m = 100 cm",
        working=[f"increase = {fmt(pct)} ÷ 100 × {L0} = {fmt(inc)} m", f"= {fmt(inc)} × 100 = **{fmt(ans_cm)} cm**"],
        hints=["Work out the increase in length first: a percentage of the original length.", f"{fmt(pct)}% means {fmt(pct)} out of every 100 m.", "Convert the answer from metres to centimetres."],
    )


@template("c10_density_change_percent", chapter=10, level=3, lo="10.2")
def density_change_percent(rng):
    m = nice(rng, 500, 800, 1000, 1200)
    V0 = nice(rng, 500, 800, 1000)
    pct = nice(rng, 2, 4, 5, 10, 20, 25)
    V1 = V0 * (100 + pct) / 100
    rho1 = m / V1
    opts, key, mis = numeric_options(rng, rho1, [
        (m / V0, "That is the original density. The volume has grown, so the density is now smaller."),
        (m / V0 * (100 + pct) / 100, "Density goes DOWN when volume goes up: divide by the new, larger volume."),
        (m / (V0 * pct / 100), "You divided by the INCREASE in volume. Use the whole new volume."),
    ], unit="g/cm³", sf=3)
    return dict(
        stem=f"A block of wax has a mass of **{m} g** and a volume of **{V0} cm³**. On warming, its volume increases by **{pct}%** while its mass stays the same. Fig. 1 shows the particles before and after warming. What is its density after warming?",
        figure=S.particles("solid", label="before: particles closer"),
        options=opts, key=key, misconceptions=mis,
        formula="new volume = original × (100 + %) ÷ 100; density = mass ÷ new volume",
        working=[f"new volume = {V0} × {100 + pct}/100 = {fmt(V1)} cm³", f"density = {m} ÷ {fmt(V1)} = **{fmt(rho1)} g/cm³**"],
        hints=["First find the new volume: the old volume plus the percentage increase.", "The particles move further apart on heating, so the same mass fills more space.", f"density = {m} ÷ ({V0} × {100 + pct}/100)."],
    )


@template("c10_conduction_times_table", chapter=10, level=3, lo="10.3")
def conduction_times_table(rng):
    mats = rng.sample([("copper", 40), ("aluminium", 55), ("iron", 95), ("glass", 400), ("steel", 120)], 3)
    rows = [[m, str(t)] for m, t in mats]
    fastest = min(mats, key=lambda x: x[1])
    slowest = max(mats, key=lambda x: x[1])
    ratio = slowest[1] / fastest[1]
    opts, key, mis = numeric_options(rng, ratio, [
        (fastest[1] / slowest[1], "You divided the small time by the large time. 'How many times longer' means long time ÷ short time."),
        (slowest[1] - fastest[1], "That is the difference in seconds, not how many TIMES longer."),
        (ratio * 2, "Check the division: longest time ÷ shortest time."),
    ], unit="times", sf=3)
    return dict(
        stem=f"Three rods of the same size have a drawing pin stuck to one end with wax. The other ends are heated equally (Fig. 1). The table shows the time for each pin to drop.\n\n{md_table(['Rod', 'Time for pin to drop / s'], rows)}\n\nHow many times longer does heat take to travel along the **{slowest[0]}** rod than along the **{fastest[0]}** rod?",
        figure=S.rod_conduction([m for m, _ in mats], [5.5 - 4.5 * (t - fastest[1]) / (slowest[1] - fastest[1] + 1) for _, t in mats]),
        options=opts, key=key, misconceptions=mis,
        formula="number of times longer = longer time ÷ shorter time",
        working=[f"{slowest[0]}: {slowest[1]} s; {fastest[0]}: {fastest[1]} s", f"{slowest[1]} ÷ {fastest[1]} = **{fmt(ratio)} times**"],
        hints=["The pin drops when heat conducted along the rod melts the wax. A longer time means a poorer conductor.", "Pick out the two times named in the question.", f"Divide the {slowest[0]} time by the {fastest[0]} time."],
    )


# ---------------------------------------------------------------- L4
@template("c10_graph_time_to_reach", chapter=10, level=4, lo="10.6")
def graph_time_to_reach(rng):
    kP, kQ = pick(rng, [(0.1, 0.05), (0.12, 0.06)])
    P = _cooling(90, 25, kP, 20, 2)
    Q = _cooling(90, 25, kQ, 20, 2)
    cup = pick(rng, ["P", "Q"])
    pts = P if cup == "P" else Q
    target_idx = rng.randint(2, 7)
    t_ans, T_target = pts[target_idx]
    other = Q if cup == "P" else P
    # time when other cup reaches the same temperature (interpolated to nearest 2 min)
    t_other = next((t for t, T in other if T <= T_target), 20)
    opts, key, mis = numeric_options(rng, t_ans, [
        (t_other, f"That is the time for the OTHER cup to reach {T_target} °C. Follow the curve for cup {cup}."),
        (T_target, "That is the temperature, not the time. Go from the temperature across to the curve, then DOWN to the time axis."),
        (t_ans + 2, "You read 2 minutes too far. Check where the curve crosses the temperature line."),
    ], unit="min", sf=3)
    return dict(
        stem=f"Fig. 1 shows the cooling curves of two cups of water. Cup P has no lid, cup Q has a lid. How long does cup **{cup}** take to cool to **{T_target} °C**?",
        figure=S.xy_graph([("P (no lid)", P), ("Q (with lid)", Q)], "time / min", "temperature / °C", 20, 100, 4, 20),
        options=opts, key=key, misconceptions=mis,
        formula="read the graph: temperature on the y-axis → across to the correct curve → down to the time axis",
        working=[f"find {T_target} °C on the vertical axis and move across to curve {cup}", f"the time below that point is **{t_ans} min**"],
        hints=["Start on the TEMPERATURE axis this time.", f"Move across until you meet the curve for cup {cup} (check the legend), then go straight down.", "Each small square on the time axis is 0.8 of a minute; the labelled marks are four minutes apart."],
    )


@template("c10_heating_graph_time_for_rise", chapter=10, level=4, lo="10.6")
def heating_graph_time_for_rise(rng):
    rate = nice(rng, 4, 5, 6, 8)      # °C per min
    T0 = nice(rng, 20, 24, 30)
    pts = [(0, T0), (10, T0 + rate * 10)]
    rise = nice(rng, 12, 16, 20, 24, 30, 32, 40)
    rise = min(rise, rate * 10 - 4)
    ans = rise / rate
    opts, key, mis = numeric_options(rng, ans, [
        (rise, "That is the temperature rise in °C, not the time."),
        ((T0 + rise) / rate, "You used the final temperature instead of the RISE. Time = rise ÷ rate of heating."),
        (rate, "That is the rate of heating (°C per minute), not the time taken."),
    ], unit="min", sf=3)
    return dict(
        stem=f"Fig. 1 shows the temperature of water in a kettle while it is being heated. How long does it take for the temperature to rise by **{rise} °C**?",
        figure=figs.graph(pts, 10, T0 + rate * 10 + 10, 2, 20, xlabel="time / min", ylabel="temperature / °C"),
        options=opts, key=key, misconceptions=mis,
        formula="rate of heating = gradient of the graph; time = temperature rise ÷ rate",
        working=[f"gradient = ({T0 + rate * 10} − {T0}) ÷ 10 = {rate} °C per minute", f"time for a {rise} °C rise = {rise} ÷ {rate} = **{fmt(ans)} min**"],
        hints=["The graph is a straight line, so the temperature rises steadily. Find how many °C it rises each minute.", f"Gradient = rise ÷ run over the whole line.", f"time = {rise} ÷ (°C per minute)."],
    )


@template("c10_house_heat_loss_percent", chapter=10, level=4, lo="10.6")
def house_heat_loss_percent(rng):
    parts = ["roof", "walls", "windows", "floor", "draughts"]
    pcts = [nice(rng, 25, 30), nice(rng, 30, 35), nice(rng, 10, 15), 10, None]
    pcts[4] = 100 - sum(p for p in pcts if p)
    total = nice(rng, 2000, 4000, 5000, 8000)   # J per second lost
    i = rng.randint(0, 4)
    ans = total * pcts[i] / 100
    opts, key, mis = numeric_options(rng, ans, [
        (pcts[i], "That is the percentage. The question asks for the energy, so take that percentage OF the total."),
        (total / 5, "The five parts are not equal shares. Use the percentage shown for the part asked about."),
        (total * (100 - pcts[i]) / 100, f"That is the heat lost through everything EXCEPT the {parts[i]}."),
    ], unit="J per second", sf=3)
    return dict(
        stem=f"Fig. 1 shows the percentage of heat lost from a house through different parts. The house loses **{total} J** of heat every second in total. How much heat is lost every second through the **{parts[i]}**?",
        figure=S.pie_chart([f"{p} ({v}%)" for p, v in zip(parts, pcts)], pcts),
        options=opts, key=key, misconceptions=mis,
        formula="energy through a part = its percentage ÷ 100 × total energy",
        working=[f"{parts[i]}: {pcts[i]}% of {total} J", f"= {pcts[i]}/100 × {total} = **{fmt(ans)} J per second**"],
        hints=[f"Find the slice for the {parts[i]} and read its percentage.", "A percentage is 'out of 100'. Apply it to the total heat lost.", f"{pcts[i]}/100 × {total}."],
    )


@template("c10_graph_insulation_compare", chapter=10, level=4, lo="10.3")
def graph_insulation_compare(rng):
    mats = [("no wrapping", 0.11), ("newspaper", 0.07), ("wool", 0.04)]
    curves = [(n, _cooling(80, 25, k, 20, 2)) for n, k in mats]
    t = nice(rng, 8, 10, 12, 16, 20)
    d = {n: dict(c) for n, c in curves}
    ans = d["wool"][t] - d["no wrapping"][t]
    opts, key, mis = numeric_options(rng, ans, [
        (d["wool"][t], "That is the wool beaker's temperature, not how much warmer it is than the unwrapped one."),
        (d["newspaper"][t] - d["no wrapping"][t], "That is the gap between NEWSPAPER and no wrapping. The question asks about wool."),
        (80 - d["wool"][t], "That is how far the wool beaker has cooled since the start."),
    ], unit="°C", sf=3)
    return dict(
        stem=f"Three identical beakers of hot water were wrapped in different materials. Fig. 1 shows their cooling curves. After **{t} minutes**, how much warmer is the water in the **wool** beaker than in the **unwrapped** beaker?",
        figure=S.xy_graph(curves, "time / min", "temperature / °C", 20, 100, 4, 20),
        options=opts, key=key, misconceptions=mis,
        formula="difference = temperature (wool) − temperature (no wrapping) at the same time",
        working=[f"at {t} min: wool = {d['wool'][t]} °C, no wrapping = {d['no wrapping'][t]} °C", f"difference = **{ans} °C**"],
        hints=["Use the legend to pick out the two curves you need.", "Read both at the same time, then subtract.", "Wool traps air, a poor conductor, so that beaker stays hottest."],
    )


@template("c10_bar_chart_conductors_rank", chapter=10, level=4, lo="10.3")
def bar_chart_conductors_rank(rng):
    mats = rng.sample([("copper", 95), ("aluminium", 80), ("iron", 45), ("glass", 8), ("plastic", 5), ("wood", 4)], 4)
    labels = [m for m, _ in mats]
    vals = [v for _, v in mats]
    ask = pick(rng, ["best", "poorest"])
    correct = labels[vals.index(max(vals) if ask == "best" else min(vals))]
    wrongs = {L: f"The bar for {L} shows a temperature rise of {v} °C, so it is not the {ask} conductor." for L, v in zip(labels, vals) if L != correct}
    opts, key, mis = text_options(rng, correct, wrongs)
    return dict(
        stem=f"Rods of four materials were heated at one end for 5 minutes and the temperature rise at the other end was measured. Fig. 1 shows the results. Which material is the **{ask}** conductor of heat?",
        figure=S.bar_chart(labels, vals, "temperature rise at far end / °C", ymax=100, ystep=20),
        options=opts, key=key, misconceptions=mis,
        formula="a bigger temperature rise at the far end means heat was conducted faster",
        working=["temperature rises: " + ", ".join(f"{L} {v} °C" for L, v in zip(labels, vals)), f"{ask} conductor = **{correct}**"],
        hints=["Heat travels along a good conductor quickly, so its far end gets hot.", f"Which bar is the {'tallest' if ask == 'best' else 'shortest'}?", "Metals conduct well; non-metals conduct poorly."],
    )


# ---------------------------------------------------------------- L5
@template("c10_rail_gap_total", chapter=10, level=5, lo="10.2")
def rail_gap_total(rng):
    per_deg = nice(rng, 0.2, 0.25, 0.3)    # mm per °C for one rail
    dT = nice(rng, 20, 25, 30, 40)
    n = nice(rng, 5, 8, 10, 12)
    one = per_deg * dT
    total = one * n
    opts, key, mis = numeric_options(rng, total, [
        (one, "That is the expansion of ONE rail. The question asks for the total for all the rails laid end to end."),
        (per_deg * n, "You forgot the temperature rise. Expansion = mm per °C × number of °C, then × the number of rails."),
        (total / 10, "Check the units: the expansion is already in mm."),
    ], unit="mm", sf=3)
    return dict(
        stem=f"Each steel rail on a track expands by **{fmt(per_deg)} mm for every 1 °C** rise in temperature.\n\n{md_table(['Quantity', 'Value'], [['expansion per rail per °C', f'{fmt(per_deg)} mm'], ['temperature rise (night to afternoon)', f'{dT} °C'], ['number of rails in the section', str(n)]])}\n\nWhat total expansion must the gaps in this section allow for?",
        options=opts, key=key, misconceptions=mis,
        formula="expansion of one rail = expansion per °C × temperature rise; total = one rail × number of rails",
        working=[f"one rail: {fmt(per_deg)} × {dT} = {fmt(one)} mm", f"{n} rails: {fmt(one)} × {n} = **{fmt(total)} mm**"],
        hints=["Start with one rail: how much does it expand for the whole temperature rise?", f"Then there are {n} rails, each expanding by the same amount.", f"{fmt(per_deg)} × {dT} × {n}."],
    )


@template("c10_cooling_rate_start_vs_end", chapter=10, level=5, lo="10.5")
def cooling_rate_start_vs_end(rng):
    pts = _cooling(90, 25, nice(rng, 0.1, 0.12), 20, 2)
    d = dict(pts)
    r1 = (d[0] - d[4]) / 4
    r2 = (d[16] - d[20]) / 4
    ratio = r1 / r2
    opts, key, mis = numeric_options(rng, ratio, [
        (r1, "That is the rate at the start in °C per minute. The question asks how many TIMES faster it is than at the end."),
        (r2 / r1, "You divided the slow rate by the fast rate. 'Times faster' = fast rate ÷ slow rate."),
        (r1 - r2, "That is the difference between the rates, not the ratio."),
    ], unit="times", sf=2)
    return dict(
        stem="Fig. 1 shows the cooling curve of hot water in a room. Compare the average rate of cooling in the **first 4 minutes** with the average rate in the **last 4 minutes** (16–20 min). How many times faster is the cooling at the start?",
        figure=figs.graph(pts, 20, 100, 4, 20, xlabel="time / min", ylabel="temperature / °C"),
        options=opts, key=key, misconceptions=mis,
        formula="rate = fall ÷ time for each interval; ratio = rate at start ÷ rate at end",
        working=[f"0–4 min: ({d[0]} − {d[4]}) ÷ 4 = {fmt(r1)} °C/min", f"16–20 min: ({d[16]} − {d[20]}) ÷ 4 = {fmt(r2)} °C/min", f"ratio = {fmt(r1)} ÷ {fmt(r2)} = **{fmt(ratio, sf=2)} times**"],
        hints=["Work out the temperature fall in each 4-minute interval from the curve.", "The curve is steep at first (big temperature difference with the room) and flat later.", "Divide the early rate by the late rate."],
    )


@template("c10_fair_test_table", chapter=10, level=5, lo="10.5")
def fair_test_table(rng):
    rows = [["P", "dull black", "200", "10"], ["Q", "shiny silver", "200", "10"], ["R", "dull black", "400", "10"], ["S", "shiny silver", "200", "20"]]
    rng.shuffle(rows)
    labels = [r[0] for r in rows]
    # the valid comparison for surface colour: same volume and distance, different colour -> P and Q
    opts, key, mis = text_options(rng, "P and Q", {
        "P and R": "P and R have the same surface but different volumes of water. That tests volume, not surface colour.",
        "Q and S": "Q and S have the same surface but different distances from the heater. Only ONE variable should change.",
        "R and S": "R and S differ in colour, volume AND distance, so you cannot tell which change caused the result.",
    })
    return dict(
        stem=f"A student wants to find out whether a dull black surface absorbs radiation faster than a shiny silver one. Four cans were set up as in the table.\n\n{md_table(['Can', 'Surface', 'Volume of water / cm³', 'Distance from heater / cm'], rows)}\n\nWhich two cans should be compared for a **fair test**?",
        options=opts, key=key, misconceptions=mis,
        formula="fair test: change only the variable being investigated; keep every other variable the same",
        working=["the variable being tested is the surface", "P and Q differ only in surface (same volume, same distance)", "**P and Q**"],
        hints=["Only the SURFACE should be different between the two cans you compare.", "Check volume and distance: they must match.", "Find the pair that differs in one column only."],
    )


@template("c10_density_mass_volume_trap", chapter=10, level=5, lo="10.2")
def density_mass_volume_trap(rng):
    rho0 = nice(rng, 0.8, 0.9, 1.0, 1.2)
    V0 = nice(rng, 200, 250, 500)
    m = rho0 * V0
    pct = nice(rng, 4, 5, 8, 10)
    V1 = V0 * (100 + pct) / 100
    rho1 = m / V1
    opts, key, mis = numeric_options(rng, rho1, [
        (rho0, "The density changes: the same mass now occupies a larger volume."),
        (rho0 * (100 - pct) / 100, f"Reducing the density by {pct}% is not the same as increasing the volume by {pct}%. Recalculate with mass ÷ new volume."),
        (m / (V1 - V0), "You divided by the CHANGE in volume. Use the whole new volume."),
    ], unit="g/cm³", sf=3)
    return dict(
        stem=f"A liquid has a density of **{fmt(rho0)} g/cm³** and fills a **{V0} cm³** flask. Fig. 1 shows the particles as the liquid is warmed; its volume increases by **{pct}%** and the mass does not change. What is the new density?",
        figure=S.particles("liquid", label="liquid: particles spread out on heating"),
        options=opts, key=key, misconceptions=mis,
        formula="mass = density × volume (unchanged); new density = mass ÷ new volume",
        working=[f"mass = {fmt(rho0)} × {V0} = {fmt(m)} g", f"new volume = {V0} × {100 + pct}/100 = {fmt(V1)} cm³", f"new density = {fmt(m)} ÷ {fmt(V1)} = **{fmt(rho1)} g/cm³**"],
        hints=["You are not told the mass directly, but you can find it from the original density and volume.", "Mass does not change on heating; volume does.", f"new density = ({fmt(rho0)} × {V0}) ÷ ({V0} × {100 + pct}/100)."],
    )


@template("c10_temperature_change_units", chapter=10, level=5, lo="10.1")
def temperature_change_units(rng):
    T0 = nice(rng, 290, 295, 300, 305)   # K
    rise = nice(rng, 12, 15, 20, 25, 30)
    T1c = T0 - 273 + rise
    opts, key, mis = numeric_options(rng, T1c, [
        (T0 + rise, "That is the final temperature in kelvin. The question asks for °C: subtract 273."),
        (T0 - 273, "That is the STARTING temperature in °C. Add the rise."),
        (T0 + rise - 273 - 100 if T0 + rise - 273 - 100 > 0 else T1c + 10, "Check your conversion: K − 273 = °C."),
    ], unit="°C", sf=3)
    return dict(
        stem=f"A metal block starts at **{T0} K**. It is heated so that its temperature rises by **{rise} °C**.\n\n{md_table(['Quantity', 'Value'], [['starting temperature', f'{T0} K'], ['rise in temperature', f'{rise} °C']])}\n\nWhat is its final temperature in **°C**? (A rise of 1 °C is the same as a rise of 1 K.)",
        options=opts, key=key, misconceptions=mis,
        formula="°C = K − 273; a temperature CHANGE has the same number in °C and K",
        working=[f"start = {T0} − 273 = {T0 - 273} °C", f"final = {T0 - 273} + {rise} = **{T1c} °C**"],
        hints=["Convert the starting temperature to °C first.", "A rise of 1 K equals a rise of 1 °C, so the rise needs no conversion.", f"({T0} − 273) + {rise}."],
    )


# ================================================================ EXPLANATION
EXPLAIN = [
    # ------------------------------------------------------------ L1
    dict(id="e10_si_unit_temperature", level=1, lo="10.1",
         stem="Fig. 1 shows a thermometer. What is the SI unit of temperature?",
         correct="kelvin (K)",
         wrongs={"degree Celsius (°C)": "°C is the everyday unit marked on most thermometers, but the SI unit is a different one.",
                 "joule (J)": "The joule is the unit of energy (heat), not temperature.", "watt (W)": "The watt is the unit of power."},
         hints=["Temperature is not the same as heat energy, so its unit is not the joule.", "The thermometer in Fig. 1 is marked in °C, but SI uses a scale that starts at absolute zero.", "0 °C = 273 ____."],
         fig=lambda rng: S.thermometer(rng.choice([24, 36, 60]))),
    dict(id="e10_conduction_definition", level=1, lo="10.3",
         stem="Fig. 1 shows heat travelling along a metal rod. Conduction is the transfer of heat",
         correct="through a material by vibrating particles passing energy to their neighbours, without the material moving",
         wrongs={"by the movement of a heated liquid or gas": "That is convection, which needs a fluid to move.",
                 "by waves that can travel through a vacuum": "That is radiation.",
                 "only through liquids and gases": "Conduction happens mainly in SOLIDS, especially metals."},
         hints=["In a solid the particles cannot move from place to place, but they can vibrate.", "The hot end's particles vibrate more and bump their neighbours.", "Energy is passed on particle to particle; the rod itself stays still."],
         fig=lambda rng: S.rod_conduction(["metal rod"], [4.5])),
    dict(id="e10_convection_fluids_only", level=1, lo="10.4",
         stem="Fig. 1 shows a convection current in a room. Convection can take place in",
         correct="liquids and gases only",
         wrongs={"solids only": "Particles in a solid cannot flow, so there can be no convection current.",
                 "solids, liquids and gases": "Convection needs the material itself to move, which solids cannot do.",
                 "a vacuum": "A vacuum has no particles at all, so no convection (or conduction) can occur."},
         hints=["Convection is the movement of the heated material itself.", "Which states of matter can flow?", "Liquids and gases are called fluids."],
         fig=lambda rng: S.room_heater("floor")),
    dict(id="e10_radiation_no_medium", level=1, lo="10.5",
         stem="Fig. 1 shows a vacuum flask. Which method of heat transfer can pass through a vacuum?",
         correct="radiation",
         wrongs={"conduction": "Conduction needs particles to pass energy along; a vacuum has none.",
                 "convection": "Convection needs a fluid to move; a vacuum has no particles.",
                 "conduction and convection": "Neither can occur without particles."},
         hints=["Heat from the Sun reaches the Earth across empty space.", "Which method does not need particles?", "Infra-red ____ travels through a vacuum."],
         fig=lambda rng: S.flask()),
    dict(id="e10_heat_flow_direction", level=1, lo="10.1",
         stem="The table shows two objects placed in contact.\n\n| Object | Temperature / °C |\n|---|---|\n| metal spoon | 20 |\n| hot soup | 70 |\n\nIn which direction does heat flow?",
         correct="from the soup to the spoon, until both are at the same temperature",
         wrongs={"from the spoon to the soup, because metals conduct well": "Good conductors carry heat quickly, but heat still flows from HOT to COLD.",
                 "in both directions equally": "There is a net flow from the hotter object to the colder one.",
                 "no heat flows because they are in contact": "Contact is exactly what lets heat flow by conduction."},
         hints=["Heat always flows from a hotter object to a colder one.", "Which object is hotter in the table?", "Flow stops when the temperatures are equal."]),

    # ------------------------------------------------------------ L2
    dict(id="e10_identify_transfer_method", level=2, lo="10.6",
         hints=["Conduction: through a solid in contact. Convection: a fluid moves. Radiation: no contact and no fluid needed.", "Is anything touching? Is a liquid or gas moving? Or is heat arriving across a gap?", "Match the description to one method."],
         fig=lambda rng: S.room_heater("floor"),
         variants=[
             dict(stem="Fig. 1 shows a heater warming a room. The air above the heater rises and spreads across the ceiling. This is mainly",
                  correct="convection", wrongs={"conduction": "Air is a poor conductor; the warmth spreads because the AIR MOVES.", "radiation": "Radiation does not need the air to move.", "evaporation": "No liquid is turning into vapour here."}),
             dict(stem="Fig. 1 shows a room with a heater. You feel warmth on your face when you stand in front of a glowing electric heater, even though the air between is not yet warm. The heat reaches you mainly by",
                  correct="radiation", wrongs={"conduction": "Air is a poor conductor and you are not touching the heater.", "convection": "Warm air rises; it does not travel sideways to your face in a straight line.", "expansion": "Expansion is an effect of heating, not a method of transfer."}),
             dict(stem="Fig. 1 shows a heated room. A metal spoon left in a pot of hot soup becomes hot at the handle. Heat travels along the spoon by",
                  correct="conduction", wrongs={"convection": "The spoon is a solid; its particles cannot flow.", "radiation": "Radiation does not travel along inside a solid rod.", "insulation": "Insulation reduces heat transfer; it is not a method of transfer."}),
         ]),
    dict(id="e10_classify_conductor", level=2, lo="10.3",
         stem="The table shows the time for heat to travel along rods of different materials.\n\n| Material | Time for wax to melt / s |\n|---|---|\n| copper | 40 |\n| iron | 95 |\n| glass | 400 |\n| plastic | 600 |\n\nWhich material is the best **insulator**?",
         correct="plastic",
         wrongs={"copper": "Copper let the heat through fastest: it is the best CONDUCTOR.", "iron": "Iron is a metal and conducts well.", "glass": "Glass is a poor conductor, but plastic took even longer."},
         hints=["An insulator is a poor conductor of heat.", "Which material let the heat through most slowly?", "Longest time = best insulator."]),
    dict(id="e10_identify_absorber_surface", level=2, lo="10.5",
         stem="Fig. 1 shows two cans placed near a heater. Which surface is the **best absorber** of radiation?",
         correct="dull black",
         wrongs={"shiny silver": "Shiny silver surfaces reflect most radiation: they are POOR absorbers.", "shiny white": "Light, shiny surfaces reflect radiation.", "polished metal": "Polished surfaces are good reflectors and poor absorbers."},
         hints=["Think about which colour of car gets hottest in the sun.", "Dark, dull surfaces take in radiation; light, shiny ones reflect it.", "Dull + dark = good absorber (and good emitter)."],
         fig=lambda rng: S.cans(["P", "Q"], ["dull black", "shiny silver"], heater=True)),
    dict(id="e10_identify_expansion_application", level=2, lo="10.2",
         hints=["Expansion: things get bigger when heated. Contraction: smaller when cooled.", "Which examples leave room for a change in size, or use a change in size?", "Think about what would happen on a hot day without the feature."],
         fig=lambda rng: S.bimetallic("none", heated=False),
         variants=[
             dict(stem="Fig. 1 shows a bimetallic strip. Which of the following is an application of thermal **expansion**?",
                  correct="a bimetallic strip in a fire alarm", wrongs={"a vacuum flask keeping tea hot": "That uses a vacuum to stop conduction and convection.", "a shiny kettle": "That reduces heat loss by radiation.", "a wooden spoon handle": "Wood is a poor conductor; nothing expands usefully here."}),
             dict(stem="Fig. 1 shows a bimetallic strip. Which of the following is a **problem** caused by thermal expansion?",
                  correct="railway tracks buckling on a very hot day", wrongs={"ice forming on a cold window": "That is freezing, a change of state.", "a cup of tea going cold": "That is heat loss by conduction, convection and radiation.", "a balloon sinking as the gas leaks out": "That is a loss of gas, not expansion."}),
         ]),
    dict(id="e10_which_state_expands_most", level=2, lo="10.2",
         stem="Fig. 1 shows the particles in a gas. For the same rise in temperature, which expands the most?",
         correct="a gas",
         wrongs={"a solid": "Solid particles are held tightly in place and move apart only a little.", "a liquid": "Liquids expand more than solids but much less than gases.", "they all expand by the same amount": "The three states expand by very different amounts."},
         hints=["In which state are the particles most free to move?", "Gas particles are far apart and move fast; heating speeds them up and they spread much further.", "Order: solids expand least, then liquids, then ____."],
         fig=lambda rng: S.particles("gas", label="gas")),

    # ------------------------------------------------------------ L3
    dict(id="e10_bimetallic_bend", level=3, lo="10.2",
         stem="Fig. 1 shows a bimetallic strip made of brass (top) and iron (bottom). Brass expands more than iron when heated. When the strip is heated it bends",
         correct="downwards, towards the iron, because the brass becomes longer than the iron",
         wrongs={"upwards, towards the brass, because the brass expands more": "The metal that expands MORE ends up on the OUTSIDE of the curve, so the strip bends away from the brass.",
                 "it stays straight because both metals are heated equally": "Equal heating still gives unequal expansion, because the metals are different.",
                 "downwards, because iron contracts when heated": "Iron also expands when heated, just less than brass."},
         hints=["Both metals get longer, but one gets longer than the other.", "The longer metal must take the outside of the curve.", "Brass is on top and gets longest, so the strip curves away from it: downwards."],
         fig=lambda rng: S.bimetallic("down")),
    dict(id="e10_plastic_handle", level=3, lo="10.3",
         stem="The table compares materials for a saucepan.\n\n| Part | Material |\n|---|---|\n| base | copper |\n| handle | plastic |\n\nWhy is the handle made of plastic?",
         correct="Plastic is a poor conductor, so heat is conducted to the hand only very slowly.",
         wrongs={"Plastic is a good conductor, so it carries heat away from the hand.": "Carrying heat TO the hand faster would burn it. Plastic conducts poorly.",
                 "Plastic absorbs radiation well.": "Absorbing radiation would make the handle hotter, not safer.",
                 "Plastic expands less than metal.": "Expansion is not why the handle stays cool."},
         hints=["You hold the handle; you want little heat to reach your hand.", "Which property of plastic stops heat moving through it?", "Poor conductor = insulator."]),
    dict(id="e10_aircon_position", level=3, lo="10.4",
         stem="Fig. 1 shows an air-conditioner mounted near the ceiling of a room. Why is this a good position?",
         correct="Cooled air is denser and sinks, while warmer air rises to be cooled, setting up a convection current that cools the whole room.",
         wrongs={"Cold air rises, so it must start near the ceiling.": "Cold air is DENSER and sinks.",
                 "Heat radiates downwards from the ceiling.": "Air-conditioners cool by circulating air, not by radiation.",
                 "The ceiling conducts the cold to the walls.": "Air and ceilings are poor conductors; the room is cooled by moving air."},
         hints=["Use the chain: cooler → denser → sinks; warmer → less dense → rises.", "The air leaving the unit is cold. What does cold air do?", "A circulation of air (convection current) results."],
         fig=lambda rng: S.room_heater("ceiling")),
    dict(id="e10_railway_gaps", level=3, lo="10.2",
         stem="The table shows the length of a steel rail at two temperatures.\n\n| Temperature / °C | Length / m |\n|---|---|\n| 20 | 25.000 |\n| 50 | 25.009 |\n\nWhy are small gaps left between rails?",
         correct="The rails expand on hot days; the gaps give them room so they do not buckle.",
         wrongs={"The rails contract on hot days and would snap.": "The table shows rails get LONGER when hotter.",
                 "The gaps let rainwater drain away.": "The gaps are for the change in length, not drainage.",
                 "The gaps make the trains run more smoothly.": "Gaps actually cause the clickety-clack; they are there for expansion."},
         hints=["Compare the two lengths in the table. What happens to the rail when it gets hotter?", "If a longer rail has no space, it pushes against the next rail.", "Expansion → needs room → gap."]),
    dict(id="e10_solar_panel_black", level=3, lo="10.5",
         stem="Fig. 1 compares a dull black can and a shiny silver can placed in the sun. Why are solar water-heating panels painted dull black?",
         correct="Dull black surfaces are good absorbers of radiation, so the water heats up faster.",
         wrongs={"Dull black surfaces reflect radiation back into the water.": "Dull black surfaces hardly reflect at all; they ABSORB.",
                 "Black paint conducts heat better than silver paint.": "Colour affects absorption of radiation, not conduction.",
                 "Black surfaces are poor emitters, so no heat escapes.": "Dull black surfaces are GOOD emitters too; they are used because they absorb well."},
         hints=["The panel receives radiation from the Sun. You want it to take in as much as possible.", "Which surface in Fig. 1 warmed up more?", "Good absorber = dull and dark."],
         fig=lambda rng: S.cans(["P", "Q"], ["dull black", "shiny silver"])),

    # ------------------------------------------------------------ L4
    dict(id="e10_sea_breeze_explain", level=4, lo="10.4",
         stem="Fig. 1 shows the air movement near a coast on a sunny day. Which explanation of the sea breeze is correct?",
         correct="Land heats up faster than the sea; the warm air above the land rises, and cooler, denser air from over the sea moves in to replace it.",
         wrongs={"The sea heats up faster than the land, so air over the sea rises and air from the land moves out to sea.": "That describes the LAND breeze at night, when the sea is warmer than the land.",
                 "Cold air over the sea rises because it is denser.": "Denser air SINKS; it is the warm, less dense air that rises.",
                 "Radiation from the land pushes the air towards the sea.": "Radiation does not push air. The breeze is a convection current."},
         hints=["In the daytime, which heats up faster: land or water?", "Warm air over the land → less dense → rises. Something must flow in to take its place.", "Cooler air from over the sea moves towards the land."],
         fig=lambda rng: S.sea_breeze(True)),
    dict(id="e10_flask_parts", level=4, lo="10.6",
         stem="Fig. 1 shows a vacuum flask. Part Q is the vacuum between the double walls. What is the purpose of the vacuum?",
         correct="It has no particles, so heat cannot be transferred across it by conduction or convection.",
         wrongs={"It stops heat loss by radiation.": "Radiation CAN cross a vacuum; the silvered walls deal with radiation.",
                 "It keeps the liquid from evaporating.": "The stopper does that. The vacuum is between the walls, not above the liquid.",
                 "It conducts heat back into the drink.": "A vacuum cannot conduct at all."},
         hints=["Which two methods of heat transfer need particles?", "A vacuum is empty space.", "No particles → no conduction and no convection."],
         fig=lambda rng: S.flask()),
    dict(id="e10_tight_lid_hot_water", level=4, lo="10.2",
         stem="The table compares the expansion of two materials for the same temperature rise.\n\n| Material | Expansion of a 10 cm length / mm |\n|---|---|\n| metal (lid) | 0.19 |\n| glass (jar) | 0.09 |\n\nWhy does running hot water over a tight metal lid help to loosen it?",
         correct="The metal lid expands more than the glass jar, so the lid becomes slightly larger than the jar's mouth.",
         wrongs={"The glass jar contracts in the hot water.": "Both materials EXPAND when heated.",
                 "The hot water melts the lid slightly.": "Hot water is far too cool to melt metal.",
                 "The glass expands more than the metal, pushing the lid off.": "The table shows the METAL expands more."},
         hints=["Both the lid and the jar get hotter. Both expand, but by how much?", "Compare the two values in the table.", "The one that expands more becomes looser."]),
    dict(id="e10_trapped_air_insulation", level=4, lo="10.3",
         stem="The table compares how fast heat passes through window types.\n\n| Window | Heat loss / units |\n|---|---|\n| single glass pane | 100 |\n| two panes with air trapped between | 45 |\n\nWhy does the trapped air reduce heat loss?",
         correct="Air is a poor conductor, and because it is trapped it cannot carry heat away by convection.",
         wrongs={"Air is a good conductor and spreads the heat evenly.": "Air is a POOR conductor. That is why it works as insulation.",
                 "The trapped air reflects radiation.": "Air does not reflect radiation noticeably.",
                 "Two panes are heavier, so they hold the heat in.": "Mass has nothing to do with it; the air gap is what matters."},
         hints=["Why is air used in wool, fur and foam as well?", "Air conducts poorly, but moving air can carry heat by convection. What stops it moving here?", "Poor conductor + no convection."]),
    dict(id="e10_thick_glass_cracks", level=4, lo="10.2",
         stem="Fig. 1 shows the particles in a solid. When boiling water is poured into a thick glass tumbler, the glass may crack. Why?",
         correct="The inside surface heats up and expands before the outside does, because glass conducts heat poorly; the uneven expansion cracks it.",
         wrongs={"The whole tumbler expands evenly and becomes too large.": "Even expansion would not crack it; it is the UNEVEN expansion that does.",
                 "Glass contracts when heated.": "Glass expands when heated.",
                 "The water is heavier than the glass can hold.": "Weight is not the problem; the glass cracks even when nearly empty."},
         hints=["Glass is a poor conductor. Which part gets hot first?", "The inside expands while the outside is still cool and the same size.", "Inner layer pushes against the outer layer → crack."],
         fig=lambda rng: S.particles("solid", label="glass")),

    # ------------------------------------------------------------ L5
    dict(id="e10_choose_cup", level=5, lo="10.6",
         stem="The table describes four cups for keeping a drink hot.\n\n| Cup | Material | Lid? | Outer surface |\n|---|---|---|---|\n| A | thin metal | no | shiny |\n| B | plastic foam | yes | white |\n| C | glass | no | dull black |\n| D | thin metal | yes | dull black |\n\nWhich cup keeps the drink hot for longest, and why?",
         correct="B: foam is a poor conductor, the lid stops convection and evaporation, and the light surface is a poor emitter.",
         wrongs={"A: the shiny surface is a poor emitter of radiation.": "True, but thin metal conducts heat away quickly and there is no lid.",
                 "C: glass is a poor conductor.": "Glass conducts less than metal, but there is no lid and the dull black surface is a good emitter.",
                 "D: the lid stops heat escaping.": "The lid helps, but metal conducts well and dull black emits radiation well."},
         hints=["Think about all three methods of transfer plus evaporation.", "Which row has a poor conductor, a lid AND a poor emitter?", "Foam + lid + light surface."]),
    dict(id="e10_predict_cans_experiment", level=5, lo="10.5",
         stem="Fig. 1 shows two cans of hot water at 80 °C left to cool: P is dull black, Q is shiny silver. Predict the result after 10 minutes.",
         correct="P is cooler than Q, because a dull black surface is a better emitter of radiation.",
         wrongs={"Q is cooler than P, because shiny surfaces lose heat faster.": "Shiny surfaces are POOR emitters, so Q loses heat more slowly.",
                 "Both are at the same temperature, because they started at the same temperature.": "Equal starting temperatures do not mean equal cooling rates; the surfaces differ.",
                 "P is cooler because black surfaces conduct heat better.": "Colour does not change conduction. The difference is in RADIATION emitted."},
         hints=["Here the heat is going OUT of the cans: think 'emitter', not 'absorber'.", "Dull black = good emitter; shiny silver = poor emitter.", "The better emitter loses heat faster and ends up cooler."],
         fig=lambda rng: S.cans(["P", "Q"], ["dull black", "shiny silver"])),
    dict(id="e10_climate_change_reasoning", level=5, lo="10.7",
         stem="The table shows two changes over 100 years.\n\n| Quantity | 1920 | 2020 |\n|---|---|---|\n| carbon dioxide in air / parts per million | 300 | 415 |\n| average global temperature / °C | 13.8 | 14.9 |\n\nWhich statement best links the two rows?",
         correct="Carbon dioxide traps heat radiated from the Earth's surface, so more of it leads to a warmer Earth.",
         wrongs={"Carbon dioxide reflects sunlight back into space, so more of it cools the Earth.": "That would give a FALLING temperature, which is not what the table shows.",
                 "The warmer Earth produces carbon dioxide, which has no effect on temperature.": "The main extra carbon dioxide comes from burning fossil fuels, and it does affect temperature.",
                 "The two rows are unrelated.": "Greenhouse gases are a known cause of the temperature rise."},
         hints=["Carbon dioxide is a greenhouse gas. What does a greenhouse do?", "Heat radiated from the ground is trapped in the atmosphere.", "More trapped heat → higher average temperature."]),
    dict(id="e10_fair_test_evaluate", level=5, lo="10.5",
         stem="A student compares how fast water cools in a dull black can and a shiny can, as in Fig. 1. The black can holds 200 cm³ of water at 80 °C; the shiny can holds 100 cm³ at 70 °C. The black can cools more slowly. What is the best comment?",
         correct="The test is unfair: the volumes and starting temperatures differ, so the result cannot be blamed on the surfaces.",
         wrongs={"The result proves shiny surfaces are better emitters.": "You cannot conclude anything about surfaces when other variables also changed.",
                 "The result proves black surfaces are poor emitters.": "A larger, hotter volume cools differently; the surfaces may not be the cause.",
                 "The test is fair because both cans are the same shape.": "Shape is the same, but volume and temperature are not."},
         hints=["In a fair test only ONE thing should be different.", "List what differs between the two cans.", "More than one difference → no valid conclusion."],
         fig=lambda rng: S.cans(["black", "shiny"], ["dull black", "shiny silver"])),
    dict(id="e10_ice_in_drink_top", level=5, lo="10.4",
         stem="Fig. 1 shows a convection current. Why is ice more effective at cooling a drink when it floats at the top than if it were held at the bottom?",
         correct="Water cooled by the ice becomes denser and sinks, while warmer water rises to the ice, so a convection current cools the whole drink.",
         wrongs={"Cold water rises from the ice, so the ice must be at the top.": "Cold water is denser and SINKS.",
                 "Ice at the bottom would melt faster and cool the drink more.": "Ice at the bottom cools only the water near it; the cold water stays at the bottom.",
                 "The ice radiates cold downwards.": "There is no such thing as 'radiating cold'."},
         hints=["Use the convection chain: cooler → denser → sinks.", "If the cold water sinks from the top, what moves up to replace it?", "A circulation forms, cooling all the drink."],
         fig=lambda rng: S.room_heater("ceiling")),
]

register_explain(EXPLAIN, chapter=10)
