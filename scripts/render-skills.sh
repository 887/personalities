#!/usr/bin/env bash
# Top-level renderer — renders every templated personality.
#
# Calls the per-family sub-renderers in order:
#   1. render-furry-skills.py — fox / cat / lion / tiger / wolf / bunny / bat
#   2. render-igor-skill.py   — igor (templated, no furry kit)
#
# Standalone non-templated skills (caveman / brief / reset) are
# hand-edited and not touched here.
#
# Add a new family-renderer to this list when one shows up.

set -euo pipefail
cd "$(dirname "$0")/.."

echo "→ furry"
python3 scripts/render-furry-skills.py "$@"

echo
echo "→ igor"
python3 scripts/render-igor-skill.py "$@"
