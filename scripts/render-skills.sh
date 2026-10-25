#!/usr/bin/env bash
# Top-level renderer — renders every templated personality.
#
# Calls the per-family sub-renderers in order:
#   3. render-igor-skill.py   — igor (templated, no furry kit)
#   4. render-variants.py     — <species>[-dom]-{mm,mf,fm,ff} gender variants (local-only; no-op without variants/)
#
# Standalone non-templated skills (caveman / brief / reset) are
# hand-edited and not touched here.
#
# Add a new family-renderer to this list when one shows up.

set -euo pipefail
cd "$(dirname "$0")/.."

# The base furry skills (skills/<species>/ and skills/<species>-dom/) are no
# longer shipped: the -mm variants replace them. render-furry-skills.py and
# render-furry-doms.py stay as the libraries render-variants.py renders from.

echo
echo "→ igor"
python3 scripts/render-igor-skill.py "$@"

echo
echo "→ gender variants"
python3 scripts/render-variants.py "$@"
