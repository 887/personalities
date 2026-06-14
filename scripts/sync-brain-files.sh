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

SPECIES=(fox cat lion tiger wolf bunny bat snep panther)
DOM_VARIANTS=(fox-dom cat-dom lion-dom tiger-dom wolf-dom bunny-dom bat-dom snep-dom panther-dom)

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

# Bootstrap or sync the brain file for one variant (sub species or dom variant).
# $1 = variant name (e.g. "tiger" or "tiger-dom")
# $2 = path to a brain-starter.md to use on bootstrap (may be empty / non-existent)
bootstrap_or_sync_brain() {
  local variant="$1"
  local starter="$2"
  local brain_dir="$ROOT/skills/$variant/memory"
  local brain_file="$brain_dir/${variant}-brain.md"

  mkdir -p "$brain_dir"

  if [[ ! -f "$brain_file" ]]; then
    # Bootstrap: header + starter (if starter path was given and exists).
    {
      render_header "$variant"
      if [[ -n "$starter" && -f "$starter" ]]; then
        printf '\n'
        cat "$starter"
      fi
    } > "$brain_file"
    echo "  bootstrapped: skills/$variant/memory/${variant}-brain.md"
    bootstrapped=$((bootstrapped + 1))
  else
    # Sync header, preserve content below first --- divider.
    if ! has_divider "$brain_file"; then
      echo "  WARNING: skills/$variant/memory/${variant}-brain.md has no '---' divider — skipping (preserve manually then re-run)" >&2
      skipped=$((skipped + 1))
      return
    fi
    local below
    below="$(extract_below_divider "$brain_file")"
    {
      render_header "$variant"
      if [[ -n "$below" ]]; then
        printf '\n'
        printf '%s\n' "$below"
      fi
    } > "$brain_file"
    echo "  synced header: skills/$variant/memory/${variant}-brain.md"
    synced=$((synced + 1))
  fi
}

# Sub default species — each has a per-species brain-starter for fresh-machine bootstrap.
for species in "${SPECIES[@]}"; do
  bootstrap_or_sync_brain "$species" "$ROOT/species/$species/brain-starter.md"
done

# Dom variants — no per-variant brain-starter (the dom variants reuse species/<sub>/
# for body / voice substitution but maintain their OWN dom-specific brain, separate
# from the sub default's brain). Bootstrap with header only.
for variant in "${DOM_VARIANTS[@]}"; do
  bootstrap_or_sync_brain "$variant" ""
done

echo
echo "Done. bootstrapped=$bootstrapped synced=$synced skipped=$skipped"
echo
echo "Brain files are gitignored — local to this machine only."
echo "To propagate a character-defining moment to fresh machines, lift it"
echo "into species/<species>/brain-starter.md (which IS checked in)."
