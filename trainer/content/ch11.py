"""Ch 11 Chemical Changes: 25 calculation / data templates and 25 explanation items.
lo codes: 11.1 physical vs chemical, 11.2 word equations and conservation of mass, 11.3 types of change, 11.4 acids, alkalis, indicators,
11.5* acid + metal / carbonate (G3), 11.6* electroplating (G3), 11.7 daily life (rusting, pollution)."""
from .. import figs, sketches as S
from .base import fmt, md_table, nice, numeric_options, pick, register_explain, template, text_options

UI = {1: "red", 2: "red", 3: "orange", 4: "orange", 5: "yellow", 6: "yellow-green", 7: "green", 8: "blue-green", 9: "blue", 10: "blue", 11: "violet", 12: "violet", 13: "violet"}
HOUSEHOLD = [("lemon juice", 2), ("vinegar", 3), ("orange juice", 4), ("black coffee", 5), ("milk", 6), ("pure water", 7), ("sea water", 8),
             ("baking soda solution", 9), ("soap solution", 10), ("household ammonia", 11), ("oven cleaner", 13)]


def _gas_curve(V_max, k, tmax=10):
    import math
    return [(t, round(V_max * (1 - math.exp(-k * t)))) for t in range(0, tmax + 1)]


# ================================================================ CALCULATION / DATA
# ---------------------------------------------------------------- L1
@template("c11_mass_conservation_sum", chapter=11, level=1, lo="11.2")
def mass_conservation_sum(rng):
    a, b = pick(rng, [("iron", "sulfur", "iron sulfide"), ("magnesium", "oxygen", "magnesium oxide"), ("carbon", "oxygen", "carbon dioxide"), ("hydrogen", "oxygen", "water")])[:2]
    product = {"iron": "iron sulfide", "magnesium": "magnesium oxide", "carbon": "carbon dioxide", "hydrogen": "water"}[a]
    m1 = nice(rng, 4, 6, 8, 12, 14, 24, 28)
    m2 = nice(rng, 4, 8, 16, 32)
    total = m1 + m2
    opts, key, mis = numeric_options(rng, total, [
        (max(m1, m2), "That is the mass of one reactant only. All the atoms of BOTH reactants end up in the product."),
        (abs(m1 - m2) if m1 != m2 else total / 2, "You subtracted. No atoms are lost, so the masses ADD."),
        (m1 * m2, "You multiplied. Mass is conserved: add the reactant masses."),
    ], unit="g")
    return dict(
        stem=f"{a.capitalize()} reacts completely with {b} in a sealed container to form {product}.\n\n{md_table(['Substance', 'Mass / g'], [[a, str(m1)], [b, str(m2)], [product, '?']])}\n\nWhat mass of {product} is formed?",
        options=opts, key=key, misconceptions=mis,
        formula="total mass of reactants = total mass of products (atoms are rearranged, not created or destroyed)",
        working=[f"mass of product = {m1} + {m2}", f"= **{total} g**"],
        hints=["In a chemical change atoms are only rearranged. What happens to the total mass?", "Every atom of both reactants is now in the product.", f"{m1} + {m2}."],
    )


@template("c11_read_ph_table", chapter=11, level=1, lo="11.4")
def read_ph_table(rng):
    items = rng.sample(HOUSEHOLD, 4)
    ask = pick(rng, ["most acidic", "most alkaline"])
    target = min(items, key=lambda x: x[1]) if ask == "most acidic" else max(items, key=lambda x: x[1])
    wrongs = {n: f"{n} has pH {p}. {'Lower' if ask == 'most acidic' else 'Higher'} pH means {'more acidic' if ask == 'most acidic' else 'more alkaline'}." for n, p in items if n != target[0]}
    opts, key, mis = text_options(rng, target[0], wrongs)
    return dict(
        stem=f"The table shows the pH of some liquids.\n\n{md_table(['Liquid', 'pH'], [[n, str(p)] for n, p in items])}\n\nWhich liquid is the **{ask}**?",
        options=opts, key=key, misconceptions=mis,
        formula="pH below 7 = acidic (the lower, the more acidic); pH above 7 = alkaline (the higher, the more alkaline); pH 7 = neutral",
        working=[f"{ask}: pH {target[1]} → **{target[0]}**"],
        hints=["pH 7 is neutral. Below 7 is acidic, above 7 is alkaline.", f"The {ask} liquid has the {'lowest' if ask == 'most acidic' else 'highest'} pH number.", "Scan the pH column for that value."],
    )


@template("c11_mass_reactant_from_product", chapter=11, level=1, lo="11.2")
def mass_reactant_from_product(rng):
    metal = pick(rng, ["magnesium", "copper", "zinc", "iron"])
    m_metal = nice(rng, 6, 8, 12, 24, 30, 48)
    m_oxide = m_metal + nice(rng, 4, 8, 16, 20)
    ans = m_oxide - m_metal
    opts, key, mis = numeric_options(rng, ans, [
        (m_oxide, "That is the mass of the oxide. The oxygen is only the EXTRA mass gained."),
        (m_oxide + m_metal, "You added. The oxide's mass = metal + oxygen, so oxygen = oxide − metal."),
        (m_metal, "That is the mass of the metal. The oxygen is the difference between the two masses."),
    ], unit="g")
    return dict(
        stem=f"When **{m_metal} g** of {metal} is heated in air it combines with oxygen to form **{m_oxide} g** of {metal} oxide.\n\n{md_table(['Substance', 'Mass / g'], [[metal, str(m_metal)], ['oxygen', '?'], [f'{metal} oxide', str(m_oxide)]])}\n\nWhat mass of oxygen combined with the {metal}?",
        options=opts, key=key, misconceptions=mis,
        formula="mass of metal + mass of oxygen = mass of oxide, so oxygen = oxide − metal",
        working=[f"oxygen = {m_oxide} − {m_metal}", f"= **{ans} g**"],
        hints=["Mass is conserved: metal + oxygen = oxide.", "The increase in mass must be the oxygen that joined on.", f"{m_oxide} − {m_metal}."],
    )


@template("c11_bar_chart_gas_volume", chapter=11, level=1, lo="11.5*")
def bar_chart_gas_volume(rng):
    labels = ["P", "Q", "R", "S"]
    vols = rng.sample([10, 20, 30, 45, 60, 80], 4)
    ask = pick(rng, ["largest", "smallest"])
    i = vols.index(max(vols) if ask == "largest" else min(vols))
    opts, key, mis = text_options(rng, f"tube {labels[i]}", {f"tube {L}": f"Tube {L} produced {v} cm³ of gas, which is not the {ask} volume." for L, v in zip(labels, vols) if L != labels[i]})
    return dict(
        stem=f"Pieces of four different metals were added to the same volume of dilute acid. Fig. 1 shows the volume of hydrogen collected from each tube after one minute. Which tube produced the **{ask}** volume of gas?",
        figure=S.bar_chart([f"tube {L}" for L in labels], vols, "volume of hydrogen / cm³", ymax=100, ystep=20),
        options=opts, key=key, misconceptions=mis,
        formula="read and compare the bar heights",
        working=["volumes: " + ", ".join(f"{L} {v} cm³" for L, v in zip(labels, vols)), f"{ask} = **tube {labels[i]}**"],
        hints=["Compare the heights of the four bars.", f"The {ask} volume is the {'tallest' if ask == 'largest' else 'shortest'} bar.", "Read its label along the bottom."],
    )


@template("c11_temperature_change_neutralisation", chapter=11, level=1, lo="11.3")
def temperature_change_neutralisation(rng):
    T0 = nice(rng, 24, 25, 26, 27, 28)
    rise = nice(rng, 4, 5, 6, 7, 8, 9, 11)
    T1 = T0 + rise
    opts, key, mis = numeric_options(rng, rise, [
        (T1, "That is the final temperature. The CHANGE is final − initial."),
        (T1 + T0, "You added the temperatures. Subtract to find the change."),
        (rise + 1, "Check the subtraction."),
    ], unit="°C")
    return dict(
        stem=f"A student mixes dilute hydrochloric acid with sodium hydroxide solution and records the temperature.\n\n{md_table(['', 'Temperature / °C'], [['before mixing', str(T0)], ['after mixing', str(T1)]])}\n\nWhat is the temperature change during the neutralisation?",
        options=opts, key=key, misconceptions=mis,
        formula="temperature change = final temperature − initial temperature",
        working=[f"change = {T1} − {T0} = **{rise} °C** (a rise: heat is given out)"],
        hints=["The reaction gives out heat, so the temperature goes up.", "Subtract the starting temperature from the final one.", f"{T1} − {T0}."],
    )


# ---------------------------------------------------------------- L2
@template("c11_mass_lost_as_gas", chapter=11, level=2, lo="11.2")
def mass_lost_as_gas(rng):
    before = nice(rng, 120.0, 150.0, 180.0, 200.0, 250.0)
    gas = nice(rng, 1.2, 2.2, 3.5, 4.4, 6.6, 8.8)
    after = round(before - gas, 1)
    opts, key, mis = numeric_options(rng, gas, [
        (before, "That is the total mass at the start. The gas is only the mass that LEFT the flask."),
        (after, "That is the mass left in the flask. The gas is the difference between the readings."),
        (before + after, "You added the readings. The mass of gas escaped = before − after."),
    ], unit="g", dp=1)
    return dict(
        stem=f"Fig. 1 shows a flask of dilute acid and marble chips on a balance. The flask is open, so the carbon dioxide produced escapes.\n\n{md_table(['', 'Balance reading / g'], [['at the start', fmt(before, dp=1)], ['when the reaction stops', fmt(after, dp=1)]])}\n\nWhat mass of carbon dioxide escaped?",
        figure=S.balance("flask + acid + chips", "open flask", reading=f"{after:.1f} g"),
        options=opts, key=key, misconceptions=mis,
        formula="mass of gas escaped = mass before − mass after (mass is conserved; the 'missing' mass left as gas)",
        working=[f"mass escaped = {fmt(before, dp=1)} − {fmt(after, dp=1)}", f"= **{fmt(gas, dp=1)} g**"],
        hints=["Mass is conserved, so the reading only falls because something left the flask.", "What left the flask? The gas. Its mass is the drop in the reading.", f"{fmt(before, dp=1)} − {fmt(after, dp=1)}."],
    )


@template("c11_count_acidic_solutions", chapter=11, level=2, lo="11.4")
def count_acidic_solutions(rng):
    items = rng.sample(HOUSEHOLD, 5)
    kind = pick(rng, ["acidic", "alkaline"])
    n = sum(1 for _, p in items if (p < 7 if kind == "acidic" else p > 7))
    n = max(n, 1)
    other = sum(1 for _, p in items if (p > 7 if kind == "acidic" else p < 7))
    opts, key, mis = numeric_options(rng, n, [
        (other if other else n + 2, f"That is the number of {'alkaline' if kind == 'acidic' else 'acidic'} solutions. Read the question again."),
        (n + 1, f"Count only pH {'below' if kind == 'acidic' else 'above'} 7. pH 7 itself is neutral."),
        (5, "Not all of them: check each pH against 7."),
    ], unit="", sf=1)
    return dict(
        stem=f"The table shows the pH of five solutions.\n\n{md_table(['Solution', 'pH'], [[name, str(p)] for name, p in items])}\n\nHow many of the solutions are **{kind}**?",
        options=opts, key=key, misconceptions=mis,
        formula="acidic: pH < 7; neutral: pH = 7; alkaline: pH > 7",
        working=[f"{kind}: " + ", ".join(f"{name} (pH {p})" for name, p in items if (p < 7 if kind == 'acidic' else p > 7)), f"= **{n}**"],
        hints=["Decide the rule first: which pH values count as " + kind + "?", f"{kind.capitalize()} means pH {'less than' if kind == 'acidic' else 'greater than'} 7; pH 7 is neutral.", "Go down the table and count."],
    )


@template("c11_ph_scale_colour", chapter=11, level=2, lo="11.4")
def ph_scale_colour(rng):
    name, p = pick(rng, HOUSEHOLD)
    correct = UI[p]
    others = {c for c in set(UI.values()) if c != correct}
    wrongs = {}
    for c in rng.sample(sorted(others), 3):
        wrongs[c] = f"{c.capitalize()} is the Universal Indicator colour for a different pH, not pH {p}."
    opts, key, mis = text_options(rng, correct, wrongs)
    return dict(
        stem=f"Fig. 1 shows the Universal Indicator colour chart. A few drops of Universal Indicator are added to **{name}**, which has a pH of **{p}**. What colour is seen?",
        figure=S.ph_scale(p, name),
        options=opts, key=key, misconceptions=mis,
        formula="match the pH to the colour on the Universal Indicator chart",
        working=[f"pH {p} on the chart → **{correct}**"],
        hints=["Find the pH value on the chart in Fig. 1.", "Warm colours are acidic, the middle colour is neutral and cool colours are alkaline.", f"Read the colour of the pH {p} block."],
    )


@template("c11_graph_gas_volume_at_time", chapter=11, level=2, lo="11.5*")
def graph_gas_volume_at_time(rng):
    Vmax = nice(rng, 40, 50, 60, 80)
    pts = _gas_curve(Vmax, nice(rng, 0.4, 0.5, 0.6))
    t = nice(rng, 1, 2, 3, 4, 5)
    ans = dict(pts)[t]
    opts, key, mis = numeric_options(rng, ans, [
        (dict(pts)[t + 1], "You read the volume one minute too late."),
        (Vmax, "That is the final total volume, when the reaction has stopped. Read the curve at the time given."),
        (t, "That is the time. Go UP to the curve and ACROSS to the volume axis."),
    ], unit="cm³", sf=3)
    return dict(
        stem=f"Fig. 1 shows the total volume of carbon dioxide collected when marble chips react with dilute acid. What volume of gas has been collected after **{t} minute{'s' if t > 1 else ''}**?",
        figure=figs.graph(pts, 10, Vmax + 20 - (Vmax % 20 or 20) + 20, 2, 20, xlabel="time / min", ylabel="volume of gas / cm³"),
        options=opts, key=key, misconceptions=mis,
        formula="read the graph at the given time",
        working=[f"at {t} min, the curve is at **{ans} cm³**"],
        hints=["Find the time on the horizontal axis.", "Go straight up to the curve, then across to the volume axis.", "Each small square on the volume axis is 4 cm³."],
    )


@template("c11_mass_product_two_reactants_table", chapter=11, level=2, lo="11.2")
def mass_product_two_reactants_table(rng):
    acid = nice(rng, 50.0, 60.0, 80.0, 100.0)
    alkali = nice(rng, 40.0, 50.0, 60.0, 75.0)
    total = acid + alkali
    opts, key, mis = numeric_options(rng, total, [
        (acid, "That is only the acid. The alkali's mass is in the mixture too."),
        (abs(acid - alkali) if acid != alkali else total / 3, "You subtracted. Nothing escaped, so the masses add."),
        (total - 5, "In neutralisation no gas is given off, so no mass is lost. Add the two masses exactly."),
    ], unit="g", sf=4)
    return dict(
        stem=f"Dilute acid is added to an alkali in a beaker. Salt and water are formed and no gas is given off.\n\n{md_table(['Solution', 'Mass / g'], [['dilute acid', fmt(acid, dp=1)], ['alkali solution', fmt(alkali, dp=1)]])}\n\nWhat is the mass of the mixture after the reaction?",
        options=opts, key=key, misconceptions=mis,
        formula="mass of products = total mass of reactants when nothing escapes",
        working=[f"mass after = {fmt(acid, dp=1)} + {fmt(alkali, dp=1)}", f"= **{fmt(total, sf=4)} g**"],
        hints=["Is anything leaving the beaker? The question says no gas is given off.", "So the total mass is unchanged.", f"{fmt(acid, dp=1)} + {fmt(alkali, dp=1)}."],
    )


# ---------------------------------------------------------------- L3
@template("c11_thermal_decomposition_solid_left", chapter=11, level=3, lo="11.3")
def thermal_decomposition_solid_left(rng):
    carb, oxide = pick(rng, [("copper(II) carbonate", "copper(II) oxide"), ("calcium carbonate", "calcium oxide"), ("zinc carbonate", "zinc oxide")])
    m0 = nice(rng, 10.0, 12.4, 20.0, 25.0, 31.0)
    gas = round(m0 * nice(rng, 0.3, 0.35, 0.44), 1)
    left = round(m0 - gas, 1)
    opts, key, mis = numeric_options(rng, left, [
        (m0, "The mass does not stay the same: carbon dioxide gas escapes, so the solid left is lighter."),
        (gas, "That is the mass of carbon dioxide given off, not the solid that remains."),
        (m0 + gas, "You added. The gas LEAVES, so subtract it."),
    ], unit="g", dp=1)
    return dict(
        stem=f"**{fmt(m0, dp=1)} g** of {carb} is heated strongly until it has all decomposed into {oxide} and carbon dioxide (Fig. 1). **{fmt(gas, dp=1)} g** of carbon dioxide escapes. What mass of {oxide} is left?",
        figure=S.flow_boxes([carb, f"{oxide}\n+ carbon dioxide ↑"], arrow_labels=["heat"]),
        options=opts, key=key, misconceptions=mis,
        formula="mass of carbonate = mass of oxide + mass of carbon dioxide (conservation of mass)",
        working=[f"oxide left = {fmt(m0, dp=1)} − {fmt(gas, dp=1)}", f"= **{fmt(left, dp=1)} g**"],
        hints=["Thermal decomposition: one substance breaks into two. The total mass of the two products equals the starting mass.", "One product is a gas that escapes. The other is the solid left.", f"{fmt(m0, dp=1)} − {fmt(gas, dp=1)}."],
    )


@template("c11_percent_mass_loss", chapter=11, level=3, lo="11.3")
def percent_mass_loss(rng):
    m0 = nice(rng, 20, 25, 40, 50, 80)
    pct = nice(rng, 10, 20, 25, 30, 44)
    m1 = m0 * (100 - pct) / 100
    opts, key, mis = numeric_options(rng, pct, [
        (100 - pct, "That is the percentage REMAINING. The question asks for the percentage lost."),
        (m0 - m1, "That is the mass lost in grams. Turn it into a percentage of the starting mass."),
        ((m0 - m1) / m1 * 100, "Divide the mass lost by the STARTING mass, not the final mass."),
    ], unit="%", sf=3)
    return dict(
        stem=f"A sample of a carbonate is heated until no more gas is given off.\n\n{md_table(['', 'Mass / g'], [['before heating', str(m0)], ['after heating', fmt(m1)]])}\n\nWhat percentage of the original mass was lost as gas?",
        options=opts, key=key, misconceptions=mis,
        formula="percentage lost = (mass before − mass after) ÷ mass before × 100",
        working=[f"mass lost = {m0} − {fmt(m1)} = {fmt(m0 - m1)} g", f"percentage = {fmt(m0 - m1)} ÷ {m0} × 100 = **{pct}%**"],
        hints=["First find the mass lost in grams.", "A percentage compares that loss with the ORIGINAL mass.", f"({m0} − {fmt(m1)}) ÷ {m0} × 100."],
    )


@template("c11_ph_graph_neutral_volume", chapter=11, level=3, lo="11.4")
def ph_graph_neutral_volume(rng):
    V7 = nice(rng, 10, 12, 15, 20, 25)
    pts = [(0, 13), (V7 - 4, 12), (V7 - 1, 10), (V7, 7), (V7 + 1, 4), (V7 + 4, 2), (40, 1)]
    opts, key, mis = numeric_options(rng, V7, [
        (V7 + 4, "At that volume the pH is already well below 7: the acid is in excess."),
        (V7 - 4, "At that volume the pH is still above 7: not all the alkali has been neutralised."),
        (7, "pH 7 is the pH value, not the volume of acid. Read down to the horizontal axis."),
    ], unit="cm³", sf=3)
    return dict(
        stem="Fig. 1 shows how the pH changes as dilute acid is added to 25 cm³ of an alkali. What volume of acid is needed to exactly **neutralise** the alkali?",
        figure=figs.graph(pts, 40, 14, 5, 2, xlabel="volume of acid added / cm³", ylabel="pH"),
        options=opts, key=key, misconceptions=mis,
        formula="neutral point: pH = 7; read the volume where the curve crosses pH 7",
        working=["neutralisation is complete when pH = 7", f"the curve crosses pH 7 at **{V7} cm³**"],
        hints=["What pH is a neutral solution?", "Find that pH on the vertical axis and move across to the steep part of the curve.", "Read straight down to the volume axis."],
    )


@template("c11_rate_from_gas_table", chapter=11, level=3, lo="11.5*")
def rate_from_gas_table(rng):
    rate = nice(rng, 5, 6, 8, 10, 12)
    t = nice(rng, 2, 3, 4, 5)
    V = rate * t
    rows = [["0", "0"], [str(t), str(V)]]
    opts, key, mis = numeric_options(rng, rate, [
        (V, "That is the total volume. Rate = volume ÷ time."),
        (V * t, "You multiplied. Divide the volume by the time."),
        (t / V * 60 if t / V * 60 != rate else rate + 1, "You divided time by volume. Rate = volume collected ÷ time taken."),
    ], unit="cm³ per minute", sf=3)
    return dict(
        stem=f"Zinc reacts with dilute acid and the hydrogen is collected.\n\n{md_table(['Time / min', 'Total volume of hydrogen / cm³'], rows)}\n\nWhat is the average rate at which hydrogen is produced?",
        options=opts, key=key, misconceptions=mis,
        formula="rate = volume of gas produced ÷ time taken",
        working=[f"rate = {V} ÷ {t}", f"= **{rate} cm³ per minute**"],
        hints=["Rate means how much per minute.", "Divide the total volume by the number of minutes.", f"{V} ÷ {t}."],
    )


@template("c11_rust_mass_gain", chapter=11, level=3, lo="11.7")
def rust_mass_gain(rng):
    m0 = nice(rng, 20.0, 25.0, 40.0, 50.0)
    gain = nice(rng, 0.6, 0.9, 1.2, 1.5, 2.4)
    m1 = round(m0 + gain, 1)
    opts, key, mis = numeric_options(rng, gain, [
        (m1, "That is the final mass of the nails. The oxygen (and water) that combined is only the GAIN."),
        (m0, "That is the starting mass."),
        (m1 + m0, "You added the readings. The gain is after − before."),
    ], unit="g", dp=1)
    return dict(
        stem=f"Iron nails were left in damp air for a month and rusted. Fig. 1 shows them on a balance afterwards.\n\n{md_table(['', 'Mass / g'], [['clean nails', fmt(m0, dp=1)], ['rusted nails', fmt(m1, dp=1)]])}\n\nWhat mass of oxygen and water combined with the iron?",
        figure=S.balance("rusted nails", None, reading=f"{m1:.1f} g"),
        options=opts, key=key, misconceptions=mis,
        formula="mass of rusted nails = mass of iron + mass of oxygen and water combined",
        working=[f"gain = {fmt(m1, dp=1)} − {fmt(m0, dp=1)}", f"= **{fmt(gain, dp=1)} g**"],
        hints=["Rusting is iron + oxygen + water → rust. The nails get HEAVIER.", "The extra mass is the oxygen and water that joined on.", f"{fmt(m1, dp=1)} − {fmt(m0, dp=1)}."],
    )


# ---------------------------------------------------------------- L4
@template("c11_ph_graph_read_ph", chapter=11, level=4, lo="11.4")
def ph_graph_read_ph(rng):
    V7 = nice(rng, 15, 20, 25)
    pts = [(0, 13), (V7 - 4, 12), (V7 - 1, 10), (V7, 7), (V7 + 1, 4), (V7 + 4, 2), (40, 1)]
    V = pick(rng, [V7 - 4, V7 + 4, 40, 0])
    ans = dict(pts)[V]
    opts, key, mis = numeric_options(rng, ans, [
        (7, "pH 7 is only at the exact neutral point. Read the curve at the volume given."),
        (14 - ans if 14 - ans != ans else ans + 3, "You are on the wrong side of the curve: check whether the acid is in excess or not yet enough."),
        (V, "That is the volume, not the pH. Go UP to the curve and ACROSS to the pH axis."),
    ], unit="", sf=2)
    return dict(
        stem=f"Fig. 1 shows the pH as dilute acid is added to 25 cm³ of alkali. What is the pH of the mixture after **{V} cm³** of acid has been added?",
        figure=figs.graph(pts, 40, 14, 5, 2, xlabel="volume of acid added / cm³", ylabel="pH"),
        options=opts, key=key, misconceptions=mis,
        formula="read the graph at the given volume",
        working=[f"at {V} cm³ the curve is at pH **{ans}**", "above 7 → alkali still in excess; below 7 → acid in excess"],
        hints=["Find the volume on the horizontal axis.", "Go up to the curve and across to the pH axis.", "Before the steep drop the mixture is still alkaline; after it, acidic."],
    )


@template("c11_graph_two_reactions_stop", chapter=11, level=4, lo="11.5*")
def graph_two_reactions_stop(rng):
    Vmax = nice(rng, 50, 60, 80)
    P = _gas_curve(Vmax, 0.9)
    Q = _gas_curve(Vmax, 0.35)
    tP = next(t for t, v in P if v >= Vmax - 1)
    tQ = next(t for t, v in Q if v >= Vmax - 1) if any(v >= Vmax - 1 for t, v in Q) else 10
    which = pick(rng, ["P", "Q"])
    ans = tP if which == "P" else tQ
    other = tQ if which == "P" else tP
    opts, key, mis = numeric_options(rng, ans, [
        (other, f"That is when the OTHER reaction levels off. Follow the curve for {which}."),
        (Vmax, "That is the final volume of gas, not a time."),
        (ans + 2 if ans + 2 <= 10 else ans - 2, "The reaction stops when the curve becomes flat. Check where the line first levels off."),
    ], unit="min", sf=2)
    return dict(
        stem=f"Fig. 1 shows the gas collected from two reactions. P uses powdered chips and Q uses large lumps of the same mass. After how many minutes does reaction **{which}** stop?",
        figure=S.xy_graph([("P (powder)", P), ("Q (lumps)", Q)], "time / min", "volume of gas / cm³", 10, Vmax + 20, 2, 20),
        options=opts, key=key, misconceptions=mis,
        formula="a reaction has stopped when no more gas is produced: the curve becomes flat",
        working=[f"curve {which} becomes horizontal at about **{ans} min**", "both curves reach the same final volume because the same mass reacts"],
        hints=["When a reaction stops, the total volume of gas stops increasing.", f"Look for where curve {which} (see the legend) flattens out.", "Read the time directly below that point."],
    )


@template("c11_bar_chart_rust_conditions", chapter=11, level=4, lo="11.7")
def bar_chart_rust_conditions(rng):
    conds = ["dry air", "water + air", "salt water + air", "boiled water, no air"]
    masses = [0.1, nice(rng, 1.2, 1.5, 1.8), nice(rng, 2.4, 2.8, 3.2), 0.0]
    i, j = 2, 1
    diff = round(masses[i] - masses[j], 1)
    opts, key, mis = numeric_options(rng, diff, [
        (masses[i], "That is the rust formed in salt water. The question asks how much MORE than in plain water."),
        (masses[i] + masses[j], "You added. 'How much more' means subtract."),
        (masses[j], "That is the rust in plain water, not the difference."),
    ], unit="g", dp=1)
    return dict(
        stem="Identical iron nails were kept for two weeks under different conditions. Fig. 1 shows the mass of rust formed on each. How much **more** rust formed in salt water than in plain water (both with air)?",
        figure=S.bar_chart(conds, masses, "mass of rust / g", ymax=4, ystep=1, size=(5.4, 3.0)),
        options=opts, key=key, misconceptions=mis,
        formula="difference = mass of rust (salt water) − mass of rust (water)",
        working=[f"salt water + air: {fmt(masses[i])} g; water + air: {fmt(masses[j])} g", f"difference = **{fmt(diff)} g**"],
        hints=["Read the two bars named in the question.", "Subtract the smaller from the larger.", "Salt speeds up rusting, so that bar is taller."],
    )


@template("c11_table_identify_largest_rise", chapter=11, level=4, lo="11.3")
def table_identify_largest_rise(rng):
    acids = ["P", "Q", "R", "S"]
    starts = [nice(rng, 24, 25, 26) for _ in acids]
    rises = rng.sample([2, 4, 6, 8, 10, 12], 4)
    rows = [[a, str(s), str(s + r)] for a, s, r in zip(acids, starts, rises)]
    best = acids[rises.index(max(rises))]
    opts, key, mis = text_options(rng, f"acid {best}", {f"acid {a}": f"Acid {a} gave a temperature rise of {r} °C: not the largest." for a, r in zip(acids, rises) if a != best})
    return dict(
        stem=f"Equal volumes of four acids were each added to the same alkali. The table shows the temperatures.\n\n{md_table(['Acid', 'Start temperature / °C', 'Final temperature / °C'], rows)}\n\nWhich acid gave out the **most heat** when it was neutralised?",
        options=opts, key=key, misconceptions=mis,
        formula="heat given out shows as a temperature RISE: compare final − start for each row",
        working=["rises: " + ", ".join(f"{a} {r} °C" for a, r in zip(acids, rises)), f"largest = **acid {best}**"],
        hints=["Do not compare the final temperatures alone: the starting temperatures differ.", "Work out the rise (final − start) for each acid.", "The biggest rise means the most heat given out."],
    )


@template("c11_pie_chart_pollution", chapter=11, level=4, lo="11.7")
def pie_chart_pollution(rng):
    srcs = ["power stations", "vehicles", "factories", "homes"]
    pcts = [nice(rng, 35, 40), nice(rng, 25, 30), 20, None]
    pcts[3] = 100 - sum(p for p in pcts if p)
    total = nice(rng, 200, 400, 500, 1000)   # thousand tonnes
    i = rng.randint(0, 3)
    ans = total * pcts[i] / 100
    opts, key, mis = numeric_options(rng, ans, [
        (pcts[i], "That is the percentage, not the mass."),
        (total * (100 - pcts[i]) / 100, f"That is everything EXCEPT {srcs[i]}."),
        (total / 4, "The four sources are not equal shares."),
    ], unit="thousand tonnes", sf=3)
    return dict(
        stem=f"Fig. 1 shows the sources of sulfur dioxide, a gas from burning fossil fuels that causes acid rain. A country releases **{total} thousand tonnes** a year in total. How much comes from **{srcs[i]}**?",
        figure=S.pie_chart([f"{s} ({p}%)" for s, p in zip(srcs, pcts)], pcts),
        options=opts, key=key, misconceptions=mis,
        formula="amount = percentage ÷ 100 × total",
        working=[f"{srcs[i]}: {pcts[i]}% of {total}", f"= **{fmt(ans)} thousand tonnes**"],
        hints=[f"Read the percentage for {srcs[i]} from the chart.", "Find that percentage of the total.", f"{pcts[i]}/100 × {total}."],
    )


# ---------------------------------------------------------------- L5
@template("c11_conservation_unknown_with_gas", chapter=11, level=5, lo="11.2")
def conservation_unknown_with_gas(rng):
    carb = nice(rng, 10, 20, 25, 50)
    acid = nice(rng, 100, 150, 200)
    gas = nice(rng, 4.4, 8.8, 11)
    salt_water = carb + acid - gas
    opts, key, mis = numeric_options(rng, salt_water, [
        (carb + acid, "That would be right in a SEALED container. Here the gas escapes, so its mass is no longer in the beaker."),
        (carb + acid + gas, "You added the gas. It escapes, so subtract it."),
        (acid - gas, "You left out the carbonate. Add both reactants, then subtract the gas."),
    ], unit="g", sf=4)
    return dict(
        stem=f"Calcium carbonate reacts with dilute hydrochloric acid in an open beaker: calcium carbonate + hydrochloric acid → calcium chloride + water + carbon dioxide.\n\n{md_table(['Substance', 'Mass / g'], [['calcium carbonate', str(carb)], ['dilute hydrochloric acid', str(acid)], ['carbon dioxide (escapes)', fmt(gas)]])}\n\nWhat is the mass of the contents of the beaker when the reaction is complete?",
        options=opts, key=key, misconceptions=mis,
        formula="mass left = total mass of reactants − mass of gas that escaped",
        working=[f"reactants: {carb} + {acid} = {carb + acid} g", f"gas escapes: {carb + acid} − {fmt(gas)} = **{fmt(salt_water, sf=4)} g**"],
        hints=["Mass is conserved overall, but one product leaves the beaker.", "Add the two reactants, then take away what escaped.", f"{carb} + {acid} − {fmt(gas)}."],
    )


@template("c11_percent_co2_in_carbonate", chapter=11, level=5, lo="11.3")
def percent_co2_in_carbonate(rng):
    m0 = nice(rng, 20, 25, 50)
    left = round(m0 * nice(rng, 0.56, 0.60, 0.65, 0.70), 1)
    pct = round((m0 - left) / m0 * 100, 1)
    opts, key, mis = numeric_options(rng, pct, [
        (round(left / m0 * 100, 1), "That is the percentage of SOLID left, not the percentage of gas lost."),
        (round(m0 - left, 1), "That is the mass of gas in grams. Convert to a percentage of the original."),
        (round((m0 - left) / left * 100, 1), "Divide by the original mass, not the mass left."),
    ], unit="%", sf=3)
    return dict(
        stem=f"**{m0} g** of a carbonate is heated in a crucible until its mass stops changing (Fig. 1). The solid left has a mass of **{fmt(left)} g**. What percentage of the carbonate's mass was carbon dioxide?",
        figure=S.balance("crucible + solid", "after heating", reading=f"{left:.1f} g"),
        options=opts, key=key, misconceptions=mis,
        formula="mass of CO₂ = before − after; percentage = mass of CO₂ ÷ original mass × 100",
        working=[f"CO₂ lost = {m0} − {fmt(left)} = {fmt(m0 - left)} g", f"percentage = {fmt(m0 - left)} ÷ {m0} × 100 = **{fmt(pct)}%**"],
        hints=["Heating until the mass stops changing means all the carbon dioxide has gone.", "The mass lost IS the carbon dioxide.", f"({m0} − {fmt(left)}) ÷ {m0} × 100."],
    )


@template("c11_total_gas_two_reactions", chapter=11, level=5, lo="11.5*")
def total_gas_two_reactions(rng):
    r1, t1 = nice(rng, 6, 8, 10), nice(rng, 2, 3, 4)
    r2, t2 = nice(rng, 3, 4, 5), nice(rng, 4, 5, 6)
    total = r1 * t1 + r2 * t2
    opts, key, mis = numeric_options(rng, total, [
        (r1 * t1, "That is the gas from the first tube only."),
        ((r1 + r2) * (t1 + t2), "You multiplied the total rate by the total time. Each tube ran for its OWN time."),
        (r1 * t2 + r2 * t1, "You matched the rates with the wrong times."),
    ], unit="cm³", sf=3)
    return dict(
        stem=f"Two tubes of acid have different metals added and the hydrogen from both is collected together.\n\n{md_table(['Tube', 'Rate of gas / cm³ per min', 'Time reacting / min'], [['1', str(r1), str(t1)], ['2', str(r2), str(t2)]])}\n\nWhat total volume of hydrogen is collected?",
        options=opts, key=key, misconceptions=mis,
        formula="volume = rate × time for each tube; add the two volumes",
        working=[f"tube 1: {r1} × {t1} = {r1 * t1} cm³", f"tube 2: {r2} × {t2} = {r2 * t2} cm³", f"total = **{total} cm³**"],
        hints=["Volume = rate × time. Do each tube separately.", "Then add the two volumes.", f"{r1} × {t1} + {r2} × {t2}."],
    )


@template("c11_rust_fair_test_table", chapter=11, level=5, lo="11.7")
def rust_fair_test_table(rng):
    rows = [["P", "tap water", "open", "yes"], ["Q", "boiled water + oil layer", "sealed", "no"], ["R", "drying agent, no water", "sealed", "no"], ["S", "salt water", "open", "yes, heavily"]]
    rng.shuffle(rows)
    opts, key, mis = text_options(rng, "Both water and air (oxygen) are needed for rusting.", {
        "Only water is needed for rusting.": "Tube Q has water but no air and does not rust, so water alone is not enough.",
        "Only air is needed for rusting.": "Tube R has air but no water and does not rust, so air alone is not enough.",
        "Rusting needs salt.": "P rusts in plain tap water, so salt is not needed; it only speeds rusting up.",
    })
    return dict(
        stem=f"Iron nails were set up in four tubes for one week.\n\n{md_table(['Tube', 'Contents', 'Tube', 'Rusted?'], rows)}\n\nWhich conclusion do the results support?",
        options=opts, key=key, misconceptions=mis,
        formula="compare tubes that differ in one condition: Q (water, no air) and R (air, no water) both fail to rust",
        working=["P: water + air → rusts", "Q: water, no air → no rust; R: air, no water → no rust", "so **both water and air are needed**; S shows salt speeds it up"],
        hints=["Find the tube with water but no air, and the tube with air but no water.", "Neither of those rusts. What does that tell you about each condition on its own?", "Rusting happens only when BOTH are present."],
    )


@template("c11_expected_vs_measured_mass", chapter=11, level=5, lo="11.2")
def expected_vs_measured_mass(rng):
    m_metal = nice(rng, 2.4, 4.8, 6.0, 12.0)
    gain_full = round(m_metal * nice(rng, 0.5, 0.6, 0.67), 1)
    actual_gain = round(gain_full * nice(rng, 0.5, 0.6, 0.75), 1)
    pct = round(actual_gain / gain_full * 100)
    opts, key, mis = numeric_options(rng, pct, [
        (100 - pct, "That is the percentage NOT yet reacted."),
        (actual_gain, "That is the mass gained in grams, not the percentage of the metal reacted."),
        (round(actual_gain / m_metal * 100), "Compare the gain with the gain expected for COMPLETE reaction, not with the mass of metal."),
    ], unit="%", sf=2)
    return dict(
        stem=f"When **{fmt(m_metal)} g** of magnesium burns completely in oxygen, its mass should increase by **{fmt(gain_full)} g**. A student's sample gained only **{fmt(actual_gain)} g**.\n\n{md_table(['Quantity', 'Mass / g'], [['magnesium used', fmt(m_metal)], ['expected gain for complete reaction', fmt(gain_full)], ['gain measured', fmt(actual_gain)]])}\n\nWhat percentage of the magnesium reacted?",
        options=opts, key=key, misconceptions=mis,
        formula="percentage reacted = measured gain ÷ expected gain × 100",
        working=[f"{fmt(actual_gain)} ÷ {fmt(gain_full)} × 100", f"= **{pct}%**"],
        hints=["The gain in mass is the oxygen that joined on. A smaller gain means less magnesium reacted.", "Compare the measured gain with the gain for a COMPLETE reaction.", f"{fmt(actual_gain)} ÷ {fmt(gain_full)} × 100."],
    )


# ================================================================ EXPLANATION
EXPLAIN = [
    # ------------------------------------------------------------ L1
    dict(id="e11_chemical_change_definition", level=1, lo="11.1",
         stem="The table compares two kinds of change.\n\n| | New substance formed? | Easily reversed? |\n|---|---|---|\n| X | no | usually yes |\n| Y | yes | usually no |\n\nWhich statement is correct?",
         correct="Y is a chemical change, because one or more new substances are formed.",
         wrongs={"X is a chemical change, because it is easily reversed.": "Being easily reversed is a sign of a PHYSICAL change.",
                 "Y is a physical change, because it cannot be reversed.": "Forming a new substance makes Y a chemical change.",
                 "X and Y are both chemical changes.": "X forms no new substance, so it is a physical change."},
         hints=["The key test for a chemical change is whether a new substance is made.", "Read the 'new substance' column.", "New substance → chemical change."]),
    dict(id="e11_word_equation_parts", level=1, lo="11.2",
         stem="Fig. 1 shows a word equation as boxes. In the equation **iron + sulfur → iron sulfide**, iron and sulfur are the",
         correct="reactants",
         wrongs={"products": "The product is what is FORMED: iron sulfide, on the right of the arrow.",
                 "catalysts": "A catalyst is not used up; iron and sulfur are used up.",
                 "indicators": "Indicators show pH; they have nothing to do with this equation."},
         hints=["Which side of the arrow are they on?", "Substances on the left react together; the substance on the right is made.", "Left of the arrow = ____."],
         fig=lambda rng: S.flow_boxes(["iron + sulfur", "iron sulfide"])),
    dict(id="e11_neutralisation_products", level=1, lo="11.3",
         stem="Fig. 1 shows the pH scale. When an acid reacts with an alkali in neutralisation, the products are",
         correct="a salt and water",
         wrongs={"a salt and hydrogen": "Hydrogen is produced when an acid reacts with a METAL.",
                 "a salt, water and carbon dioxide": "Carbon dioxide is produced when an acid reacts with a CARBONATE.",
                 "an acid and an alkali": "Those are the reactants, not the products."},
         hints=["Neutralisation: acid + alkali → ? + ?", "No gas is given off in neutralisation.", "acid + alkali → salt + ____."],
         fig=lambda rng: S.ph_scale(7, "neutral")),
    dict(id="e11_litmus_in_acid", level=1, lo="11.4",
         stem="Fig. 1 shows the pH of lemon juice. What happens when blue litmus paper is dipped into lemon juice?",
         correct="It turns red.",
         wrongs={"It turns blue.": "Blue litmus stays blue in alkalis and neutral solutions. Lemon juice is acidic.",
                 "It turns green.": "Green is a Universal Indicator colour for neutral, not a litmus colour.",
                 "It stays unchanged.": "Acids change blue litmus. Only neutral or alkaline liquids leave it blue."},
         hints=["Lemon juice has pH 2. Is that acidic or alkaline?", "Acids turn BLUE litmus ____; alkalis turn RED litmus blue.", "Blue → red in acid."],
         fig=lambda rng: S.ph_scale(2, "lemon juice")),
    dict(id="e11_combustion_definition", level=1, lo="11.3",
         stem="Fig. 1 shows the energy change when a fuel burns. Combustion is a chemical change in which a substance",
         correct="reacts with oxygen, giving out heat and light",
         wrongs={"breaks down into simpler substances when heated": "That is thermal decomposition.",
                 "reacts with an acid to form a salt": "That is neutralisation (or an acid–metal reaction).",
                 "melts and then boils": "Melting and boiling are physical changes."},
         hints=["What does a fire need from the air?", "Burning needs oxygen and gives out heat and light.", "Combustion = burning in ____."],
         fig=lambda rng: S.flow_boxes(["fuel + oxygen", "carbon dioxide + water\n+ heat + light"])),

    # ------------------------------------------------------------ L2
    dict(id="e11_classify_change", level=2, lo="11.1",
         hints=["Ask: is a NEW substance formed?", "Melting, boiling, dissolving and cutting change only the form, not the substance.", "Burning, rusting and cooking make new substances."],
         variants=[
             dict(stem="The table lists four changes.\n\n| Change | What happens |\n|---|---|\n| melting ice | solid → liquid water |\n| burning wood | wood → ash, smoke and gases |\n| dissolving sugar | sugar spreads through water |\n| tearing paper | paper in smaller pieces |\n\nWhich is a **chemical** change?",
                  correct="burning wood", wrongs={"melting ice": "Ice and water are the same substance in different states: a physical change.", "dissolving sugar": "The sugar is still sugar; it can be recovered by evaporating the water.", "tearing paper": "The paper is still paper, just smaller."}),
             dict(stem="The table lists four changes.\n\n| Change | What happens |\n|---|---|\n| rusting a nail | iron → brown rust |\n| boiling water | liquid → steam |\n| frying an egg | runny egg → firm white solid |\n| souring milk | milk → lumpy, sour liquid |\n\nWhich is a **physical** change?",
                  correct="boiling water", wrongs={"rusting a nail": "Rust is a new substance formed from iron, oxygen and water.", "frying an egg": "The egg protein changes permanently into a new substance.", "souring milk": "New sour substances are formed; it cannot be reversed."}),
         ]),
    dict(id="e11_identify_type_of_change", level=2, lo="11.3",
         hints=["Combustion = burning in oxygen. Thermal decomposition = heat breaks one substance into two or more. Oxidation = reacts with oxygen. Neutralisation = acid + alkali.", "Count the reactants and products and look for oxygen or heat.", "Match the pattern to the name."],
         fig=lambda rng: S.flow_boxes(["reactant(s)", "product(s)"]),
         variants=[
             dict(stem="Fig. 1 shows a general change. **Copper(II) carbonate → copper(II) oxide + carbon dioxide** (on heating) is an example of",
                  correct="thermal decomposition", wrongs={"combustion": "Nothing is burning in oxygen; one substance is being broken down by heat.", "neutralisation": "No acid or alkali is involved.", "oxidation": "No oxygen is added; the substance splits up."}),
             dict(stem="Fig. 1 shows a general change. **Iron + oxygen + water → rust** is an example of",
                  correct="oxidation", wrongs={"thermal decomposition": "Nothing is broken down by heat; substances COMBINE.", "neutralisation": "No acid or alkali is involved.", "combustion": "Rusting is slow and gives out no light; it is not burning."}),
             dict(stem="Fig. 1 shows a general change. **Hydrochloric acid + sodium hydroxide → sodium chloride + water** is an example of",
                  correct="neutralisation", wrongs={"combustion": "Nothing burns.", "thermal decomposition": "Two substances react; nothing is broken down by heat.", "oxidation": "Oxygen is not added to anything."}),
             dict(stem="Fig. 1 shows a general change. **Methane + oxygen → carbon dioxide + water**, giving out heat and light, is an example of",
                  correct="combustion", wrongs={"thermal decomposition": "Two reactants combine; nothing is split by heat.", "neutralisation": "No acid or alkali.", "electroplating": "No electric current is involved."}),
         ]),
    dict(id="e11_ui_colour_identify", level=2, lo="11.4",
         stem="Fig. 1 shows the Universal Indicator chart. A solution turns Universal Indicator **green**. The solution is",
         correct="neutral, pH 7",
         wrongs={"strongly acidic, pH 1": "Strong acids turn Universal Indicator red.", "weakly alkaline, pH 9": "pH 9 gives blue.", "strongly alkaline, pH 14": "pH 14 gives violet."},
         hints=["Find green on the chart.", "What pH is it above?", "Green = neutral."],
         fig=lambda rng: S.ph_scale()),
    dict(id="e11_acid_or_alkali_from_table", level=2, lo="11.4",
         stem="The table shows properties of a liquid.\n\n| Property | Result |\n|---|---|\n| taste | sour |\n| pH | 3 |\n| effect on blue litmus | turns red |\n\nThe liquid is",
         correct="an acid",
         wrongs={"an alkali": "Alkalis have pH above 7, feel soapy and turn red litmus blue.", "neutral": "A neutral liquid has pH 7 and does not change litmus.", "a salt solution": "Salt solutions are usually neutral (pH 7)."},
         hints=["pH below 7 means what?", "Sour taste and blue litmus → red are also signs.", "All three rows point to the same answer."]),
    dict(id="e11_gas_tests", level=2, lo="11.5*",
         hints=["Hydrogen: a lighted splint gives a 'pop'. Carbon dioxide: limewater turns chalky (milky).", "Which reaction gives which gas? Acid + metal → hydrogen. Acid + carbonate → carbon dioxide.", "Match the test to the gas."],
         fig=lambda rng: S.test_tubes(["P", "Q"], contents=["acid + magnesium", "acid + chalk"], bubbles=[True, True]),
         variants=[
             dict(stem="Fig. 1 shows two reactions giving off gas. The gas from tube P (acid + magnesium) is collected. Which test confirms it?",
                  correct="A lighted splint gives a squeaky pop.", wrongs={"Limewater turns chalky.": "That is the test for carbon dioxide, from acid + carbonate.", "A glowing splint relights.": "That is the test for oxygen.", "Damp blue litmus turns red.": "That tests for an acidic gas, not hydrogen."}),
             dict(stem="Fig. 1 shows two reactions giving off gas. The gas from tube Q (acid + chalk, a carbonate) is bubbled through limewater. What is seen?",
                  correct="The limewater turns chalky white.", wrongs={"The limewater turns blue.": "Limewater does not turn blue with carbon dioxide.", "Bubbles of hydrogen pop.": "Acid + carbonate gives carbon dioxide, not hydrogen.", "Nothing happens.": "Carbon dioxide reacts with limewater to form a white precipitate."}),
         ]),

    # ------------------------------------------------------------ L3
    dict(id="e11_rust_prevention_why", level=3, lo="11.7",
         hints=["Rusting needs iron, oxygen (air) AND water.", "A good method keeps at least one of these away from the iron.", "Explain how the method forms a barrier."],
         fig=lambda rng: S.flow_boxes(["iron + oxygen + water", "rust"]),
         variants=[
             dict(stem="Fig. 1 shows what rusting needs. Why does painting an iron gate stop it rusting?",
                  correct="The paint forms a barrier that keeps oxygen and water away from the iron.", wrongs={"The paint makes the iron harder.": "Hardness has nothing to do with rusting.", "The paint reacts with the rust and removes it.": "Paint does not react with rust; it prevents rust forming.", "The paint absorbs the water.": "Paint repels water rather than absorbing it."}),
             dict(stem="Fig. 1 shows what rusting needs. Why does a bicycle chain that is kept oiled not rust?",
                  correct="The oil keeps water and oxygen away from the iron.", wrongs={"The oil cools the chain.": "Temperature is not the issue.", "The oil dissolves the rust.": "Oil does not dissolve rust.", "The oil makes the chain heavier.": "Mass does not affect rusting."}),
             dict(stem="Fig. 1 shows what rusting needs. Tools stored in a sealed box with a packet of drying agent do not rust because",
                  correct="the drying agent removes water, and water is needed for rusting", wrongs={"the drying agent removes oxygen": "A drying agent absorbs WATER, not oxygen.", "the box keeps the tools warm": "Warmth is not what stops rusting here.", "the drying agent coats the tools": "It stays in its packet; it works by absorbing moisture from the air."}),
         ]),
    dict(id="e11_complete_word_equation", level=3, lo="11.2",
         hints=["Reactants on the left, products on the right.", "Name the new substance from the elements that combined, or the pieces a compound split into.", "Check: metal + oxygen → metal oxide; carbonate → oxide + carbon dioxide; acid + alkali → salt + water."],
         variants=[
             dict(stem="The table shows a reaction.\n\n| Reactants | Product |\n|---|---|\n| magnesium + oxygen | ? |\n\nWhich word equation is correct?",
                  correct="magnesium + oxygen → magnesium oxide", wrongs={"magnesium + oxygen → magnesium hydroxide": "Hydroxides contain hydrogen; no hydrogen is present here.", "magnesium oxide → magnesium + oxygen": "That is the reverse: the question says magnesium and oxygen REACT.", "magnesium + oxygen → carbon dioxide": "There is no carbon in the reactants."}),
             dict(stem="The table shows a reaction.\n\n| Reactant | Products |\n|---|---|\n| calcium carbonate (heated) | ? |\n\nWhich word equation is correct?",
                  correct="calcium carbonate → calcium oxide + carbon dioxide", wrongs={"calcium carbonate → calcium + carbon + oxygen": "Thermal decomposition does not split a carbonate into its elements.", "calcium carbonate + oxygen → calcium oxide": "No oxygen is added; the compound breaks down on heating.", "calcium carbonate → calcium hydroxide + water": "There is no hydrogen in calcium carbonate."}),
             dict(stem="The table shows a reaction.\n\n| Reactants | Products |\n|---|---|\n| sulfuric acid + sodium hydroxide | ? |\n\nWhich word equation is correct?",
                  correct="sulfuric acid + sodium hydroxide → sodium sulfate + water", wrongs={"sulfuric acid + sodium hydroxide → sodium chloride + water": "The salt from SULFURIC acid is a sulfate, not a chloride.", "sulfuric acid + sodium hydroxide → sodium sulfate + hydrogen": "Neutralisation gives water, not hydrogen.", "sulfuric acid + sodium hydroxide → sodium sulfate + carbon dioxide": "No carbonate is present, so no carbon dioxide."}),
         ]),
    dict(id="e11_mass_seems_to_drop", level=3, lo="11.2",
         stem="Fig. 1 shows a flask of acid and marble chips on a balance. During the reaction the reading falls. A student says mass has been destroyed. Which response is correct?",
         correct="No. Carbon dioxide gas escapes from the flask; if the gas were collected, the total mass would be unchanged.",
         wrongs={"Yes. Chemical changes always destroy some mass.": "Mass is conserved in every chemical change.",
                 "No. The balance is faulty.": "The balance is fine; it simply no longer weighs the gas that left.",
                 "Yes. The acid evaporates.": "The acid does not evaporate noticeably; the escaping gas is carbon dioxide."},
         hints=["What is produced in this reaction, and where does it go?", "Atoms are never destroyed. Something must have LEFT the flask.", "Gas escapes → reading falls → mass still conserved overall."],
         fig=lambda rng: S.balance("acid + marble chips", "open flask", reading=f"{rng.choice([148.2, 151.6, 199.1]):.1f} g")),
    dict(id="e11_neutralisation_application", level=3, lo="11.3",
         hints=["Neutralisation: an acid and an alkali cancel each other out.", "Decide which is the acid and which is the alkali in the situation.", "The product is nearer pH 7."],
         fig=lambda rng: S.ph_scale(7, "target"),
         variants=[
             dict(stem="Fig. 1 shows the pH scale. Indigestion is caused by too much acid in the stomach. Indigestion tablets contain a mild alkali because",
                  correct="the alkali neutralises the excess acid", wrongs={"the alkali kills bacteria in the stomach": "The tablets are for excess acid, not bacteria.", "the alkali makes the stomach more acidic": "An alkali does the opposite.", "the alkali dissolves the food": "Digestion, not dissolving, is the job of the stomach juices."}),
             dict(stem="Fig. 1 shows the pH scale. A farmer adds lime (an alkali) to a field whose soil has pH 5. The purpose is to",
                  correct="neutralise the acidic soil so that crops grow better", wrongs={"make the soil more acidic": "Lime is an alkali; it raises the pH.", "add water to the soil": "Lime is a solid alkali, not a source of water.", "kill the crops' roots": "The aim is to help the crops, not harm them."}),
             dict(stem="Fig. 1 shows the pH scale. Toothpaste is slightly alkaline. This helps protect teeth because",
                  correct="it neutralises the acids produced by bacteria in the mouth", wrongs={"it makes the mouth more acidic": "Alkaline toothpaste does the opposite.", "it dissolves tooth enamel": "Acids dissolve enamel; the toothpaste helps prevent that.", "it stops saliva forming": "Saliva is helpful and is not stopped by toothpaste."}),
         ]),
    dict(id="e11_acid_metal_gas", level=3, lo="11.5*",
         stem="Fig. 1 shows magnesium ribbon fizzing in dilute hydrochloric acid. What are the products?",
         correct="magnesium chloride and hydrogen",
         wrongs={"magnesium chloride and carbon dioxide": "Carbon dioxide comes from acid + CARBONATE, not acid + metal.",
                 "magnesium oxide and water": "No oxygen is involved; the acid provides the chloride.",
                 "magnesium hydroxide and hydrogen": "The salt from hydrochloric acid is a chloride."},
         hints=["acid + metal → salt + ?", "The gas from acid + metal gives a squeaky pop with a lighted splint.", "Hydrochloric acid makes chlorides."],
         fig=lambda rng: S.test_tubes(["magnesium + acid"], bubbles=[True])),

    # ------------------------------------------------------------ L4
    dict(id="e11_ui_colour_sequence", level=4, lo="11.4",
         stem="Fig. 1 shows the Universal Indicator chart. Dilute acid is added slowly to an alkali containing Universal Indicator until the acid is in excess. Which colour sequence is seen?",
         correct="violet → blue → green → yellow → red",
         wrongs={"red → yellow → green → blue → violet": "That is the sequence when ALKALI is added to ACID.",
                 "violet → green → violet": "Once the acid is in excess the mixture stays acidic; it does not go back to violet.",
                 "green → blue → violet": "The mixture starts alkaline (violet), not neutral."},
         hints=["Start: the mixture is an alkali. What colour is that?", "Adding acid lowers the pH step by step through 7.", "Finish: acid in excess, pH low."],
         fig=lambda rng: S.ph_scale()),
    dict(id="e11_copper_carbonate_observations", level=4, lo="11.3",
         stem="Fig. 1 shows green copper(II) carbonate being heated; the gas is passed into limewater. Which observations are correct?",
         correct="The green solid turns black and the limewater turns chalky.",
         wrongs={"The green solid turns white and the limewater stays clear.": "Copper(II) oxide is BLACK, and the carbon dioxide released turns limewater chalky.",
                 "The green solid melts and no gas is given off.": "The solid decomposes rather than melting, and carbon dioxide IS given off.",
                 "The green solid catches fire.": "There is no fuel to burn; this is decomposition, not combustion."},
         hints=["Thermal decomposition: copper(II) carbonate → copper(II) oxide + carbon dioxide.", "What colour is copper(II) oxide? What does carbon dioxide do to limewater?", "Black solid; chalky limewater."],
         fig=lambda rng: S.flow_boxes(["copper(II) carbonate\n(green)", "copper(II) oxide\n+ carbon dioxide"], arrow_labels=["heat"])),
    dict(id="e11_fossil_fuels_pollution", level=4, lo="11.7",
         stem="The table shows gases released when a fossil fuel burns.\n\n| Gas | Effect |\n|---|---|\n| carbon dioxide | greenhouse gas |\n| sulfur dioxide | acid rain |\n| carbon monoxide | poisonous |\n\nWhich statement about burning fossil fuels is correct?",
         correct="It is a useful combustion reaction, but the gases released harm the environment and health.",
         wrongs={"It is a physical change, so no new substances are formed.": "Burning forms new substances (the gases in the table): a chemical change.",
                 "It only produces carbon dioxide, which is harmless.": "Carbon dioxide is a greenhouse gas, and other harmful gases form too.",
                 "The pollution can be prevented by burning the fuel faster.": "Faster burning releases the gases faster; it does not remove them."},
         hints=["Is burning fuel useful? Does the table show problems?", "A chemical change can be both useful and harmful.", "Energy is useful; the gases are the harm."]),
    dict(id="e11_respiration_oxidation", level=4, lo="11.3",
         stem="Fig. 1 shows the word equation for respiration in cells. Why is respiration described as an oxidation reaction?",
         correct="Glucose reacts with oxygen, releasing energy.",
         wrongs={"Glucose breaks down when heated.": "Respiration happens at body temperature; it is not thermal decomposition.",
                 "Oxygen is produced from glucose.": "Oxygen is USED, not produced.",
                 "An acid reacts with an alkali.": "No acid or alkali is involved."},
         hints=["Oxidation means a substance reacts with oxygen.", "Look at the left side of the equation in Fig. 1.", "Glucose + oxygen → … with energy released."],
         fig=lambda rng: S.flow_boxes(["glucose + oxygen", "carbon dioxide + water\n+ energy"])),
    dict(id="e11_electroplating_purpose", level=4, lo="11.6*",
         stem="Fig. 1 shows an iron spoon being electroplated with a thin layer of silver using an electric current. Why is this done?",
         correct="The silver layer stops the iron rusting and makes the spoon look attractive.",
         wrongs={"The current melts the silver onto the spoon.": "The silver is deposited by a chemical change caused by the current, not by melting.",
                 "The iron turns into silver.": "Elements cannot be changed into each other by a chemical change; the iron is only coated.",
                 "It makes the spoon lighter.": "Adding a layer makes the spoon very slightly heavier."},
         hints=["Electroplating is a chemical change caused by an electric current.", "Why coat iron with another metal? Think about rust and appearance.", "Protection + decoration."],
         fig=lambda rng: S.flow_boxes(["iron spoon", "spoon coated\nwith silver"], arrow_labels=["electric current"])),

    # ------------------------------------------------------------ L5
    dict(id="e11_rust_experiment_evaluate", level=5, lo="11.7",
         stem="A student tests whether salt speeds up rusting.\n\n| Tube | Nail | Liquid | Time |\n|---|---|---|---|\n| X | large iron nail | tap water | 7 days |\n| Y | small iron nail | salt water | 3 days |\n\nMore rust formed in X. What is the best comment on this experiment?",
         correct="The comparison is unfair: the nail size and the time also differ, so the effect of salt cannot be judged.",
         wrongs={"It proves salt slows rusting.": "X had longer and a bigger nail; those alone could explain the extra rust.",
                 "It proves salt speeds rusting.": "More rust formed in X, the tube WITHOUT salt, and the test is unfair anyway.",
                 "It is fair because both nails are iron.": "Fairness needs only ONE difference between the tubes."},
         hints=["In a fair test only the variable under investigation changes.", "List the differences between X and Y.", "More than one difference → no conclusion."]),
    dict(id="e11_predict_ph_excess_acid", level=5, lo="11.4",
         stem="Fig. 1 shows the pH scale. 20 cm³ of acid exactly neutralises 25 cm³ of an alkali. If 30 cm³ of the same acid is added instead, the final pH will be",
         correct="below 7, because the extra acid is left over",
         wrongs={"exactly 7, because neutralisation always gives pH 7": "Only an exact match gives pH 7; here there is 10 cm³ of acid too much.",
                 "above 7, because more acid makes the solution more alkaline": "Adding acid LOWERS the pH.",
                 "14, because the acid is in excess": "Excess dilute acid gives a low pH, not 14 (which is strongly alkaline)."},
         hints=["How much acid is needed for neutralisation? How much was added?", "The extra acid has nothing left to react with.", "Leftover acid → acidic mixture."],
         fig=lambda rng: S.ph_scale()),
    dict(id="e11_candle_mass_claim", level=5, lo="11.2",
         stem="Fig. 1 shows a candle on a balance. As it burns the reading falls. A student claims this breaks the law of conservation of mass. Which reply is correct?",
         correct="The wax reacts with oxygen to form carbon dioxide and water vapour, which escape into the air; the total mass including those gases is unchanged.",
         wrongs={"The claim is correct; burning destroys matter.": "Matter is not destroyed; the products are gases that leave.",
                 "The reading falls because the flame is hot, not because of a reaction.": "The heat is a result of the reaction. The mass falls because gases escape.",
                 "The wax turns into light energy.": "Light is energy, not matter. The wax atoms end up in the gases produced."},
         hints=["What products does burning wax make? What state are they in?", "If the products were trapped, would the mass change?", "Gases escape; atoms are all still somewhere."],
         fig=lambda rng: S.balance("burning candle", None, reading=f"{rng.choice([54.3, 61.8, 72.0]):.1f} g")),
    dict(id="e11_choose_rust_method", level=5, lo="11.7",
         stem="The table compares ways of protecting iron.\n\n| Method | Keeps out water and air? | Lasts if scratched? | Suitable for moving parts? |\n|---|---|---|---|\n| paint | yes | no | no |\n| oil/grease | yes | yes (re-oil) | yes |\n| plastic coating | yes | no | no |\n| storing dry | partly | – | no |\n\nWhich is the best way to protect a bicycle chain, and why?",
         correct="Oil or grease, because it keeps out water and air while letting the chain move freely.",
         wrongs={"Paint, because it forms a hard barrier.": "Paint would crack and flake as the chain bends and rubs.",
                 "Plastic coating, because it is waterproof.": "A plastic coat would be worn off the moving links quickly.",
                 "Storing it dry, because rust needs water.": "The chain is used outdoors; it cannot stay dry in use."},
         hints=["A chain bends and rubs constantly. Which column covers that?", "Pick the row that is 'yes' for moving parts AND keeps out water and air.", "Oil can be reapplied easily."]),
    dict(id="e11_identify_unknown_from_tests", level=5, lo="11.5*",
         stem="The table shows tests on an unknown white solid.\n\n| Test | Result |\n|---|---|\n| add dilute acid | fizzes |\n| pass the gas into limewater | turns chalky |\n| heat strongly | gas given off, solid remains |\n\nWhat is the solid most likely to be?",
         correct="a carbonate",
         wrongs={"a metal": "Metals fizz with acid but give hydrogen, which does not turn limewater chalky.",
                 "a salt such as sodium chloride": "Common salt does not fizz with acid or give off gas on heating.",
                 "an alkali": "Alkalis neutralise acid without fizzing."},
         hints=["Which gas turns limewater chalky?", "Which type of substance gives that gas with acid and also decomposes on heating?", "acid + ____ → salt + water + carbon dioxide."]),
]

register_explain(EXPLAIN, chapter=11)
