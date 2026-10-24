"""Ch 14 Human Digestive System: 25 calculation / data templates and 25 explanation items.
lo codes: 14.1 why digest, 14.2 parts and their functions, 14.3 physical and chemical digestion, 14.4* enzymes and end products (G3),
14.5 diet and diabetes, 14.6 bacteria (helpful / harmful) and food safety."""
from .. import figs, sketches as S
from .base import fmt, md_table, nice, numeric_options, pick, register_explain, template, text_options

PARTS = ["gullet", "stomach", "small intestine", "large intestine", "rectum"]   # letters P-T on the schematic, in this order
LETTERS = ["P", "Q", "R", "S", "T"]
FOODS = [("rice", 28, 2.7, 0.3), ("chicken breast", 0, 31, 3.6), ("egg", 1.1, 13, 11), ("bread", 49, 9, 3.2), ("milk", 5, 3.4, 3.3), ("peanuts", 16, 26, 49), ("banana", 23, 1.1, 0.3), ("tofu", 1.9, 8, 4.8)]


def _glucose_curve(peak, back_to=90, slow=False):
    import math
    pts = []
    for t in range(0, 181, 15):
        if t <= 45:
            v = 90 + (peak - 90) * (t / 45)
        else:
            k = 0.012 if slow else 0.03
            v = back_to + (peak - back_to) * math.exp(-k * (t - 45))
        pts.append((t, round(v)))
    return pts


# ================================================================ CALCULATION / DATA
# ---------------------------------------------------------------- L1
@template("c14_bar_chart_time_in_part", chapter=14, level=1, lo="14.2")
def bar_chart_time_in_part(rng):
    parts = ["mouth", "stomach", "small intestine", "large intestine"]
    times = [nice(rng, 1, 2) / 60 * 60 / 60, nice(rng, 2, 3, 4), nice(rng, 4, 5, 6), nice(rng, 10, 12, 16, 24)]
    times[0] = 0.1
    i = rng.randint(1, 3)
    opts, key, mis = numeric_options(rng, times[i], [(t, f"That is the bar for the {p}.") for j, (p, t) in enumerate(zip(parts, times)) if j != i and t > 0.5], unit="hours", sf=3)
    return dict(
        stem=f"Fig. 1 shows roughly how long food spends in each part of the digestive system. How long does food spend in the **{parts[i]}**?",
        figure=S.bar_chart(parts, times, "time / hours", ymax=30, ystep=5, size=(5.0, 3.0)),
        options=opts, key=key, misconceptions=mis,
        formula="read the height of the bar",
        working=[f"{parts[i]} bar → **{fmt(times[i])} hours**"],
        hints=[f"Find the bar labelled {parts[i]}.", "Read its top against the vertical scale.", "Each small square is 1 hour."],
    )


@template("c14_nutrient_table_highest", chapter=14, level=1, lo="14.5")
def nutrient_table_highest(rng):
    foods = rng.sample(FOODS, 4)
    col = pick(rng, [1, 2, 3])
    name = ["", "carbohydrate", "protein", "fat"][col]
    rows = [[f[0], fmt(f[1]), fmt(f[2]), fmt(f[3])] for f in foods]
    best = max(foods, key=lambda f: f[col])
    wrongs = {f[0]: f"{f[0]} has {fmt(f[col])} g of {name} per 100 g: less than the highest." for f in foods if f != best}
    opts, key, mis = text_options(rng, best[0], wrongs)
    return dict(
        stem=f"The table shows the nutrients in 100 g of some foods.\n\n{md_table(['Food', 'Carbohydrate / g', 'Protein / g', 'Fat / g'], rows)}\n\nWhich food contains the most **{name}** per 100 g?",
        options=opts, key=key, misconceptions=mis,
        formula="compare the values in the right column",
        working=[f"{name} column: highest is {fmt(best[col])} g → **{best[0]}**"],
        hints=[f"Find the {name} column.", "Compare the four numbers in it.", "Read the food name in the row with the biggest value."],
    )


@template("c14_iodine_test_count", chapter=14, level=1, lo="14.3")
def iodine_test_count(rng):
    foods = ["bread", "egg white", "potato", "cooking oil", "rice", "chicken"]
    starch = {"bread", "potato", "rice"}
    chosen = rng.sample(foods, 4)
    n = sum(1 for f in chosen if f in starch)
    n = max(n, 1)
    if sum(1 for f in chosen if f in starch) == 0:
        chosen[0] = "bread"
    rows = [[f, "blue-black" if f in starch else "stays yellow-brown"] for f in chosen]
    opts, key, mis = numeric_options(rng, n, [
        (4 - n if 4 - n > 0 else n + 2, "That is the number of foods WITHOUT starch (iodine stays yellow-brown)."),
        (n + 1, "Count only the foods that turned blue-black."),
        (4, "Not every food contains starch; check each result."),
    ], unit="", sf=1)
    return dict(
        stem=f"Iodine solution turns blue-black when starch is present. The table shows the results of testing four foods.\n\n{md_table(['Food', 'Colour with iodine'], rows)}\n\nHow many of the foods contain starch?",
        options=opts, key=key, misconceptions=mis,
        formula="blue-black = starch present",
        working=[f"blue-black: {', '.join(f for f in chosen if f in starch)}", f"= **{n}**"],
        hints=["Which colour shows that starch is present?", "Count the rows with that colour.", "Yellow-brown means no starch."],
    )


@template("c14_identify_part_letter", chapter=14, level=1, lo="14.2")
def identify_part_letter(rng):
    i = rng.randint(0, 4)
    part = PARTS[i]
    correct = LETTERS[i]
    wrongs = {L: f"{L} is the {PARTS[j]}." for j, L in enumerate(LETTERS) if j != i}
    wrongs = dict(rng.sample(list(wrongs.items()), 3))
    opts, key, mis = text_options(rng, f"letter {correct}", {f"letter {L}": v for L, v in wrongs.items()})
    return dict(
        stem=f"Fig. 1 shows the human digestive system. Which letter labels the **{part}**?",
        figure=S.digestive_schematic(),
        options=opts, key=key, misconceptions=mis,
        formula="follow the path of food: mouth → gullet → stomach → small intestine → large intestine → rectum → anus",
        working=[f"{part} = **letter {correct}**"],
        hints=["Food goes from the mouth down the gullet into the stomach.", "After the stomach comes the long, coiled small intestine, then the wider large intestine.", "The rectum is the last part before the anus."],
    )


@template("c14_glucose_rise_table", chapter=14, level=1, lo="14.5")
def glucose_rise_table(rng):
    before = nice(rng, 80, 85, 90, 95)
    rise = nice(rng, 30, 40, 50, 60, 70)
    after = before + rise
    opts, key, mis = numeric_options(rng, rise, [
        (after, "That is the level after the meal. The RISE is after − before."),
        (after + before, "You added. Subtract to find the rise."),
        (rise + 10, "Check the subtraction."),
    ], unit="mg per 100 cm³", sf=3)
    return dict(
        stem=f"A student's blood glucose was measured before and after a sugary drink.\n\n{md_table(['', 'Blood glucose / mg per 100 cm³'], [['before', str(before)], ['30 min after', str(after)]])}\n\nBy how much did the blood glucose level rise?",
        options=opts, key=key, misconceptions=mis,
        formula="rise = level after − level before",
        working=[f"{after} − {before} = **{rise} mg per 100 cm³**"],
        hints=["The rise is the difference between the two readings.", "Subtract the earlier reading from the later one.", f"{after} − {before}."],
    )


# ---------------------------------------------------------------- L2
@template("c14_nutrient_in_portion", chapter=14, level=2, lo="14.5")
def nutrient_in_portion(rng):
    food = pick(rng, [f for f in FOODS if f[2] >= 8])
    portion = nice(rng, 50, 150, 200, 250)
    col = pick(rng, [1, 2, 3])
    name = ["", "carbohydrate", "protein", "fat"][col]
    per100 = food[col]
    if per100 < 1:
        col, name, per100 = 2, "protein", food[2]
    ans = per100 * portion / 100
    opts, key, mis = numeric_options(rng, ans, [
        (per100, "That is the amount in 100 g. The portion is a different size."),
        (per100 * portion, "You forgot to divide by 100. The table gives grams per 100 g."),
        (per100 + portion, "You added. Scale the 100 g value up or down to the portion size."),
    ], unit="g", sf=3)
    return dict(
        stem=f"The table shows the nutrients in 100 g of {food[0]}.\n\n{md_table(['Carbohydrate / g', 'Protein / g', 'Fat / g'], [[fmt(food[1]), fmt(food[2]), fmt(food[3])]])}\n\nHow much **{name}** is there in a **{portion} g** portion?",
        options=opts, key=key, misconceptions=mis,
        formula="amount in portion = amount per 100 g × portion mass ÷ 100",
        working=[f"{fmt(per100)} g per 100 g", f"{fmt(per100)} × {portion} ÷ 100 = **{fmt(ans)} g**"],
        hints=["The table is for 100 g. How many lots of 100 g is the portion?", f"{portion} g is {portion}/100 of 100 g.", f"{fmt(per100)} × {portion}/100."],
    )


@template("c14_glucose_graph_read", chapter=14, level=2, lo="14.5")
def glucose_graph_read(rng):
    pts = _glucose_curve(nice(rng, 140, 150, 160))
    t = nice(rng, 30, 45, 60, 90, 120)
    ans = dict(pts)[t]
    opts, key, mis = numeric_options(rng, ans, [
        (dict(pts)[t + 15] if t + 15 <= 180 else dict(pts)[t - 15], "You read the value 15 minutes away from the time asked."),
        (max(v for _, v in pts), "That is the peak value, not the value at the time asked."),
        (t, "That is the time. Read the glucose level on the vertical axis."),
    ], unit="mg per 100 cm³", sf=3)
    return dict(
        stem=f"Fig. 1 shows a person's blood glucose level after a meal eaten at time 0. What is the level **{t} minutes** after the meal?",
        figure=figs.graph(pts, 180, 200, 30, 40, xlabel="time after meal / min", ylabel="blood glucose / mg per 100 cm³"),
        options=opts, key=key, misconceptions=mis,
        formula="read the curve at the given time",
        working=[f"at {t} min → **{ans} mg per 100 cm³**"],
        hints=["Find the time on the horizontal axis.", "Go up to the curve and across.", "Each small square on the vertical axis is 8 units."],
    )


@template("c14_enzyme_temperature_table", chapter=14, level=2, lo="14.4*")
def enzyme_temperature_table(rng):
    temps = [10, 25, 37, 60]
    times = [nice(rng, 20, 24), nice(rng, 8, 10), nice(rng, 2, 3), "no change after 30"]
    rows = [[str(T), str(t)] for T, t in zip(temps, times)]
    opts, key, mis = text_options(rng, "37 °C", {"10 °C": "At 10 °C the starch took longest to disappear: the enzyme worked slowest.", "25 °C": "Faster than at 10 °C, but not the fastest.", "60 °C": "At 60 °C the enzyme no longer worked at all: the starch never disappeared."})
    return dict(
        stem=f"Saliva (containing a carbohydrase) was mixed with starch solution at different temperatures. The table shows the time for the starch to disappear.\n\n{md_table(['Temperature / °C', 'Time for starch to disappear / min'], rows)}\n\nAt which temperature did the enzyme work **fastest**?",
        options=opts, key=key, misconceptions=mis,
        formula="fastest = shortest time for the starch to disappear",
        working=[f"shortest time is {times[2]} min at **37 °C** (body temperature)"],
        hints=["A faster enzyme digests the starch in LESS time.", "Find the shortest time in the table.", "The row with no change means the enzyme was destroyed by heat."],
    )


@template("c14_intestine_length_percent", chapter=14, level=2, lo="14.2")
def intestine_length_percent(rng):
    small = nice(rng, 6.0, 6.5, 7.0)
    large = nice(rng, 1.5, 1.8, 2.0)
    total = round(small + large, 1)
    pct = round(small / total * 100)
    opts, key, mis = numeric_options(rng, pct, [
        (round(large / total * 100), "That is the LARGE intestine's share."),
        (round(small / large * 100), "Divide by the TOTAL length, not by the large intestine."),
        (round(small * 10), "A percentage needs the part divided by the whole, × 100."),
    ], unit="%", sf=2)
    return dict(
        stem=f"The table shows the lengths of the two intestines in an adult.\n\n{md_table(['Part', 'Length / m'], [['small intestine', fmt(small)], ['large intestine', fmt(large)]])}\n\nWhat percentage of the total length of the intestines is the small intestine?",
        options=opts, key=key, misconceptions=mis,
        formula="percentage = part ÷ whole × 100",
        working=[f"total = {fmt(small)} + {fmt(large)} = {fmt(total)} m", f"{fmt(small)} ÷ {fmt(total)} × 100 = **{pct}%**"],
        hints=["First find the total length of both intestines.", "Then compare the small intestine with that total.", f"{fmt(small)} ÷ {fmt(total)} × 100."],
    )


@template("c14_bar_chart_digestion_time_diff", chapter=14, level=2, lo="14.3")
def bar_chart_digestion_time_diff(rng):
    foods = ["fruit juice", "rice", "chicken", "fried food"]
    times = [nice(rng, 20, 30), nice(rng, 60, 90), nice(rng, 120, 150), nice(rng, 180, 240)]
    i, j = pick(rng, [(0, 3), (1, 3), (0, 2), (1, 2)])
    diff = times[j] - times[i]
    opts, key, mis = numeric_options(rng, diff, [
        (times[j], f"That is the time for {foods[j]} alone, not the difference."),
        (times[i], f"That is the time for {foods[i]}."),
        (times[i] + times[j], "You added. 'How much longer' means subtract."),
    ], unit="min", sf=3)
    return dict(
        stem=f"Fig. 1 shows roughly how long different foods take to leave the stomach. How much longer does **{foods[j]}** take than **{foods[i]}**?",
        figure=S.bar_chart(foods, times, "time in stomach / min", ymax=300, ystep=50, size=(5.0, 3.0)),
        options=opts, key=key, misconceptions=mis,
        formula="difference = longer time − shorter time",
        working=[f"{foods[j]}: {times[j]} min; {foods[i]}: {times[i]} min", f"difference = **{diff} min**"],
        hints=["Read both bars.", "Subtract the shorter time from the longer.", f"{times[j]} − {times[i]}."],
    )


# ---------------------------------------------------------------- L3
@template("c14_surface_area_cut", chapter=14, level=3, lo="14.3")
def surface_area_cut(rng):
    s = nice(rng, 2, 4, 6)
    sa1 = 6 * s * s
    half = s / 2
    sa8 = 8 * 6 * half * half
    opts, key, mis = numeric_options(rng, sa8, [
        (sa1, "That is the surface area of the whole cube. Cutting it exposes new faces, so the total increases."),
        (sa1 * 8, "Each small cube is smaller than the original; its surface area is not the same as the big cube's."),
        (6 * half * half, "That is the surface area of ONE small cube. There are eight of them."),
    ], unit="cm²", sf=3)
    return dict(
        stem=f"Fig. 1 shows a cube of food with sides of **{s} cm**. Chewing cuts it into **8 equal smaller cubes**. What is the total surface area of the 8 small cubes?",
        figure=figs.labelled_block(s, s, s),
        options=opts, key=key, misconceptions=mis,
        formula="surface area of a cube = 6 × side²; total = 8 × surface area of one small cube",
        working=[f"small cube side = {s} ÷ 2 = {fmt(half)} cm", f"one small cube: 6 × {fmt(half)}² = {fmt(6 * half * half)} cm²", f"eight cubes: 8 × {fmt(6 * half * half)} = **{fmt(sa8)} cm²** (double the original {sa1} cm²)"],
        hints=["Cutting the cube in half along each direction gives 8 cubes with half the side length.", "Surface area of a cube = 6 × side × side.", "Work out one small cube, then multiply by 8."],
    )


@template("c14_glucose_two_people_peak_diff", chapter=14, level=3, lo="14.5")
def glucose_two_people_peak_diff(rng):
    pA = nice(rng, 130, 140, 150)
    pB = nice(rng, 190, 200, 220)
    A = _glucose_curve(pA)
    B = _glucose_curve(pB, back_to=130, slow=True)
    diff = pB - pA
    opts, key, mis = numeric_options(rng, diff, [
        (pB, "That is B's peak level, not the difference between the peaks."),
        (pA, "That is A's peak level."),
        (pB - 90, "That is how much B's level rose above the starting level, not the gap between the two peaks."),
    ], unit="mg per 100 cm³", sf=3)
    return dict(
        stem="Fig. 1 shows the blood glucose of two people after the same meal. A is healthy; B has diabetes. How much higher is B's **peak** level than A's?",
        figure=S.xy_graph([("A (healthy)", A), ("B (diabetes)", B)], "time after meal / min", "blood glucose / mg per 100 cm³", 180, 240, 30, 40),
        options=opts, key=key, misconceptions=mis,
        formula="difference = B's highest value − A's highest value",
        working=[f"B peaks at {pB}; A peaks at {pA}", f"difference = **{diff} mg per 100 cm³**"],
        hints=["Find the highest point of each curve.", "Subtract A's from B's.", "In diabetes the level rises higher and stays high longer."],
    )


@template("c14_enzyme_rate", chapter=14, level=3, lo="14.4*")
def enzyme_rate(rng):
    start = nice(rng, 10, 12, 15, 20)   # g starch
    t = nice(rng, 4, 5, 8, 10)
    rate = nice(rng, 0.5, 1.0, 1.5, 2.0)
    left = round(start - rate * t, 1)
    if left < 0:
        left, t = 0.0, start / rate
    opts, key, mis = numeric_options(rng, rate, [
        (round(start - left, 1), "That is the total starch digested. Divide by the time for the rate."),
        (round(left / t, 2) if left else rate * 2, "You used the starch LEFT instead of the starch digested."),
        (round((start - left) * t, 1), "You multiplied. Rate = amount digested ÷ time."),
    ], unit="g per minute", sf=3)
    return dict(
        stem=f"A carbohydrase was added to starch and the mass of starch remaining was measured.\n\n{md_table(['Time / min', 'Starch remaining / g'], [['0', str(start)], [fmt(t), fmt(left)]])}\n\nWhat is the average rate at which the starch was digested?",
        options=opts, key=key, misconceptions=mis,
        formula="rate = mass of starch digested ÷ time",
        working=[f"digested = {start} − {fmt(left)} = {fmt(start - left)} g", f"rate = {fmt(start - left)} ÷ {fmt(t)} = **{fmt(rate)} g per minute**"],
        hints=["First find how much starch disappeared.", "Share that over the minutes.", f"({start} − {fmt(left)}) ÷ {fmt(t)}."],
    )


@template("c14_water_absorbed_percent", chapter=14, level=3, lo="14.2")
def water_absorbed_percent(rng):
    into = nice(rng, 1000, 1200, 1500, 2000)
    out = nice(rng, 100, 150, 200)
    pct = round((into - out) / into * 100)
    opts, key, mis = numeric_options(rng, pct, [
        (round(out / into * 100), "That is the percentage LOST in the faeces, not absorbed."),
        (into - out, "That is the volume absorbed in cm³, not the percentage."),
        (round((into - out) / out * 100), "Divide by the volume entering, not by the volume leaving."),
    ], unit="%", sf=2)
    return dict(
        stem=f"The table shows the water entering and leaving the large intestine each day.\n\n{md_table(['', 'Volume of water / cm³ per day'], [['entering the large intestine', str(into)], ['leaving in the faeces', str(out)]])}\n\nWhat percentage of the water entering the large intestine is absorbed?",
        options=opts, key=key, misconceptions=mis,
        formula="absorbed = in − out; percentage = absorbed ÷ in × 100",
        working=[f"absorbed = {into} − {out} = {into - out} cm³", f"{into - out} ÷ {into} × 100 = **{pct}%**"],
        hints=["The large intestine absorbs water, so what goes in minus what comes out is the amount absorbed.", "Turn that into a percentage of the water entering.", f"({into} − {out}) ÷ {into} × 100."],
    )


@template("c14_meal_energy_sum", chapter=14, level=3, lo="14.5")
def meal_energy_sum(rng):
    items = rng.sample([("rice", 130), ("chicken", 165), ("egg", 155), ("bread", 265), ("banana", 90), ("milk", 60)], 3)
    portions = [nice(rng, 100, 150, 200), nice(rng, 50, 100), nice(rng, 100, 200, 250)]
    rows = [[n, str(k), str(p)] for (n, k), p in zip(items, portions)]
    total = sum(k * p / 100 for (n, k), p in zip(items, portions))
    opts, key, mis = numeric_options(rng, total, [
        (sum(k for n, k in items), "That is the energy for 100 g of each. Scale each to its portion first."),
        (max(k * p / 100 for (n, k), p in zip(items, portions)), "That is one food only. Add all three."),
        (sum(k * p for (n, k), p in zip(items, portions)), "You forgot to divide by 100 for each food."),
    ], unit="kcal", sf=3)
    return dict(
        stem=f"The table shows the energy content of foods and the portion eaten.\n\n{md_table(['Food', 'Energy / kcal per 100 g', 'Portion / g'], rows)}\n\nWhat is the total energy in the meal?",
        options=opts, key=key, misconceptions=mis,
        formula="energy of each food = kcal per 100 g × portion ÷ 100; add them",
        working=[", ".join(f"{n}: {fmt(k * p / 100)} kcal" for (n, k), p in zip(items, portions)), f"total = **{fmt(total)} kcal**"],
        hints=["Work out each food separately: value per 100 g × portion ÷ 100.", "Then add the three.", "Check the portion sizes carefully."],
    )


# ---------------------------------------------------------------- L4
@template("c14_glucose_return_time", chapter=14, level=4, lo="14.5")
def glucose_return_time(rng):
    pA = nice(rng, 140, 150, 160)
    A = _glucose_curve(pA)
    B = _glucose_curve(200, back_to=130, slow=True)
    target = 100
    tA = next(t for t, v in A if t > 45 and v <= target)
    opts, key, mis = numeric_options(rng, tA, [
        (45, "That is when A's level PEAKS, not when it returns to 100."),
        (tA + 30 if tA + 30 <= 180 else tA - 30, "Read where curve A first drops to 100 after the peak."),
        (180, "That is the end of the graph; B never gets back to 100, but A does earlier."),
    ], unit="min", sf=3)
    return dict(
        stem="Fig. 1 shows blood glucose after a meal for a healthy person (A) and a person with diabetes (B). After how many minutes does **A's** level first fall back to **100 mg per 100 cm³**?",
        figure=S.xy_graph([("A (healthy)", A), ("B (diabetes)", B)], "time after meal / min", "blood glucose / mg per 100 cm³", 180, 240, 30, 40),
        options=opts, key=key, misconceptions=mis,
        formula="find 100 on the vertical axis, move across to the falling part of curve A, read the time below",
        working=[f"curve A falls to 100 at about **{tA} min**"],
        hints=["Start at 100 on the vertical axis.", "Go across to where curve A comes DOWN through that level.", "Read the time below that point."],
    )


@template("c14_enzyme_temp_bar_chart", chapter=14, level=4, lo="14.4*")
def enzyme_temp_bar_chart(rng):
    temps = ["10", "20", "30", "37", "45", "60"]
    vals = [nice(rng, 1, 2), nice(rng, 3, 4), nice(rng, 6, 7), nice(rng, 9, 10), nice(rng, 4, 5), 0]
    vals[5] = 0.0
    opts, key, mis = text_options(rng, "37 °C", {"30 °C": "Starch was digested quickly at 30 °C, but even faster at the next temperature.", "45 °C": "Above body temperature the rate falls as the enzyme starts to be damaged.", "60 °C": "At 60 °C no starch was digested: the enzyme was destroyed."})
    return dict(
        stem="Fig. 1 shows the mass of starch digested in 5 minutes by a carbohydrase at different temperatures. At which temperature does the enzyme work best?",
        figure=S.bar_chart([t + " °C" for t in temps], vals, "starch digested in 5 min / g", ymax=12, ystep=2, size=(5.2, 3.0)),
        options=opts, key=key, misconceptions=mis,
        formula="the best temperature gives the most starch digested",
        working=["tallest bar is at **37 °C**, body temperature"],
        hints=["Which bar is tallest?", "Read its temperature label.", "Human enzymes work best at body temperature."],
    )


@template("c14_diet_pie_chart", chapter=14, level=4, lo="14.5")
def diet_pie_chart(rng):
    groups = ["fruit and vegetables", "wholegrains", "protein foods", "others"]
    pcts = [nice(rng, 45, 50), 25, nice(rng, 20, 25), None]
    pcts[3] = 100 - sum(p for p in pcts if p)
    if pcts[3] <= 0:
        pcts = [45, 25, 20, 10]
    mass = nice(rng, 400, 500, 600)
    i = rng.randint(0, 2)
    ans = mass * pcts[i] / 100
    opts, key, mis = numeric_options(rng, ans, [
        (pcts[i], "That is the percentage, not the mass."),
        (mass * (100 - pcts[i]) / 100, f"That is everything EXCEPT {groups[i]}."),
        (mass / 4, "The groups are not equal shares."),
    ], unit="g", sf=3)
    return dict(
        stem=f"Fig. 1 shows a healthy plate: the share of each food group by mass. For a **{mass} g** meal, what mass of **{groups[i]}** should it contain?",
        figure=S.pie_chart([f"{g} ({p}%)" for g, p in zip(groups, pcts)], pcts),
        options=opts, key=key, misconceptions=mis,
        formula="mass = percentage ÷ 100 × total mass",
        working=[f"{groups[i]}: {pcts[i]}% of {mass} g = **{fmt(ans)} g**"],
        hints=[f"Read the percentage for {groups[i]}.", "Apply it to the total mass of the meal.", f"{pcts[i]}/100 × {mass}."],
    )


@template("c14_starch_graph_with_without_enzyme", chapter=14, level=4, lo="14.4*")
def starch_graph_with_without_enzyme(rng):
    start = nice(rng, 10, 12, 16)
    with_e = [(t, round(start * (1 - t / 10), 1)) for t in range(0, 11, 2)]
    without = [(t, start) for t in range(0, 11, 2)]
    t = nice(rng, 2, 4, 6, 8)
    ans = start - dict(with_e)[t]
    opts, key, mis = numeric_options(rng, ans, [
        (dict(with_e)[t], "That is the starch REMAINING, not the amount digested."),
        (start, "That is the starting amount; the question asks how much has been digested by that time."),
        (ans / 2, "Check the reading: digested = start − remaining."),
    ], unit="g", sf=3)
    return dict(
        stem=f"Fig. 1 shows the mass of starch in two tubes at 37 °C: one with a carbohydrase, one with water instead. How much starch has been **digested** in the enzyme tube after **{t} minutes**?",
        figure=S.xy_graph([("with enzyme", with_e), ("without enzyme", without)], "time / min", "starch remaining / g", 10, start + 4, 2, 4 if start >= 12 else 2),
        options=opts, key=key, misconceptions=mis,
        formula="digested = starting mass − mass remaining",
        working=[f"remaining at {t} min = {fmt(dict(with_e)[t])} g", f"digested = {start} − {fmt(dict(with_e)[t])} = **{fmt(ans)} g**"],
        hints=["Read the 'with enzyme' line at the time asked.", "That is what is LEFT. Subtract it from the start.", "The flat line shows no digestion without the enzyme."],
    )


@template("c14_diabetes_table_percent", chapter=14, level=4, lo="14.5")
def diabetes_table_percent(rng):
    y1, y2 = nice(rng, 8.0, 9.0, 10.0), None
    inc = nice(rng, 20, 25, 40, 50)
    y2 = round(y1 * (100 + inc) / 100, 1)
    opts, key, mis = numeric_options(rng, inc, [
        (round(y2 - y1, 1), "That is the rise in percentage points of the population. The question asks the percentage INCREASE relative to 2010."),
        (round((y2 - y1) / y2 * 100), "Divide by the 2010 value, not the 2020 value."),
        (y2, "That is the 2020 figure itself."),
    ], unit="%", sf=3)
    return dict(
        stem=f"The table shows the share of adults in a country with diabetes.\n\n{md_table(['Year', 'Adults with diabetes / %'], [['2010', fmt(y1)], ['2020', fmt(y2)]])}\n\nBy what percentage did the 2010 figure increase by 2020?",
        options=opts, key=key, misconceptions=mis,
        formula="percentage increase = (new − old) ÷ old × 100",
        working=[f"increase = {fmt(y2)} − {fmt(y1)} = {fmt(y2 - y1)}", f"{fmt(y2 - y1)} ÷ {fmt(y1)} × 100 = **{inc}%**"],
        hints=["Find the change first.", "Compare the change with the ORIGINAL (2010) value.", f"({fmt(y2)} − {fmt(y1)}) ÷ {fmt(y1)} × 100."],
    )


# ---------------------------------------------------------------- L5
@template("c14_enzyme_ph_table", chapter=14, level=5, lo="14.4*")
def enzyme_ph_table(rng):
    labels = rng.sample(["X", "Y", "Z"], 3)
    acid, neut, alk = labels
    a2, n9, z9 = nice(rng, 9, 10, 11, 12), nice(rng, 7, 8, 9), nice(rng, 8, 9, 10)
    rows = [[acid, str(a2), "0"], [neut, "0", str(n9)], [alk, "0", str(z9)]]
    rng.shuffle(rows)
    opts, key, mis = text_options(rng, f"{acid}, because it works at the acidic pH of the stomach", {
        f"{neut}, because it works at neutral pH": f"{neut} works at pH 7, but the stomach is strongly acidic (pH about 2).",
        f"{alk}, because it digested the most at pH 9": f"{alk} works in alkaline conditions, like the small intestine, not the stomach.",
        f"{acid}, because it digests the most protein in total": f"{acid} digests protein well, but the reason it suits the stomach is the pH it works at."})
    return dict(
        stem=f"Three proteases were tested at two pH values. The table shows the mass of protein digested in 10 minutes.\n\n{md_table(['Enzyme', 'Protein digested at pH 2 / g', 'Protein digested at pH 9 / g'], rows)}\n\nGastric juice in the stomach has a pH of about 2. Which enzyme is most likely to be the protease in gastric juice, and why?",
        options=opts, key=key, misconceptions=mis,
        formula="an enzyme works in the conditions of the part that makes it: stomach = acidic",
        working=[f"only {acid} digests protein at pH 2", f"**{acid}, because it works at the acidic pH of the stomach**"],
        hints=["What is the pH inside the stomach?", "Which enzyme digests protein at that pH?", "Match the enzyme to the stomach's conditions."],
    )


@template("c14_glucose_gradient", chapter=14, level=5, lo="14.5")
def glucose_gradient(rng):
    peak = nice(rng, 140, 150, 160, 170)
    pts = _glucose_curve(peak)
    rate = (peak - 90) / 45
    opts, key, mis = numeric_options(rng, rate, [
        (peak - 90, "That is the total rise. Divide by the time taken (45 min) for the rate."),
        (peak / 45, "Use the RISE (peak − start), not the peak value."),
        ((peak - 90) / 30, "The rise takes 45 minutes, not 30. Check the time of the peak."),
    ], unit="mg per 100 cm³ per minute", sf=3)
    return dict(
        stem="Fig. 1 shows blood glucose after a meal. What is the average rate of increase of blood glucose from the meal (time 0) to the peak?",
        figure=figs.graph(pts, 180, 200, 30, 40, xlabel="time after meal / min", ylabel="blood glucose / mg per 100 cm³"),
        options=opts, key=key, misconceptions=mis,
        formula="rate = (peak level − starting level) ÷ time to peak",
        working=[f"rise = {peak} − 90 = {peak - 90}", f"time to peak = 45 min", f"rate = {peak - 90} ÷ 45 = **{fmt(rate)} mg per 100 cm³ per minute**"],
        hints=["Read the starting level and the peak level.", "Read how long the rise took.", "Rate = rise ÷ time."],
    )


@template("c14_surface_area_ratio_two_cubes", chapter=14, level=5, lo="14.3")
def surface_area_ratio_two_cubes(rng):
    big = nice(rng, 2, 3, 4)
    small = 1
    n_small = big ** 3
    sa_big = 6 * big * big
    sa_small_total = n_small * 6
    ratio = sa_small_total / sa_big
    opts, key, mis = numeric_options(rng, ratio, [
        (n_small, "That is the NUMBER of small cubes. The question asks how many times the surface area increased."),
        (ratio * big, "Check: total surface area of the small cubes ÷ surface area of the big cube."),
        (1, "Cutting food into smaller pieces INCREASES the total surface area."),
    ], unit="times", sf=3)
    return dict(
        stem=f"Fig. 1 shows a cube of food of side **{big} cm**. Chewing breaks it into **1 cm** cubes. By how many times does the total surface area increase?",
        figure=figs.labelled_block(big, big, big),
        options=opts, key=key, misconceptions=mis,
        formula="number of 1 cm cubes = side³; total SA = number × 6; ratio = total SA ÷ original SA (6 × side²)",
        working=[f"original surface area = 6 × {big}² = {sa_big} cm²", f"{n_small} small cubes × 6 cm² = {sa_small_total} cm²", f"increase = {sa_small_total} ÷ {sa_big} = **{fmt(ratio)} times**"],
        hints=["How many 1 cm cubes fit in the big cube? (side × side × side)", "Each 1 cm cube has a surface area of 6 cm².", "Divide the new total by the original surface area."],
    )


@template("c14_nutrient_absorbed_percent", chapter=14, level=5, lo="14.1")
def nutrient_absorbed_percent(rng):
    eaten = nice(rng, 60, 80, 100, 120)
    lost = nice(rng, 6, 8, 12, 15, 20)
    pct = round((eaten - lost) / eaten * 100)
    opts, key, mis = numeric_options(rng, pct, [
        (round(lost / eaten * 100), "That is the percentage NOT absorbed (lost in faeces)."),
        (eaten - lost, "That is the mass absorbed in grams, not the percentage."),
        (round((eaten - lost) / lost * 100), "Divide by the amount eaten, not the amount lost."),
    ], unit="%", sf=2)
    return dict(
        stem=f"A study measured the protein a person ate in a day and the protein found in the faeces.\n\n{md_table(['', 'Protein / g per day'], [['eaten', str(eaten)], ['in faeces', str(lost)]])}\n\nWhat percentage of the protein eaten was digested and absorbed into the blood?",
        options=opts, key=key, misconceptions=mis,
        formula="absorbed = eaten − in faeces; percentage = absorbed ÷ eaten × 100",
        working=[f"absorbed = {eaten} − {lost} = {eaten - lost} g", f"{eaten - lost} ÷ {eaten} × 100 = **{pct}%**"],
        hints=["Protein that is not absorbed leaves in the faeces.", "Absorbed = eaten − lost.", f"({eaten} − {lost}) ÷ {eaten} × 100."],
    )


@template("c14_sugar_limit_cans", chapter=14, level=5, lo="14.5")
def sugar_limit_cans(rng):
    limit = nice(rng, 25, 30, 36)
    per_can = nice(rng, 30, 35, 39, 42)
    teaspoon = 4
    cans_limit = limit / per_can
    excess = per_can - limit
    tsp = excess / teaspoon
    opts, key, mis = numeric_options(rng, tsp, [
        (per_can / teaspoon, "That is the total sugar in the can in teaspoons, not the amount OVER the limit."),
        (excess, "That is the excess in grams. Convert to teaspoons (÷ 4)."),
        (limit / teaspoon, "That is the daily limit in teaspoons."),
    ], unit="teaspoons", sf=3)
    return dict(
        stem=f"Health guidelines suggest a limit of **{limit} g** of added sugar a day. One can of a soft drink contains **{per_can} g** of sugar. One teaspoon holds 4 g of sugar.\n\n{md_table(['Quantity', 'Value'], [['daily limit', f'{limit} g'], ['sugar per can', f'{per_can} g'], ['sugar per teaspoon', '4 g']])}\n\nBy how many **teaspoons** of sugar does one can exceed the daily limit?",
        options=opts, key=key, misconceptions=mis,
        formula="excess = sugar per can − limit; teaspoons = excess ÷ 4",
        working=[f"excess = {per_can} − {limit} = {excess} g", f"= {excess} ÷ 4 = **{fmt(tsp)} teaspoons**"],
        hints=["First find how many grams over the limit one can is.", "Then convert grams to teaspoons.", f"({per_can} − {limit}) ÷ 4."],
    )


# ================================================================ EXPLANATION
EXPLAIN = [
    # ------------------------------------------------------------ L1
    dict(id="e14_why_digest", level=1, lo="14.1",
         stem="Fig. 1 shows food being broken down. Why must food be digested?",
         correct="Large, insoluble food molecules must be broken down into small, soluble molecules that can be absorbed into the blood.",
         wrongs={"To make the food taste better.": "Taste is not the purpose of digestion.", "To kill all the bacteria in the food.": "Stomach acid kills some germs, but digestion is about breaking food down for absorption.", "To turn food into blood.": "Food molecules are absorbed INTO the blood; they do not become blood."},
         hints=["Think about the size of starch and protein molecules.", "Only small, soluble molecules can pass into the blood.", "Large → small, insoluble → soluble."],
         fig=lambda rng: S.flow_boxes(["large insoluble\nfood molecules", "small soluble\nmolecules", "absorbed\ninto blood"])),
    dict(id="e14_physical_vs_chemical", level=1, lo="14.3",
         stem="The table compares two kinds of digestion.\n\n| Kind | What happens |\n|---|---|\n| X | food is broken into smaller pieces by teeth and churning |\n| Y | digestive juices break large molecules into small ones |\n\nWhich statement is correct?",
         correct="X is physical digestion and Y is chemical digestion.",
         wrongs={"X is chemical digestion and Y is physical digestion.": "Teeth and churning change the SIZE of pieces, not the molecules: that is physical.", "Both X and Y are physical digestion.": "Y changes the molecules themselves, which is chemical digestion.", "Both X and Y are chemical digestion.": "X does not change the molecules, only the size of the pieces."},
         hints=["Physical digestion changes the size of the pieces.", "Chemical digestion changes the molecules, using digestive juices.", "Match each row."]),
    dict(id="e14_gullet_function", level=1, lo="14.2",
         stem="Fig. 1 shows the digestive system. What happens in the gullet (P)?",
         correct="Muscles push the food down to the stomach; no digestion takes place.",
         wrongs={"Starch is digested by saliva.": "Starch digestion begins in the MOUTH; the gullet only moves food along.", "Proteins are digested by gastric juice.": "That happens in the stomach.", "Water is absorbed.": "Water is absorbed in the large intestine."},
         hints=["The gullet is the tube between the mouth and the stomach.", "It is a passage, not a place where digestive juices are added.", "Transport only."],
         fig=lambda rng: S.digestive_schematic()),
    dict(id="e14_large_intestine_function", level=1, lo="14.2",
         stem="Fig. 1 shows the digestive system. What is the main function of the large intestine (S)?",
         correct="It absorbs water and mineral salts from the undigested food.",
         wrongs={"It digests proteins.": "Protein digestion happens in the stomach and small intestine.", "It absorbs digested food into the blood.": "That is the small intestine's job.", "It stores faeces before they leave the body.": "The rectum stores faeces."},
         hints=["By the time food reaches the large intestine, digestion is finished.", "What is left is watery undigested food.", "The faeces leave firm because something has been removed."],
         fig=lambda rng: S.digestive_schematic()),
    dict(id="e14_order_of_parts", level=1, lo="14.2",
         stem="Fig. 1 shows the path of food. Which list gives the parts in the correct order?",
         correct="mouth → gullet → stomach → small intestine → large intestine → rectum → anus",
         wrongs={"mouth → stomach → gullet → small intestine → large intestine → rectum → anus": "The gullet comes BEFORE the stomach: it carries food down to it.", "mouth → gullet → stomach → large intestine → small intestine → rectum → anus": "The small intestine comes before the large intestine.", "mouth → gullet → small intestine → stomach → large intestine → anus → rectum": "The stomach comes before the small intestine, and the rectum before the anus."},
         hints=["Follow the arrows in Fig. 1.", "The gullet links mouth and stomach; the small intestine comes before the large.", "Rectum, then anus."],
         fig=lambda rng: S.flow_boxes(["mouth", "gullet", "stomach", "small\nintestine", "large\nintestine", "rectum", "anus"], fs=8.5, size=(11, 1.6))),

    # ------------------------------------------------------------ L2
    dict(id="e14_identify_part_by_function", level=2, lo="14.2",
         hints=["Match the function to the part: mouth chews; stomach churns and digests protein; small intestine finishes digestion and absorbs food; large intestine absorbs water; rectum stores faeces.", "Find the letter for that part on the diagram.", "Food travels top to bottom."],
         fig=lambda rng: S.digestive_schematic(),
         variants=[
             dict(stem="Fig. 1 shows the digestive system. In which part is digested food absorbed into the blood?", correct="R", wrongs={"Q": "Q is the stomach, where protein digestion begins.", "S": "S is the large intestine, which absorbs water.", "P": "P is the gullet, which only transports food."}),
             dict(stem="Fig. 1 shows the digestive system. In which part does gastric juice digest proteins and kill germs?", correct="Q", wrongs={"P": "P is the gullet.", "R": "R is the small intestine, the main site of digestion and absorption.", "T": "T is the rectum."}),
             dict(stem="Fig. 1 shows the digestive system. Which part stores faeces until they leave the body?", correct="T", wrongs={"S": "S is the large intestine, which absorbs water.", "R": "R is the small intestine.", "Q": "Q is the stomach."}),
         ]),
    dict(id="e14_where_digestion_begins", level=2, lo="14.3",
         hints=["Each nutrient is digested by a different juice, and each juice is found in a different part.", "Which nutrient is the question about? Which juice in the table acts on it?", "Match it to the FIRST part where that juice is found; fats have only one place."],
         variants=[
             dict(stem="The table shows where digestive juices act.\n\n| Part | Juice present |\n|---|---|\n| mouth | saliva |\n| stomach | gastric juice |\n| small intestine | intestinal and pancreatic juices |\n\nWhere does the chemical digestion of **starch** begin?", correct="in the mouth", wrongs={"in the stomach": "Gastric juice digests protein, not starch.", "in the small intestine": "Starch digestion is completed there, but it BEGINS earlier.", "in the gullet": "No digestion takes place in the gullet."}),
             dict(stem="The table shows where digestive juices act.\n\n| Part | Juice present |\n|---|---|\n| mouth | saliva |\n| stomach | gastric juice |\n| small intestine | intestinal and pancreatic juices |\n\nWhere does the chemical digestion of **protein** begin?", correct="in the stomach", wrongs={"in the mouth": "Saliva digests starch, not protein.", "in the small intestine": "Protein digestion is completed there, but it begins earlier.", "in the large intestine": "No digestion takes place in the large intestine."}),
             dict(stem="The table shows where digestive juices act.\n\n| Part | Juice present |\n|---|---|\n| mouth | saliva |\n| stomach | gastric juice |\n| small intestine | intestinal and pancreatic juices |\n\nWhere is **fat** digested?", correct="only in the small intestine", wrongs={"in the mouth and stomach": "Neither saliva nor gastric juice digests fat.", "in the stomach only": "Gastric juice digests protein.", "in every part of the system": "Fat is digested in one place only."}),
         ]),
    dict(id="e14_classify_digestion_action", level=2, lo="14.3",
         hints=["Physical: pieces get smaller (teeth, churning). Chemical: digestive juices change the molecules.", "Does the action involve a digestive juice?", "No juice → physical."],
         variants=[
             dict(stem="The table lists actions in the digestive system.\n\n| Action |\n|---|\n| teeth cut and grind food |\n| saliva acts on starch |\n| stomach muscles churn food |\n| gastric juice acts on protein |\n\nWhich two actions are **physical** digestion?", correct="teeth grinding and stomach churning", wrongs={"saliva on starch and gastric juice on protein": "Both involve digestive juices changing molecules: chemical digestion.", "teeth grinding and saliva on starch": "Saliva's action is chemical.", "stomach churning and gastric juice on protein": "Gastric juice's action is chemical."}),
             dict(stem="The table lists actions in the digestive system.\n\n| Action |\n|---|\n| teeth cut and grind food |\n| saliva acts on starch |\n| stomach muscles churn food |\n| gastric juice acts on protein |\n\nWhich two actions are **chemical** digestion?", correct="saliva on starch and gastric juice on protein", wrongs={"teeth grinding and stomach churning": "These only make the pieces smaller: physical digestion.", "teeth grinding and saliva on starch": "Teeth grinding is physical.", "stomach churning and gastric juice on protein": "Churning is physical."}),
         ]),
    dict(id="e14_end_products", level=2, lo="14.4*",
         hints=["Each enzyme class is named after the food it digests: carbohydr-ases, prote-ases, lip-ases (lipids are fats).", "The end products are the small building blocks of that food type.", "Match the enzyme class to its food, then to the small molecules it is made of."],
         fig=lambda rng: S.flow_boxes(["large molecule", "enzyme", "end product"]),
         variants=[
             dict(stem="Fig. 1 shows digestion by an enzyme. What are the end products when **protein** is digested by proteases?", correct="amino acids", wrongs={"simple sugars (glucose)": "Simple sugars come from carbohydrates.", "fatty acids and glycerol": "These come from fats.", "water and carbon dioxide": "These are products of respiration, not digestion."}),
             dict(stem="Fig. 1 shows digestion by an enzyme. What are the end products when **fat** is digested by lipases?", correct="fatty acids and glycerol", wrongs={"amino acids": "Amino acids come from proteins.", "simple sugars": "Simple sugars come from carbohydrates.", "oxygen and water": "These are not digestion products."}),
             dict(stem="Fig. 1 shows digestion by an enzyme. Which class of enzyme digests **starch**?", correct="carbohydrases", wrongs={"proteases": "Proteases digest proteins.", "lipases": "Lipases digest fats.", "gastric acid": "Acid is not an enzyme; it kills germs and helps the stomach's protease."}),
         ]),
    dict(id="e14_bacteria_helpful_harmful", level=2, lo="14.6",
         stem="The table describes some bacteria.\n\n| Bacteria | Where / what |\n|---|---|\n| W | live in the large intestine and help keep us healthy |\n| X | used to turn milk into yoghurt |\n| Y | grow on badly stored chicken and cause food poisoning |\n| Z | used to make cheese |\n\nWhich bacteria are **harmful**?",
         correct="Y only",
         wrongs={"W and Y": "W are helpful gut bacteria.", "X, Y and Z": "X and Z are used to make foods: helpful.", "all of them": "Most bacteria listed are helpful; only one causes disease."},
         hints=["Helpful bacteria live in the gut or make foods.", "Harmful bacteria cause illness.", "Which row mentions illness?"]),

    # ------------------------------------------------------------ L3
    dict(id="e14_chewing_helps", level=3, lo="14.3",
         stem="Fig. 1 shows a cube of food before and after it is cut into smaller cubes. Why does chewing food well help digestion?",
         correct="It increases the surface area of the food, so digestive juices can act on it faster.",
         wrongs={"It adds more digestive juices to the food.": "Chewing itself adds no juice; saliva is added whether or not you chew well.", "It changes the food molecules into smaller ones.": "Chewing is physical digestion; it does not change the molecules.", "It makes the food heavier.": "Chewing does not change the mass."},
         hints=["Compare the total surface area of one big cube with eight small ones.", "Digestive juices work on the surface of the food.", "More surface → faster chemical digestion."],
         fig=lambda rng: figs.labelled_block(2, 2, 2)),
    dict(id="e14_stomach_acid_role", level=3, lo="14.2",
         stem="The table shows the pH in two parts of the digestive system.\n\n| Part | pH |\n|---|---|\n| stomach | 2 |\n| small intestine | 8 |\n\nWhat is one role of the acid in the stomach?",
         correct="It kills many of the germs that enter with food.",
         wrongs={"It digests starch.": "Starch digestion needs a carbohydrase and does not happen in the stomach.", "It absorbs water from food.": "Water is absorbed in the large intestine.", "It neutralises the food.": "Acid makes the contents acidic; it does not neutralise them."},
         hints=["The stomach's contents are very acidic (pH 2).", "Many bacteria cannot survive at that pH.", "Protection, plus the right conditions for the stomach's protease."]),
    dict(id="e14_small_intestine_long", level=3, lo="14.2",
         stem="The table shows the lengths of parts of the digestive system.\n\n| Part | Length / m |\n|---|---|\n| stomach | 0.25 |\n| small intestine | 6.5 |\n| large intestine | 1.5 |\n\nWhy is it an advantage for the small intestine to be so long?",
         correct="It gives a large surface area and more time for digestion to finish and for digested food to be absorbed.",
         wrongs={"It stores more undigested food.": "Storage is not its job; the rectum stores faeces.", "It kills more germs.": "Germ killing is mainly done by stomach acid.", "It makes food move faster.": "Length slows the passage, which helps absorption."},
         hints=["The small intestine is the main site of digestion AND absorption.", "Absorption happens across the intestine wall. What does length do to the area of wall?", "More wall + more time = more absorbed."]),
    dict(id="e14_diarrhoea", level=3, lo="14.2",
         stem="Fig. 1 shows the digestive system. A person with food poisoning has watery faeces (diarrhoea). Which part is not working properly, and why?",
         correct="S, the large intestine, because it is not absorbing enough water from the undigested food.",
         wrongs={"Q, the stomach, because it is not churning the food.": "Churning does not control how watery the faeces are.", "R, the small intestine, because it is not digesting starch.": "Undigested starch does not make faeces watery; unabsorbed WATER does.", "P, the gullet, because food is moving too quickly.": "The gullet only moves food to the stomach."},
         hints=["Which part normally removes water from the undigested food?", "If that water is not removed, what are the faeces like?", "Large intestine → water absorption."],
         fig=lambda rng: S.digestive_schematic()),
    dict(id="e14_enzyme_class_match", level=3, lo="14.4*",
         stem="The table shows an experiment.\n\n| Tube | Contents | Result after 10 min |\n|---|---|---|\n| 1 | egg white + enzyme X | egg white disappears |\n| 2 | starch + enzyme X | starch still present |\n| 3 | oil + enzyme X | oil still present |\n\nWhich class of enzyme is X?",
         correct="a protease, because it digested only the protein (egg white)",
         wrongs={"a carbohydrase, because it digested the starch": "The starch was still present, so X did not digest it.", "a lipase, because it digested the oil": "The oil was still present.", "all three classes, because it is an enzyme": "An enzyme class digests only one type of food."},
         hints=["Which food disappeared?", "Egg white is protein.", "Protein-digesting enzymes are called ____."]),

    # ------------------------------------------------------------ L4
    dict(id="e14_glucose_graph_explain", level=4, lo="14.5",
         stem="Fig. 1 shows blood glucose after a meal for a healthy person (A) and a person with diabetes (B). Which statement explains the difference?",
         correct="In B the body cannot control the blood glucose well, so the level rises higher and stays high for longer.",
         wrongs={"B ate a much larger meal.": "Both ate the SAME meal in this experiment.", "A's food was not digested.": "A's level rises, so the food WAS digested and absorbed.", "B's glucose was absorbed faster because of a shorter intestine.": "The difference is in CONTROL of glucose, not in absorption speed."},
         hints=["Both curves rise after the meal; look at how high and how long.", "Diabetes means blood glucose stays too high.", "Poor control → higher, longer peak."],
         fig=lambda rng: S.xy_graph([("A (healthy)", _glucose_curve(150)), ("B (diabetes)", _glucose_curve(200, back_to=130, slow=True))], "time after meal / min", "blood glucose / mg per 100 cm³", 180, 240, 30, 40)),
    dict(id="e14_fat_only_small_intestine", level=4, lo="14.4*",
         stem="The table shows where each class of enzyme is found.\n\n| Part | Enzymes present |\n|---|---|\n| mouth | carbohydrases |\n| stomach | proteases |\n| small intestine | carbohydrases, proteases, lipases |\n\nWhy is fat digested only in the small intestine?",
         correct="Lipases, the enzymes that digest fat, are released only into the small intestine.",
         wrongs={"Fat is too large to enter the mouth or stomach.": "Fat passes through both; it is simply not digested there.", "The stomach's acid destroys fat before it can be digested.": "Acid does not destroy fat.", "Fat is absorbed in the mouth.": "Nothing is absorbed in the mouth."},
         hints=["Each food type needs its own class of enzyme.", "Look for lipases in the table.", "They are found in only one row."]),
    dict(id="e14_food_poisoning_explain", level=4, lo="14.6",
         stem="The table describes how a meal was prepared.\n\n| Step | Detail |\n|---|---|\n| 1 | raw chicken cut on a board |\n| 2 | salad cut on the same board, unwashed |\n| 3 | chicken cooked thoroughly; salad served raw |\n\nSeveral people fell ill. Which explanation is best?",
         correct="Bacteria from the raw chicken were transferred to the salad on the board, and because the salad was not cooked they were not killed.",
         wrongs={"The chicken was undercooked.": "The table says the chicken was cooked thoroughly, which kills bacteria.", "The salad was poisonous.": "Salad is not poisonous; it was contaminated.", "Cooking the chicken produced harmful chemicals.": "Thorough cooking makes chicken safe."},
         hints=["Raw chicken often carries harmful bacteria.", "Which food touched the same board and was NOT cooked?", "No cooking → bacteria survive → illness."]),
    dict(id="e14_end_products_use", level=4, lo="14.4*",
         stem="Fig. 1 shows digested food being absorbed into the blood. What does the body use the end products of digestion for?",
         correct="Respiration to release energy, and growth and repair of tissues.",
         wrongs={"Only to make faeces.": "Faeces are the UNdigested remains; the end products are absorbed and used.", "To fill the stomach so we feel full.": "Feeling full is not the purpose of digestion's products.", "To cool the body.": "Food is used for energy, growth and repair, not cooling."},
         hints=["Why do we eat at all?", "Cells need glucose for energy and amino acids for building.", "Energy + growth + repair."],
         fig=lambda rng: S.flow_boxes(["glucose,\namino acids", "blood", "body cells:\nenergy, growth,\nrepair"])),
    dict(id="e14_absorption_needs_small", level=4, lo="14.1",
         stem="The table shows two molecules.\n\n| Molecule | Size | Soluble in water? |\n|---|---|---|\n| starch | very large | no |\n| glucose | small | yes |\n\nWhy can glucose pass into the blood but starch cannot?",
         correct="Glucose is small and soluble, so it can pass through the intestine wall; starch is too large and insoluble.",
         wrongs={"Glucose is sweet and the blood attracts it.": "Sweetness has nothing to do with absorption.", "Starch is poisonous to the blood.": "Starch is not poisonous; it is simply too large to be absorbed.", "The blood only carries liquids.": "The blood carries dissolved substances; glucose dissolves, starch does not."},
         hints=["Compare the two rows of the table.", "What must a molecule be like to cross the intestine wall?", "Small + soluble."]),

    # ------------------------------------------------------------ L5
    dict(id="e14_diet_evaluate", level=5, lo="14.5",
         stem="The table shows two students' daily habits.\n\n| | Student P | Student Q |\n|---|---|---|\n| sugary drinks per day | 3 cans | 0 |\n| fruit and vegetables | rarely | every meal |\n| exercise | none | 1 hour |\n\nWhich statement is the best evaluation of their risk of developing diabetes later?",
         correct="P has the higher risk: frequent sugary drinks, little fibre and no exercise all raise blood sugar and body fat over time.",
         wrongs={"Q has the higher risk because exercise uses up glucose too fast.": "Exercise LOWERS the risk by using glucose and keeping body fat down.", "Both have the same risk because diabetes is only inherited.": "Family history matters, but lifestyle strongly affects the risk.", "P has no risk because sugary drinks give energy.": "Regular excess sugar is a known risk factor."},
         hints=["Which habits raise the risk of diabetes?", "Sugary drinks, poor diet and no exercise.", "Count how many apply to each student."]),
    dict(id="e14_enzyme_experiment_control", level=5, lo="14.4*",
         stem="A student tests whether saliva digests starch.\n\n| Tube | Contents | Temperature |\n|---|---|---|\n| 1 | starch + saliva | 37 °C |\n| 2 | starch + water | 37 °C |\n\nWhy is tube 2 included?",
         correct="As a control: it shows that the starch does not disappear on its own, so any change in tube 1 is due to the saliva.",
         wrongs={"To make twice as much sugar.": "Tube 2 contains no enzyme and makes no sugar.", "To check that water digests starch.": "Water does not digest starch; the tube shows this.", "Because the student had extra starch.": "The tube is a deliberate part of the experimental design."},
         hints=["Only one thing differs between the tubes: saliva.", "If tube 2 changed too, what would that tell you?", "A control rules out other causes."]),
    dict(id="e14_stomach_removed_predict", level=5, lo="14.2",
         stem="Fig. 1 shows the digestive system. A patient has most of the stomach (Q) removed. Which prediction is most reasonable?",
         correct="Protein digestion starts later, in the small intestine, and the patient must eat smaller, more frequent meals.",
         wrongs={"The patient can no longer digest any food.": "The small intestine still digests all food types.", "Starch is no longer digested.": "Starch digestion happens in the mouth and small intestine, not the stomach.", "Water is no longer absorbed.": "Water absorption is the large intestine's job."},
         hints=["What does the stomach do? Store and churn food; begin protein digestion; kill germs.", "Which other part can still digest protein?", "Less storage → smaller meals."],
         fig=lambda rng: S.digestive_schematic()),
    dict(id="e14_bacteria_claim", level=5, lo="14.6",
         stem="The table shows examples of bacteria.\n\n| Example | Effect |\n|---|---|\n| gut bacteria | help keep the intestine healthy |\n| yoghurt bacteria | turn milk into yoghurt |\n| food-poisoning bacteria | cause vomiting and diarrhoea |\n\nA student says: 'All bacteria are harmful and should be killed.' Which response is best?",
         correct="Incorrect: many bacteria are helpful, such as those in our gut and those used to make food; only some cause disease.",
         wrongs={"Correct: bacteria always cause disease.": "Two of the three rows show helpful bacteria.", "Correct: the gut bacteria are harmful too.": "Gut bacteria help keep us healthy.", "Incorrect: no bacteria cause disease.": "Food-poisoning bacteria DO cause disease."},
         hints=["Read all three rows.", "How many are helpful?", "Some harmful, many helpful."]),
    dict(id="e14_iodine_predict", level=5, lo="14.3",
         stem="The table shows an experiment: starch solution mixed with saliva at 37 °C, tested with iodine every 5 minutes.\n\n| Time / min | Iodine colour |\n|---|---|\n| 0 | blue-black |\n| 5 | blue-black |\n| 10 | paler blue |\n| 15 | ? |\n\nWhat result is expected at 15 minutes, and why?",
         correct="Yellow-brown, because the carbohydrase in saliva has digested all the starch.",
         wrongs={"Blue-black, because starch cannot be digested at 37 °C.": "37 °C is body temperature, where the enzyme works best; the colour was already fading.", "Blue-black, because iodine stops working after 10 minutes.": "Iodine keeps working; the colour depends on how much starch is left.", "Yellow-brown, because the saliva has evaporated.": "Saliva does not evaporate from a test tube in 15 minutes."},
         hints=["Blue-black means starch present; paler means less starch.", "What is the trend in the table?", "Eventually no starch is left."]),
]

register_explain(EXPLAIN, chapter=14)
