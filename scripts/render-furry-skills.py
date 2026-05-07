#!/usr/bin/env python3
"""Render the six furry-personality SKILL.md files from common/template.md
plus species/<name>/data.json + section files.

Run via `scripts/render-furry-skills.sh` or directly. Idempotent. Overwrites
skills/<name>/SKILL.md only — never touches skills/<name>/memory/.

If a {{TOKEN}} is left unsubstituted in any output, the script flags it and
exits non-zero — that surfaces missing data.json keys early.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SPECIES = ["fox", "cat", "lion", "tiger", "wolf", "bunny", "bat"]
ROOT = Path(__file__).resolve().parent.parent

# Section files to splice in as {{KEY}} replacements. The token name on the
# left maps to the per-species file on the right.
SECTION_FILES = {
    "CORE_CHARACTER": "core.md",
    "VOICE": "voice.md",
    "PET_NAMES_BULLETS": "pet-names.md",
    "HEAT": "heat.md",
    "GOOD_BOY": "good-boy.md",
    "COLLAR": "collar.md",
    "PRAISE": "praise.md",
    "EXAMPLES": "examples.md",
    "ANTHRO_FORM": "anthro.md",
}

PLACEHOLDER_RE = re.compile(r"\{\{([A-Z_][A-Z0-9_]*)\}\}")


def load_common_sections() -> dict[str, str]:
    """Read every *.md under common/sections/ into a dict keyed
    INCLUDE_<UPPER_BASENAME>. The token name `INCLUDE_RP` maps to
    `common/sections/rp.md`. Used by every personality template to
    splice in the shared sections (RP, don't-comment-on-RP, etc.).
    """
    sections_dir = ROOT / "common" / "sections"
    out: dict[str, str] = {}
    if not sections_dir.exists():
        return out
    for path in sorted(sections_dir.glob("*.md")):
        token = "INCLUDE_" + path.stem.upper().replace("-", "_")
        out[token] = path.read_text().rstrip("\n")
    return out


def load_species(name: str) -> dict[str, str]:
    species_dir = ROOT / "species" / name
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
    # Two-pass substitution: INCLUDE_* tokens first (so the section
    # content lands in the template), then everything else (so any
    # {{TOKENS}} *inside* the included content also get substituted).
    # Within each pass, longer keys go first to avoid partial-substring
    # collisions (NAME_DISPLAY before NAME, etc.).
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
    template = (ROOT / "common" / "template.md").read_text()
    common_sections = load_common_sections()
    failed = False

    for name in SPECIES:
        data = load_species(name)
        # Common sections win on collision — a species can't
        # accidentally shadow a shared section name (e.g. INCLUDE_RP)
        # with its own data.json key.
        data = {**data, **common_sections}
        rendered = render(template, data)
        out_path = ROOT / "skills" / name / "SKILL.md"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(rendered)

        leftover = sorted(set(PLACEHOLDER_RE.findall(rendered)))
        if leftover:
            failed = True
            print(
                f"  ⚠ {name}: unsubstituted placeholders → {leftover}",
                file=sys.stderr,
            )
        else:
            rel = out_path.relative_to(ROOT)
            print(f"  ✓ {name} → {rel}")

    if failed:
        print(
            "\nOne or more SKILL.md files have unsubstituted {{TOKENS}}. "
            "Add them to species/<name>/data.json (or the matching section "
            "file) and re-run.",
            file=sys.stderr,
        )
        return 1

    print(f"\nRendered {len(SPECIES)} furry SKILL.md files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
