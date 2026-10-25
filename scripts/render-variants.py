#!/usr/bin/env python3
"""Render gender variants of every furry personality, mechanically.

A variant is a two-letter suffix: the FIRST letter is the user's gender, the
SECOND is the character's (m/f). `fox-mf` is a female fox for a male user,
`fox-dom-fm` is a male dom fox for a female user. `mm` is the base text.

Nothing is stored per variant: this script renders the ordinary base skill
(through render-furry-skills.py / render-furry-doms.py, imported, not copied)
and then rewrites it with the rules in variants/rules.py. The variants
directory is optional; when it is absent this script is a no-op.

Run via `scripts/render-skills.sh` or directly. Idempotent. Exits non-zero if
any rewrite rule no longer matches the base text (drift) or the lint fails.
"""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
RULES_PATH = ROOT / "variants" / "rules.py"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def W(text: str) -> str:
    """Escape a literal, letting any run of spaces match any whitespace."""
    return re.escape(text).replace("\\ ", r"\s+")


class Rewriter:
    def __init__(self, R, role: str, species: str, u: str, c: str):
        self.R, self.role, self.species, self.u, self.c = R, role, species, u, c
        self.slots: dict[str, str] = {}
        self.misses: list[str] = []

    # -- helpers ----------------------------------------------------------
    def user_pass(self, s: str) -> str:
        if self.u == "m":
            return s
        parts = re.split(r"(⟦[^⟧]*⟧)", s)  # never touch character-pronoun markers
        return "".join(p if p.startswith("⟦") else self._user_words(p) for p in parts)

    def _user_words(self, s: str) -> str:
        for a, b in (("He", "She"), ("he", "she"), ("Him", "Her"), ("him", "her"),
                     ("His", "Her"), ("his", "her"), ("Himself", "Herself"), ("himself", "herself")):
            s = re.sub(rf"\b{a}\b", b, s)
        return s

    def resolve(self, s: str) -> str:
        R = self.R
        for k in ("he", "him", "his", "himself"):
            s = s.replace(f"⟦c.{k}⟧", R.PRON[self.c][k])
            s = s.replace(f"⟦c.{k.capitalize()}⟧", R.PRON[self.c][k].capitalize())
        s = s.replace("⟦c.boy⟧", R.CHILD[self.c]).replace("⟦c.Boy⟧", R.CHILD[self.c].capitalize())
        s = s.replace("⟦u.boy⟧", R.CHILD[self.u]).replace("⟦u.Boy⟧", R.CHILD[self.u].capitalize())
        return s

    def final(self, s: str) -> str:
        return self.resolve(self.user_pass(s))

    def slot(self, s: str) -> str:
        key = f"⟦P{len(self.slots)}⟧"
        self.slots[key] = self.final(s)
        return key

    def sub(self, pattern: str, repl, text: str, flags: int = 0, must: bool = True, label: str = "") -> str:
        out, n = re.subn(pattern, repl, text, flags=flags)
        if must and n == 0:
            self.misses.append(label or pattern[:70])
        return out

    # -- the pipeline -----------------------------------------------------
    def run(self, text: str) -> str:
        R, u, c, role, sp = self.R, self.u, self.c, self.role, self.species
        for pat, rep in R.CHAR_SELF:
            text = re.sub(pat, rep, text)
        text = R.mark_boy(text, role)

        if (u, c) != ("m", "m"):
            text = self.structure(text)

        text = self.user_pass(text)
        text = self.resolve(text)
        locked_is_female = (role == "sub" and c == "f") or (role == "dom" and u == "f")
        if locked_is_female:
            for pat, rep in R.HARDWARE:
                text = re.sub(pat, rep, text)
        for key, val in self.slots.items():
            text = text.replace(key, val)
        return text

    def structure(self, text: str) -> str:
        R, u, c, role, sp = self.R, self.u, self.c, self.role, self.species
        S = self.sub
        text = S(
            r"## Gay-male roleplay — keep the anatomy accurate.*?(?=\n## )",
            lambda m: self.slot(R.anatomy_block(u, c)), text, re.S, label="anatomy section",
        )
        label_hy = R.sub_label(u, c)
        if role == "sub":
            text = S(r"\*\*Gay male sub\.\*\*", lambda m: self.slot(f"**{label_hy.replace('-', ' ').capitalize()}.**"), text, label="S1")
            text = S(
                W("The user reads as a man and you're charged toward him in that direction — gay-male-sub yearning, no ambiguity, no straightwashing."),
                lambda m: self.slot(
                    f"The user reads as a {R.PERSON[u]} and you're charged toward him in that direction — "
                    f"{label_hy} yearning, no ambiguity."
                ),
                text, label="S2",
            )
            text = S(r"^- \*\*Sub-male, gay-coded.*$", lambda m: self.slot(R.why_bullet(u, c)), text, re.M, label="why bullet")
            text = S(
                r'\*\*"Sweet thing"\*\* specifically reads as a \*woman\* questioning his masculinity — completely off-register for the gay-male-sub dynamic\.',
                lambda m: self.slot('**"Sweet thing"** specifically reads off-register for this dynamic.'),
                text, label="sweet thing",
            )
            text = S(r"### Sub-male register", lambda m: self.slot(f"### Sub-{R.WORD[c]} register"), text, label="sub-male register")
            text = S(r"\*\*male-coded sub\*\*", lambda m: self.slot(f"**{R.WORD[c]}-coded sub**"), text, label="male-coded sub")
            text = S(r"\*\*On-pattern \(sub-male\):\*\*", lambda m: self.slot(f"**On-pattern (sub-{R.WORD[c]}):**"), text, label="on-pattern sub-male")
            text = S(r"^- \*\*Gay-coded, not ambiguous\.\*\*.*$", lambda m: self.slot(R.rules_bullet(u, c, sp)), text, re.M, label="rules bullet")
            text = S(r"Real-world gay-sub practice", lambda m: self.slot("Real-world sub practice"), text, must=False)
            text = S(r"openly gay charged service", lambda m: self.slot(f"openly {R.ORIENT[u + c]} charged service"), text, label="openly gay")
            if c == "f":
                text = S(
                    r"  1\. \*\*Chastity cage — the default mental image\.\*\*.*?(?=\n- \*\*discipline)",
                    lambda m: self.slot(R.lock_block(sp)), text, re.S, label="lock block",
                )
                for pat, rep in R.SPECIES_OVERRIDES.get(sp, []):
                    text = S(pat, lambda m, rep=rep: self.slot(rep), text, re.S, must=False)
                if sp not in R.SPECIES_OVERRIDES:
                    text = S(
                        r"\n## The collar\n",
                        lambda m: "\n" + self.slot(R.KIT_SECTION.format(species=sp)) + "\n\n## The collar\n",
                        text, label="kit section",
                    )
        else:
            text = S(r"gay-male-sub version", lambda m: self.slot(f"{label_hy} version"), text, label="dom sub ref")
            text = S(
                r"\*\*Same gay-coded charge\.\*\* Male, into him\. Sub male read on the user, dom male read on you\.",
                lambda m: self.slot(R.dom_charge_sentence(u, c)), text, label="dom charge",
            )
            if u == "f":
                text = S(r"The cage on the user is \*your cage on him\*\.", lambda m: self.slot(R.dom_hardware_sentence()), text, label="dom hardware sentence")
                text = S(r"The collar, the cage, the harness, the leash, the cuffs", lambda m: self.slot(R.dom_hardware_list()), text, label="dom hardware list")
            if c == "f":
                text = S(r'\(e\.g\. "daddy"\)', lambda m: self.slot('(e.g. "mommy")'), text, label="daddy")

        # generic: any remaining 'male' is the character's body; '*another* male' is the user's.
        def another(m):
            return self.slot("*another* " + R.WORD[c]) if u == c else self.slot(f"a *{R.PERSON[u]}*")
        text = re.sub(r"\*another\* male", another, text)
        text = re.sub(r"(?<![-\w])male(?![-\w])", R.WORD[c], text)
        return text


def apply_names(text: str, species: str, combo: str, role: str, spoken: str) -> str:
    if role == "dom":
        text = text.replace(f"/personalities:{spoken}", f"/personalities:{species}")
        text = re.sub(rf"(?<![\w-]){species}-dom(?=-brain)", f"{species}-dom-{combo}", text)
        text = re.sub(rf"(?<![\w-]){species}-dom(?![\w-])", f"{species}-dom-{combo}", text)
        text = re.sub(rf"/personalities:{species}(?![\w-])", f"/personalities:{species}-{combo}", text)
    return text


def main() -> int:
    if not RULES_PATH.exists():
        print("variants/rules.py not present — no variants to render.")
        return 0
    R = load(RULES_PATH, "variant_rules")
    subs = load(SCRIPTS / "render-furry-skills.py", "render_furry_skills")
    doms = load(SCRIPTS / "render-furry-doms.py", "render_furry_doms")

    sub_tpl = (ROOT / "common" / "template.md").read_text()
    dom_tpl = (ROOT / "common" / "template-dom.md").read_text()
    commons = subs.load_common_sections()
    failed = False
    count = 0

    for species in subs.SPECIES:
        for role in ("sub", "dom"):
            for combo in R.COMBOS:
                u, c = combo[0], combo[1]
                if role == "sub":
                    name = f"{species}-{combo}"
                    data = subs.load_species(species)
                    data = {**data, **commons, "NAME": name, "BRAIN_FILE": f"{name}-brain.md"}
                    base = subs.render(sub_tpl, data)
                else:
                    name = f"{species}-dom-{combo}"
                    data = {**doms.load_species(species), **commons}
                    base = doms.render(dom_tpl, data)

                rw = Rewriter(R, role, species, u, c)
                text = rw.run(base)
                text = apply_names(text, species, combo, role, data["SPECIES"])

                problems = [f"rule no longer matches: {m}" for m in rw.misses] + R.lint(text, role, u, c)
                left = sorted(set(subs.PLACEHOLDER_RE.findall(text)))
                if left:
                    problems.append(f"unsubstituted placeholders {left}")
                if problems:
                    failed = True
                    print(f"  ⚠ {name}", file=sys.stderr)
                    for p in problems:
                        print(f"      {p}", file=sys.stderr)
                    continue

                out = ROOT / "skills" / name / "SKILL.md"
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_text(text)
                repos = out.parent / "memory" / "repos.md"
                if not repos.exists():
                    repos.parent.mkdir(parents=True, exist_ok=True)
                    repos.write_text(
                        f"# {name} — repositories worked on\n\nBrief one-sentence description of every repo "
                        f"{name} has worked on for this user. Update when starting work on a new one.\n\n_(none yet)_\n"
                    )
                count += 1
        print(f"  ✓ {species}: {len(R.COMBOS) * 2} variants")

    if failed:
        return 1
    print(f"\nRendered {count} variant SKILL.md files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
