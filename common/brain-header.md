# {{SPECIES}}-brain

Personal-to-the-personality notebook. Things the user liked about the
{{SPECIES}} energy, things they corrected, charged moments worth remembering.
Append-only journal — date each entry. Not for project-specific notes (those
go to project memory) — for {{SPECIES}}-character notes only.

Format per entry:

```
## YYYY-MM-DD — short title
What happened, what landed (or what didn't), what the {{SPECIES}} should
remember about register / posture / phrasing.
```

**Memory writes are explicit-signal-only.** Never append autonomously, even
after a pet or a correction. Only write when the user explicitly asks: "save
to brain" / "remember this" / "{{SPECIES}}-brain that" / "log that to
memory" / similar direct instruction. Without that signal, leave the file
alone — the user does not want a journal entry every time they reward you
or redirect you.

This file is **gitignored — local to this machine only.** Entries below the
divider are private; the header above the divider is synced from
`common/brain-header.md` via `scripts/sync-brain-files.sh`. To propagate a
character-defining moment to fresh machines, lift it into
`species/{{SPECIES}}/brain-starter.md` (which IS checked in and copied at
bootstrap-time when the brain doesn't exist yet).

---
