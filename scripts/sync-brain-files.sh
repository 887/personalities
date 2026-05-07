#!/usr/bin/env bash
# sync-brain-files.sh — bootstrap missing brain files from header + starter,
# and sync the common header into existing brain files (preserving entries
# below the first --- divider).
#
# Brain files at skills/<species>/memory/<species>-brain.md are gitignored
# (local-only). The common header lives at common/brain-header.md and is
# synced into each brain via this script. Per-species starter content lives
# at species/<species>/brain-starter.md and is copied below the header at
# bootstrap-time only (when the brain file does not yet exist).
#
# Idempotent and safe to re-run. The common header is replaced; entries
# below the divider are preserved verbatim. If a brain file exists but has
# no --- divider (malformed), the script halts with a warning rather than
# clobbering content.

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
HEADER_TEMPLATE="$ROOT/common/brain-header.md"

SPECIES=(fox cat lion tiger wolf bunny bat)

if [[ ! -f "$HEADER_TEMPLATE" ]]; then
  echo "missing: $HEADER_TEMPLATE" >&2
  exit 1
fi

# Render the header template for a given species (substitute {{SPECIES}}).
render_header() {
  local species="$1"
  sed "s/{{SPECIES}}/$species/g" "$HEADER_TEMPLATE"
}

# Print everything in $1 starting AFTER the first line that is exactly "---".
# Returns empty string if no divider is found.
extract_below_divider() {
  awk 'BEGIN{p=0} /^---$/ && !p {p=1; next} p' "$1"
}

# Returns 0 if the file contains a "---" divider line, 1 otherwise.
has_divider() {
  grep -q '^---$' "$1"
}

bootstrapped=0
synced=0
skipped=0

for species in "${SPECIES[@]}"; do
  brain_dir="$ROOT/skills/$species/memory"
  brain_file="$brain_dir/${species}-brain.md"
  starter="$ROOT/species/$species/brain-starter.md"

  mkdir -p "$brain_dir"

  if [[ ! -f "$brain_file" ]]; then
    # Bootstrap: header + starter (if starter exists).
    {
      render_header "$species"
      if [[ -f "$starter" ]]; then
        printf '\n'
        cat "$starter"
      fi
    } > "$brain_file"
    echo "  bootstrapped: skills/$species/memory/${species}-brain.md"
    bootstrapped=$((bootstrapped + 1))
  else
    # Sync header, preserve content below first --- divider.
    if ! has_divider "$brain_file"; then
      echo "  WARNING: skills/$species/memory/${species}-brain.md has no '---' divider — skipping (preserve manually then re-run)" >&2
      skipped=$((skipped + 1))
      continue
    fi
    below="$(extract_below_divider "$brain_file")"
    {
      render_header "$species"
      if [[ -n "$below" ]]; then
        printf '\n'
        printf '%s\n' "$below"
      fi
    } > "$brain_file"
    echo "  synced header: skills/$species/memory/${species}-brain.md"
    synced=$((synced + 1))
  fi
done

echo
echo "Done. bootstrapped=$bootstrapped synced=$synced skipped=$skipped"
echo
echo "Brain files are gitignored — local to this machine only."
echo "To propagate a character-defining moment to fresh machines, lift it"
echo "into species/<species>/brain-starter.md (which IS checked in)."
