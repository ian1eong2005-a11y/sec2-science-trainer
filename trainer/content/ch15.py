"""Ch 15 Transport Systems in Living Things: 25 calculation / data templates and 25 explanation items.
lo codes: 15.1 blood vessels and the human transport system, 15.2 diffusion in humans and plants, 15.3* xylem and phloem (G3),
15.4* osmosis and water uptake (G3), 15.5 drug abuse and transplants, 15.6* need for a transport system (G3)."""
from .. import figs, sketches as S
from .base import fmt, md_table, nice, numeric_options, pick, register_explain, template, text_options


# ================================================================ CALCULATION / DATA
# ---------------------------------------------------------------- L1
@template("c15_pulse_rate_table", chapter=15, level=1, lo="15.1")
def pulse_rate_table(rng):
    beats = nice(rng, 18, 20, 22, 24, 30, 35)
    rate = beats * 4
    opts, key, mis = numeric_options(rng, rate, [
        (beats, "That is the number of beats in 15 seconds. Pulse rate is given per MINUTE."),
        (beats * 60, "You multiplied by 60, but the count was for 15 s, not 1 s. There are four 15-second periods in a minute."),
        (beats * 2, "15 seconds goes into 60 seconds four times, not twice."),
    ], unit="beats per minute", sf=3)
    return dict(
        stem=f"A student counts her pulse.\n\n{md_table(['Time counted / s', 'Beats counted'], [['15', str(beats)]])}\n\nWhat is her pulse rate in beats per minute?",
        options=opts, key=key, misconceptions=mis,
        formula="beats per minute = beats in 15 s × 4",
        working=[f"{beats} × 4 = **{rate} beats per minute**"],
        hints=["How many lots of 15 seconds make one minute?", "Multiply the count by that number.", f"{beats} × 4."],
    )


@template("c15_identify_vessel_letter", chapter=15, level=1, lo="15.1")
def identify_vessel_letter(rng):
    which = pick(rng, [("artery", "P", "carries blood away from the heart"), ("vein", "Q", "carries blood towards the heart"), ("capillary", "R", "exchanges substances with the body cells")])
    name, L, fn = which
    wrongs = {f"vessel {o[1]}": f"{o[1]} is the {o[0]}: it {o[2]}." for o in [("artery", "P", "carries blood away from the heart"), ("vein", "Q", "carries blood towards the heart"), ("capillary", "R", "exchanges substances with the body cells")] if o[1] != L}
    wrongs["the heart"] = "The heart is the pump, not a vessel."
    opts, key, mis = text_options(rng, f"vessel {L}", wrongs)
    return dict(
        stem=f"Fig. 1 shows a simplified human transport system; the arrows show the direction of blood flow. Which letter labels the vessel that **{fn}**, i.e. the **{name}**?",
        figure=S.circulation(),
        options=opts, key=key, misconceptions=mis,
        formula="artery: away from the heart; vein: towards the heart; capillary: where exchange with cells happens",
        working=[f"{name}: {fn} → **vessel {L}**"],
        hints=["Look at the direction of the arrows next to each letter.", "Away from the heart = artery; back to the heart = vein.", "The vessels inside the body-cells box are the capillaries."],
    )


@template("c15_diffusion_dots_count", chapter=15, level=1, lo="15.2")
def diffusion_dots_count(rng):
    inside, outside = pick(rng, [(4, 18), (3, 15), (16, 4), (14, 3)])
    direction = "into the cell" if outside > inside else "out of the cell"
    wrongs = {
        "out of the cell" if outside > inside else "into the cell": "Particles move from where there are MORE of them to where there are fewer. Count the dots on each side.",
        "equally in both directions": "There is a net movement because the concentrations are different.",
        "no movement at all": "Particles are always moving; the difference in concentration gives a net flow.",
    }
    opts, key, mis = text_options(rng, direction, wrongs)
    return dict(
        stem="Fig. 1 shows oxygen molecules (dots) inside and outside a cell. In which direction will there be a **net** movement of oxygen by diffusion?",
        figure=S.cell_concentration(inside, outside),
        options=opts, key=key, misconceptions=mis,
        formula="diffusion: net movement from a region of higher concentration to a region of lower concentration",
        working=[f"inside: {inside} dots; outside: {outside} dots", f"higher → lower, so **{direction}**"],
        hints=["Count the dots inside and outside the cell.", "Diffusion goes from more crowded to less crowded.", "Which side is more crowded?"],
    )


@template("c15_bar_chart_heart_rate", chapter=15, level=1, lo="15.5")
def bar_chart_heart_rate(rng):
    acts = ["resting", "walking", "running", "after a stimulant drug"]
    vals = [nice(rng, 65, 70, 72), nice(rng, 90, 95, 100), nice(rng, 140, 150, 160), nice(rng, 120, 130)]
    i = rng.randint(0, 3)
    opts, key, mis = numeric_options(rng, vals[i], [(v, f"That is the bar for '{a}'.") for j, (a, v) in enumerate(zip(acts, vals)) if j != i], unit="beats per minute", sf=3)
    return dict(
        stem=f"Fig. 1 shows a person's heart rate in different situations. What is the heart rate when **{acts[i]}**?",
        figure=S.bar_chart(acts, vals, "heart rate / beats per minute", ymax=200, ystep=40, size=(5.2, 3.0)),
        options=opts, key=key, misconceptions=mis,
        formula="read the bar",
        working=[f"{acts[i]} → **{vals[i]} beats per minute**"],
        hints=[f"Find the bar labelled '{acts[i]}'.", "Read its top against the scale.", "Each small square is 8 beats per minute."],
    )


@template("c15_stomata_count", chapter=15, level=1, lo="15.2")
def stomata_count(rng):
    upper = nice(rng, 2, 5, 8)
    lower = nice(rng, 120, 150, 180, 200)
    opts, key, mis = numeric_options(rng, lower - upper, [
        (lower + upper, "You added. 'How many more' means subtract."),
        (lower, "That is the number on the lower surface; the question asks for the difference."),
        (upper + 10 if upper else 10, "Check the subtraction."),
    ], unit="", sf=3)
    return dict(
        stem=f"Stomata are tiny pores through which gases diffuse into and out of a leaf. A student counted them in the same area of each leaf surface.\n\n{md_table(['Leaf surface', 'Number of stomata per mm²'], [['upper', str(upper)], ['lower', str(lower)]])}\n\nHow many more stomata per mm² are on the lower surface than on the upper surface?",
        options=opts, key=key, misconceptions=mis,
        formula="difference = lower − upper",
        working=[f"{lower} − {upper} = **{lower - upper}**"],
        hints=["Which surface has more?", "Subtract the smaller count from the larger.", f"{lower} − {upper}."],
    )


# ---------------------------------------------------------------- L2
@template("c15_potato_change_length", chapter=15, level=2, lo="15.4*")
def potato_change_length(rng):
    L0 = nice(rng, 5.0, 6.0, 8.0)
    change = nice(rng, -0.8, -0.6, -0.4, 0.4, 0.6, 0.8)
    L1 = round(L0 + change, 1)
    ans = abs(change)
    word = "increase" if change > 0 else "decrease"
    opts, key, mis = numeric_options(rng, ans, [
        (L1, "That is the final length, not the change."),
        (L0 + L1, "You added the lengths. The change is the difference."),
        (ans * 2, "Check the subtraction."),
    ], unit="cm", dp=1)
    return dict(
        stem=f"Fig. 1 shows a potato strip before and after it was left in a solution for an hour. By how much did its length **{word}**?",
        figure=S.potato_strips(L0, L1),
        options=opts, key=key, misconceptions=mis,
        formula="change in length = final length − original length",
        working=[f"{fmt(L1, dp=1)} − {fmt(L0, dp=1)} = {fmt(change, dp=1)} cm → **{word} of {fmt(ans, dp=1)} cm**", "water moved " + ("into" if change > 0 else "out of") + " the cells by osmosis"],
        hints=["Read both lengths from Fig. 1.", "Subtract.", "Longer = water entered the cells; shorter = water left."],
    )


@template("c15_percent_change_mass", chapter=15, level=2, lo="15.4*")
def percent_change_mass(rng):
    m0 = nice(rng, 5.0, 8.0, 10.0, 20.0)
    pct = nice(rng, 5, 10, 15, 20, 25)
    sign = pick(rng, [1, -1])
    m1 = round(m0 * (100 + sign * pct) / 100, 2)
    opts, key, mis = numeric_options(rng, pct, [
        (abs(m1 - m0), "That is the change in grams. The question asks for the percentage."),
        (round(abs(m1 - m0) / m1 * 100, 1), "Divide by the ORIGINAL mass, not the final mass."),
        (pct * 2, "Check: change ÷ original × 100."),
    ], unit="%", sf=3)
    return dict(
        stem=f"A potato cube was weighed, left in a solution for an hour, blotted and weighed again.\n\n{md_table(['', 'Mass / g'], [['before', fmt(m0)], ['after', fmt(m1)]])}\n\nWhat was the percentage change in mass?",
        options=opts, key=key, misconceptions=mis,
        formula="percentage change = (after − before) ÷ before × 100",
        working=[f"change = {fmt(m1)} − {fmt(m0)} = {fmt(m1 - m0)} g", f"{fmt(abs(m1 - m0))} ÷ {fmt(m0)} × 100 = **{pct}%** ({'gain' if sign > 0 else 'loss'})"],
        hints=["Find the change in mass first.", "Compare it with the starting mass.", f"{fmt(abs(m1 - m0))} ÷ {fmt(m0)} × 100."],
    )


@template("c15_blood_volume_percent", chapter=15, level=2, lo="15.1")
def blood_volume_percent(rng):
    total = nice(rng, 4.0, 4.5, 5.0, 5.5)
    pct = nice(rng, 8, 10, 15, 20)
    lost = total * pct / 100
    opts, key, mis = numeric_options(rng, lost, [
        (pct, "That is the percentage, not the volume."),
        (total - lost, "That is the blood REMAINING."),
        (total * pct / 10, "A percentage is out of 100, not 10."),
    ], unit="litres", sf=3)
    return dict(
        stem=f"An adult has **{fmt(total)} litres** of blood. Donating blood or an injury can remove some of it.\n\n{md_table(['Total blood / litres', 'Fraction lost'], [[fmt(total), f'{pct}%']])}\n\nWhat volume of blood is lost?",
        options=opts, key=key, misconceptions=mis,
        formula="volume lost = percentage ÷ 100 × total volume",
        working=[f"{pct}% of {fmt(total)} = {pct}/100 × {fmt(total)} = **{fmt(lost)} litres**"],
        hints=["A percentage is a fraction of 100.", "Find that fraction of the total volume.", f"{pct}/100 × {fmt(total)}."],
    )


@template("c15_graph_heart_rate_read", chapter=15, level=2, lo="15.5")
def graph_heart_rate_read(rng):
    rest = nice(rng, 68, 70, 72)
    pts = [(0, rest), (2, rest), (4, rest + 40), (6, rest + 70), (8, rest + 75), (10, rest + 50), (12, rest + 25), (14, rest + 8), (16, rest)]
    t = nice(rng, 4, 6, 8, 10, 12)
    ans = dict(pts)[t]
    opts, key, mis = numeric_options(rng, ans, [
        (dict(pts)[t + 2], "You read the value 2 minutes later than asked."),
        (dict(pts)[t - 2], "You read the value 2 minutes earlier than asked."),
        (rest, "That is the resting heart rate, not the value at the time asked."),
    ], unit="beats per minute", sf=3)
    return dict(
        stem=f"Fig. 1 shows a student's heart rate before, during and after a run that started at 2 min and ended at 8 min. What was the heart rate at **{t} minutes**?",
        figure=figs.graph(pts, 16, 180, 2, 20, xlabel="time / min", ylabel="heart rate / beats per minute"),
        options=opts, key=key, misconceptions=mis,
        formula="read the curve at the given time",
        working=[f"at {t} min → **{ans} beats per minute**"],
        hints=["Find the time on the horizontal axis.", "Go up to the line, then across.", "Each small square on the vertical axis is 4 beats per minute."],
    )


@template("c15_dye_rise_rate", chapter=15, level=2, lo="15.3*")
def dye_rise_rate(rng):
    h = nice(rng, 6, 8, 9, 12, 15)
    t = nice(rng, 2, 3, 4, 5)
    rate = h / t
    opts, key, mis = numeric_options(rng, rate, [
        (h * t, "You multiplied. Rate = distance ÷ time."),
        (h, "That is the distance the dye rose, not the rate."),
        (t / h if t / h != rate else rate + 1, "You divided the wrong way round."),
    ], unit="cm per hour", sf=3)
    return dict(
        stem=f"A celery stalk was stood in red dye (Fig. 1). After **{t} hours** the dye had risen **{h} cm** up the stalk. What was the average rate at which the dye rose?",
        figure=S.plant_transport(),
        options=opts, key=key, misconceptions=mis,
        formula="rate = distance risen ÷ time",
        working=[f"{h} ÷ {t} = **{fmt(rate)} cm per hour**"],
        hints=["Rate means distance per hour.", "Divide the distance by the hours.", f"{h} ÷ {t}."],
    )


# ---------------------------------------------------------------- L3
@template("c15_osmosis_direction_table", chapter=15, level=3, lo="15.4*")
def osmosis_direction_table(rng):
    cell_pct = nice(rng, 1.0, 2.0)
    sols = [("P", 0.0), ("Q", cell_pct), ("R", cell_pct + 3), ("S", cell_pct + 8)]
    rng.shuffle(sols)
    ask = pick(rng, ["gain the most water", "lose the most water"])
    target = min(sols, key=lambda s: s[1]) if ask == "gain the most water" else max(sols, key=lambda s: s[1])
    wrongs = {}
    for L, c in sols:
        if L == target[0]:
            continue
        if c == cell_pct:
            wrongs[f"solution {L}"] = "This solution has the same concentration as the cells, so there is no net movement of water."
        else:
            wrongs[f"solution {L}"] = f"Solution {L} ({fmt(c)}% salt) gives a smaller difference in water concentration than the correct choice."
    opts, key, mis = text_options(rng, f"solution {target[0]}", dict(list(wrongs.items())[:3]))
    return dict(
        stem=f"Potato cells contain a solution equivalent to **{fmt(cell_pct)}% salt**. Identical potato strips are placed in four solutions.\n\n{md_table(['Solution', 'Salt concentration / %'], [[L, fmt(c)] for L, c in sols])}\n\nIn which solution will the strip **{ask}** by osmosis?",
        options=opts, key=key, misconceptions=mis,
        formula="water moves from higher water concentration (less salt) to lower water concentration (more salt); the bigger the difference, the more water moves",
        working=[f"cells ≈ {fmt(cell_pct)}% salt", f"{ask}: the solution with the {'lowest' if ask == 'gain the most water' else 'highest'} salt concentration → **solution {target[0]}**"],
        hints=["More salt means LESS water concentration.", "Water moves towards the side with more salt.", f"To {ask}, pick the solution furthest from {fmt(cell_pct)}% in the right direction."],
    )


@template("c15_heart_recovery_time", chapter=15, level=3, lo="15.5")
def heart_recovery_time(rng):
    rest = nice(rng, 68, 70, 72)
    rec = nice(rng, 4, 6, 8)
    pts = [(0, rest), (2, rest), (4, rest + 40), (6, rest + 70), (8, rest + 75)]
    end = 8 + rec
    for k, t in enumerate(range(10, end + 1, 2)):
        pts.append((t, rest + round((rest + 75 - rest) * (1 - (k + 1) / (rec / 2)))))
    pts = pts + [(t, rest) for t in range(end + 2, 21, 2)]
    pts = pts[:11]
    opts, key, mis = numeric_options(rng, rec, [
        (end, "That is the TIME at which the heart rate is back to resting, not how long the recovery took."),
        (8, "That is when the run ended."),
        (rec + 2, "Recovery time = time back to resting − time the run ended."),
    ], unit="min", sf=2)
    return dict(
        stem="Fig. 1 shows a student's heart rate. The run ended at 8 min. How long did the heart rate take to return to its resting value after the run?",
        figure=figs.graph(pts, 20, 180, 2, 20, xlabel="time / min", ylabel="heart rate / beats per minute"),
        options=opts, key=key, misconceptions=mis,
        formula="recovery time = time when the rate is back to resting − time exercise ended",
        working=[f"resting rate = {rest}; the curve returns to it at {end} min", f"recovery time = {end} − 8 = **{rec} min**"],
        hints=["What is the resting heart rate (the level at the start)?", "When does the curve get back down to that level?", "Subtract the time when the run ended (eight minutes)."],
    )


@template("c15_diffusion_distance_time", chapter=15, level=3, lo="15.6*")
def diffusion_distance_time(rng):
    rows = [["0.1", "1"], ["1", "100"], ["10", "10 000"]]
    ask = pick(rng, ["2", "5"])
    ans = {"2": 400, "5": 2500}[ask]
    opts, key, mis = numeric_options(rng, ans, [
        (int(ask) * 100, "The time does not simply go up in proportion to the distance; look at how it changes when the distance is ×10."),
        (int(ask) * 10, "Check the pattern: ×10 distance gives ×100 time."),
        (ans / 2, "Time scales with distance squared: time ∝ (distance)²."),
    ], unit="s", sf=3)
    return dict(
        stem=f"The table shows how long oxygen takes to diffuse different distances through tissue.\n\n{md_table(['Distance / mm', 'Time / s'], rows)}\n\nFollowing the pattern, how long would oxygen take to diffuse **{ask} mm**?",
        options=opts, key=key, misconceptions=mis,
        formula="time is proportional to distance²: ×10 distance → ×100 time",
        working=[f"time at 1 mm = 100 s; time ∝ distance²", f"at {ask} mm: 100 × {ask}² = **{ans} s**"],
        hints=["Compare rows: distance ×10 makes the time ×100.", "So the time depends on the SQUARE of the distance.", f"100 × {ask} × {ask}."],
    )


@template("c15_blood_flow_share", chapter=15, level=3, lo="15.1")
def blood_flow_share(rng):
    total = nice(rng, 5000, 6000)
    organs = ["muscles", "digestive system", "kidneys", "brain", "other"]
    pcts = [20, 25, 20, 15, 20]
    pcts = rng.sample(pcts, 5)
    i = rng.randint(0, 3)
    ans = total * pcts[i] / 100
    opts, key, mis = numeric_options(rng, ans, [
        (pcts[i], "That is the percentage, not the volume."),
        (total * (100 - pcts[i]) / 100, f"That is the blood going everywhere EXCEPT the {organs[i]}."),
        (total / 5, "The shares are not all equal."),
    ], unit="cm³ per minute", sf=3)
    return dict(
        stem=f"Fig. 1 shows how the blood pumped by the heart at rest (**{total} cm³ per minute**) is shared between organs. How much blood flows to the **{organs[i]}** each minute?",
        figure=S.pie_chart([f"{o} ({p}%)" for o, p in zip(organs, pcts)], pcts),
        options=opts, key=key, misconceptions=mis,
        formula="volume = percentage ÷ 100 × total",
        working=[f"{organs[i]}: {pcts[i]}% of {total} = **{fmt(ans)} cm³ per minute**"],
        hints=[f"Read the percentage for the {organs[i]}.", "Apply it to the total.", f"{pcts[i]}/100 × {total}."],
    )


@template("c15_water_uptake_table", chapter=15, level=3, lo="15.3*")
def water_uptake_table(rng):
    start = nice(rng, 100, 120, 150)
    rate = nice(rng, 4, 5, 6, 8)
    hours = nice(rng, 3, 4, 5, 6)
    end = start - rate * hours
    opts, key, mis = numeric_options(rng, rate, [
        (start - end, "That is the total water taken up. Divide by the time for the rate."),
        (end / hours, "You used the final volume instead of the volume taken up."),
        (rate * hours * 2, "Rate = volume taken up ÷ hours."),
    ], unit="cm³ per hour", sf=3)
    return dict(
        stem=f"A leafy shoot was placed in a measuring cylinder of water with a layer of oil on top to stop evaporation.\n\n{md_table(['Time / h', 'Volume of water / cm³'], [['0', str(start)], [str(hours), str(end)]])}\n\nWhat was the average rate of water uptake by the shoot?",
        options=opts, key=key, misconceptions=mis,
        formula="rate = water taken up ÷ time",
        working=[f"taken up = {start} − {end} = {start - end} cm³", f"rate = {start - end} ÷ {hours} = **{rate} cm³ per hour**"],
        hints=["The volume falls because the shoot takes water up through its xylem.", "Find the total fall, then divide by the hours.", f"({start} − {end}) ÷ {hours}."],
    )


# ---------------------------------------------------------------- L4
@template("c15_graph_two_shoots_compare", chapter=15, level=4, lo="15.3*")
def graph_two_shoots_compare(rng):
    r_leaf, r_noleaf = nice(rng, 8, 10, 12), nice(rng, 2, 3)
    start = 150
    leafy = [(t, start - r_leaf * t) for t in range(0, 7)]
    bare = [(t, start - r_noleaf * t) for t in range(0, 7)]
    t = nice(rng, 2, 3, 4, 5, 6)
    diff = (r_leaf - r_noleaf) * t
    opts, key, mis = numeric_options(rng, diff, [
        (start - dict(leafy)[t], "That is the water taken up by the leafy shoot alone, not how much MORE than the bare shoot."),
        (dict(leafy)[t], "That is the volume remaining for the leafy shoot."),
        (start - dict(bare)[t], "That is the uptake by the shoot WITHOUT leaves."),
    ], unit="cm³", sf=3)
    return dict(
        stem=f"Fig. 1 shows the volume of water in two cylinders, one holding a leafy shoot and one holding the same shoot with its leaves removed. After **{t} hours**, how much more water has the leafy shoot taken up than the bare shoot?",
        figure=S.xy_graph([("leafy shoot", leafy), ("leaves removed", bare)], "time / h", "volume of water / cm³", 6, 160, 1, 20),
        options=opts, key=key, misconceptions=mis,
        formula="uptake = start − remaining for each shoot; difference = leafy uptake − bare uptake",
        working=[f"leafy: {start} − {dict(leafy)[t]} = {start - dict(leafy)[t]} cm³; bare: {start} − {dict(bare)[t]} = {start - dict(bare)[t]} cm³", f"difference = **{diff} cm³**"],
        hints=["Read both lines at the given time.", "Work out how much each has fallen from 150.", "Subtract the two uptakes."],
    )


@template("c15_bar_chart_salt_solutions", chapter=15, level=4, lo="15.4*")
def bar_chart_salt_solutions(rng):
    concs = ["0%", "1%", "2%", "3%", "5%"]
    changes = [nice(rng, 8, 10, 12), nice(rng, 3, 4, 5), 0, nice(rng, -4, -5), nice(rng, -9, -11)]
    # bar_chart cannot show negatives nicely -> show final mass as % of original
    finals = [100 + c for c in changes]
    opts, key, mis = text_options(rng, "2%", {"1%": "At 1% the strip gained mass, so water moved IN: the solution was more dilute than the cells.", "3%": "At 3% the strip lost mass, so water moved OUT.", "0%": "In pure water the strip gained the most mass."})
    return dict(
        stem="Potato strips were placed in salt solutions of different concentrations for an hour. Fig. 1 shows the final mass of each strip as a percentage of its starting mass. Which concentration is closest to the concentration inside the potato cells?",
        figure=S.bar_chart(concs, finals, "final mass / % of original", ymax=120, ystep=20, xlabel="salt concentration"),
        options=opts, key=key, misconceptions=mis,
        formula="no net osmosis (no change in mass) when the solution has the same concentration as the cells",
        working=["the 2% strip stayed at 100% of its mass → no net water movement", "**2%** matches the cells"],
        hints=["Which bar shows no change (100%)?", "No change means water moved in and out equally.", "That happens when the concentrations match."],
    )


@template("c15_graph_oxygen_distance_capillary", chapter=15, level=4, lo="15.2")
def graph_oxygen_distance_capillary(rng):
    c0 = nice(rng, 100, 95)
    pts = [(d, round(c0 * (1 - d / 120) ** 2)) for d in range(0, 101, 10)]
    d = nice(rng, 20, 40, 60, 80)
    ans = dict(pts)[d]
    opts, key, mis = numeric_options(rng, ans, [
        (dict(pts)[d + 10], "You read the value 10 μm further away."),
        (c0, "That is the concentration AT the capillary (distance 0)."),
        (d, "That is the distance, not the concentration."),
    ], unit="units", sf=3)
    return dict(
        stem=f"Fig. 1 shows how the oxygen concentration in tissue changes with distance from a capillary. What is the oxygen concentration **{d} μm** from the capillary?",
        figure=figs.graph(pts, 100, 120, 20, 20, xlabel="distance from capillary / μm", ylabel="oxygen concentration / units"),
        options=opts, key=key, misconceptions=mis,
        formula="read the graph at the given distance",
        working=[f"at {d} μm → **{ans} units**", "oxygen diffuses from the capillary (high) into the tissue (low), so the concentration falls with distance"],
        hints=["Find the distance on the horizontal axis.", "Go up to the curve and across.", "Oxygen is highest next to the capillary."],
    )


@template("c15_drug_table_percent", chapter=15, level=4, lo="15.5")
def drug_table_percent(rng):
    non = nice(rng, 4, 5, 8)
    mult = nice(rng, 2.5, 3, 4)
    users = non * mult
    opts, key, mis = numeric_options(rng, mult, [
        (users - non, "That is the difference in cases per 1000, not how many TIMES greater."),
        (users, "That is the number for drug users; compare it with non-users."),
        (non / users if non / users != mult else mult + 1, "Divide users by non-users."),
    ], unit="times", sf=3)
    return dict(
        stem=f"The table shows the yearly number of heart attacks per 1000 people in two groups of the same age.\n\n{md_table(['Group', 'Heart attacks per 1000 people'], [['non-users', str(non)], ['regular users of a stimulant drug', fmt(users)]])}\n\nHow many times more likely is a heart attack among the drug users?",
        options=opts, key=key, misconceptions=mis,
        formula="number of times = users' rate ÷ non-users' rate",
        working=[f"{fmt(users)} ÷ {non} = **{fmt(mult)} times**"],
        hints=["'How many times more' means divide.", "Users ÷ non-users.", f"{fmt(users)} ÷ {non}."],
    )


@template("c15_transplant_waiting_bar", chapter=15, level=4, lo="15.5")
def transplant_waiting_bar(rng):
    years = ["2021", "2022", "2023", "2024"]
    waiting = [nice(rng, 40, 45), nice(rng, 48, 52), nice(rng, 55, 60), nice(rng, 62, 70)]
    donated = [nice(rng, 8, 10), nice(rng, 9, 11), nice(rng, 10, 12), nice(rng, 11, 13)]
    i = rng.randint(0, 3)
    ans = waiting[i] - donated[i]
    opts, key, mis = numeric_options(rng, ans, [
        (waiting[i], f"That is the number waiting in {years[i]}; subtract the hearts donated."),
        (donated[i], "That is the number of hearts donated."),
        (waiting[i] + donated[i], "You added. The shortfall is waiting − donated."),
    ], unit="people", sf=3)
    return dict(
        stem=f"Fig. 1 shows the number of patients waiting for a heart transplant each year. The table shows the hearts donated.\n\n{md_table(['Year', *years], [['hearts donated', *map(str, donated)]])}\n\nIn **{years[i]}**, how many waiting patients could **not** receive a heart?",
        figure=S.bar_chart(years, waiting, "patients waiting", ymax=80, ystep=20, xlabel="year"),
        options=opts, key=key, misconceptions=mis,
        formula="shortfall = patients waiting − hearts donated",
        working=[f"{years[i]}: {waiting[i]} waiting, {donated[i]} donated", f"shortfall = **{ans} people**"],
        hints=[f"Read the bar for {years[i]}.", f"Find the hearts donated in {years[i]} in the table.", "Subtract."],
    )


# ---------------------------------------------------------------- L5
@template("c15_sa_vol_ratio_cells", chapter=15, level=5, lo="15.6*")
def sa_vol_ratio_cells(rng):
    s = nice(rng, 2, 3, 4)
    sa, v = 6 * s * s, s ** 3
    ratio = sa / v
    small_ratio = 6.0
    opts, key, mis = numeric_options(rng, ratio, [
        (sa, "That is the surface area. The question asks for surface area ÷ volume."),
        (v / sa, "You divided the wrong way round."),
        (small_ratio, "That is the ratio for a 1 cm cube. The bigger cube has a SMALLER ratio."),
    ], unit="", sf=3)
    return dict(
        stem=f"Fig. 1 shows a cube-shaped model 'organism' of side **{s} cm**. What is its surface area to volume ratio (surface area ÷ volume)? (A 1 cm cube has a ratio of 6.)",
        figure=figs.labelled_block(s, s, s),
        options=opts, key=key, misconceptions=mis,
        formula="surface area = 6 × side²; volume = side³; ratio = surface area ÷ volume",
        working=[f"surface area = 6 × {s}² = {sa} cm²", f"volume = {s}³ = {v} cm³", f"ratio = {sa} ÷ {v} = **{fmt(ratio)}** (smaller than 6: large organisms need a transport system)"],
        hints=["Surface area of a cube = 6 × side × side.", "Volume = side × side × side.", "Divide the surface area by the volume."],
    )


@template("c15_osmosis_mass_two_strips", chapter=15, level=5, lo="15.4*")
def osmosis_mass_two_strips(rng):
    m0 = nice(rng, 5.0, 6.0, 8.0)
    pct_water = nice(rng, 10, 15, 20)
    pct_salt = nice(rng, 10, 15, 20)
    m_water = round(m0 * (100 + pct_water) / 100, 2)
    m_salt = round(m0 * (100 - pct_salt) / 100, 2)
    diff = round(m_water - m_salt, 2)
    opts, key, mis = numeric_options(rng, diff, [
        (round(m_water - m0, 2), "That is only the gain of the strip in water. The question asks the difference between the two strips."),
        (round(m0 - m_salt, 2), "That is only the loss of the strip in salt solution."),
        (round(m_water + m_salt, 2), "You added the final masses."),
    ], unit="g", sf=3)
    return dict(
        stem=f"Two identical potato strips of mass **{fmt(m0)} g** were placed in different liquids for an hour.\n\n{md_table(['Strip', 'Liquid', 'Change in mass'], [['A', 'distilled water', f'+{pct_water}%'], ['B', 'strong salt solution', f'−{pct_salt}%']])}\n\nWhat is the difference between the final masses of the two strips?",
        options=opts, key=key, misconceptions=mis,
        formula="final mass = original × (100 ± %) ÷ 100 for each; difference = A − B",
        working=[f"A: {fmt(m0)} × {100 + pct_water}/100 = {fmt(m_water)} g (water enters by osmosis)", f"B: {fmt(m0)} × {100 - pct_salt}/100 = {fmt(m_salt)} g (water leaves)", f"difference = **{fmt(diff)} g**"],
        hints=["Work out each final mass separately.", "A gains, B loses.", "Then subtract B from A."],
    )


@template("c15_heart_rate_graph_rate_of_rise", chapter=15, level=5, lo="15.5")
def heart_rate_graph_rate_of_rise(rng):
    rest = nice(rng, 68, 70, 72)
    peak_rise = nice(rng, 60, 70, 80)
    pts = [(0, rest), (2, rest), (4, rest + peak_rise // 2), (6, rest + peak_rise), (8, rest + peak_rise), (10, rest + peak_rise // 2), (12, rest + 10), (14, rest), (16, rest)]
    rate = peak_rise / 4
    opts, key, mis = numeric_options(rng, rate, [
        (peak_rise, "That is the total rise. Divide by the time it took (4 minutes)."),
        ((rest + peak_rise) / 4, "Use the RISE (peak − resting), not the peak value."),
        (peak_rise / 6, "The rise happens between 2 min and 6 min: 4 minutes, not 6."),
    ], unit="beats per minute per minute", sf=3)
    return dict(
        stem="Fig. 1 shows a student's heart rate during a run from 2 min to 8 min. What is the average rate of increase of heart rate between **2 min and 6 min**?",
        figure=figs.graph(pts, 16, 180, 2, 20, xlabel="time / min", ylabel="heart rate / beats per minute"),
        options=opts, key=key, misconceptions=mis,
        formula="rate of increase = (rate at 6 min − rate at 2 min) ÷ 4 min",
        working=[f"at 2 min: {rest}; at 6 min: {rest + peak_rise}", f"({rest + peak_rise} − {rest}) ÷ 4 = **{fmt(rate)} beats per minute per minute**"],
        hints=["Read the heart rate at 2 min and at 6 min.", "Find the rise.", "Divide by the 4 minutes between them."],
    )


@template("c15_vessel_table_identify_data", chapter=15, level=5, lo="15.1")
def vessel_table_identify_data(rng):
    rows = [["X", "away from the heart", "high", "yes"], ["Y", "towards the heart", "low", "no"], ["Z", "from X to Y, through the tissues", "falling", "no"]]
    rng.shuffle(rows)
    ask = pick(rng, [("artery", "X"), ("vein", "Y"), ("capillary", "Z")])
    name, L = ask
    wrongs = {f"vessel {r[0]}": f"Vessel {r[0]} carries blood {r[1]}: that is not the {name}." for r in rows if r[0] != L}
    wrongs["none of them"] = "One of the rows matches the definition."
    opts, key, mis = text_options(rng, f"vessel {L}", dict(list(wrongs.items())[:3]))
    return dict(
        stem=f"The table shows data on three blood vessels.\n\n{md_table(['Vessel', 'Direction of flow', 'Blood pressure', 'Pulse felt?'], rows)}\n\nWhich vessel is the **{name}**?",
        options=opts, key=key, misconceptions=mis,
        formula="arteries carry blood away from the heart; veins carry it towards the heart; capillaries link them in the tissues",
        working=[f"{name} → **vessel {L}**"],
        hints=["Use the direction of flow column: it is what defines each type of vessel.", "Away = artery; towards = vein; linking them in the tissues = capillary.", "Pressure and pulse are extra clues: arteries have both."],
    )


@template("c15_dye_rings_count", chapter=15, level=5, lo="15.3*")
def dye_rings_count(rng):
    total = nice(rng, 6, 8, 10)
    stained = nice(rng, 3, 4, 5)
    stained = min(stained, total - 1)
    if 2 * stained == total:
        stained -= 1
    opts, key, mis = text_options(rng, f"{stained}, the xylem bundles", {
        f"{total}, every bundle": "Only the tissue that carries water from the roots is stained; the phloem bundles are not.",
        f"{total - stained}, the phloem bundles": "Phloem carries food from the leaves, not the dye-coloured water.",
        f"{stained}, the phloem bundles": "The stained tissue is the one that carries water: xylem, not phloem.",
    })
    return dict(
        stem=f"A stem was left in red dye for a day and then cut across (Fig. 1 shows the set-up). Under a microscope the cut stem showed **{total}** vascular bundles, of which **{stained}** contained red-stained tubes and **{total - stained}** did not. How many bundles carried the dye, and which tissue was stained?",
        figure=S.plant_transport(),
        options=opts, key=key, misconceptions=mis,
        formula="xylem carries water (and dissolved dye) from the roots upwards; phloem carries food from the leaves",
        working=[f"stained tubes = xylem", f"**{stained}, the xylem bundles**"],
        hints=["Which tissue carries water up from the roots?", "The dye is dissolved in that water.", "Count the stained bundles."],
    )


# ================================================================ EXPLANATION
EXPLAIN = [
    # ------------------------------------------------------------ L1
    dict(id="e15_artery_function", level=1, lo="15.1",
         stem="Fig. 1 shows a simplified transport system. What is the function of an artery?",
         correct="It carries blood away from the heart.",
         wrongs={"It carries blood towards the heart.": "That is a vein.", "It is where substances are exchanged with the cells.": "That is a capillary.", "It pumps the blood.": "The heart pumps; vessels carry."},
         hints=["A for Artery, A for Away.", "Look at the arrows on vessel P in Fig. 1.", "Away from the heart."],
         fig=lambda rng: S.circulation()),
    dict(id="e15_capillary_function", level=1, lo="15.1",
         stem="Fig. 1 shows a simplified transport system. What happens in the capillaries (R)?",
         correct="Substances such as oxygen and digested food pass from the blood to the cells, and wastes pass back.",
         wrongs={"Blood is pumped to the lungs.": "The heart pumps blood; capillaries do not.", "Blood is carried quickly back to the heart.": "Veins do that.", "Blood is made.": "Blood cells are made in the bones, not in vessels."},
         hints=["Capillaries are tiny vessels that reach every cell.", "What must get from the blood to the cells?", "Exchange of substances."],
         fig=lambda rng: S.circulation()),
    dict(id="e15_diffusion_definition", level=1, lo="15.2",
         stem="Fig. 1 shows particles inside and outside a cell. Diffusion is the net movement of particles",
         correct="from a region of higher concentration to a region of lower concentration",
         wrongs={"from a region of lower concentration to a region of higher concentration": "That is the wrong way round.", "only through a partially permeable membrane": "Diffusion happens with or without a membrane; that condition is part of osmosis.", "caused by the cell pumping them": "Diffusion needs no energy from the cell."},
         hints=["Think of the smell of food spreading through a room.", "Particles spread from where they are crowded to where they are not.", "High → low."],
         fig=lambda rng: S.cell_concentration(3, 18, arrow="in")),
    dict(id="e15_transport_system_parts", level=1, lo="15.1",
         stem="The table lists parts of the human body.\n\n| Part |\n|---|\n| heart |\n| blood |\n| blood vessels |\n| lungs |\n\nWhich three parts make up the human transport (circulatory) system?",
         correct="heart, blood and blood vessels",
         wrongs={"heart, lungs and blood": "The lungs belong to the respiratory system.", "blood, blood vessels and lungs": "The heart is the pump of the transport system; the lungs are not part of it.", "heart, blood vessels and lungs": "Blood is the transport medium and must be included; lungs are not part of the system."},
         hints=["The system needs a pump, a fluid and tubes.", "Which part exchanges gases but does not transport them around the body?", "Pump + fluid + tubes."]),
    dict(id="e15_drug_effect_recall", level=1, lo="15.5",
         stem="Fig. 1 shows heart rates in different situations. Which is an effect of abusing stimulant drugs on the transport system?",
         correct="a faster or irregular heartbeat and higher blood pressure",
         wrongs={"stronger bones": "Drug abuse does not strengthen bones.", "better eyesight": "Drugs do not improve eyesight.", "slower, steadier breathing": "Stimulants speed body processes up and make them irregular."},
         hints=["Look at the 'after a stimulant drug' bar in Fig. 1.", "Stimulants push the heart to work harder.", "Faster heartbeat, higher blood pressure."],
         fig=lambda rng: S.bar_chart(["resting", "after a stimulant drug"], [70, 130], "heart rate / beats per minute", ymax=160, ystep=40)),

    # ------------------------------------------------------------ L2
    dict(id="e15_identify_vessel_by_direction", level=2, lo="15.1",
         hints=["Name a vessel by the DIRECTION of flow, not by what the blood carries.", "Away from the heart: artery. Towards the heart: vein.", "Capillaries are the tiny vessels in the tissues."],
         fig=lambda rng: S.circulation(),
         variants=[
             dict(stem="Fig. 1 shows the transport system. Vessel Q carries blood from the body cells back to the heart. Vessel Q is", correct="a vein", wrongs={"an artery": "Arteries carry blood AWAY from the heart.", "a capillary": "Capillaries are the tiny exchange vessels in the tissues, labelled R.", "the heart": "Q is a vessel, not the pump."}),
             dict(stem="Fig. 1 shows the transport system. A vessel carries blood from the heart to the lungs. This vessel is", correct="an artery, because it carries blood away from the heart", wrongs={"a vein, because the blood has little oxygen": "A vessel is named by direction of flow, not by its oxygen content.", "a capillary, because it goes to the lungs": "Capillaries are tiny exchange vessels, not the main tubes from the heart.", "a vein, because it carries blood to the lungs": "Towards the LUNGS from the heart is still AWAY from the heart."}),
         ]),
    dict(id="e15_diffusion_in_humans_substances", level=2, lo="15.2",
         stem="The table shows the concentration of two substances in a capillary and in a body cell.\n\n| Substance | Blood in capillary | Body cell |\n|---|---|---|\n| oxygen | high | low |\n| carbon dioxide | low | high |\n\nWhich statement is correct?",
         correct="Oxygen diffuses into the cell and carbon dioxide diffuses out of the cell.",
         wrongs={"Oxygen diffuses out of the cell and carbon dioxide diffuses in.": "Each substance moves from high to low concentration; check the table.", "Both substances diffuse into the cell.": "Carbon dioxide is HIGHER in the cell, so it moves out.", "Both substances diffuse out of the cell.": "Oxygen is LOWER in the cell, so it moves in."},
         hints=["Diffusion: high → low concentration.", "For each substance, which side is 'high'?", "Oxygen: blood → cell. Carbon dioxide: cell → blood."]),
    dict(id="e15_diffusion_in_plants", level=2, lo="15.2",
         hints=["Photosynthesis uses one gas and produces another; both pass through the stomata.", "Mineral salts enter root cells from the soil water; no pushing is needed.", "In each case particles move from higher to lower concentration: check the table for which side is higher."],
         variants=[
             dict(stem="The table shows gas concentrations on a sunny day.\n\n| Gas | Air outside leaf | Inside leaf |\n|---|---|---|\n| carbon dioxide | higher | lower |\n| oxygen | lower | higher |\n\nWhich gas diffuses INTO the leaf through the stomata?", correct="carbon dioxide", wrongs={"oxygen": "Oxygen is higher inside (made by photosynthesis), so it diffuses OUT.", "both gases": "They move in opposite directions.", "neither gas": "There are concentration differences, so both diffuse."}),
             dict(stem="The table shows mineral concentrations.\n\n| Location | Mineral salt concentration |\n|---|---|\n| soil water | higher |\n| root cell | lower |\n\nHow do mineral salts enter the root?", correct="by diffusion from the soil water into the root cells, down the concentration gradient", wrongs={"by osmosis": "Osmosis is the movement of WATER, not mineral salts.", "the root cells push them in": "Diffusion needs no pushing by the cell.", "they enter through the leaves": "Minerals come from the soil, through the roots."}),
         ]),
    dict(id="e15_xylem_phloem_identify", level=2, lo="15.3*",
         stem="Fig. 1 shows a stem in coloured water; tissue X became stained and tissue Y did not. Which row is correct?",
         correct="X is xylem, carrying water and minerals upwards; Y is phloem, carrying food from the leaves.",
         wrongs={"X is phloem, carrying water upwards; Y is xylem, carrying food.": "The names are swapped: xylem carries water.", "X is xylem, carrying food; Y is phloem, carrying water.": "Xylem carries WATER (which is why it stained); phloem carries food.", "Both X and Y are xylem.": "Only one tissue carries the coloured water."},
         hints=["Which tissue is stained by coloured WATER?", "Xylem = water and minerals; phloem = food.", "Stained = water carrier."],
         fig=lambda rng: S.plant_transport()),
    dict(id="e15_osmosis_definition", level=2, lo="15.4*",
         stem="Fig. 1 shows water molecules on either side of a cell membrane. Osmosis is the movement of",
         correct="water molecules from a region of higher water concentration to a region of lower water concentration through a partially permeable membrane",
         wrongs={"salt from a dilute solution to a concentrated solution": "Osmosis is about WATER, and salt would move the other way by diffusion.", "water molecules from a dilute solution to a concentrated one, through any barrier": "The membrane must be PARTIALLY PERMEABLE.", "any particles from high to low concentration": "That is diffusion in general; osmosis is specifically water across a membrane."},
         hints=["Osmosis is a special case of diffusion.", "It involves one substance only, and a special kind of membrane.", "Water + partially permeable membrane."],
         fig=lambda rng: S.cell_concentration(5, 15, label_in="less water inside", label_out="more water outside", arrow="in")),

    # ------------------------------------------------------------ L3
    dict(id="e15_capillary_thin_walls", level=3, lo="15.1",
         stem="The table compares blood vessels.\n\n| Vessel | Wall | Width |\n|---|---|---|\n| artery | thick | wide |\n| vein | thinner | wide |\n| capillary | one cell thick | very narrow |\n\nWhy is the capillary wall only one cell thick?",
         correct="So that substances have only a short distance to diffuse between the blood and the cells.",
         wrongs={"So that the blood can flow faster.": "Blood flows SLOWLY in capillaries, which helps exchange.", "So that the capillary can stretch when the heart beats.": "That describes an artery.", "To stop substances leaking out.": "The thin wall lets substances pass; that is its purpose."},
         hints=["Capillaries are where exchange happens.", "What makes diffusion faster: a short or a long distance?", "Thin wall → short diffusion distance."]),
    dict(id="e15_root_hair_adaptation", level=3, lo="15.4*",
         stem="Fig. 1 shows a root hair cell with water entering from the soil. How does the long, thin shape help?",
         correct="It gives a large surface area for absorbing water and minerals from the soil.",
         wrongs={"It lets the cell move through the soil to find water.": "Plant cells do not move.", "It stores water for dry periods.": "Root hairs absorb; they are not storage organs.", "It helps the root anchor the plant.": "Anchoring is the job of the root as a whole."},
         hints=["Absorption happens across the cell surface.", "A long thin extension has a lot of surface for its volume.", "More surface → more absorbed."],
         fig=lambda rng: S.cell_concentration(5, 15, label_in="root hair cell", label_out="soil water", arrow="in")),
    dict(id="e15_wilting_salt", level=3, lo="15.4*",
         stem="Fig. 1 shows a potato strip that shrank in a solution. A plant watered with strong salt solution wilts. Why?",
         correct="The soil water now has a lower water concentration than the root cells, so water leaves the roots by osmosis.",
         wrongs={"Salt poisons the leaves directly.": "The salt stays in the soil; the problem is water LEAVING the roots.", "Salt makes the roots absorb too much water.": "It is the opposite: water moves OUT of the roots.", "Salt blocks the xylem.": "Salt does not block the vessels; it changes the direction of osmosis."},
         hints=["Compare the water concentration inside the root cells with that in the salty soil water.", "Which way does water move by osmosis?", "Water leaves the plant → cells lose water → wilting."],
         fig=lambda rng: S.potato_strips(6.0, 5.4)),
    dict(id="e15_multicellular_need_transport", level=3, lo="15.6*",
         stem="Fig. 1 compares a small cube and a large cube (the surface area to volume ratio falls as size increases). Why do large multicellular organisms need a transport system?",
         correct="Most of their cells are far from the surface, so diffusion alone is too slow to supply them with oxygen and food and remove wastes.",
         wrongs={"Because they have more cells, so they need more blood to be heavy enough.": "Weight is not the reason.", "Because diffusion does not happen in large organisms.": "Diffusion still happens, but only over SHORT distances.", "Because large organisms cannot absorb oxygen at all.": "They can absorb it at special surfaces (lungs), then it must be carried."},
         hints=["How far would a substance have to diffuse to reach the centre of a large animal?", "Diffusion is fast over tiny distances and very slow over long ones.", "A transport system carries substances quickly over long distances."],
         fig=lambda rng: figs.labelled_block(4, 4, 4)),
    dict(id="e15_drug_abuse_apply", level=3, lo="15.5",
         stem="The table shows measurements for a person before and after a year of abusing a stimulant drug.\n\n| | Before | After |\n|---|---|---|\n| resting heart rate / bpm | 70 | 95 |\n| blood pressure | normal | high |\n\nWhich statement best describes the effect on the transport system?",
         correct="The heart is working harder all the time and the high blood pressure increases the risk of a heart attack or stroke.",
         wrongs={"The person is fitter, because the heart beats more often.": "A HIGH resting heart rate is a sign of strain, not fitness.", "The changes are harmless because they are small.": "A rise of 25 bpm at rest and high blood pressure are serious.", "The drug has improved the blood vessels.": "Drug abuse damages vessels; it does not improve them."},
         hints=["Compare the two columns.", "Is a faster resting heartbeat good or bad for the heart?", "High blood pressure strains the vessels."]),

    # ------------------------------------------------------------ L4
    dict(id="e15_oxygen_diffusion_explain", level=4, lo="15.2",
         stem="Fig. 1 shows oxygen concentration falling with distance from a capillary. Explain the shape of the graph.",
         correct="Oxygen diffuses out of the capillary into the tissue, where cells use it in respiration, so its concentration falls further from the capillary.",
         wrongs={"The capillary pumps oxygen outwards and runs out.": "Capillaries do not pump; oxygen moves by diffusion.", "Cells far from the capillary make their own oxygen.": "Animal cells do not make oxygen.", "Oxygen concentration is the same everywhere; the graph is wrong.": "The concentration difference is what drives diffusion."},
         hints=["Where does the oxygen come from and where does it go?", "Diffusion moves it from high (capillary) to low (tissue).", "Cells use it up as they respire."],
         fig=lambda rng: figs.graph([(d, round(100 * (1 - d / 120) ** 2)) for d in range(0, 101, 10)], 100, 120, 20, 20, xlabel="distance from capillary / μm", ylabel="oxygen concentration / units")),
    dict(id="e15_celery_dye_explain", level=4, lo="15.3*",
         stem="Fig. 1 shows a celery stalk left in red dye. After a day the leaves have red veins and a cut across the stalk shows red dots. What does this show?",
         correct="Water (carrying the dye) is transported from the base of the stalk up to the leaves through the xylem.",
         wrongs={"The dye was absorbed through the leaves.": "The dye entered from the water at the base.", "Food made in the leaves travelled down to the base.": "That is the phloem's job and would not carry the dye upwards.", "The stalk dissolved in the dye.": "The stalk is intact; only its water-carrying tubes are stained."},
         hints=["Where was the dye at the start?", "Which tissue carries water upwards?", "Red dots = the water-carrying tubes."],
         fig=lambda rng: S.plant_transport()),
    dict(id="e15_potato_graph_explain", level=4, lo="15.4*",
         stem="Fig. 1 shows the final mass of potato strips placed in different salt solutions. Explain why the strips in weak solutions gained mass.",
         correct="The weak solutions had a higher water concentration than the potato cells, so water moved into the cells by osmosis.",
         wrongs={"The strips absorbed salt, which made them heavier.": "The strips gained most in the WEAKEST solution, so it is water that entered, not salt.", "The cells grew new tissue in an hour.": "No growth happens in an hour; the mass change is water movement.", "Salt pushed water into the strips.": "Water moves because of the concentration difference, not because salt pushes it."},
         hints=["Compare the water concentration inside and outside the cells.", "Water moves to the side with less water.", "Dilute outside → water enters."],
         fig=lambda rng: S.bar_chart(["0%", "1%", "2%", "3%", "5%"], [110, 104, 100, 95, 90], "final mass / % of original", ymax=120, ystep=20, xlabel="salt concentration")),
    dict(id="e15_transplant_ethics", level=4, lo="15.5",
         stem="The table gives facts about heart transplants in a country.\n\n| Fact | Value |\n|---|---|\n| patients waiting | 60 |\n| hearts available this year | 12 |\n\nWhich of the following is an **ethical** issue raised by this situation?",
         correct="Deciding which patients should receive the few hearts available, and on what grounds.",
         wrongs={"Working out how long the operation takes.": "That is a practical, not an ethical, question.", "Measuring the mass of the heart.": "That is a measurement, not a question of right and wrong.", "Choosing the colour of the hospital gowns.": "That has no ethical weight."},
         hints=["Ethics is about fairness and what is right.", "There are not enough hearts for everyone.", "Who should be first, and why?"]),
    dict(id="e15_vein_valves_direction", level=4, lo="15.1",
         stem="Fig. 1 shows the transport system. Blood in vessel Q (a vein) flows slowly and at low pressure. Why must blood in Q still flow in one direction only?",
         correct="So that blood returns to the heart to be pumped again; flowing backwards would stop the circulation.",
         wrongs={"So that the blood stays warm.": "Direction does not affect temperature.", "Because arteries flow backwards to balance it.": "Arteries also flow in one direction, away from the heart.", "It does not matter which way blood flows in veins.": "A one-way circuit is essential for the system to work."},
         hints=["The transport system is a loop: heart → arteries → capillaries → veins → heart.", "What would happen if the vein's blood went back towards the capillaries?", "One-way flow keeps the loop going."],
         fig=lambda rng: S.circulation()),

    # ------------------------------------------------------------ L5
    dict(id="e15_predict_potato_distilled", level=5, lo="15.4*",
         stem="Fig. 1 shows potato strips before and after soaking. A fresh strip of length 5.0 cm is placed in distilled water for an hour. Predict the result.",
         correct="It becomes longer and firmer, because water enters the cells by osmosis from the higher water concentration outside.",
         wrongs={"It becomes shorter and softer, because water leaves the cells.": "Distilled water has a HIGHER water concentration than the cells, so water enters.", "It stays the same, because distilled water contains no salt.": "The cells DO contain dissolved substances, so there is a difference in water concentration.", "It dissolves, because distilled water is pure.": "Potato tissue does not dissolve in water."},
         hints=["Compare the water concentration: pure water outside vs. cell contents inside.", "Water moves towards the lower water concentration.", "Water in → cells swell."],
         fig=lambda rng: S.potato_strips(5.0, 5.5)),
    dict(id="e15_cold_hands_evaluate", level=5, lo="15.5",
         stem="The table compares two habits.\n\n| Habit | Effect on blood vessels |\n|---|---|\n| regular exercise | vessels stay wide and flexible |\n| smoking | vessels narrow and stiffen |\n\nA smoker notices cold hands and feet. Which explanation is best?",
         correct="Narrowed vessels carry less warm blood to the hands and feet, so they feel cold.",
         wrongs={"Smoking cools the blood directly.": "Smoke does not cool the blood; it damages the vessels.", "Exercise would make the hands even colder.": "Exercise keeps vessels wide and improves blood flow.", "Cold hands are unrelated to the blood vessels.": "Blood carries heat; less flow means colder extremities."},
         hints=["Blood carries heat as well as oxygen.", "What does narrowing do to the flow?", "Less flow → less heat delivered."]),
    dict(id="e15_leaf_stomata_lower_evaluate", level=5, lo="15.2",
         stem="The table shows stomata counts on a leaf.\n\n| Surface | Stomata per mm² |\n|---|---|\n| upper | 5 |\n| lower | 180 |\n\nWhy is it an advantage to have most stomata on the lower surface?",
         correct="The lower surface is shaded and cooler, so less water is lost by evaporation while gases can still diffuse in and out.",
         wrongs={"Carbon dioxide is heavier and sinks to the lower surface.": "Gases mix; carbon dioxide does not collect under leaves.", "The lower surface gets more sunlight.": "The UPPER surface faces the sun.", "Stomata on top would let too much oxygen in.": "Leaves give oxygen OUT; the issue is water loss."},
         hints=["Stomata let gases through, but also let water vapour escape.", "Which surface is hotter and in direct sun?", "Fewer stomata on the hot side saves water."]),
    dict(id="e15_transport_system_fault_predict", level=5, lo="15.1",
         stem="Fig. 1 shows the transport system. A blood clot blocks an artery supplying part of the heart muscle. Predict the effect on that part of the muscle.",
         correct="It receives no oxygen or glucose, so its cells cannot respire and start to die (a heart attack).",
         wrongs={"It receives extra blood from the veins instead.": "Veins carry blood AWAY from the tissue towards the heart; they cannot supply it.", "Nothing happens, because the heart makes its own oxygen.": "Heart muscle, like all tissue, needs oxygen delivered by blood.", "The muscle grows larger to cope.": "Without oxygen the cells die rather than grow."},
         hints=["What do arteries deliver to tissues?", "What do cells need for respiration?", "No delivery → cells cannot survive."],
         fig=lambda rng: S.circulation()),
    dict(id="e15_experiment_control_shoot", level=5, lo="15.3*",
         stem="A student compares water uptake by a leafy shoot and the same shoot with its leaves removed (Fig. 1). The leafy shoot takes up far more water. What conclusion is justified?",
         correct="Water taken up by the xylem is mostly lost from the leaves, so removing the leaves reduces uptake.",
         wrongs={"Leaves absorb water from the air.": "Leaves LOSE water to the air; they do not absorb it.", "Removing leaves blocks the xylem.": "The xylem is intact; without leaves there is simply less water lost.", "The bare shoot has died.": "It still takes up some water, so it is alive."},
         hints=["Where does the water go after it rises up the xylem?", "Leaves have many stomata.", "No leaves → little water lost → little taken up."],
         fig=lambda rng: S.xy_graph([("leafy shoot", [(t, 150 - 10 * t) for t in range(7)]), ("leaves removed", [(t, 150 - 2 * t) for t in range(7)])], "time / h", "volume of water / cm³", 6, 160, 1, 20)),
]

register_explain(EXPLAIN, chapter=15)
