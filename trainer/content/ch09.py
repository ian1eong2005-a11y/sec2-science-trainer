"""Ch 9 Application of Forces and Transfer of Energy: 25 calculation / data templates and 25 explanation items.
lo codes: 9.1 forces, 9.2 mass and weight, 9.3 effects of forces, 9.4* pressure (G3), 9.5* work (G3), 9.6 energy, 9.7 energy sources.
A trailing * marks G3-only content."""
from .. import figs, sketches as S
from ..config import G
from .base import fmt, md_table, nice, numeric_options, pick, register_explain, template

PLANETS = [("the Moon", 1.6), ("Mars", 3.7), ("Mercury", 3.7), ("Venus", 8.9), ("Jupiter", 25), ("Neptune", 11), ("Saturn", 10.4)]


# ================================================================ CALCULATION / DATA
# ---------------------------------------------------------------- L1
@template("c9_weight_from_mass", chapter=9, level=1, lo="9.2")
def weight_from_mass(rng):
    m = nice(rng, 0.5, 1.2, 2.0, 2.5, 3.0, 4.0, 4.5, 6.0, 8.0)
    W = m * G
    opts, key, mis = numeric_options(rng, W, [
        (m, "That is the mass in kilograms. Weight is a force, found by multiplying the mass by g."),
        (m / G, "You divided by g. Weight = mass × g, so the number of newtons is larger than the number of kilograms."),
        (m + G, "You added 10. Weight is mass MULTIPLIED by the gravitational field strength."),
    ], unit="N")
    return dict(
        stem=f"A bag of rice has a mass of **{fmt(m)} kg**. The gravitational field strength on Earth is 10 N/kg. Fig. 1 shows the bag hanging from a spring balance. What is the weight of the bag?",
        figure=S.spring_balance(W, max_n=100 if W > 50 else 50, label="rice"),
        options=opts, key=key, misconceptions=mis,
        formula="weight = mass × gravitational field strength (W = m × g)",
        working=["W = m × g", f"= {fmt(m)} kg × 10 N/kg", f"= **{fmt(W)} N**"],
        hints=["Weight is the pull of gravity on an object. Which formula links weight, mass and g?",
               "On Earth every kilogram is pulled down with a force of 10 N. How many kilograms are there?",
               f"W = {fmt(m)} × 10. Multiply, and keep the unit N."],
    )


@template("c9_mass_from_weight", chapter=9, level=1, lo="9.2")
def mass_from_weight(rng):
    m = nice(rng, 0.4, 0.8, 1.5, 2.5, 3.0, 4.5, 5.0, 7.0)
    W = m * G
    opts, key, mis = numeric_options(rng, m, [
        (W, "That is the weight in newtons. Mass is found by dividing the weight by g."),
        (W * G, "You multiplied by g. To go from weight back to mass you must DIVIDE by g."),
        (W - G, "You subtracted 10. Weight = mass × g, so mass = weight ÷ g."),
    ], unit="kg")
    return dict(
        stem=f"Fig. 1 shows a stone hanging from a spring balance. The balance reads **{fmt(W)} N**. Taking g = 10 N/kg, what is the mass of the stone?",
        figure=S.spring_balance(W, max_n=100 if W > 50 else 50, label="stone"),
        options=opts, key=key, misconceptions=mis,
        formula="mass = weight ÷ gravitational field strength (m = W ÷ g)",
        working=["W = m × g, so m = W ÷ g", f"= {fmt(W)} N ÷ 10 N/kg", f"= **{fmt(m)} kg**"],
        hints=["The balance measures a force (weight). You want the mass. Which way round is the formula?",
               "Every 10 N of weight comes from 1 kg of mass. How many lots of 10 N are there?",
               f"m = {fmt(W)} ÷ 10."],
    )


@template("c9_read_spring_balance", chapter=9, level=1, lo="9.1")
def read_spring_balance(rng):
    max_n = nice(rng, 5, 10, 20)
    step = max_n / 50
    reading = round(rng.randint(8, 46) * step, 2)
    opts, key, mis = numeric_options(rng, reading, [
        (reading + step * 5, "You read the next labelled mark above the pointer. Read the mark that the pointer is level with."),
        (reading - step * 5, "You read the labelled mark below the pointer. Count the small divisions up to the pointer."),
        (reading * 2 if max_n != 20 else reading / 2, "Check the value of each small division: the scale goes from 0 to %g N in 50 divisions." % max_n),
    ], unit="N", dp=1 if step >= 0.1 else 2)
    return dict(
        stem="Fig. 1 shows a spring balance (force-meter) being used to measure the weight of a toy. What is the reading on the balance?",
        figure=S.spring_balance(reading, max_n=max_n, label="toy"),
        options=opts, key=key, misconceptions=mis,
        formula="reading = labelled mark below the pointer + (number of small divisions × value of one division)",
        working=[f"the scale runs from 0 to {max_n} N; each labelled mark is {fmt(max_n / 10)} N and each small division is {fmt(step)} N",
                 f"the pointer is level with **{fmt(reading)} N**"],
        hints=["First work out what one small division is worth: the whole scale is divided into 50 small divisions.",
               f"Each labelled mark is {fmt(max_n / 10)} N, so each small division is {fmt(step)} N.",
               "Start from the labelled mark just below the pointer and add one small division for each line up to the pointer."],
    )


@template("c9_pressure_simple", chapter=9, level=1, lo="9.4*")
def pressure_simple(rng):
    F = nice(rng, 20, 40, 60, 80, 120, 150, 200, 300)
    A = nice(rng, 0.5, 2, 4, 5, 10)
    P = F / A
    opts, key, mis = numeric_options(rng, P, [
        (F * A, "You multiplied. Pressure = force ÷ area: spreading a force over a bigger area gives a SMALLER pressure."),
        (A / F, "You divided the wrong way round. Pressure = force ÷ area."),
        (F, "That is just the force. Pressure tells you how much force acts on each square metre."),
    ], unit="Pa")
    return dict(
        stem=f"A box is placed on the floor. It presses down with a force of **{F} N** on an area of **{fmt(A)} m²**, as shown in Fig. 1. What is the pressure exerted by the box on the floor?",
        figure=S.block_area(A, 1, f"F = {F} N", unit="m"),
        options=opts, key=key, misconceptions=mis,
        formula="pressure = force ÷ area (P = F ÷ A); 1 Pa = 1 N/m²",
        working=["P = F ÷ A", f"= {F} N ÷ {fmt(A)} m²", f"= **{fmt(P)} Pa**"],
        hints=["Pressure is the force acting on each unit of area. Which operation shares the force out over the area?",
               "A bigger area means the same force is spread more thinly, so the pressure must get smaller as the area grows.",
               f"P = {F} ÷ {fmt(A)}. The unit N/m² is written Pa."],
    )


@template("c9_work_simple", chapter=9, level=1, lo="9.5*")
def work_simple(rng):
    F = nice(rng, 15, 20, 25, 40, 50, 60, 80)
    d = nice(rng, 2, 3, 4, 5, 6, 8, 10)
    W = F * d
    opts, key, mis = numeric_options(rng, W, [
        (F / d, "You divided. Work done = force × distance moved in the direction of the force."),
        (F + d, "You added the two numbers. Work done is the force MULTIPLIED by the distance."),
        (F, "That is only the force. Work is done because the force moves the box through a distance."),
    ], unit="J")
    return dict(
        stem=f"A student pushes a box along the floor with a steady horizontal force of **{F} N**, as shown in Fig. 1. The box moves **{d} m** in the direction of the force. How much work is done on the box?",
        figure=figs.force_diagram([(f"{F} N", "right", 1.6)], label_body="box"),
        options=opts, key=key, misconceptions=mis,
        formula="work done = force × distance moved in the direction of the force (W = F × d)",
        working=["W = F × d", f"= {F} N × {d} m", f"= **{fmt(W)} J**"],
        hints=["Work is done when a force makes something move in the direction of the force. Which two quantities multiply to give it?",
               "The unit of work is the joule. 1 J = 1 N × 1 m.",
               f"W = {F} × {d}."],
    )


# ---------------------------------------------------------------- L2
@template("c9_weight_other_planet", chapter=9, level=2, lo="9.2")
def weight_other_planet(rng):
    name, g = pick(rng, PLANETS[:5])
    m = nice(rng, 2, 5, 8, 10, 12, 15, 20, 25, 30, 50)
    W = m * g
    rows = [["Earth", "10"], ["the Moon", "1.6"], ["Mars", "3.7"], ["Venus", "8.9"], ["Jupiter", "25"]]
    opts, key, mis = numeric_options(rng, W, [
        (m * G, "That is the weight on Earth. On %s the gravitational field strength is different, so use the value from the table." % name),
        (m, "That is the mass. Mass does not change from place to place, but weight does: multiply by g."),
        (m / g if m / g != W else m / g + 1, "You divided by g. Weight = mass × g."),
    ], unit="N")
    return dict(
        stem=f"The table shows the gravitational field strength on some bodies in the Solar System.\n\n{md_table(['Body', 'g / N/kg'], rows)}\n\nA probe has a mass of **{m} kg**. What is its weight on **{name}**?",
        options=opts, key=key, misconceptions=mis,
        formula="weight = mass × gravitational field strength of that body",
        working=[f"g on {name} = {g} N/kg (from the table)", f"W = m × g = {m} kg × {g} N/kg", f"= **{fmt(W)} N**"],
        hints=["Weight depends on where the object is. Find the value of g for the right body in the table.",
               f"The mass stays {m} kg everywhere. Multiply it by the g for {name}.",
               f"W = {m} × {g}."],
    )


@template("c9_pressure_area_cm2", chapter=9, level=2, lo="9.4*")
def pressure_area_cm2(rng):
    F = nice(rng, 30, 50, 60, 100, 150, 200)
    A_cm2 = nice(rng, 20, 25, 40, 50, 100, 200, 250, 500)
    A = A_cm2 / 10000
    P = F / A
    opts, key, mis = numeric_options(rng, P, [
        (F / A_cm2, "That is the pressure in N/cm². The question asks for pascals, so the area must be in m² (1 m² = 10 000 cm²)."),
        (F / (A_cm2 / 100), "You used 1 m² = 100 cm². In fact 1 m = 100 cm, so 1 m² = 100 × 100 = 10 000 cm²."),
        (F * A, "You multiplied force by area. Pressure = force ÷ area."),
    ], unit="Pa")
    return dict(
        stem=f"A brick weighing **{F} N** rests on its largest face, which has an area of **{A_cm2} cm²**, as in Fig. 1. What is the pressure the brick exerts on the table, in **pascals**?",
        figure=S.block_area(A_cm2 // 10 if A_cm2 % 10 == 0 else A_cm2, 10 if A_cm2 % 10 == 0 else 1, f"W = {F} N"),
        options=opts, key=key, misconceptions=mis,
        formula="P = F ÷ A, with A in m² (divide cm² by 10 000)",
        working=[f"A = {A_cm2} cm² = {A_cm2} ÷ 10 000 m² = {fmt(A, sf=4)} m²", f"P = {F} ÷ {fmt(A, sf=4)}", f"= **{fmt(P)} Pa**"],
        hints=["A pascal is a newton per square METRE. Is the area given in square metres?",
               "1 m = 100 cm, so a square metre is 100 cm × 100 cm. How many cm² is that?",
               f"Divide {A_cm2} by 10 000 to get m², then P = {F} ÷ area."],
    )


@template("c9_pressure_rearranged", chapter=9, level=2, lo="9.4*")
def pressure_rearranged(rng):
    want = pick(rng, ["force", "area"])
    P = nice(rng, 200, 400, 500, 800, 1000, 1500, 2000)
    A = nice(rng, 0.2, 0.25, 0.4, 0.5, 2, 4)
    F = P * A
    if want == "force":
        opts, key, mis = numeric_options(rng, F, [
            (P / A, "You divided. Force = pressure × area (rearrange P = F ÷ A)."),
            (P + A, "You added. Multiply the pressure by the area to get the force."),
            (P, "That is the pressure. The force is the pressure multiplied by the area it acts on."),
        ], unit="N")
        stem = f"The table shows measurements for a container standing on a floor.\n\n{md_table(['Quantity', 'Value'], [['pressure on the floor', f'{P} Pa'], ['area of the base', f'{fmt(A)} m²']])}\n\nWhat is the force exerted by the container on the floor?"
        working = ["P = F ÷ A, so F = P × A", f"= {P} Pa × {fmt(A)} m²", f"= **{fmt(F)} N**"]
        hints = ["Start from P = F ÷ A. Which quantity do you want, and how do you make it the subject?",
                 "If a pressure of P acts on every square metre, the total force is P for each of the A square metres.",
                 f"F = {P} × {fmt(A)}."]
        formula = "force = pressure × area (F = P × A)"
    else:
        opts, key, mis = numeric_options(rng, A, [
            (F * P, "You multiplied. Area = force ÷ pressure."),
            (P / F, "You divided the wrong way round. Area = force ÷ pressure."),
            (F, "That is the force itself. Divide it by the pressure to find the area."),
        ], unit="m²")
        stem = f"The table shows measurements for a container standing on a floor.\n\n{md_table(['Quantity', 'Value'], [['force on the floor', f'{fmt(F)} N'], ['pressure on the floor', f'{P} Pa']])}\n\nWhat is the area of the base of the container?"
        working = ["P = F ÷ A, so A = F ÷ P", f"= {fmt(F)} N ÷ {P} Pa", f"= **{fmt(A)} m²**"]
        hints = ["Start from P = F ÷ A and make A the subject.",
                 "Pressure is force per square metre, so the number of square metres is force ÷ pressure.",
                 f"A = {fmt(F)} ÷ {P}."]
        formula = "area = force ÷ pressure (A = F ÷ P)"
    return dict(stem=stem, options=opts, key=key, misconceptions=mis, formula=formula, working=working, hints=hints)


@template("c9_turning_effect_table", chapter=9, level=2, lo="9.3")
def turning_effect_table(rng):
    forces = rng.sample([10, 15, 20, 25, 30, 40], 4)
    dists = rng.sample([0.2, 0.3, 0.4, 0.5, 0.6, 0.8], 4)
    rows = [[L, f"{F}", f"{fmt(d)}"] for L, F, d in zip("ABCD", forces, dists)]
    prods = [F * d for F, d in zip(forces, dists)]
    best = max(range(4), key=lambda i: prods[i])
    if sorted(prods)[-1] == sorted(prods)[-2]:
        dists[best] = dists[best] + 0.1
        rows[best][2] = fmt(dists[best])
        prods[best] = forces[best] * dists[best]
    correct = "ABCD"[best]
    options = {L: f"case {L}" for L in "ABCD"}
    mis = {}
    for i, L in enumerate("ABCD"):
        if L == correct:
            continue
        if forces[i] == max(forces):
            mis[L] = "This is the largest force, but it acts close to the pivot. Turning effect depends on the force AND how far from the pivot it acts."
        elif dists[i] == max(dists):
            mis[L] = "This force acts furthest from the pivot, but it is small. Compare force × distance for each case."
        else:
            mis[L] = f"Force × distance here is {fmt(prods[i])} N m, which is not the largest."
    return dict(
        stem=f"A student pushes a door at different places with different forces. The table shows the force and its distance from the hinge (pivot).\n\n{md_table(['Case', 'Force / N', 'Distance from hinge / m'], rows)}\n\nIn which case is the turning effect on the door the largest?",
        options=options, key=correct, misconceptions=mis,
        formula="turning effect increases with the force and with its distance from the pivot (compare force × distance)",
        working=[f"force × distance: " + ", ".join(f"{L} = {fmt(p)} N m" for L, p in zip("ABCD", prods)), f"the largest is **{correct}**"],
        hints=["A bigger force gives a bigger turning effect, but so does pushing further from the hinge. You need to consider both.",
               "Multiply each force by its distance from the hinge and compare the products.",
               "The case with the largest force × distance has the largest turning effect."],
    )


@template("c9_energy_conservation_sum", chapter=9, level=2, lo="9.6")
def energy_conservation_sum(rng):
    device, useful = pick(rng, [("lamp", "light"), ("electric fan", "kinetic"), ("loudspeaker", "sound"), ("electric motor", "kinetic")])
    E_in = nice(rng, 100, 200, 250, 400, 500, 1000)
    frac = nice(rng, 0.1, 0.2, 0.25, 0.4, 0.6, 0.75)
    E_use = E_in * frac
    E_waste = E_in - E_use
    opts, key, mis = numeric_options(rng, E_waste, [
        (E_in, "That is the total energy supplied. Some of it becomes useful energy, so the wasted part is less than this."),
        (E_use, f"That is the useful {useful} energy. The question asks how much is wasted as heat."),
        (E_in + E_use, "Energy cannot be created. The useful and wasted energy together must ADD UP TO the energy supplied."),
    ], unit="J")
    return dict(
        stem=f"Fig. 1 shows the energy conversion in a {device}. Every second it is supplied with **{E_in} J** of electrical energy and converts **{fmt(E_use)} J** of it into useful {useful} energy. The rest is wasted as heat. How much energy is wasted as heat every second?",
        figure=S.pie_chart([f"useful {useful} energy", "wasted heat"], [E_use, E_waste]),
        options=opts, key=key, misconceptions=mis,
        formula="energy supplied = useful energy + wasted energy (conservation of energy)",
        working=["energy supplied = useful + wasted", f"{E_in} = {fmt(E_use)} + wasted", f"wasted = {E_in} − {fmt(E_use)} = **{fmt(E_waste)} J**"],
        hints=["Energy cannot be created or destroyed. So what must the useful energy and the wasted energy add up to?",
               f"Total in = {E_in} J. Useful out = {fmt(E_use)} J. The rest is the wasted heat.",
               f"wasted = {E_in} − {fmt(E_use)}."],
    )


# ---------------------------------------------------------------- L3
@template("c9_pressure_block_from_mass", chapter=9, level=3, lo="9.4*")
def pressure_block_from_mass(rng):
    m = nice(rng, 2, 4, 5, 8, 10, 12, 20)
    a, b = pick(rng, [(20, 10), (25, 20), (40, 25), (50, 20), (40, 40), (50, 40), (10, 10)])
    A = a * b / 10000
    W = m * G
    P = W / A
    opts, key, mis = numeric_options(rng, P, [
        (m / A, "You used the mass instead of the weight. Pressure needs the FORCE in newtons: W = m × g first."),
        (W / (a * b), "That is in N/cm². Convert the area to m² (divide cm² by 10 000) to get pascals."),
        (W * A, "You multiplied the weight by the area. Pressure = force ÷ area."),
    ], unit="Pa")
    return dict(
        stem=f"A block of mass **{m} kg** rests on a table on the face shown in Fig. 1, which measures **{a} cm by {b} cm**. Taking g = 10 N/kg, what pressure does the block exert on the table?",
        figure=S.block_area(a, b, f"mass {m} kg"),
        options=opts, key=key, misconceptions=mis,
        formula="W = m × g, then P = W ÷ A with A in m²",
        working=[f"W = m × g = {m} × 10 = {fmt(W)} N", f"A = {a} cm × {b} cm = {a * b} cm² = {fmt(A, sf=4)} m²", f"P = {fmt(W)} ÷ {fmt(A, sf=4)} = **{fmt(P)} Pa**"],
        hints=["Two steps: first the force pressing down (its weight), then pressure = force ÷ area.",
               f"Weight = {m} kg × 10 N/kg. Area = {a} × {b} cm², and 10 000 cm² make 1 m².",
               f"P = ({m} × 10) ÷ ({a * b} ÷ 10 000)."],
    )


@template("c9_work_lifting", chapter=9, level=3, lo="9.5*")
def work_lifting(rng):
    m = nice(rng, 2, 3, 5, 8, 10, 12, 15, 20)
    h = nice(rng, 0.5, 1.2, 1.5, 2, 2.5, 3, 4)
    W = m * G
    work = W * h
    opts, key, mis = numeric_options(rng, work, [
        (m * h, "You used the mass instead of the force. The force needed to lift the box equals its WEIGHT, m × g."),
        (W, "That is the weight (the force). Work done = force × distance moved, so multiply by the height."),
        (W / h, "You divided by the height. Work done = force × distance."),
    ], unit="J")
    return dict(
        stem=f"A worker lifts a box of mass **{m} kg** straight up onto a shelf **{fmt(h)} m** high at a steady speed, as in Fig. 1. Taking g = 10 N/kg, how much work does the worker do on the box?",
        figure=figs.force_diagram([(f"lift", "up", 1.4), (f"weight", "down", 1.4)], label_body=f"{m} kg", ground=False),
        options=opts, key=key, misconceptions=mis,
        formula="force needed = weight = m × g; work done = force × distance moved (W = F × d)",
        working=[f"force needed = weight = {m} × 10 = {fmt(W)} N", f"work done = {fmt(W)} N × {fmt(h)} m", f"= **{fmt(work)} J**"],
        hints=["To lift the box at a steady speed the worker must pull up with a force equal to the box's weight. Find that force first.",
               f"Weight = {m} × 10 N. Then work done = force × distance moved upwards.",
               f"Work = ({m} × 10) × {fmt(h)}."],
    )


@template("c9_spring_extension_table", chapter=9, level=3, lo="9.1")
def spring_extension_table(rng):
    L0 = nice(rng, 10.0, 12.0, 15.0, 20.0)
    k = nice(rng, 0.5, 1.0, 1.5, 2.0, 2.5)           # cm per N
    loads = [0, 1, 2, 3]
    rows = [[f"{F}", fmt(L0 + k * F)] for F in loads]
    ask = nice(rng, 4, 5, 6, 8)
    ans = L0 + k * ask
    opts, key, mis = numeric_options(rng, ans, [
        (k * ask, "That is the EXTENSION for this load. The question asks for the total length: add the original length."),
        (L0 + k * (ask - 1), "Each extra newton stretches the spring by the same amount. Count the newtons from 0 N, not from the last row."),
        (L0 + k * ask * 2, "You doubled the extension. Find the extension for 1 N from the table, then multiply by the load."),
    ], unit="cm", dp=1)
    return dict(
        stem=f"A student hangs different loads on a spring and measures its length.\n\n{md_table(['Load / N', 'Length of spring / cm'], rows)}\n\nThe spring is not overstretched. What will its length be when the load is **{ask} N**?",
        options=opts, key=key, misconceptions=mis,
        formula="extension per newton = (length − original length) ÷ load; length = original length + extension",
        working=[f"original length (0 N) = {fmt(L0)} cm", f"each 1 N stretches the spring by {fmt(k)} cm", f"length at {ask} N = {fmt(L0)} + {ask} × {fmt(k)} = **{fmt(ans, dp=1)} cm**"],
        hints=["Look at how much the length increases each time the load goes up by 1 N. Is the pattern steady?",
               f"The length rises by the same amount for each newton. Work out that amount, then apply it {ask} times from the 0 N length.",
               f"length = {fmt(L0)} + {ask} × (extension for 1 N)."],
    )


@template("c9_bounce_energy_fraction", chapter=9, level=3, lo="9.6")
def bounce_energy_fraction(rng):
    h0 = nice(rng, 100, 120, 150, 200, 250)
    frac = nice(rng, 0.5, 0.6, 0.64, 0.7, 0.75, 0.8)
    h1 = round(h0 * frac)
    E0 = nice(rng, 2.0, 4.0, 5.0, 8.0, 10.0)
    E_lost = E0 * (1 - h1 / h0)
    opts, key, mis = numeric_options(rng, E_lost, [
        (E0 * h1 / h0, "That is the energy the ball still has at the top of its bounce. The question asks how much was converted to heat and sound."),
        (E0, "That is all the energy the ball started with. Only part of it is lost; the ball still rises after the bounce."),
        (E0 * h1 / 100 if h0 != 100 else E0 * 0.1, "Compare the bounce height with the DROP height, not with 100 cm."),
    ], unit="J", sf=3)
    return dict(
        stem=f"A ball is dropped from a height of **{h0} cm** and bounces back to **{h1} cm**, as in Fig. 1. At the moment it is released the ball has **{fmt(E0)} J** of energy. The energy of the ball at a given height is proportional to that height. How much energy was converted to heat and sound during the bounce?",
        figure=S.bounce([h0, h1]),
        options=opts, key=key, misconceptions=mis,
        formula="energy remaining ∝ height; energy lost = initial energy × (drop height − bounce height) ÷ drop height",
        working=[f"fraction of height lost = ({h0} − {h1}) ÷ {h0} = {fmt((h0 - h1) / h0)}", f"energy lost = {fmt((h0 - h1) / h0)} × {fmt(E0)} J", f"= **{fmt(E_lost)} J**"],
        hints=["Energy is conserved: the energy 'missing' at the top of the bounce became heat and sound. How much of the height was lost?",
               f"The ball lost {h0 - h1} cm out of {h0} cm. The same fraction of its energy was lost.",
               f"energy lost = ({h0} − {h1}) ÷ {h0} × {fmt(E0)}."],
    )


@template("c9_pressure_skis_vs_boots", chapter=9, level=3, lo="9.4*")
def pressure_skis_vs_boots(rng):
    W = nice(rng, 400, 500, 600, 700, 800)
    boots = nice(rng, 0.04, 0.05, 0.08, 0.1)
    skis = nice(rng, 0.4, 0.5, 0.8, 1.0)
    P_b, P_s = W / boots, W / skis
    which = pick(rng, ["boots", "skis"])
    P = P_b if which == "boots" else P_s
    other = P_s if which == "boots" else P_b
    opts, key, mis = numeric_options(rng, P, [
        (other, f"That is the pressure on the {'skis' if which == 'boots' else 'boots'}. Read the question again: it asks about the {which}."),
        (W * (boots if which == "boots" else skis), "You multiplied weight by area. Pressure = force ÷ area."),
        (P / 2, "The weight is spread over BOTH feet, and the table gives the total area of both, so do not halve again."),
    ], unit="Pa")
    return dict(
        stem=f"A skier weighs **{W} N**.\n\n{md_table(['Standing on', 'Total area in contact with the snow / m²'], [['two boots', fmt(boots)], ['two skis', fmt(skis)]])}\n\nWhat pressure does the skier exert on the snow when standing on the **{which}**?",
        options=opts, key=key, misconceptions=mis,
        formula="P = F ÷ A, using the total area in contact",
        working=[f"P = W ÷ A = {W} ÷ {fmt(boots if which == 'boots' else skis)}", f"= **{fmt(P)} Pa**",
                 f"(on the {'skis' if which == 'boots' else 'boots'} it would be {fmt(other)} Pa: the larger area gives the smaller pressure)"],
        hints=["Pressure = force ÷ area. The force is the skier's weight. Which area row do you need?",
               f"Pick the area for the {which} from the table; it is already the total for both feet.",
               f"P = {W} ÷ {fmt(boots if which == 'boots' else skis)}."],
    )


# ---------------------------------------------------------------- L4
@template("c9_graph_extension_load", chapter=9, level=4, lo="9.1")
def graph_extension_load(rng):
    k = nice(rng, 0.5, 1.0, 1.5, 2.0)          # cm per N
    Fmax = 10
    pts = [(0, 0), (Fmax, k * Fmax)]
    ymax = k * Fmax
    ask_ext = nice(rng, *[k * F for F in (2, 3, 4, 6, 7, 8)])
    ans = ask_ext / k
    opts, key, mis = numeric_options(rng, ans, [
        (ask_ext, "You read off the extension itself. The question asks for the LOAD that produces this extension: go across to the line, then down to the load axis."),
        (ask_ext * k, "You multiplied instead of reading the graph. Find the extension on the vertical axis, move across to the line and read the load below."),
        (ans + 1, "You misread the load scale by one division. Check the value of each small square."),
    ], unit="N", sf=3)
    return dict(
        stem=f"Fig. 1 shows how the extension of a spring changes with the load hung on it. What load produces an extension of **{fmt(ask_ext)} cm**?",
        figure=figs.graph(pts, Fmax, ymax, 2, ymax / 5, xlabel="load / N", ylabel="extension / cm"),
        options=opts, key=key, misconceptions=mis,
        formula="read the graph: find the extension on the y-axis, go across to the line, then down to the load on the x-axis",
        working=[f"from the graph, each 1 N gives an extension of {fmt(k)} cm", f"extension of {fmt(ask_ext)} cm ↔ load = {fmt(ask_ext)} ÷ {fmt(k)} = **{fmt(ans)} N**"],
        hints=["Which axis shows extension? Start there with the given value.",
               "Move horizontally until you meet the line, then straight down to the load axis.",
               f"Alternatively: the line shows {fmt(k)} cm for every newton, so load = {fmt(ask_ext)} ÷ {fmt(k)}."],
    )


@template("c9_bar_chart_weight_planets", chapter=9, level=4, lo="9.2")
def bar_chart_weight_planets(rng):
    m = nice(rng, 2, 4, 5, 10, 20)
    chosen = rng.sample(PLANETS[:5], 3)
    names = ["Earth"] + [c[0].replace("the ", "") for c in chosen]
    gs = [10] + [c[1] for c in chosen]
    weights = [m * g for g in gs]
    ask_i = rng.randint(1, 3)
    ans = gs[ask_i]
    ymax = max(weights) * 1.2
    ystep = 10 if ymax <= 60 else (50 if ymax <= 300 else 100)
    ymax = ystep * (int(ymax / ystep) + 1)
    opts, key, mis = numeric_options(rng, ans, [
        (weights[ask_i], f"That is the WEIGHT on {names[ask_i]}, read from the bar. The gravitational field strength is weight ÷ mass."),
        (weights[ask_i] * m, "You multiplied weight by mass. g = weight ÷ mass."),
        (m / weights[ask_i] if m / weights[ask_i] != ans else ans * 2, "You divided the wrong way round. g = weight ÷ mass, in N/kg."),
    ], unit="N/kg", sf=3)
    return dict(
        stem=f"Fig. 1 shows the weight of the same **{m} kg** object on different bodies in the Solar System. What is the gravitational field strength on **{names[ask_i]}**?",
        figure=S.bar_chart(names, weights, "weight / N", ymax=ymax, ystep=ystep),
        options=opts, key=key, misconceptions=mis,
        formula="gravitational field strength = weight ÷ mass (g = W ÷ m)",
        working=[f"weight on {names[ask_i]} (from the bar) = {fmt(weights[ask_i])} N", f"g = W ÷ m = {fmt(weights[ask_i])} ÷ {m}", f"= **{fmt(ans)} N/kg**"],
        hints=[f"Read the height of the bar for {names[ask_i]}: that is the weight of the object there.",
               "g is the weight of EACH kilogram. You know the weight and the mass of the object.",
               f"g = (bar height) ÷ {m}."],
    )


@template("c9_energy_pie_chart", chapter=9, level=4, lo="9.6")
def energy_pie_chart(rng):
    device, useful = pick(rng, [("filament lamp", "light"), ("electric kettle", "heat in the water"), ("motor", "kinetic"), ("LED lamp", "light")])
    pct_useful = nice(rng, 10, 20, 25, 40, 60, 75, 80, 90)
    E_in = nice(rng, 200, 500, 800, 1000, 2000, 5000)
    ans = E_in * pct_useful / 100
    other = 100 - pct_useful
    opts, key, mis = numeric_options(rng, ans, [
        (E_in * other / 100, f"That is the wasted energy ({other}%). The question asks for the useful {useful} energy."),
        (pct_useful, "That is the percentage, not an energy. Find that percentage OF the energy supplied."),
        (E_in, "That is all the energy supplied. Only the useful share becomes " + useful + " energy."),
    ], unit="J", sf=3)
    return dict(
        stem=f"Fig. 1 shows what happens to the energy supplied to a {device}: **{pct_useful}%** becomes useful {useful} energy and the rest is wasted. If **{E_in} J** of electrical energy is supplied, how much useful {useful} energy is produced?",
        figure=S.pie_chart([f"useful {useful} ({pct_useful}%)", f"wasted ({other}%)"], [pct_useful, other]),
        options=opts, key=key, misconceptions=mis,
        formula="useful energy = percentage useful ÷ 100 × energy supplied",
        working=[f"useful energy = {pct_useful}% of {E_in} J", f"= {pct_useful} ÷ 100 × {E_in}", f"= **{fmt(ans)} J**"],
        hints=["The pie chart shares the total energy out. Which slice is the useful one, and what percentage is it?",
               f"{pct_useful}% means {pct_useful} out of every 100 J. The total supplied is {E_in} J.",
               f"useful = {pct_useful}/100 × {E_in}."],
    )


@template("c9_graph_pressure_depth", chapter=9, level=4, lo="9.4*")
def graph_pressure_depth(rng):
    rate = nice(rng, 8, 10, 12)                  # kPa per metre (approx water with g = 10 → 10 kPa/m)
    depth_max = 10
    pts = [(0, 0), (depth_max, rate * depth_max)]
    ask = nice(rng, 2, 3, 4, 5, 6, 7, 8)
    ans = rate * ask
    opts, key, mis = numeric_options(rng, ans, [
        (rate * (ask + 1), "You read one division too far along the depth axis. Check the depth value carefully."),
        (ask, "That is the depth, not the pressure. Go up from the depth to the line, then across to the pressure axis."),
        (rate * depth_max, "That is the pressure at the bottom of the graph (10 m), not at the depth asked for."),
    ], unit="kPa", sf=3)
    return dict(
        stem=f"Fig. 1 shows how the pressure due to the water in a reservoir changes with depth below the surface. What is the pressure due to the water at a depth of **{ask} m**?",
        figure=figs.graph(pts, depth_max, rate * depth_max, 2, rate * 2, xlabel="depth / m", ylabel="pressure / kPa"),
        options=opts, key=key, misconceptions=mis,
        formula="read the graph: depth on the x-axis → up to the line → across to the pressure axis",
        working=[f"the graph is a straight line: pressure rises by {rate} kPa for every metre of depth", f"at {ask} m, pressure = {ask} × {rate} = **{fmt(ans)} kPa**"],
        hints=["Liquid pressure increases with depth. Start at the given depth on the horizontal axis.",
               "Go straight up to the line, then straight across to read the pressure.",
               f"Check: the line rises {rate} kPa per metre, so at {ask} m it is {ask} × {rate}."],
    )


@template("c9_work_total_distance", chapter=9, level=4, lo="9.5*")
def work_total_distance(rng):
    F = nice(rng, 20, 25, 30, 40, 50)
    legs = [nice(rng, 2, 3, 4, 5), nice(rng, 3, 4, 6, 8), nice(rng, 1, 2, 5, 7)]
    total = sum(legs)
    work = F * total
    rows = [[f"{i + 1}", f"{d}"] for i, d in enumerate(legs)]
    opts, key, mis = numeric_options(rng, work, [
        (F * legs[0], "That is the work done on the first leg only. Work is done on every leg, so use the total distance."),
        (F * total * 3, "You multiplied by the number of legs as well. Add the distances, then multiply by the force once."),
        (F + total, "You added force and distance. Work done = force × total distance."),
    ], unit="J", sf=4)
    return dict(
        stem=f"A sledge is pulled along flat snow with a steady horizontal force of **{F} N** in three stages.\n\n{md_table(['Stage', 'Distance pulled / m'], rows)}\n\nWhat is the total work done on the sledge?",
        options=opts, key=key, misconceptions=mis,
        formula="total work done = force × total distance moved in the direction of the force",
        working=[f"total distance = {' + '.join(str(d) for d in legs)} = {total} m", f"work done = {F} N × {total} m", f"= **{fmt(work, sf=4)} J**"],
        hints=["The force is the same in every stage, so you can add the distances first.",
               f"Total distance = {' + '.join(str(d) for d in legs)} m.",
               f"Work = {F} × (total distance)."],
    )


# ---------------------------------------------------------------- L5
@template("c9_pressure_two_conversions", chapter=9, level=5, lo="9.4*")
def pressure_two_conversions(rng):
    m = nice(rng, 1.5, 2.5, 4, 6, 7.5)
    a, b = pick(rng, [(5, 4), (8, 5), (10, 5), (12, 10), (15, 8), (20, 5)])
    A_cm2 = a * b
    A = A_cm2 / 10000
    W = m * G
    P = W / A
    opts, key, mis = numeric_options(rng, P, [
        (W / A_cm2, "That is N/cm². The pascal is N/m², so divide the area in cm² by 10 000 first."),
        (m / A, "You used the mass in kg instead of the weight in N. Force = m × g."),
        (W / (A_cm2 / 100), "1 m² is 10 000 cm², not 100 cm² (100 cm × 100 cm)."),
    ], unit="Pa", sf=3)
    return dict(
        stem=f"A vase of mass **{fmt(m)} kg** stands on a table on a base measuring **{a} cm × {b} cm**, as shown in Fig. 1. Taking g = 10 N/kg, what pressure does the vase exert on the table?",
        figure=S.block_area(a, b, f"mass {fmt(m)} kg"),
        options=opts, key=key, misconceptions=mis,
        formula="W = m × g; A (m²) = A (cm²) ÷ 10 000; P = W ÷ A",
        working=[f"W = {fmt(m)} × 10 = {fmt(W)} N", f"A = {a} × {b} = {A_cm2} cm² = {fmt(A, sf=4)} m²", f"P = {fmt(W)} ÷ {fmt(A, sf=4)} = **{fmt(P)} Pa**"],
        hints=["Three things to sort out: the force (not the mass), the area in m², then P = F ÷ A.",
               f"Weight = {fmt(m)} × 10. Area = {a} × {b} cm², and there are 10 000 cm² in 1 m².",
               f"P = ({fmt(m)} × 10) ÷ ({A_cm2} ÷ 10 000)."],
    )


@template("c9_pressure_max_min_faces", chapter=9, level=5, lo="9.4*")
def pressure_max_min_faces(rng):
    dims = pick(rng, [(2, 4, 5), (2, 5, 10), (4, 5, 10), (5, 10, 20), (2, 10, 20), (3, 6, 8)])
    a, b, c = dims
    W = nice(rng, 20, 40, 60, 80, 120)
    faces = sorted([a * b, a * c, b * c])
    want = pick(rng, ["largest", "smallest"])
    A = faces[0] if want == "largest" else faces[2]
    P = W / (A / 10000)
    other = W / (faces[2 if want == "largest" else 0] / 10000)
    mid = W / (faces[1] / 10000)
    opts, key, mis = numeric_options(rng, P, [
        (other, f"That is the {'smallest' if want == 'largest' else 'largest'} pressure: you used the {'largest' if want == 'largest' else 'smallest'} face. The {want} pressure comes from the {'smallest' if want == 'largest' else 'largest'} face."),
        (mid, "You used the middle-sized face. Compare all three faces: the smallest area gives the largest pressure."),
        (W / A, "That is in N/cm². Convert the area to m² for pascals."),
    ], unit="Pa", sf=3)
    return dict(
        stem=f"A block has sides of **{a} cm, {b} cm and {c} cm** (Fig. 1) and weighs **{W} N**. It can rest on any of its faces. What is the **{want}** pressure it can exert on the table?",
        figure=figs.labelled_block(a, b, c),
        options=opts, key=key, misconceptions=mis,
        formula="P = F ÷ A: the smallest face gives the largest pressure, the largest face the smallest pressure",
        working=[f"face areas: {a}×{b} = {a * b} cm², {a}×{c} = {a * c} cm², {b}×{c} = {b * c} cm²", f"the {want} pressure uses the {'smallest' if want == 'largest' else 'largest'} face, {A} cm² = {fmt(A / 10000, sf=4)} m²", f"P = {W} ÷ {fmt(A / 10000, sf=4)} = **{fmt(P)} Pa**"],
        hints=["Work out the area of each of the three different faces first.",
               f"The same weight on a smaller face gives a bigger pressure. For the {want} pressure, which face should it stand on?",
               f"P = {W} ÷ (that area in m²). Remember 10 000 cm² = 1 m²."],
    )


@template("c9_energy_two_stage_losses", chapter=9, level=5, lo="9.6")
def energy_two_stage_losses(rng):
    E_in = nice(rng, 1000, 2000, 4000, 5000, 8000)
    loss1 = nice(rng, 20, 25, 40, 50)
    loss2 = nice(rng, 10, 20, 25, 50)
    E1 = E_in * (100 - loss1) / 100
    E2 = E1 * (100 - loss2) / 100
    opts, key, mis = numeric_options(rng, E2, [
        (E_in * (100 - loss1 - loss2) / 100, f"You subtracted the two percentages ({loss1}% + {loss2}%). The second loss is {loss2}% of what is LEFT after the first stage, not of the original."),
        (E1, f"That is the energy after the first stage only. Another {loss2}% is lost in the second stage."),
        (E_in * loss1 / 100 * loss2 / 100, "You multiplied the two LOSS fractions. Work with the fractions that remain after each stage."),
    ], unit="J", sf=3)
    return dict(
        stem=f"Fig. 1 shows energy passing through a two-stage machine. **{E_in} J** of electrical energy goes into stage 1, which loses **{loss1}%** as heat. Stage 2 then loses **{loss2}%** of the energy it receives as heat and sound. How much useful energy comes out of stage 2?",
        figure=S.energy_arrows(["input", "after stage 1", "useful output"], [E_in, E1, E2]),
        options=opts, key=key, misconceptions=mis,
        formula="energy remaining after a stage = energy in × (100 − % lost) ÷ 100, applied stage by stage",
        working=[f"after stage 1: {E_in} × {100 - loss1}/100 = {fmt(E1)} J", f"after stage 2: {fmt(E1)} × {100 - loss2}/100 = **{fmt(E2)} J**"],
        hints=["Take the stages one at a time. After stage 1, what percentage of the energy is still there?",
               f"Stage 1 keeps {100 - loss1}% of {E_in} J. Stage 2 then keeps {100 - loss2}% of THAT amount.",
               f"output = {E_in} × {100 - loss1}/100 × {100 - loss2}/100."],
    )


@template("c9_weight_earth_to_planet", chapter=9, level=5, lo="9.2")
def weight_earth_to_planet(rng):
    name, g = pick(rng, PLANETS[:5])
    m = nice(rng, 3, 6, 12, 15, 24, 30, 45)
    W_e = m * G
    W_p = m * g
    opts, key, mis = numeric_options(rng, W_p, [
        (W_e * g, f"You multiplied the Earth WEIGHT by g. First find the mass (Earth weight ÷ 10), then multiply by g on {name}."),
        (W_e, f"The weight changes when g changes. {name} has g = {g} N/kg, not 10 N/kg."),
        (m, "That is the mass in kg. The question asks for the weight in newtons."),
    ], unit="N", sf=3)
    return dict(
        stem=f"A rover weighs **{fmt(W_e)} N** on Earth, where g = 10 N/kg.\n\n{md_table(['Body', 'g / N/kg'], [['Earth', '10'], [name.capitalize() if not name.startswith('the') else name, f'{g}']])}\n\nWhat would the rover weigh on **{name}**?",
        options=opts, key=key, misconceptions=mis,
        formula="mass = Earth weight ÷ 10; weight elsewhere = mass × g there",
        working=[f"mass = {fmt(W_e)} ÷ 10 = {m} kg (mass is the same everywhere)", f"weight on {name} = {m} × {g}", f"= **{fmt(W_p)} N**"],
        hints=["You are given a weight, not a mass. What quantity stays the same when the rover travels to another planet?",
               f"Find the mass from the Earth weight: m = W ÷ 10. Then use g for {name}.",
               f"W = ({fmt(W_e)} ÷ 10) × {g}."],
    )


@template("c9_work_or_no_work_table", chapter=9, level=5, lo="9.5*")
def work_or_no_work_table(rng):
    F1, d1 = nice(rng, 50, 60, 80), nice(rng, 2, 3, 4)
    F2, d2 = nice(rng, 20, 25, 30), nice(rng, 6, 8, 10)
    F3 = nice(rng, 300, 400, 500)
    F4, d4 = nice(rng, 100, 150, 200), nice(rng, 1, 1.5, 2)
    acts = [("pushes a trolley", F1, d1, F1 * d1), ("pulls a sledge", F2, d2, F2 * d2), ("holds a heavy box still", F3, 0, 0), ("lifts a crate", F4, d4, F4 * d4)]
    rng.shuffle(acts)
    rows = [[L, a[0], f"{a[1]}", f"{fmt(a[2])}"] for L, a in zip("ABCD", acts)]
    works = [a[3] for a in acts]
    best = max(range(4), key=lambda i: works[i])
    if works.count(works[best]) > 1:
        acts[best] = (acts[best][0], acts[best][1], acts[best][2] + 1, acts[best][1] * (acts[best][2] + 1))
        rows[best][3] = fmt(acts[best][2])
        works[best] = acts[best][3]
    correct = "ABCD"[best]
    mis = {}
    for i, L in enumerate("ABCD"):
        if L == correct:
            continue
        if acts[i][2] == 0:
            mis[L] = "This is the biggest force, but the box does not move. No movement in the direction of the force means NO work is done."
        else:
            mis[L] = f"Work done here is {acts[i][1]} × {fmt(acts[i][2])} = {fmt(acts[i][3])} J, which is less than the largest value."
    return dict(
        stem=f"Four students each apply a force. The table shows the force and the distance the object moves in the direction of that force.\n\n{md_table(['Student', 'Action', 'Force / N', 'Distance moved / m'], rows)}\n\nWhich student does the **most work**?",
        options={L: f"student {L}" for L in "ABCD"}, key=correct, misconceptions=mis,
        formula="work done = force × distance moved in the direction of the force; no movement → no work",
        working=["work done: " + ", ".join(f"{L} = {fmt(w)} J" for L, w in zip("ABCD", works)), f"the most work is done by **{correct}**"],
        hints=["Work done = force × distance moved. A large force on its own is not enough.",
               "One student's object does not move at all. How much work is done there?",
               "Multiply force by distance for each row and pick the largest product."],
    )


# ================================================================ EXPLANATION
EXPLAIN = [
    # ------------------------------------------------------------ L1 recall
    dict(id="e9_force_definition", level=1, lo="9.1",
         stem="Fig. 1 shows a force-meter. A force is best described as",
         correct="a push or a pull, measured in newtons",
         wrongs={"a type of energy, measured in joules": "Energy is measured in joules. A force is not energy; it is a push or a pull.",
                 "the amount of matter in an object": "That is mass, measured in kilograms.",
                 "the speed of a moving object": "Speed describes motion. A force is what can CHANGE the motion."},
         hints=["Think of what you do when you open a door or kick a ball.", "The instrument in Fig. 1 is a spring balance; what unit is marked on its scale?", "A force is a push or a ____, measured in ____."],
         fig=lambda rng: S.spring_balance(4.0, max_n=10)),
    dict(id="e9_si_unit_energy", level=1, lo="9.6",
         stem="Fig. 1 shows an energy conversion in a torch. What is the SI unit of energy?",
         correct="joule (J)",
         wrongs={"newton (N)": "The newton is the unit of force.", "watt (W)": "The watt is the unit of power (energy per second).", "kilogram (kg)": "The kilogram is the unit of mass."},
         hints=["Energy and work share the same unit.", "It is not the unit of force, mass or power.", "The unit is named after the scientist James ____."],
         fig=lambda rng: S.flow_boxes(["chemical energy\nin the cell", "electrical\nenergy", "light + heat\nenergy"])),
    dict(id="e9_non_contact_force", level=1, lo="9.1",
         stem="Fig. 1 shows two magnets near each other. Which of the following is a **non-contact** force?",
         correct="magnetic force",
         wrongs={"friction": "Friction only acts between surfaces that are touching.", "air resistance": "Air resistance needs the air to touch the moving object.",
                 "elastic force in a stretched spring": "The spring must be attached to the object it pulls."},
         hints=["A non-contact force can act across a gap, without the two objects touching.", "Friction, air resistance and elastic force all need something touching the object.", "The force between the two magnets in Fig. 1 acts across the gap. What kind of force is it?"],
         fig=lambda rng: S.magnets([("N", "S")])),
    dict(id="e9_mass_definition", level=1, lo="9.2",
         stem="Fig. 1 shows a stone on an electronic balance. The **mass** of the stone is",
         correct="the amount of matter in it",
         wrongs={"the pull of gravity on it": "That is its weight, a force measured in newtons.", "the space it takes up": "That is its volume.",
                 "the force it exerts on the balance": "That force is its weight. The balance converts it to a mass reading in grams."},
         hints=["Mass is the same on the Earth and on the Moon. Which option would not change if the stone were moved?", "Weight is a force (newtons); volume is space (cm³).", "Mass is the amount of ____ in an object."],
         fig=lambda rng: S.balance("stone", None, reading=f"{rng.choice([120, 250, 365, 480]):.1f} g")),
    dict(id="e9_conservation_statement", level=1, lo="9.6",
         stem="Fig. 1 shows the energy conversion in an electric fan. Which statement is the principle of conservation of energy?",
         correct="Energy cannot be created or destroyed; it can only be converted from one form to another.",
         wrongs={"Energy is used up when a device is switched on.": "Energy is never used up. It is converted to other forms, some of them wasted as heat.",
                 "The useful energy from a device is always more than the energy supplied.": "The useful energy can never be MORE than the energy supplied.",
                 "Energy can be created by machines such as motors.": "Machines convert energy; they never create it."},
         hints=["The word 'conservation' means the total stays the same.", "A device can only change the FORM of energy. It cannot make new energy or get rid of any.", "Energy cannot be ____ or destroyed."],
         fig=lambda rng: S.flow_boxes(["electrical\nenergy", "kinetic energy\n+ heat + sound"])),

    # ------------------------------------------------------------ L2 identify / classify
    dict(id="e9_classify_force_example", level=2, lo="9.1",
         hints=["Ask: must the two objects touch for this force to act?", "Gravitational and magnetic forces act at a distance; all the others need contact.", "Decide whether the named force is contact or non-contact and whether it matches the description."],
         fig=lambda rng: figs.force_diagram([("push", "right", 1.4), ("friction", "left", 1.0)], label_body="box"),
         variants=[
             dict(stem="Fig. 1 shows a box being pushed along a rough floor. Which force in this situation is a **contact** force?",
                  correct="the friction between the box and the floor",
                  wrongs={"the gravitational force on the box": "Gravity acts on the box without touching it: a non-contact force.",
                          "the magnetic force of the Earth on the box": "Magnetic forces are non-contact forces (and the box is not magnetic).",
                          "the pull of the Moon on the box": "That is a gravitational (non-contact) force."}),
             dict(stem="Fig. 1 shows a box on a floor. Which of the following forces acting on the box is a **non-contact** force?",
                  correct="its weight",
                  wrongs={"the friction from the floor": "Friction acts only where the box touches the floor: a contact force.",
                          "the push from the student's hands": "A push needs the hands to touch the box.",
                          "the support (normal) force from the floor": "The floor must touch the box to push up on it."}),
             dict(stem="Fig. 1 shows a box sliding across a floor and slowing down. The force that slows it is",
                  correct="friction, a contact force that opposes motion",
                  wrongs={"gravity, a non-contact force pulling it backwards": "Gravity pulls DOWN, not backwards, and the floor stops the box falling.",
                          "magnetic force from the floor": "Floors are not magnets. The slowing force comes from the surfaces rubbing.",
                          "air resistance, the only force acting": "Air resistance is small here; the main slowing force is between the box and the floor."}),
         ]),
    dict(id="e9_effect_of_force", level=2, lo="9.3",
         hints=["Forces can change an object's motion, its shape or size, or make it turn.", "Does the object start/stop/change direction, change shape, or rotate about a pivot?", "Match the description to one of the three effects."],
         fig=lambda rng: S.lever(0.15, ("nut", 0.1), ("push", 0.9)),
         variants=[
             dict(stem="Fig. 1 shows a spanner turning a nut. The effect of the force applied to the spanner is mainly to",
                  correct="produce a turning effect about the nut",
                  wrongs={"change the shape of the spanner": "A spanner is rigid; the force does not squash or stretch it noticeably.",
                          "change the mass of the nut": "Forces never change mass.",
                          "stop the nut moving": "The nut is already at rest; the force makes it rotate."}),
             dict(stem="A footballer kicks a ball that is rolling towards her, and it flies off in a different direction. Fig. 1 shows a lever for comparison. The main effect of her kick on the ball is to",
                  correct="change the direction of its motion",
                  wrongs={"change its mass": "Forces never change mass.",
                          "produce a turning effect about a pivot": "The ball is not fixed at a pivot; its whole motion changes.",
                          "make it permanently larger": "A ball may be squashed for a moment, but it is not made permanently larger."}),
             dict(stem="A student squeezes a lump of modelling clay in her hand. Fig. 1 shows a lever for comparison. The effect of the force on the clay is to",
                  correct="change its shape",
                  wrongs={"change its mass": "The amount of clay is unchanged.",
                          "make it move faster": "The clay stays in her hand; its motion does not change.",
                          "produce a turning effect": "There is no pivot; the clay is simply squashed."}),
         ]),
    dict(id="e9_mass_vs_weight_statement", level=2, lo="9.2",
         stem="The table compares mass and weight.\n\n| | Mass | Weight |\n|---|---|---|\n| SI unit | kilogram | newton |\n| Changes with location? | no | yes |\n\nWhich statement is correct?",
         correct="Weight is a force, so it is measured in newtons.",
         wrongs={"Mass is a force, so it is measured in newtons.": "Mass is the amount of matter, in kilograms. The table shows weight in newtons.",
                 "Mass becomes smaller on the Moon.": "Mass is the same everywhere; it is weight that is smaller on the Moon.",
                 "Weight is measured with a beam balance.": "A beam balance compares masses. Weight is measured with a spring balance (force-meter)."},
         hints=["Read the unit row of the table: which quantity is in newtons?", "A quantity in newtons must be a force.", "Weight is the pull of gravity, so it is a ____."]),
    dict(id="e9_renewable_classify", level=2, lo="9.7",
         hints=["Renewable sources will not run out because they are replaced naturally.", "Coal, oil and natural gas took millions of years to form and are being used up.", "Which option is replaced naturally within a human lifetime?"],
         variants=[
             dict(stem="The table lists some energy sources.\n\n| Source | Will it run out? |\n|---|---|\n| coal | yes |\n| natural gas | yes |\n| solar | no |\n| oil | yes |\n\nWhich source is **renewable**?",
                  correct="solar",
                  wrongs={"coal": "Coal is a fossil fuel. Once burnt it is not replaced.", "natural gas": "Natural gas is a fossil fuel and non-renewable.", "oil": "Oil is a fossil fuel and non-renewable."}),
             dict(stem="The table lists some energy sources.\n\n| Source | Will it run out? |\n|---|---|\n| wind | no |\n| hydro (falling water) | no |\n| coal | yes |\n| solar | no |\n\nWhich source is **non-renewable**?",
                  correct="coal",
                  wrongs={"wind": "Wind keeps blowing; it is renewable.", "hydro (falling water)": "Rain refills rivers and dams; hydro is renewable.", "solar": "The Sun will keep shining for billions of years; solar is renewable."}),
         ]),
    dict(id="e9_energy_conversion_device", level=2, lo="9.6",
         hints=["Ask what energy goes IN to the device and what useful energy comes OUT.", "Electrical devices take in electrical energy; what do you see, hear or feel coming out?", "Fill in the missing box in the chain."],
         fig=lambda rng: S.flow_boxes(["energy in", "device", "energy out"]),
         variants=[
             dict(stem="Fig. 1 shows an energy chain. For an **electric kettle** heating water, the main useful conversion is",
                  correct="electrical energy → heat energy",
                  wrongs={"heat energy → electrical energy": "The kettle is plugged in: electrical energy goes IN and heat comes out.",
                          "electrical energy → light energy": "A kettle is meant to heat water, not light the room.",
                          "chemical energy → heat energy": "A kettle uses electricity, not fuel."}),
             dict(stem="Fig. 1 shows an energy chain. For a **solar cell** powering a calculator, the main conversion is",
                  correct="light energy → electrical energy",
                  wrongs={"electrical energy → light energy": "That is a lamp. A solar cell takes light IN.",
                          "heat energy → electrical energy": "A solar cell uses the light falling on it, not heat.",
                          "chemical energy → electrical energy": "That is a battery, not a solar cell."}),
             dict(stem="Fig. 1 shows an energy chain. When a **battery-powered torch** is switched on, the main conversion is",
                  correct="chemical energy → electrical energy → light energy",
                  wrongs={"light energy → electrical energy → chemical energy": "That is the chain backwards.",
                          "electrical energy → chemical energy → light energy": "The battery's chemical energy is the starting point.",
                          "kinetic energy → light energy": "Nothing in the torch moves to make light."}),
         ]),

    # ------------------------------------------------------------ L3 apply
    dict(id="e9_spanner_easier", level=3, lo="9.3",
         stem="Fig. 1 shows a spanner turning a nut. A mechanic finds the nut hard to turn. Which change would make it easiest to turn with the same force?",
         correct="Push at the far end of a longer spanner.",
         wrongs={"Push closer to the nut.": "Pushing closer to the pivot gives a SMALLER turning effect for the same force.",
                 "Use a shorter spanner.": "A shorter spanner means the force acts closer to the nut, so the turning effect is smaller.",
                 "Push with the same force at the middle of the spanner.": "The turning effect grows with distance from the pivot; the middle is not the furthest point."},
         hints=["The turning effect depends on the force and on how far from the pivot (the nut) it acts.", "To get more turning effect from the SAME force, change the distance.", "Further from the pivot = bigger turning effect."],
         fig=lambda rng: S.lever(0.1, ("nut", 0.1), ("push", 0.92))),
    dict(id="e9_knife_sharp", level=3, lo="9.4*",
         stem="Fig. 1 shows the thin edge of a knife pressing on a carrot with a force F. A sharp knife cuts more easily than a blunt one because",
         correct="the force acts on a smaller area, so the pressure is larger",
         wrongs={"the sharp knife has a larger mass": "The mass of the knife hardly matters; it is the area of the edge that counts.",
                 "the force acts on a larger area, so the pressure is smaller": "A smaller pressure would make cutting HARDER.",
                 "the sharp edge produces more friction": "Friction opposes the cut. The sharp edge works through pressure, not friction."},
         hints=["Pressure = force ÷ area. What is special about a sharp edge?", "The same force on a smaller area gives a larger pressure.", "Larger pressure → the edge sinks into the carrot."],
         fig=lambda rng: S.block_area(10, 0.1 if False else 1, "F")),
    dict(id="e9_bounce_lower", level=3, lo="9.6",
         stem="Fig. 1 shows a ball dropped from 100 cm bouncing to 64 cm. Why does the ball not return to its original height?",
         correct="Some of its energy is converted to heat and sound during the bounce.",
         wrongs={"Some of its energy is destroyed when it hits the floor.": "Energy is never destroyed. It is converted to other forms (heat, sound).",
                 "Its mass decreases each time it bounces.": "The mass of the ball does not change.",
                 "Gravity becomes stronger after the bounce.": "The gravitational field strength is the same throughout."},
         hints=["Use the principle of conservation of energy: energy cannot be destroyed, so where did the 'missing' energy go?", "You can HEAR the bounce, and the ball and floor warm up slightly.", "Energy → heat and ____."],
         fig=lambda rng: S.bounce([100, 64])),
    dict(id="e9_astronaut_moon", level=3, lo="9.2",
         stem="The table shows g on Earth and on the Moon.\n\n| Body | g / N/kg |\n|---|---|\n| Earth | 10 |\n| Moon | 1.6 |\n\nAn astronaut travels from the Earth to the Moon. Which statement is correct?",
         correct="Her mass is unchanged but her weight is smaller.",
         wrongs={"Her mass and her weight are both smaller.": "Mass is the amount of matter in her body and does not change.",
                 "Her mass is smaller but her weight is unchanged.": "It is the other way round: weight = mass × g, and g is smaller on the Moon.",
                 "Her mass and her weight are both unchanged.": "g is 1.6 N/kg on the Moon, so her weight is much smaller."},
         hints=["Which quantity depends on g? Look at the table: g changes between Earth and Moon.", "Weight = mass × g. Mass is the amount of matter and is the same everywhere.", "Mass unchanged; weight ____."]),
    dict(id="e9_is_work_done", level=3, lo="9.5*",
         hints=["Work is done only when the force makes the object move in the direction of the force.", "Check two things: is there a force, and does the object move along that force?", "No movement in the direction of the force → no work done."],
         fig=lambda rng: figs.force_diagram([("force", "up", 1.3), ("weight", "down", 1.3)], label_body="bag", ground=False),
         variants=[
             dict(stem="Fig. 1 shows a student holding a heavy bag still at shoulder height for two minutes. In the scientific sense, the student does",
                  correct="no work on the bag, because it does not move in the direction of the force",
                  wrongs={"a lot of work, because the bag is heavy": "Feeling tired is not the same as doing work. The bag does not move, so no work is done on it.",
                          "work equal to the weight of the bag": "Weight is a force in newtons, not an amount of work.",
                          "work that increases with the time held": "Time does not come into work done = force × distance."}),
             dict(stem="Fig. 1 shows the forces on a bag. In which case is work done on the bag?",
                  correct="The bag is lifted from the floor onto a table.",
                  wrongs={"The bag is held still above the ground.": "No movement → no work done.",
                          "The bag rests on the floor.": "Nothing moves, so no work is done.",
                          "The bag is carried horizontally while being held at a steady height.": "The upward holding force is at right angles to the horizontal movement, so that force does no work."}),
         ]),

    # ------------------------------------------------------------ L4 explain
    dict(id="e9_snowshoes_explain", level=4, lo="9.4*",
         stem="The table compares the area of a boot and a snowshoe.\n\n| Footwear | Area in contact with snow / cm² |\n|---|---|\n| boot | 250 |\n| snowshoe | 1500 |\n\nWhy does a person wearing snowshoes not sink into soft snow?",
         correct="The weight is spread over a larger area, so the pressure on the snow is smaller.",
         wrongs={"Snowshoes make the person lighter.": "Snowshoes add to the weight, if anything. It is the AREA that changes.",
                 "The larger area increases the pressure on the snow.": "A larger area DECREASES the pressure (pressure = force ÷ area).",
                 "Snowshoes increase the friction with the snow.": "Friction stops sliding; it does not stop sinking. Sinking depends on pressure."},
         hints=["Compare the two areas in the table. The weight is the same in both cases.", "Pressure = force ÷ area. What happens to the pressure when the area is six times bigger?", "Smaller pressure → the snow is not pushed down so far."]),
    dict(id="e9_suction_cup", level=4, lo="9.4*",
         stem="Fig. 1 shows a rubber suction cup pressed onto a smooth tile. Why does it stay attached?",
         correct="Pressing the cup pushes most of the air out, so the atmospheric pressure outside holds the cup against the tile.",
         wrongs={"The rubber is sticky.": "A clean suction cup has no glue. It works because of air pressure.",
                 "The tile pulls the cup with a magnetic force.": "Rubber and tiles are not magnetic.",
                 "The air inside the cup pushes it onto the tile.": "There is very little air left inside; it is the air OUTSIDE that pushes the cup on."},
         hints=["What happens to the air inside the cup when you press it flat?", "Air pressure acts on everything. If there is less air inside the cup than outside, which way is the net push?", "Atmospheric pressure outside > pressure inside → the cup is held on."],
         fig=lambda rng: figs.force_diagram([("atmospheric pressure", "down", 1.4)], label_body="cup", ground=True)),
    dict(id="e9_dam_thicker_bottom", level=4, lo="9.4*",
         stem="Fig. 1 shows how water pressure changes with depth. Why is the wall of a dam built thicker at the bottom than at the top?",
         correct="Liquid pressure increases with depth, so the wall must withstand a larger pressure near the bottom.",
         wrongs={"Water at the bottom is colder and heavier.": "Temperature is not the reason. Pressure increases because of the weight of the water above.",
                 "The pressure of water is the same at all depths.": "The graph shows pressure rising with depth.",
                 "The bottom of the dam holds more water than the top.": "The wall does not 'hold' water by volume; it resists the pressure, which depends on depth."},
         hints=["Look at the graph: what happens to pressure as depth increases?", "The water pressing on the lowest part of the wall has all the water above it pushing down.", "Larger pressure at the bottom → the wall must be stronger there."],
         fig=lambda rng: figs.graph([(0, 0), (10, 100)], 10, 100, 2, 20, xlabel="depth / m", ylabel="pressure / kPa")),
    dict(id="e9_roller_coaster_energy", level=4, lo="9.6",
         stem="Fig. 1 shows the height of a roller-coaster car along a track. It starts from rest at A. Ignoring friction, which statement about the car is correct?",
         correct="At B it is moving fastest because most of its gravitational potential energy has become kinetic energy.",
         wrongs={"At B it has the most gravitational potential energy.": "B is the LOWEST point, so it has the LEAST gravitational potential energy there.",
                 "At C it is moving faster than at B.": "C is higher than B, so some kinetic energy has turned back into gravitational potential energy and the car is slower.",
                 "Energy is created as the car speeds up.": "Energy is converted, not created: the gain in kinetic energy equals the loss in gravitational potential energy."},
         hints=["Where is the car lowest? Where is it highest?", "Going down converts gravitational potential energy to kinetic energy; going up converts it back.", "Fastest at the lowest point."],
         fig=lambda rng: figs.graph([(0, 40), (2, 30), (4, 5), (6, 25), (8, 20)], 8, 50, 2, 10, xlabel="position / m", ylabel="height / m",
                                    labels=[(0, 40, "A", 10, 10), (4, 5, "B", 0, 12), (6, 25, "C", 0, 12)])),
    dict(id="e9_friction_heating", level=4, lo="9.1",
         stem="Fig. 1 shows a box being pushed across a rough floor. After a while the bottom of the box feels warm. Which explanation is correct?",
         correct="Friction between the surfaces converts some of the kinetic energy to heat energy.",
         wrongs={"The box gains heat from the student's hands.": "The warm part is the bottom, where it rubs against the floor.",
                 "Friction creates new energy as heat.": "Energy is not created. Friction CONVERTS kinetic energy to heat.",
                 "The floor pushes the box forward, making it hotter.": "Friction from the floor acts BACKWARDS, opposing the motion."},
         hints=["Which surfaces are rubbing together?", "Friction opposes motion and makes rubbing surfaces warm up.", "Kinetic energy → heat energy because of friction."],
         fig=lambda rng: figs.force_diagram([("push", "right", 1.4), ("friction", "left", 1.0)], label_body="box")),

    # ------------------------------------------------------------ L5 evaluate / predict
    dict(id="e9_choose_energy_source", level=5, lo="9.7",
         stem="A remote sunny village with no rivers and little wind needs electricity. The table compares options.\n\n| Source | Renewable? | Pollution when used | Suits the village? |\n|---|---|---|---|\n| diesel generator | no | carbon dioxide, smoke | fuel must be delivered |\n| solar panels | yes | none | sunny all year |\n| hydroelectric | yes | none | no river |\n| wind turbines | yes | none | little wind |\n\nWhich source is the best choice, and why?",
         correct="Solar panels: renewable, no pollution in use, and the village is sunny all year.",
         wrongs={"Hydroelectric: renewable and clean.": "Clean, but there is no river to drive the turbines.",
                 "Wind turbines: renewable and clean.": "Clean, but the table says there is little wind.",
                 "Diesel generator: it works anywhere.": "It works, but it burns a non-renewable fuel, releases carbon dioxide and needs fuel delivered."},
         hints=["Use ALL the columns: renewable, pollution AND whether it suits the village.", "Two of the renewable options cannot work here. Which row explains why?", "Renewable + clean + works in this place."]),
    dict(id="e9_energy_used_up_claim", level=5, lo="9.6",
         stem="Fig. 1 shows a ball bouncing lower each time. A student says: 'This proves energy gets used up.' Which response is correct?",
         correct="No. The total energy is unchanged; some is converted to heat and sound at each bounce, so less is left as the ball's kinetic and gravitational potential energy.",
         wrongs={"Yes. The lower bounces show that energy has been destroyed.": "Energy is never destroyed. The lower bounces show energy has been CONVERTED to heat and sound.",
                 "Yes, but only the energy in the ball is used up, not the energy in the floor.": "No energy is used up anywhere; it changes form.",
                 "No. The ball bounces lower because gravity gets weaker.": "Gravity does not change. The ball has less energy available to rise."},
         hints=["Start from the principle of conservation of energy.", "Where could the 'missing' energy have gone? You can hear each bounce.", "Converted, not used up."],
         fig=lambda rng: S.bounce([100, 70, 49])),
    dict(id="e9_bag_strap_width", level=5, lo="9.4*",
         stem="Two school bags carry the same load. Bag P has straps 2 cm wide; bag Q has straps 6 cm wide (Fig. 1 compares the strap areas). Which bag is more comfortable on the shoulders, and why?",
         correct="Q, because the same force is spread over a larger area, so the pressure on the shoulders is smaller.",
         wrongs={"P, because narrow straps grip the shoulder better.": "Narrow straps dig in: the same force on a small area gives a large pressure.",
                 "Q, because wider straps make the bag lighter.": "The load is the same; the straps change the AREA, not the weight.",
                 "They are equally comfortable because the load is the same.": "The force is the same, but the area is not, so the pressure is different."},
         hints=["Pressure = force ÷ area. The force (weight of the bag) is the same for both.", "Which strap spreads that force over more shoulder?", "Larger area → smaller pressure → more comfortable."],
         fig=lambda rng: S.bar_chart(["P (2 cm wide)", "Q (6 cm wide)"], [2, 6], "strap width / cm", ymax=8, ystep=2)),
    dict(id="e9_balances_on_moon", level=5, lo="9.2",
         stem="The table shows readings for a rock on Earth. The rock is taken to the Moon, where g = 1.6 N/kg.\n\n| Instrument | Reading on Earth |\n|---|---|\n| beam balance | 3.0 kg |\n| spring balance | 30 N |\n\nWhat will the two instruments read on the Moon?",
         correct="beam balance 3.0 kg; spring balance 4.8 N",
         wrongs={"beam balance 0.48 kg; spring balance 4.8 N": "A beam balance compares masses, and mass does not change, so it still reads 3.0 kg.",
                 "beam balance 3.0 kg; spring balance 30 N": "The spring balance measures weight = m × g = 3.0 × 1.6 N, which is much less on the Moon.",
                 "beam balance 0.48 kg; spring balance 30 N": "This has both readings the wrong way round: mass stays the same and weight falls."},
         hints=["Which instrument measures mass and which measures weight (a force)?", "Mass does not change. Weight = mass × g, and g on the Moon is 1.6 N/kg.", "Spring balance: 3.0 × 1.6 N."]),
    dict(id="e9_forces_in_nature_statement", level=5, lo="9.3",
         stem="The table gives data on two natural events.\n\n| Event | Wind speed / km/h | Effect |\n|---|---|---|\n| strong breeze | 40 | leaves move |\n| cyclone | 200 | roofs torn off |\n\nWhich statement best explains why the cyclone is so destructive?",
         correct="The fast-moving air exerts very large forces on objects, which can change their shape and move them.",
         wrongs={"The cyclone creates new energy that destroys buildings.": "Energy is not created. The cyclone's kinetic energy is transferred to the objects it hits.",
                 "Air has no mass, so only its speed matters.": "Air DOES have mass; moving air carries kinetic energy and exerts forces.",
                 "Roofs are torn off because gravity is weaker during a storm.": "Gravity does not change. The wind's force lifts and tears the roofs."},
         hints=["Faster air carries more kinetic energy. What happens when it hits a roof?", "Forces can change the shape of objects and set them moving.", "Large force → shape changed and objects moved."]),
]

register_explain(EXPLAIN, chapter=9)
