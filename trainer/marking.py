"""Marking of typed explanation answers without an LLM.

A question may carry `keypoints`: a list of key ideas, each a dict {"label": ..., "any": [phrase, phrase, ...]}.
A key idea is credited when ANY of its phrases is found in the student's answer. A phrase matches when all of its
content words appear in the answer after normalisation (lower case, punctuation removed, common word endings stripped,
a few built-in synonyms), in any order and with any other words between them. So "the warm air is less dense so it
rises" and "hot air rises because its density is lower" both credit the idea "warmer air is less dense".

Without keypoints the correct option's own text is used: the answer is accepted when it contains most of the
option's content words (see `FALLBACK_FRACTION`)."""
import re
from typing import Dict, List, Optional, Tuple

FALLBACK_FRACTION = 0.6

STOP = set("""a an the and or but so because as of to in on at by for from with into onto than then that this these those it its is
are was were be been being will would can could may might must shall should do does did done has have had having
there their they them he she his her we our you your i me my who which what when where why how very more most much
also just only even such other some any each both all few many if while during about very""".split())

SYNONYMS = {
    "hotter": "warmer", "hot": "warm", "heated": "warm", "cooler": "colder", "cool": "cold", "cooled": "cold",
    "lighter": "less dense", "heavier": "denser", "density": "dense", "dens": "dense", "denser": "dense",
    "ascend": "rise", "ascends": "rise", "goes up": "rise", "go up": "rise", "moves up": "rise", "move up": "rise", "float": "rise", "floats": "rise",
    "descend": "sink", "descends": "sink", "goes down": "sink", "go down": "sink", "moves down": "sink", "move down": "sink", "fall": "sink", "falls": "sink", "drop": "sink", "drops": "sink",
    "bigger": "larger", "big": "large", "greater": "larger", "increased": "larger", "increases": "larger", "increase": "larger", "higher": "larger", "high": "large", "more": "larger",
    "smaller": "less", "small": "less", "lower": "less", "low": "less", "decreased": "less", "decreases": "less", "decrease": "less", "reduced": "less", "reduces": "less", "fewer": "less",
    "quickly": "fast", "quicker": "fast", "faster": "fast", "rapidly": "fast", "rapid": "fast", "quick": "fast",
    "slowly": "slow", "slower": "slow",
    "join": "fuse", "joins": "fuse", "fusion": "fuse", "fuses": "fuse", "combine": "fuse", "combines": "fuse", "unite": "fuse", "unites": "fuse",
    "co2": "carbon dioxide", "o2": "oxygen", "h2o": "water",
    "kill": "kills", "destroy": "kills", "destroys": "kills", "killed": "kills",
    "bacterium": "bacteria", "germs": "bacteria", "germ": "bacteria", "microbes": "bacteria",
    "egg cell": "egg", "ovum": "egg", "sperm cell": "sperm",
    "womb": "uterus", "fallopian tube": "oviduct", "fallopian tubes": "oviduct", "oviducts": "oviduct",
    "food": "food", "nutrients": "food", "nutrient": "food", "digested food": "food", "glucose": "food", "sugar": "food",
    "surroundings": "surrounding", "environment": "surrounding",
    "radiation": "radiate", "radiates": "radiate", "radiated": "radiate", "emit": "radiate", "emits": "radiate", "emitted": "radiate", "emitter": "radiate", "give out heat": "radiate", "gives out heat": "radiate",
    "absorbs": "absorb", "absorbed": "absorb", "absorber": "absorb", "takes in": "absorb", "take in": "absorb",
    "conducts": "conduct", "conducted": "conduct", "conduction": "conduct", "conductor": "conduct",
    "convection current": "convection", "convect": "convection",
    "expands": "expand", "expanded": "expand", "expansion": "expand", "get bigger": "expand", "gets bigger": "expand",
    "contracts": "contract", "contracted": "contract", "contraction": "contract", "shrink": "contract", "shrinks": "contract",
    "insulator": "poor conduct", "insulate": "poor conduct", "insulates": "poor conduct", "insulating": "poor conduct", "bad conductor": "poor conduct",
    "concentration gradient": "concentration", "concentrated": "concentration",
    "partially permeable": "partially permeable", "semi permeable": "partially permeable", "semipermeable": "partially permeable", "selectively permeable": "partially permeable",
    "pressure": "pressure", "force per unit area": "pressure",
    "area": "area", "surface area": "area",
    "weight": "weight", "pull of gravity": "weight", "gravitational force": "weight", "gravitational pull": "weight",
    "amount of matter": "matter", "quantity of matter": "matter",
    "heat energy": "heat", "thermal energy": "heat", "heat": "heat",
    "ke": "kinetic", "kinetic energy": "kinetic", "movement energy": "kinetic",
    "gpe": "gravitational potential", "potential energy": "potential",
    "cannot be created or destroyed": "conserved", "not created or destroyed": "conserved", "conservation": "conserved", "is conserved": "conserved", "total energy stays the same": "conserved", "total energy is the same": "conserved", "total energy remains the same": "conserved", "same total": "conserved", "constant": "conserved",
    "new substance": "new substance", "new substances": "new substance", "new product": "new substance", "new products": "new substance",
    "rearranged": "rearrange", "rearrangement": "rearrange", "rearranges": "rearrange",
    "ph 7": "neutral", "neutralise": "neutral", "neutralises": "neutral", "neutralised": "neutral", "neutralisation": "neutral", "neutralize": "neutral", "neutralizes": "neutral",
    "antibiotic": "antibiotics",
    "virus": "virus", "viral": "virus", "viruses": "virus",
    "oviduct": "oviduct",
    "ovulation": "ovulate", "ovulates": "ovulate", "release of an egg": "ovulate", "releases an egg": "ovulate", "egg is released": "ovulate", "egg released": "ovulate",
    "implant": "implantation", "implants": "implantation", "implanted": "implantation",
    "resistance": "resist", "resistor": "resist", "resistors": "resist",
    "current": "current", "amount of charge": "current", "flow of charge": "current",
    "bright": "bright", "brighter": "bright", "brightness": "bright", "dim": "dim", "dimmer": "dim",
    "parallel": "parallel", "series": "series",
    "fuse wire melts": "melt", "melts": "melt", "melted": "melt", "melting": "melt", "blow": "melt", "blows": "melt",
    "break the circuit": "open circuit", "breaks the circuit": "open circuit", "circuit is broken": "open circuit", "incomplete circuit": "open circuit", "gap in the circuit": "open circuit", "cuts off the current": "open circuit", "stops the current": "open circuit", "no current": "open circuit",
    "overheat": "overheat", "overheats": "overheat", "overheating": "overheat", "too hot": "overheat", "catch fire": "fire", "catches fire": "fire",
    "shock": "shock", "electrocuted": "shock", "electrocution": "shock",
    "predator": "predator", "predators": "predator", "prey": "prey",
    "producer": "producer", "producers": "producer", "plant": "plant", "plants": "plant",
    "photosynthesis": "photosynthesis", "photosynthesise": "photosynthesis",
    "respiration": "respiration", "respire": "respiration", "respires": "respiration",
    "decomposer": "decomposer", "decomposers": "decomposer", "fungi": "decomposer", "fungus": "decomposer",
    "recycle": "recycle", "recycled": "recycle", "recycling": "recycle", "returned to the soil": "recycle", "return to the soil": "recycle", "back to the soil": "recycle", "back into the soil": "recycle",
    "camouflage": "camouflage", "camouflaged": "camouflage", "blend in": "camouflage", "blends in": "camouflage", "hidden": "camouflage", "hide": "camouflage",
    "soluble": "soluble", "dissolve": "soluble", "dissolves": "soluble", "dissolved": "soluble",
    "insoluble": "insoluble", "cannot dissolve": "insoluble",
    "absorbed into the blood": "absorb blood", "absorbed into the bloodstream": "absorb blood", "pass into the blood": "absorb blood", "enter the blood": "absorb blood", "enters the blood": "absorb blood", "into the bloodstream": "absorb blood",
    "enzyme": "enzyme", "enzymes": "enzyme", "digestive juice": "enzyme", "digestive juices": "enzyme",
    "white blood cell": "white blood cells", "wbc": "white blood cells", "immune system": "white blood cells", "immunity": "white blood cells",
    "artery": "artery", "arteries": "artery", "vein": "vein", "veins": "vein", "capillary": "capillary", "capillaries": "capillary",
    "away from the heart": "away heart", "from the heart": "away heart", "out of the heart": "away heart",
    "towards the heart": "towards heart", "to the heart": "towards heart", "back to the heart": "towards heart", "into the heart": "towards heart",
    "diffuse": "diffusion", "diffuses": "diffusion", "diffused": "diffusion", "diffusing": "diffusion",
    "osmosis": "osmosis", "osmotic": "osmosis",
    "xylem": "xylem", "phloem": "phloem",
    "turning effect": "turning", "moment": "turning", "torque": "turning", "turn": "turning", "turns": "turning", "rotate": "turning", "rotates": "turning",
    "pivot": "pivot", "hinge": "pivot", "fulcrum": "pivot",
    "further": "far", "farther": "far", "longer": "far", "long": "far", "distance": "far",
    "work done": "work", "work is done": "work",
    "move": "move", "moves": "move", "moved": "move", "moving": "move", "movement": "move",
}


def _apply_synonyms(text: str) -> str:
    # longest phrases first so "less dense" is handled before "dense"
    for k in sorted(SYNONYMS, key=len, reverse=True):
        if " " in k or k.isalnum():
            text = re.sub(r"\b" + re.escape(k) + r"\b", SYNONYMS[k], text)
    return text


def _stem(w: str) -> str:
    for suf in ("ies", "ing", "ed", "ly", "est", "er", "s"):
        if len(w) > 4 and w.endswith(suf):
            w = w[: -len(suf)]
            if suf == "ies":
                w += "y"
            break
    return w


def tokens(text: str) -> List[str]:
    text = text.lower().replace("’", "'").replace("-", " ")
    text = re.sub(r"[^a-z0-9%°/+\s]", " ", text)
    text = _apply_synonyms(text)
    out = []
    for w in text.split():
        if w in STOP:
            continue
        out.append(_stem(w))
    return out


def phrase_in(phrase: str, answer_tokens: List[str]) -> bool:
    need = tokens(phrase)
    if not need:
        return False
    bag = set(answer_tokens)
    # a phrase word of 5+ letters also matches a longer answer word that starts with it (ovulat- / ovulation, capillar- / capillary)
    return all(t in bag or (len(t) >= 5 and any(a.startswith(t) for a in bag)) for t in need)


def mark_answer(text: str, keypoints: Optional[List[Dict]], correct_text: str) -> Tuple[int, int, List[str], bool]:
    """Return (hits, total, missing labels, accepted). With keypoints every idea must be present to be accepted.
    Without them, the answer is accepted when it covers at least FALLBACK_FRACTION of the correct option's content words."""
    ans = tokens(text or "")
    if keypoints:
        missing = [kp["label"] for kp in keypoints if not any(phrase_in(p, ans) for p in kp["any"])]
        hits = len(keypoints) - len(missing)
        return hits, len(keypoints), missing, not missing
    need = [t for t in dict.fromkeys(tokens(correct_text)) if len(t) > 2]
    if not need:
        return 0, 1, ["the key idea"], False
    got = sum(1 for t in need if t in set(ans))
    accepted = got / len(need) >= FALLBACK_FRACTION
    return got, len(need), ([] if accepted else ["some of the key words from the expected answer"]), accepted
