"""Ch 13 Electrical Systems: 25 calculation / data templates and 25 explanation items.
lo codes: 13.1 circuits and symbols, 13.2 current, p.d., resistance, 13.3* series / parallel resistors and variable resistance (G3),
13.4 effects of current, 13.5 hazards and safety, 13.6 power and saving electricity, 13.7* cost of electricity in kWh (G3)."""
from .. import figs, sketches as S
from .base import fmt, md_table, nice, numeric_options, pick, register_explain, template, text_options

APPLIANCES = [("kettle", 2000), ("iron", 1200), ("hair dryer", 1500), ("television", 100), ("fan", 60), ("LED lamp", 10), ("filament lamp", 60), ("air-conditioner", 1000), ("rice cooker", 500), ("laptop", 50)]


def money(x):
    return f"${x:,.2f}"


# ================================================================ CALCULATION / DATA
# ---------------------------------------------------------------- L1
@template("c13_energy_from_power_seconds", chapter=13, level=1, lo="13.6")
def energy_from_power_seconds(rng):
    name, P = pick(rng, APPLIANCES[3:])
    t = nice(rng, 5, 10, 20, 30, 60)
    E = P * t
    opts, key, mis = numeric_options(rng, E, [
        (P, "That is the power: the energy converted in ONE second. Multiply by the number of seconds."),
        (P / t, "You divided. Energy = power × time."),
        (P + t, "You added. Energy = power × time."),
    ], unit="J", sf=3)
    return dict(
        stem=f"The table gives the power rating of an appliance.\n\n{md_table(['Appliance', 'Power rating'], [[name, f'{P} W']])}\n\nA power of 1 W means 1 J of electrical energy is converted every second. How much electrical energy does the {name} convert in **{t} seconds**?",
        options=opts, key=key, misconceptions=mis,
        formula="energy converted (J) = power (W) × time (s)",
        working=[f"E = {P} W × {t} s", f"= **{fmt(E, sf=4)} J**"],
        hints=["Power tells you the joules converted EACH second.", f"How many seconds? Multiply.", f"{P} × {t}."],
    )


@template("c13_series_current_same", chapter=13, level=1, lo="13.2")
def series_current_same(rng):
    I = nice(rng, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6)
    opts, key, mis = numeric_options(rng, I, [
        (I / 2, "In a SERIES circuit the current is the same everywhere; it is not shared between the lamps."),
        (I * 2, "The current does not add up around a series loop. It is the same at every point."),
        (I + 0.1, "The current is the same everywhere in a series circuit."),
    ], unit="A", sf=2)
    return dict(
        stem=f"Fig. 1 shows two lamps and two ammeters connected in series. Ammeter A₁ reads **{fmt(I)} A**. What does ammeter A₂ read?",
        figure=S.circuit(["ammeter", "lamp", "lamp", "ammeter"], top=("cell",), labels=["A₁", "", "", "A₂"]),
        options=opts, key=key, misconceptions=mis,
        formula="in a series circuit the current is the same at every point",
        working=[f"series circuit → same current everywhere", f"A₂ = **{fmt(I)} A**"],
        hints=["Is there more than one path for the current?", "In a single loop, the charge that passes A₁ must also pass A₂.", "Same current at every point."],
    )


@template("c13_kwh_simple", chapter=13, level=1, lo="13.7*")
def kwh_simple(rng):
    P = nice(rng, 1, 1.5, 2, 2.5, 3)
    t = nice(rng, 2, 3, 4, 5, 8, 10)
    E = P * t
    opts, key, mis = numeric_options(rng, E, [
        (P / t, "You divided. Energy = power × time."),
        (P + t, "You added. Multiply the power in kW by the time in hours."),
        (E * 1000, "Power in kW × time in h gives kWh directly; do not multiply by 1000."),
    ], unit="kWh", sf=3)
    return dict(
        stem=f"The table shows an appliance's power and how long it is used.\n\n{md_table(['Power / kW', 'Time used / h'], [[fmt(P), str(t)]])}\n\nHow much electrical energy does it use, in kWh?",
        options=opts, key=key, misconceptions=mis,
        formula="energy (kWh) = power (kW) × time (h)",
        working=[f"E = {fmt(P)} kW × {t} h", f"= **{fmt(E)} kWh**"],
        hints=["A kilowatt-hour is the energy used by 1 kW running for 1 hour.", "Multiply the kilowatts by the hours.", f"{fmt(P)} × {t}."],
    )


@template("c13_cost_simple", chapter=13, level=1, lo="13.7*")
def cost_simple(rng):
    E = nice(rng, 4, 5, 8, 10, 12, 20, 25)
    tariff = nice(rng, 0.20, 0.25, 0.30, 0.32)
    cost = E * tariff
    opts, key, mis = numeric_options(rng, cost, [
        (E / tariff, "You divided. Cost = number of kWh × cost of one kWh."),
        (E + tariff, "You added. Multiply."),
        (cost * 100, "Check the units: the tariff is in dollars per kWh, so the answer is in dollars."),
    ], unit="dollars", sf=3)
    return dict(
        stem=f"The table shows electricity used and the tariff.\n\n{md_table(['Energy used / kWh', 'Tariff'], [[str(E), f'${fmt(tariff, dp=2)} per kWh']])}\n\nWhat is the cost of the electricity?",
        options=opts, key=key, misconceptions=mis,
        formula="cost = energy (kWh) × tariff ($ per kWh)",
        working=[f"cost = {E} × ${fmt(tariff, dp=2)}", f"= **${fmt(cost, dp=2)}**"],
        hints=["Each kWh costs the tariff.", "How many kWh were used? Multiply.", f"{E} × {fmt(tariff, dp=2)}."],
    )


@template("c13_count_lamps_series", chapter=13, level=1, lo="13.1")
def count_lamps_series(rng):
    n = rng.randint(1, 3)
    comps = ["lamp"] * n + ["resistor", "switch_closed"]
    rng.shuffle(comps)
    opts, key, mis = text_options(rng, f"{n} lamp{'s' if n > 1 else ''}, in series", {
        f"{n} lamp{'s' if n > 1 else ''}, in parallel": "There is only one loop, so the components are in SERIES.",
        f"{n + 1} lamp{'s' if n + 1 > 1 else ''}, in series": "Count the circles with a cross: the rectangle is a resistor, not a lamp.",
        f"{n + 2} lamps, in series": "You counted the switch or the cell as a lamp. Only the crossed circles are lamps.",
    })
    return dict(
        stem="Fig. 1 shows a circuit. How many lamps does it contain, and how are the components connected?",
        figure=S.circuit(comps, top=("cell",)),
        options=opts, key=key, misconceptions=mis,
        formula="lamp symbol = circle with a cross; one loop = series",
        working=[f"crossed circles: {n}", "single loop → series", f"**{n} lamp{'s' if n > 1 else ''}, in series**"],
        hints=["The lamp symbol is a circle with an X inside.", "A rectangle is a resistor; the gap with a dot each side is a switch.", "One path for the current means series."],
    )


# ---------------------------------------------------------------- L2
@template("c13_parallel_currents_add", chapter=13, level=2, lo="13.2")
def parallel_currents_add(rng):
    I1 = nice(rng, 0.2, 0.3, 0.4, 0.5)
    I2 = nice(rng, 0.1, 0.2, 0.3, 0.6)
    total = round(I1 + I2, 2)
    opts, key, mis = numeric_options(rng, total, [
        (max(I1, I2), "In parallel the branch currents ADD to give the main current."),
        (abs(I1 - I2) if I1 != I2 else total / 4, "You subtracted. The main current is the SUM of the branch currents."),
        (total / 2, "You averaged. Add the two branch currents."),
    ], unit="A", sf=2)
    return dict(
        stem=f"Fig. 1 shows two lamps in parallel. The current through lamp X is **{fmt(I1)} A** and through lamp Y is **{fmt(I2)} A**. What is the reading on the ammeter in the main circuit?",
        figure=S.circuit([], top=("cell", "ammeter"), parallel=[["lamp"], ["lamp"]], labels=["X", "Y"]),
        options=opts, key=key, misconceptions=mis,
        formula="main current = sum of the currents in the parallel branches",
        working=[f"I = {fmt(I1)} + {fmt(I2)}", f"= **{fmt(total)} A**"],
        hints=["The current splits at the junction and joins up again.", "What goes into the junction must come out: add the branches.", f"{fmt(I1)} + {fmt(I2)}."],
    )


@template("c13_w_to_kw_energy", chapter=13, level=2, lo="13.7*")
def w_to_kw_energy(rng):
    name, P = pick(rng, [a for a in APPLIANCES if a[1] >= 500])
    t = nice(rng, 2, 3, 4, 5, 6)
    E = P / 1000 * t
    opts, key, mis = numeric_options(rng, E, [
        (P * t, "That is in watt-hours. Convert the power to kW (divide by 1000) first."),
        (P / 1000 / t, "You divided by the time. Energy = power × time."),
        (P / 100 * t, "1 kW = 1000 W, not 100 W."),
    ], unit="kWh", sf=3)
    return dict(
        stem=f"The table shows an appliance.\n\n{md_table(['Appliance', 'Power', 'Time used'], [[name, f'{P} W', f'{t} h']])}\n\nHow much energy does it use, in **kWh**?",
        options=opts, key=key, misconceptions=mis,
        formula="power in kW = W ÷ 1000; energy (kWh) = kW × h",
        working=[f"P = {P} W = {fmt(P / 1000)} kW", f"E = {fmt(P / 1000)} × {t} = **{fmt(E)} kWh**"],
        hints=["kWh needs the power in KILOwatts.", "1000 W = 1 kW.", f"({P} ÷ 1000) × {t}."],
    )


@template("c13_minutes_to_hours_cost", chapter=13, level=2, lo="13.7*")
def minutes_to_hours_cost(rng):
    P = nice(rng, 1.2, 1.5, 2.0, 2.4, 3.0)
    mins = nice(rng, 15, 20, 30, 45)
    tariff = nice(rng, 0.20, 0.25, 0.30)
    E = P * mins / 60
    cost = E * tariff
    opts, key, mis = numeric_options(rng, cost, [
        (P * mins * tariff, "You used the time in minutes. Convert to hours first (÷ 60)."),
        (E, "That is the energy in kWh. Multiply by the tariff to get the cost."),
        (P * tariff, "You forgot the time. Energy = power × time (in hours)."),
    ], unit="dollars", sf=3)
    return dict(
        stem=f"A **{fmt(P)} kW** heater is used for **{mins} minutes**. Electricity costs **${fmt(tariff, dp=2)} per kWh**.\n\n{md_table(['Power / kW', 'Time / min', 'Tariff'], [[fmt(P), str(mins), f'${fmt(tariff, dp=2)} per kWh']])}\n\nWhat is the cost?",
        options=opts, key=key, misconceptions=mis,
        formula="time in h = min ÷ 60; E = P × t; cost = E × tariff",
        working=[f"t = {mins} ÷ 60 = {fmt(mins / 60)} h", f"E = {fmt(P)} × {fmt(mins / 60)} = {fmt(E)} kWh", f"cost = {fmt(E)} × ${fmt(tariff, dp=2)} = **${fmt(cost, dp=2)}**"],
        hints=["The time must be in HOURS for kWh.", f"{mins} minutes is {mins}/60 of an hour.", f"{fmt(P)} × ({mins} ÷ 60) × {fmt(tariff, dp=2)}."],
    )


@template("c13_power_from_energy_time", chapter=13, level=2, lo="13.6")
def power_from_energy_time(rng):
    P = nice(rng, 40, 60, 100, 500, 800, 1200)
    t = nice(rng, 5, 10, 20, 30, 60)
    E = P * t
    opts, key, mis = numeric_options(rng, P, [
        (E, "That is the energy in joules. Power is the energy converted PER SECOND."),
        (E * t, "You multiplied. Power = energy ÷ time."),
        (t / E * 1e6 if t / E * 1e6 != P else P + 10, "You divided the wrong way round. Power = energy ÷ time."),
    ], unit="W", sf=3)
    return dict(
        stem=f"An appliance converts electrical energy as shown.\n\n{md_table(['Energy converted / J', 'Time / s'], [[fmt(E, sf=4), str(t)]])}\n\nWhat is the power of the appliance?",
        options=opts, key=key, misconceptions=mis,
        formula="power (W) = energy converted (J) ÷ time (s)",
        working=[f"P = {fmt(E, sf=4)} ÷ {t}", f"= **{P} W**"],
        hints=["Power is the energy converted every second.", "Share the energy equally over the seconds.", f"{fmt(E, sf=4)} ÷ {t}."],
    )


@template("c13_series_pd_shared", chapter=13, level=2, lo="13.2")
def series_pd_shared(rng):
    V = nice(rng, 3.0, 4.5, 6.0, 9.0, 12.0)
    V1 = round(V * nice(rng, 0.25, 0.4, 0.5, 0.6), 1)
    V2 = round(V - V1, 1)
    opts, key, mis = numeric_options(rng, V2, [
        (V, "The p.d. of the supply is SHARED between the two lamps in series."),
        (V1, "That is the p.d. across lamp P. Lamp Q gets the rest."),
        (V + V1, "You added. The two p.d.s add up TO the supply p.d., so Q = supply − P."),
    ], unit="V", sf=2)
    return dict(
        stem=f"Fig. 1 shows two lamps P and Q in series with a **{fmt(V)} V** supply. The voltmeter across lamp P reads **{fmt(V1)} V**. What is the p.d. across lamp Q?",
        figure=S.circuit(["lamp", "lamp"], top=("battery",), voltmeter_across=0, labels=["P", "Q"]),
        options=opts, key=key, misconceptions=mis,
        formula="in series, the p.d.s across the components add up to the supply p.d.",
        working=[f"V_Q = {fmt(V)} − {fmt(V1)}", f"= **{fmt(V2)} V**"],
        hints=["In a series circuit the supply voltage is shared out.", "P's share plus Q's share equals the supply.", f"{fmt(V)} − {fmt(V1)}."],
    )


# ---------------------------------------------------------------- L3
@template("c13_total_cost_table", chapter=13, level=3, lo="13.7*")
def total_cost_table(rng):
    items = rng.sample([a for a in APPLIANCES if a[1] >= 100], 3)
    hours = [nice(rng, 1, 2, 4), nice(rng, 0.5, 1, 3), nice(rng, 2, 5, 8)]
    tariff = nice(rng, 0.20, 0.25, 0.30)
    rows = [[n, str(P), fmt(h)] for (n, P), h in zip(items, hours)]
    E = sum(P / 1000 * h for (n, P), h in zip(items, hours))
    cost = E * tariff
    opts, key, mis = numeric_options(rng, cost, [
        (E, "That is the total energy in kWh. Multiply by the tariff."),
        (sum(P * h for (n, P), h in zip(items, hours)) * tariff, "You left the power in watts. Convert each to kW first."),
        (max(P / 1000 * h for (n, P), h in zip(items, hours)) * tariff, "That is the cost of one appliance only. Add all three."),
    ], unit="dollars", sf=3)
    return dict(
        stem=f"The table shows three appliances used in one day. Electricity costs **${fmt(tariff, dp=2)} per kWh**.\n\n{md_table(['Appliance', 'Power / W', 'Time used / h'], rows)}\n\nWhat is the total cost for the day?",
        options=opts, key=key, misconceptions=mis,
        formula="for each: E = (W ÷ 1000) × h; total E; cost = total E × tariff",
        working=[", ".join(f"{n}: {fmt(P / 1000 * h)} kWh" for (n, P), h in zip(items, hours)), f"total = {fmt(E)} kWh", f"cost = {fmt(E)} × ${fmt(tariff, dp=2)} = **${fmt(cost, dp=2)}**"],
        hints=["Work out the kWh for each appliance (kW × h).", "Add the three energies.", "Then multiply the total by the tariff."],
    )


@template("c13_resistance_current_pattern", chapter=13, level=3, lo="13.3*")
def resistance_current_pattern(rng):
    I0 = nice(rng, 1.2, 2.4, 3.0, 6.0)
    rows = [["1", fmt(I0)], ["2", fmt(I0 / 2)], ["3", fmt(I0 / 3)]]
    ask = nice(rng, 4, 6)
    ans = I0 / ask
    opts, key, mis = numeric_options(rng, ans, [
        (I0 * ask, "The current goes DOWN as resistance goes up. Look at the pattern in the table."),
        (I0 / (ask - 1), "Check the pattern: each time the resistance is multiplied, the current is divided by the same number."),
        (I0 - ask * 0.1, "The current is not falling by a fixed amount; it is being divided."),
    ], unit="A", sf=3)
    return dict(
        stem=f"A student changes the resistance in a circuit and records the current.\n\n{md_table(['Resistance / units', 'Current / A'], rows)}\n\nFollowing the pattern, what current flows when the resistance is **{ask} units**?",
        options=opts, key=key, misconceptions=mis,
        formula="increasing the resistance decreases the current: here the current = (current at 1 unit) ÷ resistance",
        working=[f"pattern: current = {fmt(I0)} ÷ resistance", f"at {ask} units: {fmt(I0)} ÷ {ask} = **{fmt(ans)} A**"],
        hints=["Does the current rise or fall as the resistance rises?", "Compare row 1 with row 2: what happened to the current when the resistance doubled?", f"{fmt(I0)} ÷ {ask}."],
    )


@template("c13_energy_saved_led", chapter=13, level=3, lo="13.6")
def energy_saved_led(rng):
    P_old, P_new = pick(rng, [(60, 10), (100, 12), (40, 6)])
    t = nice(rng, 4, 5, 6, 8)
    saved = (P_old - P_new) / 1000 * t
    opts, key, mis = numeric_options(rng, saved, [
        (P_old / 1000 * t, "That is the energy the filament lamp uses. The saving is the DIFFERENCE between the two lamps."),
        ((P_old - P_new) * t, "That is in watt-hours. Divide by 1000 for kWh."),
        (P_new / 1000 * t, "That is the energy the LED uses, not the saving."),
    ], unit="kWh", sf=3)
    return dict(
        stem=f"Fig. 1 compares two lamps that give the same brightness. Both are used for **{t} hours** a day. How much energy is saved in one day by using the LED lamp instead of the filament lamp?",
        figure=S.bar_chart(["filament lamp", "LED lamp"], [P_old, P_new], "power / W", ymax=120, ystep=20),
        options=opts, key=key, misconceptions=mis,
        formula="saving = (power difference in kW) × time in h",
        working=[f"difference = {P_old} − {P_new} = {P_old - P_new} W = {fmt((P_old - P_new) / 1000)} kW", f"saved = {fmt((P_old - P_new) / 1000)} × {t} = **{fmt(saved)} kWh**"],
        hints=["Find the difference in power between the two lamps.", "Convert that to kW, then multiply by the hours.", f"({P_old} − {P_new}) ÷ 1000 × {t}."],
    )


@template("c13_bar_chart_energy_difference", chapter=13, level=3, lo="13.6")
def bar_chart_energy_difference(rng):
    items = rng.sample([a for a in APPLIANCES if a[1] >= 100 and a[1] <= 2000], 4)
    t = nice(rng, 10, 30, 60)   # minutes
    names = [n for n, _ in items]
    Ps = [P for _, P in items]
    hi, lo = max(Ps), min(Ps)
    diff = (hi - lo) * t * 60   # J
    opts, key, mis = numeric_options(rng, diff, [
        (hi * t * 60, "That is the energy used by the most powerful appliance alone."),
        ((hi - lo) * t, "You used minutes. Convert to seconds for joules (× 60)."),
        (hi - lo, "That is the difference in POWER (W), not in energy."),
    ], unit="J", sf=3)
    return dict(
        stem=f"Fig. 1 shows the power ratings of four appliances. Each is switched on for **{t} minutes**. How much more energy does the most powerful appliance convert than the least powerful one?",
        figure=S.bar_chart(names, Ps, "power / W", ymax=2500, ystep=500, size=(5.2, 3.0)),
        options=opts, key=key, misconceptions=mis,
        formula="energy (J) = power (W) × time (s); difference = (P_max − P_min) × t",
        working=[f"P_max − P_min = {hi} − {lo} = {hi - lo} W", f"t = {t} min = {t * 60} s", f"difference = {hi - lo} × {t * 60} = **{fmt(diff)} J**"],
        hints=["Read the tallest and shortest bars.", "Energy = power × time, with time in seconds for joules.", f"({hi} − {lo}) × {t} × 60."],
    )


@template("c13_parallel_unknown_branch", chapter=13, level=3, lo="13.2")
def parallel_unknown_branch(rng):
    total = nice(rng, 0.9, 1.0, 1.2, 1.5)
    I1 = nice(rng, 0.2, 0.3, 0.4)
    I2 = nice(rng, 0.2, 0.3)
    I3 = round(total - I1 - I2, 2)
    if I3 <= 0:
        I3, total = 0.3, round(I1 + I2 + 0.3, 2)
    opts, key, mis = numeric_options(rng, I3, [
        (total, "That is the main current. The third branch gets what is LEFT after the other two."),
        (round(total - I1, 2), "You subtracted only one branch."),
        (round(I1 + I2, 2), "That is the total of the two known branches."),
    ], unit="A", sf=2)
    return dict(
        stem=f"Three lamps are connected in parallel. The table shows the ammeter readings.\n\n{md_table(['Position', 'Current / A'], [['main circuit', fmt(total)], ['branch 1', fmt(I1)], ['branch 2', fmt(I2)], ['branch 3', '?']])}\n\nWhat is the current in branch 3?",
        options=opts, key=key, misconceptions=mis,
        formula="main current = branch 1 + branch 2 + branch 3",
        working=[f"branch 3 = {fmt(total)} − {fmt(I1)} − {fmt(I2)}", f"= **{fmt(I3)} A**"],
        hints=["The branch currents add up to the main current.", "Two branches are known; the third is the remainder.", f"{fmt(total)} − {fmt(I1)} − {fmt(I2)}."],
    )


# ---------------------------------------------------------------- L4
@template("c13_graph_energy_time_power", chapter=13, level=4, lo="13.6")
def graph_energy_time_power(rng):
    P = nice(rng, 20, 40, 50, 100)
    pts = [(0, 0), (10, P * 10)]
    opts, key, mis = numeric_options(rng, P, [
        (P * 10, "That is the energy after 10 s. Power is energy per SECOND: divide by the time."),
        (P / 10, "You divided by the time twice. Power = energy ÷ time = gradient of the line."),
        (P * 2, "Check the gradient: rise ÷ run."),
    ], unit="W", sf=3)
    return dict(
        stem="Fig. 1 shows the electrical energy converted by a lamp against time. What is the power of the lamp?",
        figure=figs.graph(pts, 10, P * 10, 2, P * 2, xlabel="time / s", ylabel="energy / J"),
        options=opts, key=key, misconceptions=mis,
        formula="power = energy ÷ time = gradient of an energy–time graph",
        working=[f"at 10 s, energy = {P * 10} J", f"power = {P * 10} ÷ 10 = **{P} W**"],
        hints=["Pick a point on the line and read both its coordinates.", "Power is energy divided by time.", "Use the point at 10 s to keep the division easy."],
    )


@template("c13_monthly_cost_table", chapter=13, level=4, lo="13.7*")
def monthly_cost_table(rng):
    name, P = pick(rng, [("air-conditioner", 1000), ("water heater", 2000), ("refrigerator", 150), ("television", 100)])
    h = nice(rng, 2, 4, 6, 8)
    days = 30
    tariff = nice(rng, 0.25, 0.30)
    E = P / 1000 * h * days
    cost = E * tariff
    opts, key, mis = numeric_options(rng, cost, [
        (P / 1000 * h * tariff, "That is the cost for ONE day. The question asks for 30 days."),
        (P * h * days * tariff, "You left the power in watts. Convert to kW."),
        (E, "That is the energy in kWh, not the cost."),
    ], unit="dollars", sf=3)
    return dict(
        stem=f"The table shows how a household uses an appliance.\n\n{md_table(['Appliance', 'Power / W', 'Hours per day', 'Days', 'Tariff'], [[name, str(P), str(h), str(days), f'${fmt(tariff, dp=2)} per kWh']])}\n\nWhat is the cost of running the {name} for the month?",
        options=opts, key=key, misconceptions=mis,
        formula="E = kW × hours per day × days; cost = E × tariff",
        working=[f"E = {fmt(P / 1000)} kW × {h} h × {days} = {fmt(E)} kWh", f"cost = {fmt(E)} × ${fmt(tariff, dp=2)} = **${fmt(cost, dp=2)}**"],
        hints=["Find the total hours in the month first (hours per day × days).", "Energy = kW × total hours.", "Then × tariff."],
    )


@template("c13_bar_chart_percent_saved", chapter=13, level=4, lo="13.6")
def bar_chart_percent_saved(rng):
    before = nice(rng, 400, 500, 600, 800)
    pct = nice(rng, 10, 15, 20, 25, 30)
    after = before * (100 - pct) / 100
    opts, key, mis = numeric_options(rng, pct, [
        (100 - pct, "That is the percentage still being used, not the saving."),
        (before - after, "That is the saving in kWh. Turn it into a percentage of the ORIGINAL."),
        (round((before - after) / after * 100), "Divide by the original (before) value, not the new one."),
    ], unit="%", sf=3)
    return dict(
        stem="Fig. 1 shows a household's monthly electricity use before and after it switched to LED lamps and a fan instead of air-conditioning. By what percentage did its electricity use fall?",
        figure=S.bar_chart(["before", "after"], [before, after], "energy used / kWh per month", ymax=1000, ystep=200),
        options=opts, key=key, misconceptions=mis,
        formula="percentage fall = (before − after) ÷ before × 100",
        working=[f"fall = {before} − {fmt(after)} = {fmt(before - after)} kWh", f"= {fmt(before - after)} ÷ {before} × 100 = **{pct}%**"],
        hints=["Read both bars.", "Find the fall, then compare it with the BEFORE value.", f"({before} − {fmt(after)}) ÷ {before} × 100."],
    )


@template("c13_graph_current_vs_resistance", chapter=13, level=4, lo="13.3*")
def graph_current_vs_resistance(rng):
    V = nice(rng, 6, 12)
    pts = [(R, V / R) for R in (2, 3, 4, 6, 8, 10, 12)]
    ask = nice(rng, 3, 4, 6, 12)
    ans = V / ask
    opts, key, mis = numeric_options(rng, ans, [
        (V / (ask / 2), "You read the current at half that resistance."),
        (ask, "That is the resistance. Read the current on the vertical axis."),
        (V / (ask * 2), "You read the current at twice that resistance."),
    ], unit="A", sf=3)
    return dict(
        stem=f"Fig. 1 shows how the current in a circuit changes as the resistance of a variable resistor is increased. What is the current when the resistance is **{ask} Ω**?",
        figure=figs.graph(pts, 12, V / 2 + 1, 2, 1, xlabel="resistance / Ω", ylabel="current / A"),
        options=opts, key=key, misconceptions=mis,
        formula="read the graph: resistance on the x-axis → up to the curve → across to the current axis",
        working=[f"at {ask} Ω the curve is at **{fmt(ans)} A**", "increasing the resistance decreases the current"],
        hints=["Find the resistance on the horizontal axis.", "Go up to the curve and across.", "As resistance rises the current falls, so the curve slopes down."],
    )


@template("c13_meter_readings_bill", chapter=13, level=4, lo="13.7*")
def meter_readings_bill(rng):
    start = rng.randint(10000, 20000)
    used = nice(rng, 180, 240, 300, 360, 420)
    end = start + used
    tariff = nice(rng, 0.25, 0.30)
    cost = used * tariff
    opts, key, mis = numeric_options(rng, cost, [
        (used, "That is the number of kWh used. Multiply by the tariff for the cost."),
        (end * tariff, "You multiplied the final reading by the tariff. Only the DIFFERENCE between the readings was used this month."),
        (used * tariff * 100, "The tariff is in dollars per kWh, so the answer is in dollars."),
    ], unit="dollars", sf=3)
    return dict(
        stem=f"An electricity meter counts kWh.\n\n{md_table(['Reading', 'kWh'], [['1 March', str(start)], ['1 April', str(end)]])}\n\nElectricity costs **${fmt(tariff, dp=2)} per kWh**. What is the bill for March?",
        options=opts, key=key, misconceptions=mis,
        formula="kWh used = final reading − initial reading; cost = kWh × tariff",
        working=[f"used = {end} − {start} = {used} kWh", f"cost = {used} × ${fmt(tariff, dp=2)} = **${fmt(cost, dp=2)}**"],
        hints=["The meter keeps counting; the month's use is the change in the reading.", "Subtract the readings first.", f"({end} − {start}) × {fmt(tariff, dp=2)}."],
    )


# ---------------------------------------------------------------- L5
@template("c13_lamp_lifetime_cost", chapter=13, level=5, lo="13.7*")
def lamp_lifetime_cost(rng):
    P_f, P_l = 60, 8
    price_f, price_l = nice(rng, 1, 2), nice(rng, 6, 8, 10)
    hours = nice(rng, 1000, 1500, 2000)
    tariff = nice(rng, 0.25, 0.30)
    cost_f = price_f + P_f / 1000 * hours * tariff
    cost_l = price_l + P_l / 1000 * hours * tariff
    saving = cost_f - cost_l
    opts, key, mis = numeric_options(rng, saving, [
        ((P_f - P_l) / 1000 * hours * tariff, "That is the saving on electricity only. The LED costs more to buy; include the purchase prices."),
        (cost_f, "That is the total cost of the filament lamp, not the saving."),
        (price_l - price_f, "That is only the difference in purchase price; you must also compare the electricity costs."),
    ], unit="dollars", sf=3)
    return dict(
        stem=f"The table compares two lamps of the same brightness over **{hours} hours** of use at **${fmt(tariff, dp=2)} per kWh**.\n\n{md_table(['Lamp', 'Power / W', 'Price to buy'], [['filament', str(P_f), f'${price_f}'], ['LED', str(P_l), f'${price_l}']])}\n\nHow much money is saved overall by choosing the LED lamp?",
        options=opts, key=key, misconceptions=mis,
        formula="total cost = price + (kW × h × tariff); saving = filament total − LED total",
        working=[f"filament: {price_f} + {fmt(P_f / 1000)} × {hours} × {fmt(tariff, dp=2)} = ${fmt(cost_f, dp=2)}", f"LED: {price_l} + {fmt(P_l / 1000)} × {hours} × {fmt(tariff, dp=2)} = ${fmt(cost_l, dp=2)}", f"saving = **${fmt(saving, dp=2)}**"],
        hints=["Work out the TOTAL cost of each lamp: price plus electricity.", "Electricity = kW × hours × tariff.", "Subtract the two totals."],
    )


@template("c13_parallel_two_branches_trap", chapter=13, level=5, lo="13.2")
def parallel_two_branches_trap(rng):
    I_x = nice(rng, 0.3, 0.4, 0.6)
    I_y = nice(rng, 0.2, 0.3, 0.5)
    total = round(I_x + I_y, 2)
    opts, key, mis = numeric_options(rng, I_y, [
        (total, "A₁ is in the MAIN circuit, so it reads the total. A₂ is in branch Y only and reads just that branch."),
        (I_x, "That is the current through X. A₂ is on branch Y."),
        (round(total + I_x, 2), "Currents in parallel add up to the main current; nothing is larger than the main current."),
    ], unit="A", sf=2)
    return dict(
        stem=f"Fig. 1 shows lamps X and Y in parallel. Ammeter A₁ in the main circuit reads **{fmt(total)} A**, and the current through X is **{fmt(I_x)} A**. What does ammeter A₂, in series with lamp Y, read?",
        figure=S.circuit([], top=("cell", "ammeter"), parallel=[["lamp"], ["lamp", "ammeter"]], labels=["X", "Y, A₂"]),
        options=opts, key=key, misconceptions=mis,
        formula="main current = I_X + I_Y, so I_Y = main − I_X",
        working=[f"I_Y = {fmt(total)} − {fmt(I_x)}", f"= **{fmt(I_y)} A**"],
        hints=["Which ammeter is in the main circuit and which is in a branch?", "Main current = sum of the branch currents.", f"{fmt(total)} − {fmt(I_x)}."],
    )


@template("c13_kwh_mixed_units", chapter=13, level=5, lo="13.7*")
def kwh_mixed_units(rng):
    P = nice(rng, 800, 1200, 1500, 2400)
    mins = nice(rng, 10, 15, 20, 30)
    days = nice(rng, 7, 14, 30)
    tariff = nice(rng, 0.25, 0.30)
    E = P / 1000 * mins / 60 * days
    cost = E * tariff
    opts, key, mis = numeric_options(rng, cost, [
        (P / 1000 * mins * days * tariff, "You used minutes as if they were hours. Divide the minutes by 60."),
        (P * mins / 60 * days * tariff, "You left the power in watts. Divide by 1000 for kW."),
        (P / 1000 * mins / 60 * tariff, "That is the cost for ONE day. Multiply by the number of days."),
    ], unit="dollars", sf=3)
    return dict(
        stem=f"A **{P} W** toaster is used for **{mins} minutes** every day for **{days} days**. Electricity costs **${fmt(tariff, dp=2)} per kWh**.\n\n{md_table(['Power / W', 'Minutes per day', 'Days', 'Tariff'], [[str(P), str(mins), str(days), f'${fmt(tariff, dp=2)}']])}\n\nWhat is the total cost?",
        options=opts, key=key, misconceptions=mis,
        formula="E = (W ÷ 1000) × (min ÷ 60) × days; cost = E × tariff",
        working=[f"E = {fmt(P / 1000)} kW × {fmt(mins / 60)} h × {days} = {fmt(E)} kWh", f"cost = {fmt(E)} × ${fmt(tariff, dp=2)} = **${fmt(cost, dp=2)}**"],
        hints=["Two conversions: W → kW and minutes → hours.", "Then multiply by the number of days.", f"({P}/1000) × ({mins}/60) × {days} × {fmt(tariff, dp=2)}."],
    )


@template("c13_hours_less_aircon", chapter=13, level=5, lo="13.7*")
def hours_less_aircon(rng):
    P = nice(rng, 1.0, 1.2, 1.5)
    h = nice(rng, 6, 8, 10)
    target_kwh = nice(rng, 1.5, 2.0, 3.0)
    hours_less = target_kwh / P
    opts, key, mis = numeric_options(rng, hours_less, [
        (target_kwh, "That is the energy saving in kWh, not the hours."),
        (target_kwh * P, "You multiplied. Hours = energy ÷ power."),
        (h - target_kwh, "Subtracting kWh from hours mixes units. Convert the energy to hours first."),
    ], unit="hours", sf=3)
    return dict(
        stem=f"A family runs a **{fmt(P)} kW** air-conditioner for **{h} hours** each night. They want to save **{fmt(target_kwh)} kWh** per night.\n\n{md_table(['Power / kW', 'Hours per night', 'Target saving / kWh'], [[fmt(P), str(h), fmt(target_kwh)]])}\n\nBy how many hours per night must they cut its use?",
        options=opts, key=key, misconceptions=mis,
        formula="energy saved = power × hours cut, so hours cut = energy saved ÷ power",
        working=[f"hours cut = {fmt(target_kwh)} ÷ {fmt(P)}", f"= **{fmt(hours_less)} hours**"],
        hints=["Every hour the air-conditioner is off saves P kWh.", "How many such hours give the target saving?", f"{fmt(target_kwh)} ÷ {fmt(P)}."],
    )


@template("c13_energy_per_minute_kj", chapter=13, level=5, lo="13.6")
def energy_per_minute_kj(rng):
    P = nice(rng, 500, 800, 1200, 2000)
    mins = nice(rng, 2, 3, 5)
    E_kJ = P * mins * 60 / 1000
    opts, key, mis = numeric_options(rng, E_kJ, [
        (P * mins / 1000, "You used minutes as seconds. 1 minute = 60 s."),
        (P * mins * 60, "That is in joules. The question asks for kilojoules (÷ 1000)."),
        (P * 60 / 1000, "That is the energy in one minute only."),
    ], unit="kJ", sf=3)
    return dict(
        stem=f"A **{P} W** heater is switched on for **{mins} minutes**.\n\n{md_table(['Power / W', 'Time / min'], [[str(P), str(mins)]])}\n\nHow much electrical energy does it convert, in **kJ**?",
        options=opts, key=key, misconceptions=mis,
        formula="E (J) = P (W) × t (s); 1 kJ = 1000 J",
        working=[f"t = {mins} × 60 = {mins * 60} s", f"E = {P} × {mins * 60} = {fmt(P * mins * 60, sf=4)} J = **{fmt(E_kJ)} kJ**"],
        hints=["Power is joules per SECOND, so convert the minutes.", "Then divide the joules by 1000.", f"{P} × {mins} × 60 ÷ 1000."],
    )


# ================================================================ EXPLANATION
EXPLAIN = [
    # ------------------------------------------------------------ L1
    dict(id="e13_unit_current", level=1, lo="13.2",
         stem="Fig. 1 shows a circuit with an ammeter. What does the ammeter measure, and in what unit?",
         correct="current, in amperes (A)",
         wrongs={"potential difference, in volts (V)": "A voltmeter measures potential difference.", "resistance, in ohms (Ω)": "Resistance is not measured by an ammeter.", "energy, in joules (J)": "Energy is not measured by a circuit meter."},
         hints=["The letter on the meter is A.", "It is connected in series and measures how much charge flows each second.", "Flow of charge = current."],
         fig=lambda rng: S.circuit(["lamp", "ammeter"], top=("cell",))),
    dict(id="e13_ammeter_connection", level=1, lo="13.1",
         stem="Fig. 1 shows a lamp circuit. To measure the current through the lamp, an ammeter must be connected",
         correct="in series with the lamp",
         wrongs={"in parallel with the lamp": "That is how a VOLTMETER is connected.", "across the cell": "Across means in parallel; an ammeter must be in the current's path.", "anywhere, as long as it touches a wire": "It must be IN the circuit path so the current flows through it."},
         hints=["The current must flow THROUGH the ammeter.", "That means it is part of the same loop as the lamp.", "Same loop = series."],
         fig=lambda rng: S.circuit(["lamp"], top=("cell",))),
    dict(id="e13_voltmeter_connection", level=1, lo="13.1",
         stem="Fig. 1 shows a voltmeter correctly connected to measure the p.d. across lamp P. A voltmeter is connected",
         correct="in parallel with (across) the component",
         wrongs={"in series with the component": "A voltmeter in series would stop the current; it goes ACROSS the component.", "only across the cell": "It can go across any component.", "in the main circuit next to the ammeter": "That is the ammeter's place; a voltmeter is placed across a component."},
         hints=["Look at how the V meter is wired in Fig. 1.", "Its two leads touch either side of the lamp.", "Either side of = parallel."],
         fig=lambda rng: S.circuit(["lamp", "resistor"], top=("cell",), voltmeter_across=0, labels=["P", "Q"])),
    dict(id="e13_conductor_insulator", level=1, lo="13.1",
         stem="The table shows what happened when different materials were put into a gap in a lamp circuit.\n\n| Material | Lamp lights? |\n|---|---|\n| copper | yes |\n| plastic | no |\n| iron | yes |\n| rubber | no |\n\nWhich statement is correct?",
         correct="Copper and iron are conductors; plastic and rubber are insulators.",
         wrongs={"Copper and iron are insulators; plastic and rubber are conductors.": "The lamp lit with copper and iron, so they let current flow: conductors.", "All four materials are conductors.": "The lamp did not light with plastic or rubber.", "Only copper is a conductor.": "Iron also made the lamp light."},
         hints=["A conductor lets current flow, so the lamp lights.", "Read the 'lights?' column.", "Metals conduct; plastics and rubber do not."]),
    dict(id="e13_power_meaning", level=1, lo="13.6",
         stem="The table shows a label on a lamp.\n\n| Lamp | Rating |\n|---|---|\n| P | 60 W |\n\nThe rating 60 W means the lamp",
         correct="converts 60 J of electrical energy every second",
         wrongs={"uses a current of 60 A": "Watts measure power, not current.", "needs a p.d. of 60 V": "Volts measure p.d.; watts measure power.", "stores 60 J of energy": "Power is a RATE: energy per second, not stored energy."},
         hints=["Power is measured in watts.", "Power = energy converted per unit time.", "1 W = 1 J per second."]),

    # ------------------------------------------------------------ L2
    dict(id="e13_identify_symbol", level=2, lo="13.1",
         hints=["Rectangle = resistor; rectangle with an arrow through it = variable resistor.", "Circle with a cross = lamp; circle with A = ammeter; circle with V = voltmeter.", "Long thin line and short thick line = cell."],
         fig=lambda rng: S.circuit(["lamp", "variable", "ammeter"], top=("cell", "switch_open"), labels=["P", "Q", "R"]),
         variants=[
             dict(stem="Fig. 1 shows a circuit. Which component is **Q**?", correct="a variable resistor", wrongs={"a fixed resistor": "A fixed resistor is a plain rectangle; Q has an arrow through it.", "a fuse": "A fuse symbol is a rectangle with a line through it, not an arrow.", "a lamp": "The lamp is the crossed circle, P."}),
             dict(stem="Fig. 1 shows a circuit. Which statement about the circuit is correct?", correct="The switch is open, so no current flows.", wrongs={"The switch is closed, so the lamp is lit.": "The switch symbol shows a gap: it is open.", "There is no cell in the circuit.": "The cell is on the top wire (long thin line and short thick line).", "Q is an ammeter.": "The ammeter is R; Q is the variable resistor."}),
         ]),
    dict(id="e13_identify_effect", level=2, lo="13.4",
         hints=["Heating effect: something gets hot. Magnetic effect: a coil attracts iron or makes a motor turn. Chemical effect: a substance is coated or split.", "What does the device DO with the current?", "Match the action to the effect."],
         fig=lambda rng: S.electromagnet(),
         variants=[
             dict(stem="Fig. 1 shows a coil with an iron core. An electric bell uses an electromagnet to pull a striker. This is the", correct="magnetic effect of current", wrongs={"heating effect of current": "The bell does not work by getting hot.", "chemical effect of current": "No chemical change takes place in a bell.", "lighting effect of current": "The bell makes sound, not light."}),
             dict(stem="Fig. 1 shows an electromagnet for comparison. A toaster's wires glow red and brown the bread. This is the", correct="heating effect of current", wrongs={"magnetic effect of current": "Nothing is attracted or turned.", "chemical effect of current": "The toaster wire itself does not change chemically.", "cooling effect of current": "Current heats a resistance wire; it does not cool it."}),
             dict(stem="Fig. 1 shows an electromagnet for comparison. A steel spoon is coated with a thin layer of silver by passing a current through a solution. This is the", correct="chemical effect of current", wrongs={"heating effect of current": "The coating forms by a chemical change, not by heat.", "magnetic effect of current": "Nothing is attracted or moved.", "lighting effect of current": "No light is produced."}),
         ]),
    dict(id="e13_identify_hazard", level=2, lo="13.5",
         hints=["Hazards: overloading a socket, damaged insulation, water near electricity, overheating.", "Which option describes a danger rather than a safe practice?", "Think: could this cause a shock or a fire?"],
         fig=lambda rng: S.plug_wiring(),
         variants=[
             dict(stem="Fig. 1 shows a plug. Which of the following is an electrical **hazard**?", correct="plugging five high-power appliances into one socket with an adaptor", wrongs={"switching off an appliance at the socket before unplugging it": "That is a safe practice.", "replacing a frayed cable": "That removes a hazard.", "keeping a hair dryer away from the bathroom sink": "That is a safe practice."}),
             dict(stem="Fig. 1 shows a plug. Which situation is most likely to cause an electric shock?", correct="touching a switch with wet hands", wrongs={"using a plug with the correct fuse": "A correct fuse protects the circuit.", "switching off before changing a lamp": "That prevents shocks.", "using an appliance with intact insulation": "Intact insulation keeps the user safe."}),
         ]),
    dict(id="e13_switch_open_which_lamps", level=2, lo="13.1",
         stem="Fig. 1 shows two lamps in parallel; the switch is in series with lamp Y only. When the switch is **open**,",
         correct="X stays lit and Y goes out",
         wrongs={"both lamps go out": "The switch is only in Y's branch; X still has a complete path.", "both lamps stay lit": "Y's branch is broken, so Y goes out.", "X goes out and Y stays lit": "The switch is in Y's branch, not X's."},
         hints=["Trace the complete loop from the cell through each lamp.", "Which loop passes through the open switch?", "Only that lamp loses its current."],
         fig=lambda rng: S.circuit([], top=("cell",), parallel=[["lamp"], ["lamp", "switch_open"]], labels=["X", "Y"])),
    dict(id="e13_units_table", level=2, lo="13.2",
         stem="The table matches quantities with units.\n\n| Quantity | Unit |\n|---|---|\n| current | ampere |\n| potential difference | ? |\n| resistance | ohm |\n| power | watt |\n\nWhich unit completes the table?",
         correct="volt",
         wrongs={"joule": "The joule is the unit of energy.", "coulomb": "The coulomb is the unit of charge.", "kilowatt-hour": "That is a unit of energy used for electricity bills."},
         hints=["Potential difference is measured with the meter marked V.", "The unit shares its first letter with that meter's symbol.", "It is named after the Italian scientist Alessandro Volta."]),

    # ------------------------------------------------------------ L3
    dict(id="e13_add_resistor_series", level=3, lo="13.3*",
         stem="Fig. 1 shows a lamp in series with a resistor. A second resistor is added in series. What happens to the lamp?",
         correct="It becomes dimmer, because the total resistance increases and the current decreases.",
         wrongs={"It becomes brighter, because there are more components.": "More resistance in series means LESS current.", "It stays the same, because the cell has not changed.": "The same cell drives less current through a larger resistance.", "It goes out, because resistors block current.": "Resistors reduce current; they do not stop it."},
         hints=["Resistors in series add up.", "More resistance → less current from the same cell.", "Less current through the lamp → dimmer."],
         fig=lambda rng: S.circuit(["lamp", "resistor", "resistor"], top=("cell",))),
    dict(id="e13_house_wiring_parallel", level=3, lo="13.1",
         stem="Fig. 1 shows two lamps connected in parallel. Why are the lamps in a house wired in parallel rather than in series?",
         correct="Each lamp gets the full supply p.d. and can be switched on and off without affecting the others.",
         wrongs={"Parallel wiring uses less wire.": "Parallel wiring usually needs MORE wire.", "In parallel the lamps share the current, so they last longer.": "Each lamp draws its own current; the advantage is independence and full p.d.", "Series wiring would blow the fuse.": "Series wiring would make the lamps dim and all go off together, not blow the fuse."},
         hints=["If one lamp in a series circuit breaks, what happens to the rest?", "In parallel each lamp has its own loop.", "Independent control + full brightness."],
         fig=lambda rng: S.circuit([], top=("battery",), parallel=[["lamp", "switch_closed"], ["lamp", "switch_open"]])),
    dict(id="e13_fuse_how", level=3, lo="13.5",
         stem="Fig. 1 shows a plug with a fuse. How does the fuse protect the appliance?",
         correct="If the current becomes too large, the thin fuse wire melts and breaks the circuit.",
         wrongs={"It cools the wires when they get hot.": "A fuse does not cool anything; it breaks the circuit.", "It increases the current to the appliance.": "A fuse never increases current.", "It stores extra charge for the appliance.": "A fuse stores nothing."},
         hints=["What is inside a fuse? A thin wire.", "What happens to a thin wire when a large current heats it?", "Melts → gap → no current."],
         fig=lambda rng: S.plug_wiring()),
    dict(id="e13_dimmer_variable_resistor", level=3, lo="13.3*",
         stem="Fig. 1 shows a lamp in series with a variable resistor. Sliding the contact increases the resistance. What happens to the lamp?",
         correct="It becomes dimmer, because the current decreases.",
         wrongs={"It becomes brighter, because the voltage increases.": "The supply voltage is unchanged; the current falls.", "It flickers on and off.": "A variable resistor changes the current smoothly.", "Nothing changes, because resistance does not affect current.": "Resistance DOES affect current: more resistance, less current."},
         hints=["A variable resistor controls the current.", "More resistance → ? current.", "Current and brightness go together."],
         fig=lambda rng: S.circuit(["lamp", "variable"], top=("cell",))),
    dict(id="e13_heating_element_material", level=3, lo="13.4",
         stem="The table compares two wires.\n\n| Wire | Resistance | Melting point |\n|---|---|---|\n| copper | low | 1085 °C |\n| nichrome | high | 1400 °C |\n\nWhy is nichrome used for the heating element in a kettle?",
         correct="Its high resistance makes it heat up strongly, and its high melting point means it does not melt.",
         wrongs={"Its low resistance lets a large current flow.": "Nichrome has HIGH resistance; that is why it gets hot.", "It is a good insulator.": "An insulator would carry no current at all.", "It is the cheapest metal.": "Cost is not the reason; its properties are."},
         hints=["The heating effect is stronger in a wire with higher resistance.", "An element gets very hot, so what else must the wire resist?", "High resistance + high melting point."]),

    # ------------------------------------------------------------ L4
    dict(id="e13_electromagnet_stronger", level=4, lo="13.4",
         stem="Fig. 1 shows an electromagnet picking up paper clips. Which change would make it pick up MORE clips?",
         correct="Increasing the number of turns of wire or the current.",
         wrongs={"Replacing the iron core with a plastic rod.": "Iron concentrates the magnetic effect; plastic would make it much weaker.", "Using fewer turns of wire.": "Fewer turns → weaker electromagnet.", "Opening the switch.": "No current → no magnetism at all."},
         hints=["What produces the magnetism: the current in the coil.", "More current or more coil → stronger field.", "An iron core also helps."],
         fig=lambda rng: S.electromagnet(turns=rng.choice([5, 8]))),
    dict(id="e13_overloading_explain", level=4, lo="13.5",
         stem="The table shows appliances plugged into one wall socket through an adaptor.\n\n| Appliance | Current / A |\n|---|---|\n| heater | 8 |\n| kettle | 9 |\n| iron | 5 |\n\nThe socket's wiring is rated for 13 A. Why is this dangerous?",
         correct="The total current (22 A) is far more than the wiring can carry, so the wires overheat and could start a fire.",
         wrongs={"The appliances will run too slowly.": "Overloading does not slow appliances; it overheats wires.", "The voltage will become too high.": "The supply voltage stays the same; it is the CURRENT that is too large.", "It is safe because each appliance is below 13 A.": "The currents ADD in the socket's wiring."},
         hints=["Add up the currents.", "Compare the total with 13 A.", "Too much current → heating effect in the wires."]),
    dict(id="e13_wet_hands_explain", level=4, lo="13.5",
         stem="Fig. 1 shows a plug. Why should you never handle plugs or switches with wet hands?",
         correct="Water on the skin conducts electricity more easily, so a current can pass through the body and cause a shock.",
         wrongs={"Water makes the plug rust.": "Rust is not the safety concern here.", "Wet hands slip and drop the plug.": "Dropping is not the main danger; electric shock is.", "Water increases the voltage of the supply.": "The supply voltage does not change."},
         hints=["Dry skin is a fairly poor conductor.", "What does water do to that?", "Better conductor → current through you."],
         fig=lambda rng: S.plug_wiring()),
    dict(id="e13_series_all_out", level=4, lo="13.1",
         stem="Fig. 1 shows three lamps in series. One lamp's filament breaks. Explain what happens to the other two lamps.",
         correct="They go out, because the broken filament leaves a gap and there is no longer a complete path for the current.",
         wrongs={"They become brighter, because they share the p.d. between two instead of three.": "No current can flow at all with a gap in the single loop.", "They stay the same, because each lamp has its own current.": "In series there is only one path; a break stops everything.", "Only the lamp next to the broken one goes out.": "The whole loop is broken, so every lamp goes out."},
         hints=["How many paths does the current have in a series circuit?", "A broken filament is like an open switch.", "Open circuit → no current anywhere."],
         fig=lambda rng: S.circuit(["lamp", "lamp", "lamp"], top=("cell",))),
    dict(id="e13_energy_label_choice", level=4, lo="13.6",
         stem="The table compares two refrigerators of the same size.\n\n| Model | Power rating | Energy label |\n|---|---|---|\n| P | 150 W | 2 ticks |\n| Q | 90 W | 4 ticks |\n\nWhich statement explains why Q is the better choice for saving electricity?",
         correct="Q converts less energy every second, so over a year it uses fewer kWh and costs less to run.",
         wrongs={"Q is better because higher power means more cooling.": "Q has LOWER power; it cools the same space using less energy.", "P is better because it works faster.": "A higher rating means more energy used, not better performance here.", "There is no difference because both are fridges.": "The power ratings differ, so the energy used differs."},
         hints=["Power = energy used per second.", "Lower power for the same job = less energy over time.", "More ticks = more efficient."]),

    # ------------------------------------------------------------ L5
    dict(id="e13_choose_appliance_lowest_cost", level=5, lo="13.7*",
         stem="The table shows two ways to cool a bedroom for 8 hours a night.\n\n| Option | Power | Cost to buy |\n|---|---|---|\n| air-conditioner | 1000 W | $800 |\n| fan | 60 W | $60 |\n\nElectricity costs $0.30 per kWh. Which statement is correct?",
         correct="The fan costs about $0.14 a night to run and the air-conditioner about $2.40, so the fan saves money every night as well as being cheaper to buy.",
         wrongs={"The air-conditioner is cheaper to run because it cools faster.": "It uses about 16 times the power, so it costs far more to run.", "Both cost the same to run because both run for 8 hours.": "Cost depends on power × time, and the powers are very different.", "The fan is more expensive overall because it must run longer.": "Both run for 8 hours in the question."},
         hints=["Energy per night = kW × 8 h for each option.", "Air-con: 1 kW × 8 h = 8 kWh. Fan: 0.06 × 8 = 0.48 kWh.", "Multiply each by $0.30 and compare."]),
    dict(id="e13_parallel_lamp_blows_predict", level=5, lo="13.2",
         stem="Fig. 1 shows lamps X and Y in parallel with an ammeter in the main circuit reading 0.8 A. Lamp Y's filament breaks. Predict the new readings.",
         correct="X stays lit at the same brightness; the ammeter reading falls to the current through X alone.",
         wrongs={"X goes out and the ammeter reads zero.": "X still has its own complete loop, so it stays lit.", "X becomes brighter and the ammeter reads more than 0.8 A.": "X's branch is unchanged; the total current FALLS because Y's branch has gone.", "Nothing changes.": "Y's current has stopped, so the main current falls."},
         hints=["Each parallel branch is independent.", "Y's branch is now open; X's branch is unchanged.", "Main current = sum of the branches that still work."],
         fig=lambda rng: S.circuit([], top=("cell", "ammeter"), parallel=[["lamp"], ["lamp"]], labels=["X", "Y"])),
    dict(id="e13_most_dangerous_scenario", level=5, lo="13.5",
         stem="The table lists four situations in a kitchen.\n\n| Situation | Detail |\n|---|---|\n| P | a toaster is unplugged after use |\n| Q | a kettle's cable has cracked insulation and is used near the sink |\n| R | a fridge is plugged into its own socket |\n| S | a lamp is switched off at the wall |\n\nWhich situation is the most dangerous, and why?",
         correct="Q: exposed live wire near water could give a fatal shock.",
         wrongs={"P: unplugging may spark.": "Unplugging after switching off is a safe practice.", "R: fridges use a lot of current.": "One appliance on its own socket is not an overload.", "S: switching off wastes electricity.": "Switching off saves electricity and is safe."},
         hints=["Look for damaged insulation and water together.", "Which row has BOTH?", "Exposed conductor + water = shock risk."]),
    dict(id="e13_circuit_design_evaluate", level=5, lo="13.1",
         stem="Fig. 1 shows a circuit for a bedroom with two lamps. A student wants each lamp to be controlled by its own switch and to stay at full brightness. Which design works?",
         correct="Lamps in parallel, with a switch in series with each lamp in its own branch.",
         wrongs={"Lamps in series with one switch for both.": "One switch controls both, and each lamp gets only half the p.d.", "Lamps in series with a switch beside each lamp.": "In series, opening either switch turns BOTH lamps off.", "Lamps in parallel with one switch in the main circuit.": "One switch in the main circuit controls both lamps together."},
         hints=["Independent control needs separate branches.", "Where must each switch go to affect only its own lamp?", "Parallel branches, one switch per branch."],
         fig=lambda rng: S.circuit([], top=("battery",), parallel=[["lamp", "switch_closed"], ["lamp", "switch_open"]])),
    dict(id="e13_uses_up_electricity_claim", level=5, lo="13.6",
         stem="The table shows two lamps.\n\n| Lamp | Power |\n|---|---|\n| P | 100 W |\n| Q | 40 W |\n\nA student says 'lamp P uses up more electricity'. Which is the most accurate scientific statement?",
         correct="Lamp P converts electrical energy to light and heat faster (100 J every second), so it uses more energy in the same time.",
         wrongs={"Lamp P destroys 100 J of electricity each second.": "Energy is never destroyed; it is converted to light and heat.", "Both lamps use the same energy because they are on the same supply.": "The same supply does not mean the same power; P converts energy 2.5 times as fast.", "Lamp Q uses more energy because it is on for longer.": "The question gives no times; compare the powers."},
         hints=["Power is the rate of converting energy.", "Energy is conserved: it changes form.", "100 W = 100 J per second converted."]),
]

register_explain(EXPLAIN, chapter=13)
