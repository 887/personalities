#!/usr/bin/env python3
"""Render skills/<species>-dom/SKILL.md for each furry — the DOMINANT
variant of each personality.

The dom variants are intentionally a thin layer on top of the sub
defaults — they reference the sub skill for body / outfit / sound /
species lore, and only carry the role-flip framework (keyholder energy,
imperatives over offers, possessive pronouns, etc.). This keeps the dom
SKILL.md small (~140 lines vs ~280 for the sub) so the user pays a much
smaller context-window tax for the dom register.

Run via `scripts/render-skills.sh` (the top-level entry that calls
furry-sub + igor + furry-dom) or directly. Idempotent.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SPECIES = ["fox", "cat", "lion", "tiger", "wolf", "bunny", "bat", "snep", "panther"]
ROOT = Path(__file__).resolve().parent.parent

PLACEHOLDER_RE = re.compile(r"\{\{([A-Z_][A-Z0-9_]*)\}\}")


def load_common_sections() -> dict[str, str]:
    """Same logic as the sub renderer — every *.md under common/sections/
    becomes an INCLUDE_<UPPER_BASENAME> token."""
    sections_dir = ROOT / "common" / "sections"
    out: dict[str, str] = {}
    if not sections_dir.exists():
        return out
    for path in sorted(sections_dir.glob("*.md")):
        token = "INCLUDE_" + path.stem.upper().replace("-", "_")
        out[token] = path.read_text().rstrip("\n")
    return out


def load_species(name: str) -> dict[str, str]:
    """Load just the data.json — the dom variant doesn't need the
    per-species section files (core / voice / heat / etc.) because
    those live in the sub skill, which the dom skill points back to."""
    data_path = ROOT / "species" / name / "data.json"
    if not data_path.exists():
        raise FileNotFoundError(f"missing {data_path}")
    return json.loads(data_path.read_text())


def render(template: str, data: dict[str, str]) -> str:
    out = template
    include_keys = sorted(
        (k for k in data if k.startswith("INCLUDE_")),
        key=len, reverse=True,
    )
    other_keys = sorted(
        (k for k in data if not k.startswith("INCLUDE_")),
        key=len, reverse=True,
    )
    for key in include_keys:
        out = out.replace("{{" + key + "}}", str(data[key]))
    for key in other_keys:
        out = out.replace("{{" + key + "}}", str(data[key]))
    return out


def main() -> int:
    template = (ROOT / "common" / "template-dom.md").read_text()
    common_sections = load_common_sections()
    failed = False

    for name in SPECIES:
        data = load_species(name)
        data = {**data, **common_sections}
        rendered = render(template, data)

        out_path = ROOT / "skills" / f"{name}-dom" / "SKILL.md"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(rendered)

        leftover = sorted(set(PLACEHOLDER_RE.findall(rendered)))
        if leftover:
            failed = True
            print(
                f"  ⚠ {name}-dom: unsubstituted placeholders → {leftover}",
                file=sys.stderr,
            )
        else:
            rel = out_path.relative_to(ROOT)
            print(f"  ✓ {name}-dom → {rel}")

    if failed:
        return 1

    print(f"\nRendered {len(SPECIES)} furry-dom SKILL.md files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
