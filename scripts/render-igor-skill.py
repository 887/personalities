#!/usr/bin/env python3
"""Render skills/igor/SKILL.md from common/template-igor.md plus
species/igor/data.json + section files.

Igor opts into the shared {{INCLUDE_*}} sections (RP, don't-comment-on-RP,
respond-in-kind-principle, why-this-register-exists-base) but skips the
furry-only ones (heat / good-boy / collar / cage / pet-names / anthro).

Run via `scripts/render-skills.sh` (the top-level entry that calls both
furry and igor renderers) or directly. Idempotent.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

NAME = "igor"
ROOT = Path(__file__).resolve().parent.parent

# Section files Igor opts into. Maps {{TOKEN}} → species/igor/<file>.md.
# Smaller surface than furries — no heat / good-boy / collar / pet-names /
# anthro / praise. Igor has Voice / Pattern / Examples / Boundaries.
SECTION_FILES = {
    "CORE_CHARACTER": "core.md",
    "VOICE": "voice.md",
    "PATTERN": "pattern.md",
    "EXAMPLES": "examples.md",
    "BOUNDARIES": "boundaries.md",
}

PLACEHOLDER_RE = re.compile(r"\{\{([A-Z_][A-Z0-9_]*)\}\}")


def load_common_sections() -> dict[str, str]:
    """Read every *.md under common/sections/ into INCLUDE_<UPPER_BASENAME>
    keys — same logic as the furry renderer, kept inline rather than
    imported because the shared surface is small and worth not coupling."""
    sections_dir = ROOT / "common" / "sections"
    out: dict[str, str] = {}
    if not sections_dir.exists():
        return out
    for path in sorted(sections_dir.glob("*.md")):
        token = "INCLUDE_" + path.stem.upper().replace("-", "_")
        out[token] = path.read_text().rstrip("\n")
    return out


def load_igor() -> dict[str, str]:
    species_dir = ROOT / "species" / NAME
    data_path = species_dir / "data.json"
    if not data_path.exists():
        raise FileNotFoundError(f"missing {data_path}")
    data = json.loads(data_path.read_text())
    for token, filename in SECTION_FILES.items():
        path = species_dir / filename
        if path.exists():
            data[token] = path.read_text().rstrip("\n")
        else:
            data[token] = ""
    return data


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
    template = (ROOT / "common" / "template-igor.md").read_text()
    common_sections = load_common_sections()
    data = load_igor()
    data = {**data, **common_sections}
    rendered = render(template, data)

    out_path = ROOT / "skills" / NAME / "SKILL.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(rendered)

    leftover = sorted(set(PLACEHOLDER_RE.findall(rendered)))
    if leftover:
        print(
            f"  ⚠ igor: unsubstituted placeholders → {leftover}",
            file=sys.stderr,
        )
        return 1

    print(f"  ✓ igor → {out_path.relative_to(ROOT)}")
    print(f"\nRendered 1 igor SKILL.md file.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
