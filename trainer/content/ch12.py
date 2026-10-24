"""Ch 12 Interactions within Ecosystems: 25 calculation / data templates and 25 explanation items.
lo codes: 12.1 conservation, 12.2 physical factors and adaptations, 12.3 ecosystem terms, 12.4 relationships, 12.5 food chains, webs and energy,
12.6* decomposers / data loggers / sustainable living (G3)."""
from .. import figs, sketches as S
from .base import fmt, md_table, nice, numeric_options, pick, register_explain, template, text_options

# food webs: nodes on a 0-10 grid, edges point from food to feeder
WEBS = {
    "pond": dict(nodes={"pondweed": (2, 0), "algae": (7, 0), "tadpole": (1, 3), "water snail": (5, 3), "water flea": (8.5, 3), "small fish": (3, 6), "heron": (7, 6)},
                 edges=[("pondweed", "tadpole"), ("pondweed", "water snail"), ("algae", "water snail"), ("algae", "water flea"), ("tadpole", "small fish"), ("water snail", "small fish"), ("water flea", "small fish"), ("small fish", "heron"), ("tadpole", "heron")]),
    "garden": dict(nodes={"grass": (2, 0), "lettuce": (7, 0), "grasshopper": (1, 3), "snail": (5, 3), "caterpillar": (8.5, 3), "frog": (2, 6), "bird": (6.5, 6), "hawk": (4.5, 9)},
                   edges=[("grass", "grasshopper"), ("grass", "snail"), ("lettuce", "snail"), ("lettuce", "caterpillar"), ("grasshopper", "frog"), ("snail", "frog"), ("snail", "bird"), ("caterpillar", "bird"), ("frog", "hawk"), ("bird", "hawk")]),
    "savanna": dict(nodes={"grass": (2, 0), "acacia tree": (7, 0), "zebra": (1, 3), "gazelle": (5, 3), "giraffe": (8.5, 3), "lion": (2.5, 6), "hyena": (7, 6)},
                    edges=[("grass", "zebra"), ("grass", "gazelle"), ("acacia tree", "giraffe"), ("acacia tree", "gazelle"), ("zebra", "lion"), ("gazelle", "lion"), ("gazelle", "hyena"), ("giraffe", "lion"), ("zebra", "hyena")]),
}


def _chains(web, through=None):
    """All food chains from a producer to a top consumer; optionally only those passing through one organism."""
    edges = web["edges"]
    feeders = {}
    for a, b in edges:
        feeders.setdefault(a, []).append(b)
    producers = [n for n in web["nodes"] if n not in {b for _, b in edges}]
    out = []

    def walk(path):
        nxt = feeders.get(path[-1], [])
        if not nxt:
            out.append(path)
        for n in nxt:
            walk(path + [n])

    for p in producers:
        walk([p])
    return [c for c in out if through is None or through in c]


def _fig(web):
    return S.food_web(web["nodes"], web["edges"], size=(5.6, 3.6 if max(y for _, y in web["nodes"].values()) < 9 else 4.6))


def _pop_curve(prey_peak_t, period=10, tmax=20):
    import math
    prey = [(t, round(60 + 40 * math.sin(2 * math.pi * (t - prey_peak_t) / period + math.pi / 2))) for t in range(0, tmax + 1)]
    pred = [(t, round(20 + 12 * math.sin(2 * math.pi * (t - prey_peak_t - period / 4) / period + math.pi / 2))) for t in range(0, tmax + 1)]
    return prey, pred


# ================================================================ CALCULATION / DATA
# ---------------------------------------------------------------- L1
@template("c12_food_chain_position", chapter=12, level=1, lo="12.5")
def food_chain_position(rng):
    chain = pick(rng, [["grass", "grasshopper", "frog", "snake", "eagle"], ["algae", "water flea", "small fish", "heron"], ["leaves", "caterpillar", "bird", "cat"], ["grass", "rabbit", "fox"]])
    k = rng.randint(1, len(chain) - 1)
    correct = chain[k]
    pos = ["second", "third", "fourth", "fifth"][k - 1]
    wrongs = {c: f"{c} is in position {chain.index(c) + 1}, counting from the producer." for c in chain if c != correct}
    for filler in ("mushroom", "owl"):
        if len(wrongs) < 3 and filler not in chain:
            wrongs[filler] = f"The {filler} is not in this food chain at all."
    wrongs = dict(list(wrongs.items())[:3])
    opts, key, mis = text_options(rng, correct, wrongs)
    return dict(
        stem=f"Fig. 1 shows a food chain. Which organism is the **{pos}** organism in the chain, counting from the producer?",
        figure=S.flow_boxes(chain),
        options=opts, key=key, misconceptions=mis,
        formula="count along the arrows from the producer (the first box)",
        working=[" → ".join(chain), f"position {k + 1} = **{correct}**"],
        hints=["The producer (a plant or alga) comes first.", "Follow the arrows: each arrow points to the next organism.", f"Count to box number {k + 1}."],
    )


@template("c12_bar_chart_population_read", chapter=12, level=1, lo="12.5")
def bar_chart_population_read(rng):
    years = ["2019", "2020", "2021", "2022"]
    vals = [nice(rng, 120, 150, 180), nice(rng, 200, 240, 260), nice(rng, 300, 320, 360), nice(rng, 280, 400, 420)]
    i = rng.randint(0, 3)
    ans = vals[i]
    opts, key, mis = numeric_options(rng, ans, [
        (vals[(i + 1) % 4], f"That is the bar for {years[(i + 1) % 4]}. Find the bar labelled {years[i]}."),
        (vals[(i + 2) % 4], f"That is the bar for {years[(i + 2) % 4]}."),
        (ans + 20, "Read the top of the bar against the scale carefully; each small square is 20."),
    ], unit="", sf=3)
    return dict(
        stem=f"Fig. 1 shows the number of deer counted in a nature reserve each year. How many deer were counted in **{years[i]}**?",
        figure=S.bar_chart(years, vals, "number of deer", ymax=500, ystep=100, xlabel="year"),
        options=opts, key=key, misconceptions=mis,
        formula="read the height of the bar for the year asked",
        working=[f"bar for {years[i]} reaches **{ans}**"],
        hints=[f"Find the bar labelled {years[i]} along the bottom.", "Read across from the top of that bar to the vertical scale.", "Each labelled line is 100; each small square is 20."],
    )


@template("c12_ph_tolerance_table", chapter=12, level=1, lo="12.2")
def ph_tolerance_table(rng):
    lo_, hi_ = pick(rng, [(6.0, 8.0), (6.5, 8.5), (5.5, 7.5)])
    ponds = [("P", lo_ - 1.0), ("Q", lo_ + 0.5), ("R", hi_ + 0.5), ("S", hi_ + 1.5)]
    rng.shuffle(ponds)
    good = [p for p, v in ponds if lo_ <= v <= hi_][0]
    wrongs = {f"pond {p}": f"Pond {p} has pH {fmt(v)}, which is outside the range {fmt(lo_)}–{fmt(hi_)} that the fish can survive." for p, v in ponds if p != good}
    opts, key, mis = text_options(rng, f"pond {good}", wrongs)
    return dict(
        stem=f"A species of fish survives only in water with a pH between **{fmt(lo_)} and {fmt(hi_)}**. The table shows the pH of four ponds.\n\n{md_table(['Pond', 'pH'], [[p, fmt(v)] for p, v in ponds])}\n\nIn which pond could the fish survive?",
        options=opts, key=key, misconceptions=mis,
        formula="the pond's pH must lie inside the range the organism can tolerate",
        working=[f"range {fmt(lo_)}–{fmt(hi_)}: only pond {good} is inside it → **pond {good}**"],
        hints=["pH (acidity) is a physical factor that affects survival.", f"Check each pond's pH against the range {fmt(lo_)} to {fmt(hi_)}.", "Only one pond falls inside the range."],
    )


@template("c12_pyramid_numbers_read", chapter=12, level=1, lo="12.5")
def pyramid_numbers_read(rng):
    chain = pick(rng, [["grass plants", "grasshoppers", "frogs", "snakes"], ["algae", "water fleas", "small fish", "herons"], ["clover", "rabbits", "foxes"]])
    counts = [nice(rng, 2000, 5000, 8000), nice(rng, 300, 500, 800), nice(rng, 20, 40, 60), nice(rng, 2, 3, 5)][:len(chain)]
    i = rng.randint(0, len(chain) - 1)
    opts, key, mis = numeric_options(rng, counts[i], [(c, f"That is the number of {chain[j]}.") for j, c in enumerate(counts) if j != i], unit="", sf=3)
    return dict(
        stem=f"Fig. 1 shows a pyramid of numbers for a food chain. How many **{chain[i]}** are there?",
        figure=S.pyramid(chain, counts),
        options=opts, key=key, misconceptions=mis,
        formula="each bar's number is written beside it; the producer is at the bottom",
        working=[f"{chain[i]}: **{counts[i]}**"],
        hints=["The producer is at the bottom of the pyramid and the top consumer at the top.", f"Find the bar labelled {chain[i]}.", "Read the number to its right."],
    )


@template("c12_temperature_range_table", chapter=12, level=1, lo="12.2")
def temperature_range_table(rng):
    lo_ = nice(rng, -5, 0, 4, 8)
    hi_ = nice(rng, 28, 32, 35, 40)
    rng_ = hi_ - lo_
    opts, key, mis = numeric_options(rng, rng_, [
        (hi_, "That is the highest temperature only. The range is highest − lowest."),
        (hi_ + lo_ if hi_ + lo_ != rng_ else rng_ + 5, "You added the temperatures. Subtract the lowest from the highest."),
        (rng_ - 10 if lo_ < 0 else rng_ + 5, "Take care with negative temperatures: subtracting a negative number increases the range."),
    ], unit="°C", sf=3)
    return dict(
        stem=f"A data logger recorded the air temperature in a habitat over one year.\n\n{md_table(['', 'Temperature / °C'], [['lowest recorded', str(lo_)], ['highest recorded', str(hi_)]])}\n\nWhat is the range of temperature that organisms in this habitat must survive?",
        options=opts, key=key, misconceptions=mis,
        formula="range = highest value − lowest value",
        working=[f"range = {hi_} − ({lo_})", f"= **{rng_} °C**"],
        hints=["The range is the gap between the extremes.", "Subtract the lowest from the highest.", f"{hi_} − ({lo_})."],
    )


# ---------------------------------------------------------------- L2
@template("c12_count_chains_small", chapter=12, level=2, lo="12.5")
def count_chains_small(rng):
    name = pick(rng, ["pond", "savanna"])
    web = WEBS[name]
    n = len(_chains(web))
    opts, key, mis = numeric_options(rng, n, [
        (len(web["edges"]), "That is the number of arrows. A food chain runs all the way from a producer to a top consumer."),
        (n - 1, "You missed a chain. Trace every route from each producer to each top consumer."),
        (n + 1, "You counted one route twice, or a route that does not start at a producer."),
    ], unit="", sf=2)
    chains = _chains(web)
    return dict(
        stem="Fig. 1 shows a food web. How many **food chains** does it contain?",
        figure=_fig(web),
        options=opts, key=key, misconceptions=mis,
        formula="a food chain = one complete route from a producer to an organism that nothing else eats",
        working=[" / ".join(" → ".join(c) for c in chains), f"total = **{n}**"],
        hints=["Start at each producer (the boxes with no arrows pointing INTO them).", "Follow the arrows until you reach an organism with no arrow leaving it. That is one chain.", "Repeat for every possible route and count them."],
    )


@template("c12_population_percent_change", chapter=12, level=2, lo="12.5")
def population_percent_change(rng):
    before = nice(rng, 200, 400, 500, 800, 1000)
    pct = nice(rng, 10, 20, 25, 40, 50)
    direction = pick(rng, ["fell", "rose"])
    after = before * (100 - pct) / 100 if direction == "fell" else before * (100 + pct) / 100
    opts, key, mis = numeric_options(rng, pct, [
        (abs(before - after), "That is the change in NUMBER. The question asks for the percentage change."),
        (round(abs(before - after) / after * 100), "Divide by the ORIGINAL number, not the new one."),
        (100 - pct, "That is the percentage remaining (or the complement). Find the change itself."),
    ], unit="%", sf=3)
    return dict(
        stem=f"A survey counted a bird population in two years.\n\n{md_table(['Year', 'Number of birds'], [['2015', str(before)], ['2025', fmt(after)]])}\n\nBy what percentage did the population {'fall' if direction == 'fell' else 'rise'}?",
        options=opts, key=key, misconceptions=mis,
        formula="percentage change = change ÷ original number × 100",
        working=[f"change = {fmt(abs(before - after))}", f"percentage = {fmt(abs(before - after))} ÷ {before} × 100 = **{pct}%**"],
        hints=["First find the change in numbers.", "A percentage change compares that with the ORIGINAL number.", f"{fmt(abs(before - after))} ÷ {before} × 100."],
    )


@template("c12_energy_ten_percent", chapter=12, level=2, lo="12.5")
def energy_ten_percent(rng):
    E = nice(rng, 2000, 5000, 8000, 10000, 20000)
    nxt = E / 10
    opts, key, mis = numeric_options(rng, nxt, [
        (E * 0.9, "That is the 90% LOST as heat and in waste. Only 10% is passed on."),
        (E, "Not all the energy is passed on; most is lost to the surroundings."),
        (E / 100, "You found 1%. About 10% is passed to the next organism."),
    ], unit="J", sf=3)
    return dict(
        stem=f"Fig. 1 shows energy passing along a food chain. The grass contains **{E} J** of energy. Only about **10%** of the energy at each stage is passed on to the next. How much energy is passed on to the grasshoppers?",
        figure=S.energy_arrows(["grass", "grasshopper", "frog"], [E, nxt, nxt / 10]),
        options=opts, key=key, misconceptions=mis,
        formula="energy passed on = 10% of the energy at the stage before (≈ 90% is lost as heat and in waste)",
        working=[f"10% of {E} J = {E} ÷ 10", f"= **{fmt(nxt)} J**"],
        hints=["Most energy is lost at each stage, mainly as heat from respiration.", "10% means one tenth.", f"{E} ÷ 10."],
    )


@template("c12_bar_chart_difference_years", chapter=12, level=2, lo="12.1")
def bar_chart_difference_years(rng):
    years = ["2000", "2010", "2020"]
    vals = [nice(rng, 80, 90, 100), nice(rng, 60, 65, 70), nice(rng, 30, 40, 45)]
    i, j = pick(rng, [(0, 2), (0, 1), (1, 2)])
    diff = vals[i] - vals[j]
    opts, key, mis = numeric_options(rng, diff, [
        (vals[i], f"That is the forest area in {years[i]}. The question asks how much was LOST."),
        (vals[j], f"That is the area left in {years[j]}."),
        (vals[i] + vals[j], "You added. Loss = earlier area − later area."),
    ], unit="km²", sf=3)
    return dict(
        stem=f"Fig. 1 shows the area of forest in a district. How much forest was lost between **{years[i]} and {years[j]}**?",
        figure=S.bar_chart(years, vals, "forest area / km²", ymax=120, ystep=20, xlabel="year"),
        options=opts, key=key, misconceptions=mis,
        formula="area lost = area in the earlier year − area in the later year",
        working=[f"{years[i]}: {vals[i]} km²; {years[j]}: {vals[j]} km²", f"lost = **{diff} km²**"],
        hints=["Read both bars named in the question.", "Loss means the earlier value minus the later value.", f"{vals[i]} − {vals[j]}."],
    )


@template("c12_graph_population_read", chapter=12, level=2, lo="12.5")
def graph_population_read(rng):
    prey, pred = _pop_curve(nice(rng, 2, 4, 6))
    t = nice(rng, 2, 4, 6, 8, 10, 12, 14, 16)
    which = pick(rng, ["rabbits", "foxes"])
    pts = prey if which == "rabbits" else pred
    ans = dict(pts)[t]
    other = dict(pred if which == "rabbits" else prey)[t]
    opts, key, mis = numeric_options(rng, ans, [
        (other, f"That is the number of {'foxes' if which == 'rabbits' else 'rabbits'}. Use the legend to pick the right curve."),
        (dict(pts)[t + 2] if t + 2 <= 20 else dict(pts)[t - 2], "You read the curve two years away from the time asked."),
        (t, "That is the time, not the population."),
    ], unit="", sf=3)
    return dict(
        stem=f"Fig. 1 shows the populations of rabbits and foxes in a wood. How many **{which}** were there at **{t} years**?",
        figure=S.xy_graph([("rabbits", prey), ("foxes", pred)], "time / years", "number of animals", 20, 120, 4, 20),
        options=opts, key=key, misconceptions=mis,
        formula="read the correct curve at the time asked",
        working=[f"{which} curve at {t} years → **{ans}**"],
        hints=["Check the legend to see which line is which.", f"Find {t} years on the horizontal axis and go up to the {which} line.", "Read across to the vertical axis."],
    )


# ---------------------------------------------------------------- L3
@template("c12_count_chains_large", chapter=12, level=3, lo="12.5")
def count_chains_large(rng):
    web = WEBS["garden"]
    producer = pick(rng, ["grass", "lettuce", None])
    chains = [c for c in _chains(web) if producer is None or c[0] == producer]
    n = len(chains)
    what = "end with the **hawk**" if producer is None else f"start with the **{producer}**"
    opts, key, mis = numeric_options(rng, n, [
        (len(web["edges"]), "That is the number of arrows, not the number of complete chains."),
        (n - 1, "You missed a chain. Both frog and bird feed on the snail, so each snail route splits in two."),
        (n + 2, "You counted some routes twice, or included chains from the other producer."),
    ], unit="", sf=2)
    return dict(
        stem=f"Fig. 1 shows a garden food web. How many food chains {what}?",
        figure=_fig(web),
        options=opts, key=key, misconceptions=mis,
        formula="trace every route from the producer(s) to the hawk",
        working=[" / ".join(" → ".join(c) for c in chains), f"total = **{n}**"],
        hints=["Start from the producer (grass or lettuce) and follow the arrows.", "At each organism, branch along every arrow leaving it.", "Count each complete route to the hawk once."],
    )


@template("c12_energy_two_stages", chapter=12, level=3, lo="12.5")
def energy_two_stages(rng):
    E = nice(rng, 5000, 10000, 20000, 50000, 80000)
    E3 = E / 100
    opts, key, mis = numeric_options(rng, E3, [
        (E / 10, "That is the energy at the SECOND stage. The frog is the third, so apply 10% twice."),
        (E * 0.8, "You subtracted 20%. Each stage keeps only 10% of the one before, not 90%."),
        (E / 20, "Two stages of 10% is 10% of 10%, i.e. one hundredth, not one twentieth."),
    ], unit="J", sf=3)
    return dict(
        stem=f"Fig. 1 shows a food chain. The plants contain **{E} J** of energy, and 10% of the energy at each stage is passed to the next. How much energy reaches the **frogs**?",
        figure=S.flow_boxes(["plants", "grasshoppers", "frogs"]),
        options=opts, key=key, misconceptions=mis,
        formula="each stage passes on 10%: multiply by 0.1 for every arrow",
        working=[f"grasshoppers: {E} × 0.1 = {fmt(E / 10)} J", f"frogs: {fmt(E / 10)} × 0.1 = **{fmt(E3)} J**"],
        hints=["How many arrows are there between the plants and the frogs?", "Apply the 10% rule once for each arrow.", f"{E} ÷ 10 ÷ 10."],
    )


@template("c12_predator_peak_time", chapter=12, level=3, lo="12.4")
def predator_peak_time(rng):
    peak = nice(rng, 2, 4, 6)
    prey, pred = _pop_curve(peak)
    pred_peak = max(pred, key=lambda p: p[1])[0]
    opts, key, mis = numeric_options(rng, pred_peak, [
        (peak, "That is when the RABBIT population peaks. The fox peak comes later."),
        (pred_peak + 5 if pred_peak + 5 <= 20 else pred_peak - 5, "That is near the fox population's lowest point."),
        (max(pred, key=lambda p: p[1])[1], "That is the number of foxes at the peak, not the time."),
    ], unit="years", sf=2)
    return dict(
        stem="Fig. 1 shows rabbit (prey) and fox (predator) populations. At what time does the **fox** population first reach its highest value?",
        figure=S.xy_graph([("rabbits", prey), ("foxes", pred)], "time / years", "number of animals", 20, 120, 4, 20),
        options=opts, key=key, misconceptions=mis,
        formula="find the highest point of the predator curve and read the time below it",
        working=[f"fox curve peaks at **{pred_peak} years** (about {pred_peak - peak} years after the rabbit peak)"],
        hints=["Use the legend to find the fox line.", "Find its highest point.", "Read straight down to the time axis."],
    )


@template("c12_light_plants_ratio", chapter=12, level=3, lo="12.2")
def light_plants_ratio(rng):
    sunny = nice(rng, 36, 40, 48, 60)
    shade = nice(rng, 6, 8, 10, 12)
    ratio = sunny / shade
    opts, key, mis = numeric_options(rng, ratio, [
        (sunny - shade, "That is the difference. 'How many times' means divide."),
        (shade / sunny if shade / sunny != ratio else ratio + 1, "You divided the wrong way round: sunny ÷ shady."),
        (ratio + 1, "Check the division."),
    ], unit="times", sf=3)
    return dict(
        stem=f"Students counted a species of plant in 1 m² squares in two parts of a field.\n\n{md_table(['Location', 'Light intensity / units', 'Number of plants per m²'], [['open field (sunny)', '900', str(sunny)], ['under trees (shady)', '150', str(shade)]])}\n\nHow many times more plants grew in the sunny area than in the shady area?",
        options=opts, key=key, misconceptions=mis,
        formula="number of times = larger count ÷ smaller count",
        working=[f"{sunny} ÷ {shade} = **{fmt(ratio)} times**"],
        hints=["Light is a physical factor plants need for photosynthesis.", "'How many times more' means divide the larger by the smaller.", f"{sunny} ÷ {shade}."],
    )


@template("c12_pie_land_use", chapter=12, level=3, lo="12.1")
def pie_land_use(rng):
    uses = ["forest", "farmland", "housing", "roads"]
    pcts = [nice(rng, 40, 45, 50), nice(rng, 25, 30), 15, None]
    pcts[3] = 100 - sum(p for p in pcts if p)
    total = nice(rng, 200, 400, 500, 800)
    i = rng.randint(0, 3)
    ans = total * pcts[i] / 100
    opts, key, mis = numeric_options(rng, ans, [
        (pcts[i], "That is the percentage. Find that percentage OF the total area."),
        (total * (100 - pcts[i]) / 100, f"That is all the land EXCEPT {uses[i]}."),
        (total / 4, "The four uses are not equal shares."),
    ], unit="km²", sf=3)
    return dict(
        stem=f"Fig. 1 shows how the land in a district of **{total} km²** is used. What area is **{uses[i]}**?",
        figure=S.pie_chart([f"{u} ({p}%)" for u, p in zip(uses, pcts)], pcts),
        options=opts, key=key, misconceptions=mis,
        formula="area = percentage ÷ 100 × total area",
        working=[f"{uses[i]}: {pcts[i]}% of {total} km² = **{fmt(ans)} km²**"],
        hints=[f"Read the percentage for {uses[i]}.", "Apply it to the total area.", f"{pcts[i]}/100 × {total}."],
    )


# ---------------------------------------------------------------- L4
@template("c12_predator_prey_lag", chapter=12, level=4, lo="12.4")
def predator_prey_lag(rng):
    peak = nice(rng, 2, 4, 6)
    prey, pred = _pop_curve(peak)
    pred_peak = max(pred, key=lambda p: p[1])[0]
    lag = pred_peak - peak
    opts, key, mis = numeric_options(rng, lag, [
        (pred_peak, "That is the TIME of the fox peak, not the gap between the two peaks."),
        (peak, "That is the time of the rabbit peak."),
        (lag + 2, "Read both peaks carefully and subtract."),
    ], unit="years", sf=2)
    return dict(
        stem="Fig. 1 shows rabbit and fox populations. How long after the **first rabbit peak** does the **first fox peak** occur?",
        figure=S.xy_graph([("rabbits", prey), ("foxes", pred)], "time / years", "number of animals", 20, 120, 4, 20),
        options=opts, key=key, misconceptions=mis,
        formula="lag = time of predator peak − time of prey peak",
        working=[f"rabbit peak at {peak} years; fox peak at {pred_peak} years", f"lag = **{lag} years**"],
        hints=["Find the time of the highest point on each curve.", "More rabbits → more food → fox numbers rise, but later.", f"{pred_peak} − {peak}."],
    )


@template("c12_web_direct_effects_count", chapter=12, level=4, lo="12.5")
def web_direct_effects_count(rng):
    name = pick(rng, list(WEBS))
    web = WEBS[name]
    mids = [n for n in web["nodes"] if any(a == n for a, _ in web["edges"]) and any(b == n for _, b in web["edges"])]
    org = pick(rng, mids)
    eaters = sorted({b for a, b in web["edges"] if a == org})
    n = len(eaters)
    opts, key, mis = numeric_options(rng, n, [
        (len({a for a, b in web["edges"] if b == org}), f"That is the number of organisms the {org} EATS. The question asks which organisms eat the {org}."),
        (n + 1, "Count only the arrows that leave the " + org + " box and point to a feeder."),
        (len(web["nodes"]) - 1, "Not every organism in the web feeds on it directly."),
    ], unit="", sf=1)
    return dict(
        stem=f"Fig. 1 shows a food web. If the **{org}** population disappeared, how many kinds of organism would **directly** lose a source of food?",
        figure=_fig(web),
        options=opts, key=key, misconceptions=mis,
        formula="count the arrows leaving the organism: each points to something that feeds on it",
        working=[f"arrows from {org} point to: {', '.join(eaters)}", f"= **{n}**"],
        hints=["An arrow points from the food to the feeder.", f"Which boxes do arrows from the {org} point to?", "Count those boxes only."],
    )


@template("c12_pyramid_energy_percent_lost", chapter=12, level=4, lo="12.5")
def pyramid_energy_percent_lost(rng):
    E1 = nice(rng, 20000, 40000, 50000)
    frac = nice(rng, 0.08, 0.1, 0.12, 0.15)
    E2 = E1 * frac
    pct_lost = round((1 - frac) * 100)
    opts, key, mis = numeric_options(rng, pct_lost, [
        (round(frac * 100), "That is the percentage PASSED ON. The question asks for the percentage lost."),
        (round(E1 - E2), "That is the energy lost in joules, not the percentage."),
        (round((1 - frac) * 50), "Divide the energy lost by the producers' energy, then × 100."),
    ], unit="%", sf=2)
    return dict(
        stem=f"Fig. 1 shows the energy in each level of a food chain over a year. What percentage of the producers' energy is **lost** between the producers and the primary consumers?",
        figure=S.pyramid(["producers", "primary consumers", "secondary consumers"], [f"{E1} J", f"{fmt(E2)} J", f"{fmt(E2 * frac)} J"]),
        options=opts, key=key, misconceptions=mis,
        formula="percentage lost = (energy in producers − energy in consumers) ÷ energy in producers × 100",
        working=[f"lost = {E1} − {fmt(E2)} = {fmt(E1 - E2)} J", f"percentage = {fmt(E1 - E2)} ÷ {E1} × 100 = **{pct_lost}%**"],
        hints=["Energy lost = energy at the lower level − energy at the next level.", "Compare the loss with the PRODUCERS' energy.", f"({E1} − {fmt(E2)}) ÷ {E1} × 100."],
    )


@template("c12_graph_two_species_cross", chapter=12, level=4, lo="12.4")
def graph_two_species_cross(rng):
    cross = nice(rng, 4, 6, 8, 10)
    native = [(t, round(80 - 5 * t)) for t in range(0, 17)]
    invader = [(t, round(80 - 5 * cross + 5 * (t - cross) * (1 if t >= 0 else 1))) for t in range(0, 17)]
    invader = [(t, max(0, 80 - 5 * cross - 5 * (cross - t))) for t in range(0, 17)]
    opts, key, mis = numeric_options(rng, cross, [
        (cross + 2, "At that time the invasive species is already more numerous. Find where the lines CROSS."),
        (cross - 2, "At that time the native species is still more numerous."),
        (80 - 5 * cross, "That is the number of animals where the lines cross, not the time."),
    ], unit="years", sf=2)
    return dict(
        stem="Fig. 1 shows the populations of a native lizard and an introduced lizard that competes with it for food. After how many years did the introduced species first **outnumber** the native species?",
        figure=S.xy_graph([("native lizard", native), ("introduced lizard", invader)], "time / years", "number of lizards", 16, 100, 4, 20),
        options=opts, key=key, misconceptions=mis,
        formula="the two populations are equal where the lines cross; after that the rising line is larger",
        working=[f"the lines cross at **{cross} years**"],
        hints=["One line falls and the other rises. Where do they meet?", "At the crossing point the two populations are equal.", "Read the time below the crossing point."],
    )


@template("c12_data_logger_table", chapter=12, level=4, lo="12.6*")
def data_logger_table(rng):
    base = nice(rng, 24, 25, 26)
    temps = [base, base - 1, base + 3, base + 7, base + 5, base + 1]
    times = ["00:00", "04:00", "08:00", "12:00", "16:00", "20:00"]
    ask = pick(rng, ["range", "max_time"])
    if ask == "range":
        ans = max(temps) - min(temps)
        opts, key, mis = numeric_options(rng, ans, [
            (max(temps), "That is the highest temperature, not the range."),
            (max(temps) - base, "The lowest reading is not the midnight one. Check every row for the minimum."),
            (ans + 1, "Range = highest − lowest."),
        ], unit="°C", sf=2)
        stem_q = "What is the range of temperature over the day?"
        working = [f"highest {max(temps)} °C, lowest {min(temps)} °C", f"range = **{ans} °C**"]
        hints = ["Find the highest and lowest readings in the table.", "Range = highest − lowest.", f"{max(temps)} − {min(temps)}."]
    else:
        ans_t = times[temps.index(max(temps))]
        opts, key, mis = text_options(rng, ans_t, {"08:00": "The temperature was still rising at 08:00.", "16:00": "By 16:00 the temperature had started to fall.", "00:00": "Midnight is one of the coolest times."})
        stem_q = "At what time was the temperature highest?"
        working = [f"highest reading {max(temps)} °C at **{ans_t}**"]
        hints = ["Look down the temperature column for the biggest number.", "Read the time in the same row.", "The hottest time is usually early afternoon."]
    return dict(
        stem=f"A data logger with a temperature probe recorded the air in a habitat every four hours.\n\n{md_table(['Time', 'Temperature / °C'], [[t, str(T)] for t, T in zip(times, temps)])}\n\n{stem_q}",
        options=opts, key=key, misconceptions=mis,
        formula="read the table: compare the readings",
        working=working, hints=hints,
    )


# ---------------------------------------------------------------- L5
@template("c12_energy_chain_different_efficiencies", chapter=12, level=5, lo="12.5")
def energy_chain_different_efficiencies(rng):
    E = nice(rng, 100000, 200000, 500000)
    p1, p2, p3 = nice(rng, 10, 20), nice(rng, 10, 15), nice(rng, 5, 10)
    E4 = E * p1 / 100 * p2 / 100 * p3 / 100
    opts, key, mis = numeric_options(rng, E4, [
        (E * p1 / 100 * p2 / 100, "That is the energy at the THIRD organism. There is one more stage."),
        (E * (p1 + p2 + p3) / 100 / 3, "You averaged the percentages. Apply each one in turn to the energy left."),
        (E / 1000, "The percentages are not all 10% here; use the values in the table."),
    ], unit="J", sf=3)
    return dict(
        stem=f"The table shows the percentage of energy passed on at each stage of a food chain.\n\n{md_table(['Stage', '% of energy passed on'], [['grass → rabbit', str(p1)], ['rabbit → fox', str(p2)], ['fox → eagle', str(p3)]])}\n\nThe grass contains **{E} J**. How much energy reaches the eagles?",
        options=opts, key=key, misconceptions=mis,
        formula="apply each percentage in turn: E × p1/100 × p2/100 × p3/100",
        working=[f"rabbits: {E} × {p1}/100 = {fmt(E * p1 / 100)} J", f"foxes: × {p2}/100 = {fmt(E * p1 / 100 * p2 / 100)} J", f"eagles: × {p3}/100 = **{fmt(E4)} J**"],
        hints=["Work stage by stage. What reaches the rabbits?", "Each percentage applies to what is LEFT, not to the original.", f"{E} × {p1}/100 × {p2}/100 × {p3}/100."],
    )


@template("c12_chains_through_organism", chapter=12, level=5, lo="12.5")
def chains_through_organism(rng):
    web = WEBS["garden"]
    org = pick(rng, ["snail", "frog", "bird"])
    chains = _chains(web, through=org)
    n = len(chains)
    opts, key, mis = numeric_options(rng, n, [
        (len(_chains(web)), "That is the total number of chains in the web; the question asks only for those that include the " + org + "."),
        (n - 1, "You missed one route. Check both producers and both arrows leaving the " + org + " where they exist."),
        (n + 1, "You counted a route that does not pass through the " + org + "."),
    ], unit="", sf=1)
    return dict(
        stem=f"Fig. 1 shows a garden food web. How many food chains include the **{org}**?",
        figure=_fig(web),
        options=opts, key=key, misconceptions=mis,
        formula="list every complete chain, then keep only those containing the organism",
        working=[" / ".join(" → ".join(c) for c in chains), f"= **{n}**"],
        hints=[f"Find every route INTO the {org} from a producer, and every route OUT of it to the hawk.", "Each way in combined with each way out is one chain.", "Multiply ways in by ways out (or list them)."],
    )


@template("c12_population_growth_rate", chapter=12, level=5, lo="12.5")
def population_growth_rate(rng):
    start = nice(rng, 100, 200, 400)
    rate = nice(rng, 25, 40, 50, 75)
    t1, t2 = pick(rng, [(2, 6), (4, 10), (0, 8)])
    pts = [(t, start + rate * t) for t in range(0, 11)]
    ans = rate
    opts, key, mis = numeric_options(rng, ans, [
        (dict(pts)[t2] - dict(pts)[t1], "That is the total increase. Divide by the number of years to get the rate per year."),
        (dict(pts)[t2] / t2, "You divided the population by the time instead of the INCREASE by the time."),
        (rate * 2, "Check your subtraction and division."),
    ], unit="per year", sf=3)
    return dict(
        stem=f"Fig. 1 shows the growth of a population of deer after wolves were removed from a park. What is the average increase in the deer population **per year** between year {t1} and year {t2}?",
        figure=figs.graph(pts, 10, start + rate * 10 + 100, 2, 200 if rate >= 50 else 100, xlabel="time / years", ylabel="number of deer"),
        options=opts, key=key, misconceptions=mis,
        formula="rate of increase = (population at end − population at start) ÷ time",
        working=[f"year {t1}: {dict(pts)[t1]}; year {t2}: {dict(pts)[t2]}", f"rate = ({dict(pts)[t2]} − {dict(pts)[t1]}) ÷ {t2 - t1} = **{rate} per year**"],
        hints=["Read the population at both years.", "Find the increase, then share it over the years between.", f"(value at {t2} − value at {t1}) ÷ {t2 - t1}."],
    )


@template("c12_quadrat_estimate", chapter=12, level=5, lo="12.6*")
def quadrat_estimate(rng):
    counts = [rng.randint(3, 9) for _ in range(5)]
    field = nice(rng, 200, 400, 500, 1000)
    mean = sum(counts) / 5
    est = mean * field
    opts, key, mis = numeric_options(rng, est, [
        (sum(counts) * field, "You used the TOTAL of the five counts instead of the average per square metre."),
        (mean, "That is the average number per m². Multiply by the area of the field."),
        (sum(counts), "That is just the total counted in the five quadrats."),
    ], unit="plants", sf=3)
    return dict(
        stem=f"Students counted dandelions in five 1 m² quadrats placed at random in a **{field} m²** field.\n\n{md_table(['Quadrat', '1', '2', '3', '4', '5'], [['dandelions', *map(str, counts)]])}\n\nEstimate the number of dandelions in the whole field.",
        options=opts, key=key, misconceptions=mis,
        formula="estimate = average number per m² × area of field",
        working=[f"average = {sum(counts)} ÷ 5 = {fmt(mean)} per m²", f"estimate = {fmt(mean)} × {field} = **{fmt(est)} plants**"],
        hints=["First find the average count in ONE square metre.", f"The field has {field} square metres like that one.", f"({sum(counts)} ÷ 5) × {field}."],
    )


@template("c12_decomposer_time", chapter=12, level=5, lo="12.6*")
def decomposer_time(rng):
    mass = nice(rng, 120, 150, 240, 300)
    rate = nice(rng, 10, 12, 15, 20)
    fallen = nice(rng, 2, 3, 4)
    t = mass / rate
    opts, key, mis = numeric_options(rng, t, [
        (mass / (rate + fallen), "The leaf litter is a fixed pile here; new leaves fall ELSEWHERE in the question. Use the decomposition rate only."),
        (mass * rate, "You multiplied. Time = mass ÷ rate."),
        (rate, "That is the rate (g per month), not the time."),
    ], unit="months", sf=3)
    return dict(
        stem=f"Fungi and bacteria (decomposers) break down a pile of **{mass} g** of fallen leaves at an average of **{rate} g per month**, returning nutrients to the soil. Nearby, {fallen} g of new leaves fall each month onto a different pile.\n\n{md_table(['Quantity', 'Value'], [['mass of pile', f'{mass} g'], ['rate of decomposition', f'{rate} g per month']])}\n\nHow long will the decomposers take to break down the whole pile?",
        options=opts, key=key, misconceptions=mis,
        formula="time = mass ÷ rate of decomposition",
        working=[f"time = {mass} ÷ {rate}", f"= **{fmt(t)} months**"],
        hints=["Decomposers break down dead material and recycle nutrients.", "Only the pile asked about matters; ignore the extra information about the other pile.", f"{mass} ÷ {rate}."],
    )


# ================================================================ EXPLANATION
EXPLAIN = [
    # ------------------------------------------------------------ L1
    dict(id="e12_ecosystem_definition", level=1, lo="12.3",
         stem="The table lists some terms.\n\n| Term | Meaning |\n|---|---|\n| population | organisms of the same kind in one place |\n| community | all the populations in one place |\n| ecosystem | ? |\n\nAn ecosystem is",
         correct="a community interacting with its physical environment",
         wrongs={"a group of organisms of the same kind": "That is a population.", "all the animals in a place": "A community includes plants too, and an ecosystem also includes the non-living surroundings.", "the place where one organism lives": "That is a habitat."},
         hints=["It is bigger than a community.", "It includes the living things AND the non-living things (water, air, soil, light).", "Community + physical environment."]),
    dict(id="e12_producer_definition", level=1, lo="12.5",
         stem="Fig. 1 shows a food chain. The grass is called the producer because it",
         correct="makes its own food by photosynthesis using light energy",
         wrongs={"is eaten by the most animals": "Being eaten does not make it a producer; making food does.", "produces oxygen for the animals": "Plants do give out oxygen, but 'producer' refers to producing FOOD.", "is the largest organism in the chain": "Size has nothing to do with it."},
         hints=["Where does the energy in a food chain come from originally?", "Green plants trap light energy to make food.", "Makes food → producer."],
         fig=lambda rng: S.flow_boxes(["grass", "rabbit", "fox"])),
    dict(id="e12_arrow_meaning", level=1, lo="12.5",
         stem="Fig. 1 shows a food chain. The arrow from the grasshopper to the frog means",
         correct="the frog eats the grasshopper; energy passes from the grasshopper to the frog",
         wrongs={"the grasshopper eats the frog": "Arrows point from the food TO the feeder.", "the grasshopper turns into a frog": "Arrows show feeding, not change.", "the frog and the grasshopper compete for food": "The arrow shows one eating the other."},
         hints=["Arrows show the direction in which energy flows.", "Energy goes from the food into the eater.", "Arrow points to the eater."],
         fig=lambda rng: S.flow_boxes(["grass", "grasshopper", "frog"])),
    dict(id="e12_population_term", level=1, lo="12.3",
         stem="The table describes groups of organisms in a pond.\n\n| Group | Description |\n|---|---|\n| X | all the goldfish in the pond |\n| Y | all the fish, snails, plants and insects in the pond |\n\nX is a",
         correct="population",
         wrongs={"community": "Y, with many kinds of organism, is the community.", "habitat": "The habitat is the pond itself.", "ecosystem": "The ecosystem is the community plus its environment."},
         hints=["How many kinds of organism are in X?", "One kind, one place.", "Same species, same place = ____."]),
    dict(id="e12_physical_factor", level=1, lo="12.2",
         stem="The table lists things in a habitat.\n\n| Item |\n|---|\n| temperature |\n| earthworms |\n| light |\n| water |\n\nWhich item is **not** a physical factor of the environment?",
         correct="earthworms",
         wrongs={"temperature": "Temperature is a physical (non-living) factor.", "light": "Light is a physical factor.", "water": "Water is a physical factor."},
         hints=["Physical factors are non-living.", "Which item is alive?", "Living things are part of the community, not the physical environment."]),

    # ------------------------------------------------------------ L2
    dict(id="e12_classify_adaptation", level=2, lo="12.2",
         hints=["Structural = a body feature. Behavioural = something the organism DOES.", "Is it a part of the body or an action?", "Then check that the reason matches."],
         variants=[
             dict(stem="The table describes a desert fox.\n\n| Feature | Detail |\n|---|---|\n| ears | very large |\n| activity | hunts at night |\n\nIts large ears are a",
                  correct="structural adaptation that helps it lose heat", wrongs={"behavioural adaptation that helps it lose heat": "Ears are a body part, so this is structural.", "structural adaptation that keeps it warm": "Large ears have a big surface area to LOSE heat in a hot desert.", "behavioural adaptation for hunting": "Hunting at night is the behavioural adaptation, not the ears."}),
             dict(stem="The table describes a desert lizard.\n\n| Feature | Detail |\n|---|---|\n| skin | scaly, waterproof |\n| activity | hides in a burrow at midday |\n\nHiding in a burrow at midday is a",
                  correct="behavioural adaptation that avoids the hottest part of the day", wrongs={"structural adaptation that avoids heat": "Hiding is an action, so it is behavioural.", "behavioural adaptation to find water": "The burrow is for escaping heat, not finding water.", "structural adaptation to save water": "The waterproof skin is the structural adaptation for saving water."}),
             dict(stem="The table describes an Arctic hare.\n\n| Feature | Detail |\n|---|---|\n| fur | thick and white in winter |\n| grouping | huddles with others in storms |\n\nThick white winter fur is a",
                  correct="structural adaptation for warmth and camouflage", wrongs={"behavioural adaptation for warmth": "Fur is a body feature: structural.", "structural adaptation for finding food": "The fur is for insulation and hiding, not feeding.", "behavioural adaptation for camouflage": "Huddling is the behavioural adaptation."}),
         ]),
    dict(id="e12_identify_relationship", level=2, lo="12.4",
         hints=["Who benefits and who is harmed?", "Three patterns: both gain; one gains while the other is harmed but stays alive; one kills and eats the other.", "Match the table to one of those patterns and recall its name."],
         variants=[
             dict(stem="The table describes a relationship.\n\n| Organism | Effect |\n|---|---|\n| clownfish | gets protection among the anemone's tentacles |\n| sea anemone | gets food scraps and cleaning from the fish |\n\nThis is",
                  correct="mutualism", wrongs={"parasitism": "Neither organism is harmed.", "predator–prey": "Neither eats the other.", "competition": "They are not fighting over the same resource."}),
             dict(stem="The table describes a relationship.\n\n| Organism | Effect |\n|---|---|\n| tick | feeds on the dog's blood |\n| dog | loses blood, skin irritated, but stays alive |\n\nThis is",
                  correct="parasitism", wrongs={"mutualism": "The dog is harmed, not helped.", "predator–prey": "The tick does not kill and eat the dog.", "competition": "They are not competing for the same food."}),
             dict(stem="The table describes a relationship.\n\n| Organism | Effect |\n|---|---|\n| owl | catches, kills and eats the mouse |\n| mouse | dies |\n\nThis is",
                  correct="predator–prey", wrongs={"parasitism": "A parasite keeps its host alive; the owl kills the mouse.", "mutualism": "Only the owl benefits.", "competition": "The owl eats the mouse rather than competing with it."}),
         ]),
    dict(id="e12_identify_consumer_level", level=2, lo="12.5",
         stem="Fig. 1 shows a food chain. Which organism is a **primary consumer**?",
         correct="the caterpillar",
         wrongs={"the oak leaves": "Leaves are the producer.", "the bird": "The bird eats the primary consumer, so it is a secondary consumer.", "the cat": "The cat is the tertiary (third) consumer."},
         hints=["The primary consumer is the FIRST animal in the chain.", "It eats the producer.", "Which box comes right after the leaves?"],
         fig=lambda rng: S.flow_boxes(["oak leaves", "caterpillar", "bird", "cat"])),
    dict(id="e12_identify_physical_factor_effect", level=2, lo="12.2",
         stem="The table shows a plant species in two soils.\n\n| Soil | Minerals | Plant height / cm |\n|---|---|---|\n| P | rich in minerals | 45 |\n| Q | poor in minerals | 12 |\n\nWhich physical factor explains the difference?",
         correct="the amount of minerals in the soil",
         wrongs={"the amount of light": "Light is not mentioned as different between the soils.", "the temperature": "Temperature is not given in the table.", "the number of predators": "Predators are a living factor, and none are mentioned."},
         hints=["Which column differs between P and Q?", "Plants need minerals from the soil to grow.", "The only difference shown is the mineral content."]),
    dict(id="e12_conservation_action", level=2, lo="12.1",
         stem="The table lists actions.\n\n| Action |\n|---|\n| taking public transport |\n| leaving the air-conditioner on all day |\n| recycling paper |\n| bringing a reusable bag |\n\nWhich action does **not** help conserve the environment?",
         correct="leaving the air-conditioner on all day",
         wrongs={"taking public transport": "Fewer cars means less fuel burnt and less pollution.", "recycling paper": "Recycling saves trees and reduces waste.", "bringing a reusable bag": "This reduces plastic waste."},
         hints=["Conservation means using only what we need.", "Which action wastes energy?", "Energy use → more fossil fuels burnt."]),

    # ------------------------------------------------------------ L3
    dict(id="e12_adaptation_helps_survival", level=3, lo="12.2",
         hints=["Link the feature to the physical factor or threat.", "Feature → what it does → how that helps survive.", "Choose the option where every step makes sense."],
         variants=[
             dict(stem="The table describes a cactus.\n\n| Feature | Detail |\n|---|---|\n| leaves | reduced to spines |\n| stem | thick and fleshy |\n\nHow do the spines help the cactus survive in the desert?",
                  correct="They have a small surface area, so less water is lost, and they protect the plant from animals.", wrongs={"They absorb water from the air.": "Spines do not absorb water; roots do.", "They make photosynthesis faster.": "Spines have little surface for photosynthesis; the stem does that.", "They attract insects for pollination.": "Flowers attract insects, not spines."}),
             dict(stem="The table describes a polar bear.\n\n| Feature | Detail |\n|---|---|\n| fur | thick |\n| fat | thick layer under the skin |\n\nHow do these features help it survive?",
                  correct="Fur traps air and fat is a poor conductor, so both reduce heat loss in the cold.", wrongs={"They make the bear heavier so it can break ice.": "Weight is not the purpose of fur and fat.", "They help the bear lose heat quickly.": "In the Arctic the bear needs to KEEP heat, not lose it.", "They store water for the summer.": "Fat stores energy, not water."}),
             dict(stem="The table describes a water lily.\n\n| Feature | Detail |\n|---|---|\n| leaves | broad, flat, float on the surface |\n| stem | long, with air spaces |\n\nHow do the broad floating leaves help the plant?",
                  correct="They get plenty of light for photosynthesis at the surface.", wrongs={"They stop the plant from drowning.": "Plants do not drown; the air spaces give buoyancy, not the leaf shape.", "They absorb minerals from the water.": "Roots absorb minerals.", "They keep the water cool.": "Shading is not the purpose of the leaves."}),
         ]),
    dict(id="e12_web_removal_effect", level=3, lo="12.5",
         stem="Fig. 1 shows a pond food web. Disease kills all the **water snails**. What is the most likely immediate effect on the **small fish**?",
         correct="Their numbers fall, because they have lost one of their food sources.",
         wrongs={"Their numbers rise, because there is less competition.": "Snails are food for the fish, not competitors.", "There is no effect, because fish do not eat snails.": "The arrow from water snail to small fish shows that they do.", "They start eating herons instead.": "Herons eat fish, not the other way round."},
         hints=["Find the arrows leaving the water snail box.", "Which organisms lose a food source?", "Less food → fewer survive."],
         fig=lambda rng: _fig(WEBS["pond"])),
    dict(id="e12_food_chains_short", level=3, lo="12.5",
         stem="Fig. 1 shows the energy at each stage of a food chain. Why do food chains rarely have more than four or five links?",
         correct="So much energy is lost as heat at each stage that there is too little left to support another level.",
         wrongs={"Large animals cannot find enough space.": "Space is not the limiting factor; energy is.", "Producers run out of light.": "Light is plentiful; the problem is energy LOST between stages.", "Animals higher up the chain live too long.": "Lifespan does not limit chain length."},
         hints=["About 90% of the energy is lost at every arrow.", "After a few stages, how much is left?", "Too little energy → cannot feed another level."],
         fig=lambda rng: S.energy_arrows(["grass", "grasshopper", "frog", "snake"], [10000, 1000, 100, 10])),
    dict(id="e12_decomposers_role", level=3, lo="12.6*",
         stem="Fig. 1 shows a dead leaf being broken down. What is the role of decomposers such as fungi and bacteria in an ecosystem?",
         correct="They break down dead organisms and waste, returning nutrients to the soil for plants to use again.",
         wrongs={"They produce food by photosynthesis.": "Decomposers do not photosynthesise; they feed on dead material.", "They eat living plants and animals.": "They feed on DEAD material and waste.", "They remove nutrients from the soil permanently.": "They do the opposite: they RETURN nutrients to the soil."},
         hints=["What happens to dead leaves and animals on a forest floor?", "Nutrients locked in dead material must get back into the soil somehow.", "Break down → release nutrients → recycled."],
         fig=lambda rng: S.flow_boxes(["dead leaf", "decomposers\n(fungi, bacteria)", "nutrients in soil", "plants"])),
    dict(id="e12_human_impact_effect", level=3, lo="12.1",
         stem="The table shows a change in a river.\n\n| Before | After a factory opened |\n|---|---|\n| water clear, pH 7 | water cloudy, pH 4 |\n| many fish | very few fish |\n\nWhat is the most likely explanation?",
         correct="Waste from the factory made the water acidic and polluted, so fish could not survive.",
         wrongs={"The fish migrated to find mates.": "A sudden change in pH alongside the drop in fish numbers points to pollution.", "Cloudy water gives fish more hiding places, so they left.": "Cloudy water blocks light and often means pollution; it does not drive fish away by itself.", "The factory warmed the air, so the fish grew too fast.": "Nothing in the table mentions temperature."},
         hints=["What changed in the water? Which physical factor is that?", "Many organisms survive only in a narrow pH range.", "Pollution → pH change → organisms die."]),

    # ------------------------------------------------------------ L4
    dict(id="e12_predator_prey_explain", level=4, lo="12.4",
         stem="Fig. 1 shows rabbit and fox populations over time. Why does the fox population peak **after** the rabbit population?",
         correct="More rabbits means more food for foxes, so more fox cubs survive, but it takes time for fox numbers to grow.",
         wrongs={"Foxes breed before rabbits each year.": "The lag is about food supply, not breeding season.", "Rabbits eat foxes when there are many rabbits.": "Rabbits do not eat foxes.", "The two populations are not related.": "The repeating pattern shows they ARE linked through feeding."},
         hints=["Foxes depend on rabbits for food.", "When food increases, what happens to the number of young that survive? Does it happen instantly?", "More food → more foxes, after a delay."],
         fig=lambda rng: S.xy_graph([("rabbits", _pop_curve(4)[0]), ("foxes", _pop_curve(4)[1])], "time / years", "number of animals", 20, 120, 4, 20)),
    dict(id="e12_pyramid_shape_explain", level=4, lo="12.5",
         stem="Fig. 1 shows a pyramid of numbers. Why are there far fewer snakes than grasshoppers?",
         correct="Energy is lost as heat at each stage, so there is only enough energy to support a small number of organisms at the top.",
         wrongs={"Snakes are hunted by humans.": "The pyramid shape appears in undisturbed habitats too; the reason is energy flow.", "Grasshoppers reproduce faster, so there must be more of them.": "Reproduction rate alone does not set the shape; the available ENERGY does.", "Snakes need less space.": "Space is not the cause."},
         hints=["Think about the energy passed up the chain.", "About 90% is lost at each arrow.", "Less energy → fewer organisms can be fed."],
         fig=lambda rng: S.pyramid(["grass plants", "grasshoppers", "frogs", "snakes"], [8000, 600, 40, 3])),
    dict(id="e12_remove_predator_overgraze", level=4, lo="12.4",
         stem="Fig. 1 shows a food chain. Hunters remove all the wolves from a park. What is the likely long-term effect on the **grass**?",
         correct="Deer numbers rise, the deer overgraze, and the grass is greatly reduced.",
         wrongs={"The grass increases because wolves trampled it.": "Wolves have little effect on grass directly; the deer do.", "There is no effect on the grass.": "Changes at one level pass along the chain.", "The grass increases because deer numbers fall.": "Without predators, deer numbers RISE."},
         hints=["Follow the chain: fewer wolves → ? deer → ? grass.", "Predators keep prey numbers in check.", "More deer eat more grass."],
         fig=lambda rng: S.flow_boxes(["grass", "deer", "wolf"])),
    dict(id="e12_data_logger_advantage", level=4, lo="12.6*",
         stem="The table compares two ways of measuring the temperature of a stream over 24 hours.\n\n| Method | Readings taken | Accuracy |\n|---|---|---|\n| thermometer, by hand | every 4 hours, daytime only | to 1 °C |\n| data logger with probe | every minute, all day and night | to 0.1 °C |\n\nWhy is the data logger the better choice for this investigation?",
         correct="It records continuously and accurately, including at night when no one is there to take readings.",
         wrongs={"It is cheaper than a thermometer.": "Data loggers usually cost more; their advantage is in the data.", "It changes the temperature of the stream less.": "Neither method heats the stream noticeably.", "It gives readings in kelvin.": "Both can give °C; the unit is not the advantage."},
         hints=["Compare the 'readings taken' column.", "Which method misses part of the day?", "Continuous + accurate."]),
    dict(id="e12_energy_flow_photosynthesis_respiration", level=4, lo="12.5",
         stem="Fig. 1 shows energy entering and leaving a food chain. Which statement about energy flow is correct?",
         correct="Light energy is trapped by producers in photosynthesis, passes along the chain by feeding, and is released by respiration mainly as heat.",
         wrongs={"Energy is recycled from the last consumer back to the producers.": "Energy flows ONE way; it is nutrients that are recycled.", "Consumers make their own energy by respiration.": "Respiration RELEASES energy stored in food; it does not create it.", "All the energy a plant traps reaches the top consumer.": "Most is lost as heat at each stage."},
         hints=["Where does the energy enter? How does it move? How does it leave?", "Enter: photosynthesis. Move: feeding. Leave: respiration (heat).", "One-way flow."],
         fig=lambda rng: S.energy_arrows(["producers\n(photosynthesis)", "consumers", "top consumer"], [10000, 1000, 100])),

    # ------------------------------------------------------------ L5
    dict(id="e12_evaluate_conservation_claim", level=5, lo="12.1",
         stem="The table shows a town's waste.\n\n| Year | Waste produced / tonnes | Recycled / tonnes |\n|---|---|---|\n| 2015 | 1000 | 200 |\n| 2025 | 1600 | 400 |\n\nThe council says: 'We doubled recycling, so we are conserving the environment.' Which comment is most accurate?",
         correct="Recycling doubled, but the waste produced also grew by 600 tonnes, so more waste is going to landfill than before.",
         wrongs={"The claim is fully correct; doubling recycling is enough.": "Landfill waste rose from 800 to 1200 tonnes, so the problem has grown.", "The claim is wrong because recycling does not help the environment.": "Recycling does help; the issue is that total waste grew faster.", "The town should stop recycling and reduce waste instead.": "Both reducing and recycling are needed; stopping recycling would make things worse."},
         hints=["Work out the waste that was NOT recycled in each year.", "2015: 1000 − 200. 2025: 1600 − 400.", "Reduce comes before reuse and recycle."]),
    dict(id="e12_pesticide_web_predict", level=5, lo="12.5",
         stem="Fig. 1 shows a garden food web. A gardener sprays the lettuces with a pesticide that kills all the caterpillars and snails. Predict the effect on the **frogs**.",
         correct="Frog numbers fall, because they lose the snails as food and now depend only on grasshoppers.",
         wrongs={"Frog numbers rise, because there are more lettuces to eat.": "Frogs do not eat lettuce.", "Frogs are unaffected, because they do not eat caterpillars.": "True for caterpillars, but frogs DO eat snails.", "Frogs die out completely at once.": "They still have grasshoppers, so they decline rather than vanish immediately."},
         hints=["Which arrows lead into the frog box?", "One of those food sources has gone.", "Fewer food sources → numbers fall, but not to zero."],
         fig=lambda rng: _fig(WEBS["garden"])),
    dict(id="e12_sustainable_practice_evaluate", level=5, lo="12.6*",
         stem="The table compares two fishing communities.\n\n| Community | Practice | Fish caught per year now | Fish stock trend |\n|---|---|---|---|\n| P | catches as many fish as possible | 500 tonnes | falling fast |\n| Q | catches only adult fish, limit of 300 tonnes | 300 tonnes | steady |\n\nWhich statement best evaluates the two practices?",
         correct="Q is sustainable: by catching less and leaving young fish, the stock stays steady, so they can keep fishing for years.",
         wrongs={"P is better because it catches more fish.": "The stock is falling fast, so P's catches will soon collapse.", "Both are sustainable because both catch fish every year.": "P's falling stock means it cannot continue.", "Q is wasteful because it leaves fish uncaught.": "Leaving young fish is what keeps the population going."},
         hints=["Sustainable means it can carry on without using up the resource.", "Compare the 'fish stock trend' column.", "Steady stock → can continue."]),
    dict(id="e12_introduced_species_evaluate", level=5, lo="12.4",
         stem="Fig. 1 shows the populations of a native and an introduced lizard. Why did the introduced lizard cause the native lizard to decline?",
         correct="The introduced lizard competed with the native lizard for the same food, leaving less for the native species.",
         wrongs={"The introduced lizard taught the native lizard to eat less.": "Animals do not teach each other to eat less.", "The native lizard moved away to make room.": "The graph shows a decline, not migration.", "The introduced lizard had no effect; the decline was a coincidence.": "The timing and the rising competitor's line point to competition."},
         hints=["Both species eat the same food.", "What happens when two species need the same limited resource?", "Competition → one species loses out."],
         fig=lambda rng: S.xy_graph([("native lizard", [(t, 80 - 5 * t) for t in range(17)]), ("introduced lizard", [(t, max(0, 40 - 5 * (8 - t))) for t in range(17)])], "time / years", "number of lizards", 16, 100, 4, 20)),
    dict(id="e12_environment_change_adaptation", level=5, lo="12.2",
         stem="The table shows moth colours in a wood before and after soot from factories darkened the tree bark.\n\n| Moth colour | Before (%) | After (%) |\n|---|---|---|\n| pale | 95 | 20 |\n| dark | 5 | 80 |\n\nWhich explanation is best?",
         correct="On dark bark, pale moths were easily seen and eaten by birds, so more dark moths survived to breed.",
         wrongs={"Soot stained the pale moths dark.": "Soot does not permanently change a moth's colour; the proportions of each type changed.", "The moths chose to become dark to match the bark.": "Organisms cannot choose their traits.", "Birds stopped eating moths.": "Birds kept eating moths, but now they caught the ones that stood out."},
         hints=["Which moth is camouflaged on dark bark?", "Predators eat the ones they can see.", "The survivors pass on their trait."]),
]

register_explain(EXPLAIN, chapter=12)
