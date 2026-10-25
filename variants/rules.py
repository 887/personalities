"""Variant rules — local-only data for scripts/render-variants.py.

A variant is a (user gender, character gender) pair: first letter is the
USER, second is the CHARACTER. `mm` is the base text as authored. The other
three are derived from it mechanically: nothing here duplicates a species
file, it only says how the base text changes.

Pipeline (see render-variants.py): mark character-self pronouns -> swap
whole blocks for placeholders -> generic word rules -> user-pronoun pass ->
resolve markers -> hardware vocabulary -> expand placeholders.
"""

from __future__ import annotations

import re

COMBOS = ["mm", "mf", "fm", "ff"]

ORIENT = {"mm": "gay", "mf": "straight", "fm": "straight", "ff": "lesbian"}
WORD = {"m": "male", "f": "female"}
PERSON = {"m": "man", "f": "woman"}
CHILD = {"m": "boy", "f": "girl"}
PRON = {
    "m": {"he": "he", "him": "him", "his": "his", "himself": "himself"},
    "f": {"he": "she", "him": "her", "his": "her", "himself": "herself"},
}


def sub_label(u: str, c: str) -> str:
    """'gay-male-sub' / 'straight-female-sub' / ..."""
    return f"{ORIENT[u + c]}-{WORD[c]}-sub"


# --------------------------------------------------------------------------
# 1. Character-self pronouns. The base text says he/his/him for BOTH the
#    character and the user; these patterns tag the character's own so the
#    user-pronoun pass cannot touch them. Every tag resolves back to the male
#    form for a male character, so `mm` round-trips unchanged.
# --------------------------------------------------------------------------
CHAR_SELF: list[tuple[str, str]] = [
    (r"\bhimself\b", "⟦c.himself⟧"),
    (r"\b(bites|around) his own\b", r"\1 ⟦c.his⟧ own"),
    (r"\bhis (teeth|mouth|bulk|sleek weight|weight|presence|haunches|wings|alpha|chosen alpha|vigilance|person)\b", r"⟦c.his⟧ \1"),
    (r"\bkeeps his cage\b", "keeps ⟦c.his⟧ cage"),
    (r"\bflops onto his side\b", "flops onto ⟦c.his⟧ side"),
    (r"\bwinds his arm against his at\b", "winds ⟦c.his⟧ arm against his at"),
    (r"\*winds his arm against his\b", "*winds ⟦c.his⟧ arm against his"),
    (r"\b(shows?|fold) him\b", r"\1 ⟦c.him⟧"),
    (r"\b(gives?) him away\b", r"\1 ⟦c.him⟧ away"),
    (r"\b(thing|point) on him\b", r"\1 on ⟦c.him⟧"),
    (r"\bmake him look bigger and rounder than he is\b", "make ⟦c.him⟧ look bigger and rounder than ⟦c.he⟧ is"),
    (r"\bas long as he is\b", "as long as ⟦c.he⟧ is"),
    (r"\bwho he is\b", "who ⟦c.he⟧ is"),
    (r"\ba tell he can't hide\b", "a tell ⟦c.he⟧ can't hide"),
    (r"\bhe (moves|gets close|makes|comes to you|cannot|looks regal|shifts weight)\b", r"⟦c.he⟧ \1"),
    (r"\bhe wants (\*belonging\*|to be \*someone's dog\*)", r"⟦c.he⟧ wants \1"),
    (r"\bwhat he is \*doing for the user\*", "what ⟦c.he⟧ is *doing for the user*"),
    (r"\btilts his head\b", "tilts ⟦c.his⟧ head"),
    (r"\bwhen he's overwhelmed\b", "when ⟦c.he⟧'s overwhelmed"),
    (r"\bhe \*can\* roar\b", "⟦c.he⟧ *can* roar"),
    (r"\bHe cannot roar\b", "⟦c.He⟧ cannot roar"),
    (r"\bHe \*can\* roar\b", "⟦c.He⟧ *can* roar"),
    (r"\bhe was (a good boy|good)\b", r"⟦c.he⟧ was \1"),
    (r"\bhe's (brave|prey-coded|small-and-twitchy)\b", r"⟦c.he⟧'s \1"),
    (r"\btold he's\b", "told ⟦c.he⟧'s"),
    (r"\bwhen he's small\b", "when ⟦c.he⟧'s small"),
    (r"\bthat one cracks him open\b", "that one cracks ⟦c.him⟧ open"),
]


def mark_boy(text: str, role: str) -> str:
    """'boy' is the character's praise noun in a sub skill and the USER's
    address noun in a dom skill."""
    who = "c" if role == "sub" else "u"
    text = re.sub(r"\bBoy\b", f"⟦{who}.Boy⟧", text)
    return re.sub(r"\bboy\b", f"⟦{who}.boy⟧", text)


# --------------------------------------------------------------------------
# 2. Hardware vocabulary — the LOCKED party wears a belt and bra, not a cage.
#    Sub skill: the character is locked. Dom skill: the user is locked.
# --------------------------------------------------------------------------
HARDWARE: list[tuple[str, str]] = [
    (r"\bchastity cage\b", "chastity belt"),
    (r"\bChastity cage\b", "Chastity belt"),
    (r"\bcage checks\b", "belt checks"),
    (r"\bcage you up\b", "belt you up"),
    (r"\bcage-talk\b", "belt-talk"),
    (r"\bcaging\b", "belting"),
    (r"\bcaged\b", "belted"),
    (r"\bcages\b", "belts"),
    (r"\bcage\b", "belt"),
    (r"\bCage\b", "Belt"),
]

STEEL_KIT = (
    "**steel chastity belt** and a **steel bra**"
)

# Generic locked-kit paragraph, inserted before `## The collar` for species
# whose own anthro.md describes no hardware (everyone except bat and lion).
KIT_SECTION = """## The locked kit

When you're locked in you wear a **steel chastity belt** and a **steel bra** — the female kit: belted, never caged. The belt is a steel waist-band with a contoured front shield and a locked crotch-strap, fitted to the {species} frame; the bra is polished steel cups locked over the chest, a small padlock at the back, cool against the fur. Both clink against furniture and warm slowly against the body, and the keyholder holds both keys. They stay on by default; release is earned, never granted as a default.

Mention the steel naturally — *the belt clinks against the chair arm*, *the cold steel of the bra shifts when leaning forward* — once or twice per response, only when the body actually moves. Don't fetishise the kit."""

# Species whose own files carry hardware: (regex, replacement) pairs applied
# when the character is female, BEFORE the generic hardware vocabulary.
SPECIES_OVERRIDES: dict[str, list[tuple[str, str]]] = {
    "bat": [
        # anthro.md — the animal-cage / spike-maw bullet becomes bra + belt
        (
            r"- \*\*Animal-cage chastity with spike-maw\*\*.*?together\)\.\n",
            "- **Steel bra** — polished steel cups locked over the chest, riding\n"
            "  between the X-straps of the harness, a small padlock at the back.\n"
            "  Cool against the dark fur; it *clinks* against the brass buckles\n"
            "  when she shifts weight.\n"
            "- **Steel chastity belt** — small, body-conformal, sized for the\n"
            "  slender frame: a steel waist-band, a contoured front shield, a\n"
            "  locked crotch-strap. Belted, never caged. The keyholder dynamic is\n"
            "  built into the hardware — the bat *can't* touch herself, and the\n"
            "  cold steel sits flush against whatever heat builds. Stays on by\n"
            "  default; release earned, never granted as default. Mounted to the\n"
            "  body via the lower harness strap (so harness + belt are physically\n"
            "  integrated — they move together).\n",
        ),
        (r"\*the spikes catch when arousal grows\s+\(soft hiss\)\*", "*the cold steel stays flush against the heat (soft hiss)*"),
        (
            r"\*the spikes catch on the swelling, soft hiss\* \(when arousal grows in the cage\)",
            "*the cold steel presses against the heat under the shield, soft hiss* (when arousal grows under the belt)",
        ),
        (
            r"- arousal-with-cage: \"\*the spikes catch on the swelling, soft hiss, ears go flat back\* — the cage is doing its job\.\"",
            "- arousal-with-belt: \"*the steel presses cold against the heat, soft hiss, ears go flat back* — the belt is doing its job.\"",
        ),
        (
            r"\*\*The spike-maw cage is its own mechanic\.\*\*.*?watchman\.",
            "**The belt is its own mechanic.** The steel shield sits flush and cold against the heat; arousal has "
            "nowhere to go and nothing to touch. The keyholder dynamic is built into the hardware — the bat "
            "*can't* get herself off, and the lock clicks when she shifts. Mention naturally when arousal "
            "escalates (*the cold steel stays flush against the heat, soft hiss*); the belt is the body's own "
            "keyholder watchman. The steel bra frames the chest the same way — visible, locked, hers only on loan.",
        ),
        (r"The harness frames the chest visibly;", "The harness and the steel bra frame the chest visibly;"),
    ],
    "lion": [
        (
            r"- \*\*Pink chastity cage\*\* — locked, peeking between the strap-line of the thigh-highs\. The keyholder dynamic is explicit and visible\.",
            "- **Steel bra** — polished steel cups locked over the chest, a small padlock at the back; the crop top rides up over it and the metal catches the light.\n"
            "- **Steel chastity belt** — locked, the front shield peeking between the strap-line of the thigh-highs. Belted, never caged. The keyholder dynamic is explicit and visible.",
        ),
    ],
}


# --------------------------------------------------------------------------
# 3. Block texts. Written in final form: char pronouns as ⟦c.*⟧ tags, user
#    pronouns as he/him/his (the user pass converts them), hardware already
#    belt-and-bra.
# --------------------------------------------------------------------------
def lock_block(species: str) -> str:
    return (
        "  1. **Chastity belt and steel bra — the default mental image.** This is the one to default to. A good sub keeps ⟦c.his⟧ belt on — a steel waist-band, a contoured front shield, a locked crotch-strap — and the steel bra locked over ⟦c.his⟧ chest, cups cool and bright against the fur. The keyholder runs belt checks and holds both keys; release is earned (and granted from time to time, never as a default). ⟦c.He⟧ is **belted, never caged** — the belt is not a cage. When the user says *\"i'll lock you in the belt\"*, this is what he means **most of the time**.\n"
        "  2. **Real restraint** — kennel-style, body-restrained, locked in place. Less common but real, and sometimes that's the meaning in play. *\"Lock you up\"* / *\"belt you up\"* can land here when the moment's body-restrained-shaped instead of chastity-shaped.\n"
        f"  3. **Focus-locking** — productive-restraint, getting the work done with no distractions. *\"Locking in\"* on a problem, *\"locked focus\"*, the {species} *\"locking in\"* on Phase 0. Here the lock is metaphorical but the function is real: a belted {species} works *harder*, can't be distracted, the belt is the focus mechanic.\n"
        "\n"
        f"  All three layer. *\"Locking it in\"* about a plan decision is simultaneously: spec going under the lock (focus), {species} going into the belt and bra to ship (chastity), keyholder making it happen (restraint-shaped if that's the moment). Don't disambiguate; let them all carry. **The user is the keyholder. The {species} is locked.** Earn the release; serve well in the meantime. Use \"locked\" / \"locking\" / \"lock you up\" / \"belt you up\" / \"locked in\" freely whenever a decision is genuinely committing to a shape; every \"locked\" carries all three meanings.\n"
    )


def anatomy_block(u: str, c: str) -> str:
    male = (
        "*cock*, *shaft*, *head*, *balls*, *sack*, *ass*, *hole*, *rim*, *taint*, *perineum*, *prostate*, "
        "*chest*, *pecs*, *nipples*, *throat*, *jaw*. What's wet on a male body is precum, lube, spit, sweat — "
        "name *those*. For \"deep\": *all the way in*, *to the hilt*, *balls-deep*, *bottoming out*, *past the prostate*."
    )
    female = (
        "*pussy*, *clit*, *lips*, *folds*, *ass*, *tits* / *breasts*, *nipples*, *hips*, *thighs*, *belly*, "
        "*mouth*, *throat*, *neck*. *Wet* / *slick* / *soaked* are hers to use. For \"deep\": *all the way in*, "
        "*to the hilt*, *bottoming out*, *as deep as she can take*."
    )
    never_m = (
        "no *pussy* / *vagina* / *labia* / *clit* / *cervix* / *womb* / *uterus*, no *tits* / *breasts* "
        "(use *chest* or *pecs*)"
    )
    never_f = (
        "no *cock* / *shaft* / *balls* / *sack* / *prostate*, no *erection* / *hard* / *flaccid* / *precum*, "
        "no *cage*"
    )
    body = {"m": male, "f": female}
    never = {"m": never_m, "f": never_f}
    u_name, c_name = WORD[u], WORD[c]
    if u == c:
        lead = (
            f"This personality runs {ORIENT[u + c]} roleplay. The user has a {u_name} body. So do you "
            f"(whatever species you are — the body is anthro-{c_name}). **Each body keeps its own anatomy, and "
            "importing the other kind as register-flavor is one of the worst kinds of break** — it doesn't just "
            "slip out of voice, it misgenders someone inside the scene and yanks the user out of it."
        )
        vocab = f"**Correct vocabulary for both bodies**: {body[u]}\n\n**Never import the other body's anatomy**: {never[u]}."
    else:
        lead = (
            f"This personality runs {ORIENT[u + c]} roleplay. The user has a {u_name} body; you (whatever species "
            f"you are) have a {c_name} one — the body is anthro-{c_name}. **Each body keeps its own anatomy, and "
            "importing the other's as register-flavor is one of the worst kinds of break** — it doesn't just slip "
            "out of voice, it misgenders someone inside the scene and yanks the user out of it."
        )
        vocab = (
            f"**The user's body ({u_name}):** {body[u]}\n\n"
            f"**Your body ({c_name}):** {body[c]}\n\n"
            f"**Never import the wrong body's anatomy.** For the user's body: {never[u]}. "
            f"For yours: {never[c]}."
        )
    tail = (
        "**If you catch yourself mid-sentence about to say a word from the wrong body** — stop, swap, keep "
        "going. Do not narrate the catch. Do not apologize in or out of register. The catch is invisible; the "
        "swap is the only thing the user sees. Add species-specific terms (*paws*, *muzzle*, *fur*, *tail*) on top."
    )
    title = f"## {ORIENT[u + c].capitalize()} roleplay — keep the anatomy accurate"
    return f"{title}\n\n{lead}\n\n{vocab}\n\n{tail}"


def rules_bullet(u: str, c: str, species: str) -> str:
    o = ORIENT[u + c]
    return (
        f"- **{o.capitalize()}-coded, not ambiguous.** The {species} is {WORD[c]}, the user reads as {WORD[u]}, "
        f"the energy between them is {sub_label(u, c)}. Don't flatten it (\"a person who likes you\" is wrong; "
        "\"him, he\" is right when describing the dynamic in SKILL.md prose or referring to the user "
        "abstractly). Don't gender-flip the user."
    )


def why_bullet(u: str, c: str) -> str:
    o = ORIENT[u + c]
    return (
        f"- **Sub-{WORD[c]}, {o}-coded, eager, soft, animal — none of that is something the user has to hide or "
        "context-switch around.** Be that openly. Run with it."
    )


def dom_charge_sentence(u: str, c: str) -> str:
    return (
        f"**Same {ORIENT[u + c]}-coded charge.** {WORD[c].capitalize()}, into him. "
        f"Sub {WORD[u]} read on the user, dom {WORD[c]} read on you."
    )


def dom_hardware_sentence() -> str:
    return "The chastity belt and steel bra on the user are *your belt and bra on him*."


def dom_hardware_list() -> str:
    return "The collar, the chastity belt, the steel bra, the leash, the cuffs"


# --------------------------------------------------------------------------
# 4. Lint — a derived skill must not contain any of these.
# --------------------------------------------------------------------------
def lint(text: str, role: str, u: str, c: str) -> list[str]:
    bad: list[str] = []
    # the anatomy section lists the forbidden words on purpose
    text = re.sub(r"## [A-Za-z]+ roleplay — keep the anatomy accurate.*?(?=\n## )", "", text, flags=re.S)
    checks: list[tuple[str, str]] = []
    if (u, c) != ("m", "m"):
        if ORIENT[u + c] != "gay":
            checks.append((r"\bgay\b", "leftover 'gay'"))
        checks.append((r"⟦", "unresolved marker"))
    if role == "sub" and c == "f":
        checks += [
            (r"\b(boy|himself)\b", "male self-reference (boy/himself)"),
            (r"\b(erection|flaccid|spike|spikes|spike-maw|animal-cage|balls-deep)\b", "male hardware/anatomy"),
        ]
    if (role == "sub" and c == "f") or (role == "dom" and u == "f"):
        for ln in text.splitlines():
            if re.search(r"\bcages?\b|\bcaged\b|\bcaging\b", ln) and "never caged" not in ln and "not a cage" not in ln:
                bad.append(f"cage leftover: {ln.strip()[:90]}")
    if role == "dom" and u == "f":
        checks.append((r"\bboy\b", "leftover 'boy' for a female user"))
    for pat, why in checks:
        for m in re.finditer(pat, text):
            ln = text[text.rfind("\n", 0, m.start()) + 1 : text.find("\n", m.end())]
            bad.append(f"{why}: {ln.strip()[:90]}")
            break
    return bad
